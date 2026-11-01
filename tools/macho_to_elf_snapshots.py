#!/usr/bin/env python3
"""
macho_to_elf_snapshots.py — iOS Flutter App (Mach-O) → synthetic ELF for Blutter.

Blutter (worawit/blutter) supports iOS Dart snapshots (TARGET_OS=ios) but its
ELF loader cannot read Mach-O. This tool extracts the 4 Dart snapshot regions
from the iOS `App` binary and packs them into a minimal synthetic ELF64 with
the exact symbols Blutter's ElfHelper expects:
    _kDartVmSnapshotData, _kDartVmSnapshotInstructions,
    _kDartIsolateSnapshotData, _kDartIsolateSnapshotInstructions

It also prints the Dart snapshot hash (needed to build the matching Dart VM).

Usage:
    python3 macho_to_elf_snapshots.py <App-mach-o-binary> <out-libapp.so>

stdout (last lines):
    SNAPSHOT_HASH=<32 hex chars>
    SNAPSHOT_FLAGS=<flags string>
"""
import struct
import sys

ELF_MAGIC = b"\x7fELF"
SHT_STRTAB = 3
SHT_DYNSYM = 11

SYMS = [
    "_kDartVmSnapshotData",
    "_kDartVmSnapshotInstructions",
    "_kDartIsolateSnapshotData",
    "_kDartIsolateSnapshotInstructions",
]


def parse_macho(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:4] != struct.pack("<I", 0xFEEDFACF):
        sys.exit("Not a little-endian Mach-O 64-bit file: " + path)
    ncmds = struct.unpack_from("<I", data, 16)[0]
    off = 32
    sections = []  # (segname, sectname, addr, size, offset)
    symbols = {}   # name -> value (file/vm offset)
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", data, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            nsects = struct.unpack_from("<I", data, off + 64)[0]
            so = off + 72
            for _s in range(nsects):
                sectname = data[so:so + 16].rstrip(b"\0").decode()
                segname = data[so + 16:so + 32].rstrip(b"\0").decode()
                addr, size = struct.unpack_from("<QQ", data, so + 32)
                offset = struct.unpack_from("<I", data, so + 48)[0]
                sections.append((segname, sectname, addr, size, offset))
                so += 80
        elif cmd == 0x2:  # LC_SYMTAB
            symoff, nsyms, stroff, _strsize = struct.unpack_from("<IIII", data, off + 8)
            for i in range(nsyms):
                n_strx = struct.unpack_from("<I", data, symoff + i * 16)[0]
                _t, _s, _d, value = struct.unpack_from("<BBHQ", data, symoff + i * 16 + 4)
                end = data.index(b"\0", stroff + n_strx)
                name = data[stroff + n_strx:end].decode(errors="replace")
                if name in SYMS:
                    symbols[name] = value
        off += cmdsize
    if len(symbols) != 4:
        sys.exit(f"Missing snapshot symbols, found: {sorted(symbols)}")
    return data, sections, symbols


def section_bounds(sections, sym_value):
    """End offset of the Mach-O section containing sym_value (by addr range)."""
    for segname, sectname, addr, size, offset in sections:
        if size and addr <= sym_value < addr + size:
            return offset + size
    # fallback: end of file region heuristic
    return None


