#!/usr/bin/env python3
"""
run_blutter_ios.py — Run Blutter (worawit/blutter) on an iOS Flutter app.

Blutter natively supports iOS snapshot analysis (TARGET_OS=ios) but its Python
entry point assumes ELF inputs. This wrapper:
  1. takes a synthetic ELF produced by macho_to_elf_snapshots.py
  2. builds the matching Dart VM (version + snapshot hash) and Blutter
  3. runs the analysis

Usage:
    python3 run_blutter_ios.py <synthetic-libapp.so> <outdir>

Env:
    DART_VERSION   e.g. 3.6.2        (default: 3.6.2)
    DART_OS        default: ios
    DART_ARCH      default: arm64
    SNAPSHOT_HASH  32-hex from macho_to_elf_snapshots.py (recommended)
    BLUTTER_DIR    default: /tmp/blutter
"""
import importlib.util
import os
import sys

BLUTTER_DIR = os.environ.get("BLUTTER_DIR", "/tmp/blutter")
DART_VERSION = os.environ.get("DART_VERSION", "3.6.2")
DART_OS = os.environ.get("DART_OS", "ios")
DART_ARCH = os.environ.get("DART_ARCH", "arm64")
SNAPSHOT_HASH = os.environ.get("SNAPSHOT_HASH") or None


def load_blutter_module():
    sys.path.insert(0, BLUTTER_DIR)
    spec = importlib.util.spec_from_file_location(
        "blutter_mod", os.path.join(BLUTTER_DIR, "blutter.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["blutter_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    libapp, outdir = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    os.makedirs(outdir, exist_ok=True)

    B = load_blutter_module()
    dart_info = B.DartLibInfo(DART_VERSION, DART_OS, DART_ARCH,
                              snapshot_hash=SNAPSHOT_HASH)
    print(f"# Dart lib: {dart_info.lib_name} | "
          f"compressed_ptrs={dart_info.has_compressed_ptrs} | "
          f"snapshot_hash={SNAPSHOT_HASH}", file=sys.stderr)

    inp = B.BlutterInput(libapp, dart_info, outdir,
                         rebuild_blutter=False, create_vs_sln=False,
                         no_analysis=False)
    B.build_and_run(inp)
    print("# blutter done -> " + outdir, file=sys.stderr)


if __name__ == "__main__":
    main()