def build_elf(blobs, out_path):
    """blobs: list of (name, bytes). Returns None. Synthetic ELF64 LE AARCH64."""
    # .dynstr
    dynstr = bytearray(b"\0")
    name_off = {}
    for name, _ in blobs:
        name_off[name] = len(dynstr)
        dynstr += name.encode() + b"\0"
    # .shstrtab
    shstrtab = bytearray(b"\0")
    shname_off = {}
    for s in [b".dynsym", b".dynstr", b".snapdata", b".shstrtab"]:
        shname_off[s.decode()] = len(shstrtab)
        shstrtab += s + b"\0"

    ehsize = 64
    shentsize = 64
    ndynsym = len(blobs) + 1
    dynsym_size = ndynsym * 24

    off = ehsize
    # .dynsym
    dynsym_off = off
    off += dynsym_size
    # .dynstr
    dynstr_off = off
    off += len(dynstr)
    # blobs (16-aligned)
    blob_offs = []
    for name, blob in blobs:
        off = (off + 15) & ~15
        blob_offs.append(off)
        off += len(blob)
    # .shstrtab
    off = (off + 15) & ~15
    shstrtab_off = off
    off += len(shstrtab)
    # section headers
    off = (off + 15) & ~15
    shoff = off
    shnum = 5  # NULL, .dynsym, .dynstr, .snapdata, .shstrtab
    total = shoff + shnum * shentsize

    out = bytearray(total)

    # ELF header
    eh = bytearray(64)
    eh[0:4] = ELF_MAGIC
    eh[4] = 2      # ELFCLASS64
    eh[5] = 1      # little endian
    eh[6] = 1      # version
    struct.pack_into("<HHIQQQIHHHHHH", eh, 16,
                     3,          # e_type = ET_DYN
                     0xB7,       # e_machine = EM_AARCH64
                     1,          # e_version
                     0,          # e_entry
                     0,          # e_phoff
                     shoff,      # e_shoff
                     0,          # e_flags
                     ehsize,     # e_ehsize
                     0, 0,       # phentsize, phnum
                     shentsize, shnum,
                     4)          # e_shstrndx = index of .shstrtab
    out[0:64] = eh

    # .dynsym — entry 0 = null
    for i, (name, blob) in enumerate(blobs, start=1):
        ent_off = dynsym_off + i * 24
        struct.pack_into("<IBBHQQ", out, ent_off,
                         name_off[name],  # st_name
                         0x12,            # st_info = GLOBAL|OBJECT
                         0,               # st_other
                         3,               # st_shndx (index of .snapdata)
                         blob_offs[i - 1],  # st_value = FILE OFFSET (Blutter: elf+value)
                         len(blob))         # st_size

    out[dynstr_off:dynstr_off + len(dynstr)] = dynstr
    for i, (name, blob) in enumerate(blobs):
        out[blob_offs[i]:blob_offs[i] + len(blob)] = blob
    out[shstrtab_off:shstrtab_off + len(shstrtab)] = shstrtab

    # section headers: [NULL, .dynsym, .dynstr, .snapdata, .shstrtab]
    def shdr(idx, sh_name, sh_type, sh_offset, sh_size, sh_entsize, sh_link=0):
        o = shoff + idx * shentsize
        # Elf64_Shdr: name(I) type(I) flags(Q) addr(Q) offset(Q) size(Q) link(I) info(I) addralign(Q) entsize(Q)
        struct.pack_into("<IIQQQQIIQQ", out, o,
                         sh_name, sh_type, 0, 0, sh_offset, sh_size,
                         sh_link, 0, 1 if sh_type == SHT_DYNSYM else 0, sh_entsize)

    shdr(0, 0, 0, 0, 0, 0)
    shdr(1, shname_off[".dynsym"], SHT_DYNSYM, dynsym_off, dynsym_size, 24, sh_link=2)
    shdr(2, shname_off[".dynstr"], SHT_STRTAB, dynstr_off, len(dynstr), 0)
    total_blob = sum(len(b) for _, b in blobs)
    shdr(3, shname_off[".snapdata"], 1, blob_offs[0], total_blob, 0)  # PROGBITS
    shdr(4, shname_off[".shstrtab"], SHT_STRTAB, shstrtab_off, len(shstrtab), 0)

    with open(out_path, "wb") as f:
        f.write(out)
    return total


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    data, sections, symbols = parse_macho(src)

    vm_data = symbols["_kDartVmSnapshotData"]
    iso_data = symbols["_kDartIsolateSnapshotData"]
    vm_ins = symbols["_kDartVmSnapshotInstructions"]
    iso_ins = symbols["_kDartIsolateSnapshotInstructions"]

    vm_data_end = section_bounds(sections, vm_data)
    iso_data_end = section_bounds(sections, iso_data)
    vm_ins_end = iso_ins
    iso_ins_end = section_bounds(sections, iso_ins)

    regions = [
        # VM data ends where isolate data begins (same __const section)
        ("_kDartVmSnapshotData", vm_data,
         iso_data if iso_data > vm_data else (vm_data_end or len(data))),
        ("_kDartIsolateSnapshotData", iso_data, iso_data_end or len(data)),
        ("_kDartVmSnapshotInstructions", vm_ins,
         iso_ins if iso_ins > vm_ins else (vm_ins_end or len(data))),
        ("_kDartIsolateSnapshotInstructions", iso_ins, iso_ins_end or len(data)),
    ]

    blobs = []
    for name, start, end in regions:
        size = end - start
        if size <= 0:
            sys.exit(f"Invalid region {name}: {start:#x}..{end:#x}")
        blobs.append((name, data[start:end]))
        print(f"# {name}: file {start:#x}..{end:#x} size={size:#x}", file=sys.stderr)

    build_elf(blobs, dst)
    print(f"# wrote {dst}", file=sys.stderr)

    # Extract snapshot hash (32 bytes at offset 20 of VM snapshot data) + flags
    vm_blob = blobs[0][1]
    snap_hash = vm_blob[20:52].decode("ascii", errors="replace")
    rest = vm_blob[52:52 + 300]
    flags = rest[:rest.index(b"\0")].decode("ascii", errors="replace").strip()
    print(f"SNAPSHOT_HASH={snap_hash}")
    print(f"SNAPSHOT_FLAGS={flags}")


if __name__ == "__main__":
    main()
