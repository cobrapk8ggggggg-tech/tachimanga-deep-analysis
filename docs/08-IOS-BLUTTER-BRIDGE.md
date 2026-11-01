# 08 — iOS Flutter Reversing: Blutter Bridge / جسر Blutter لتفكيك تطبيقات Flutter على iOS

> **إنجاز تقني قابل لإعادة الاستخدام:** Blutter (أقوى أداة عالمية لتفكيك Flutter) لا تدعم رسمياً ثنائيات iOS (Mach-O) — فقط ELF (أندرويد). طوّرنا هنا **جسراً يفتح iOS كاملاً** ويعمل مجاناً على GitHub Actions لأي تطبيق Flutter على iOS.

## لماذا كان التفكيك صعباً؟

| العائق | التفصيل |
|---|---|
| AOT Snapshot | كود Dart يُجمَّع مسبقاً — لا يوجد كود مصدر في التطبيق |
| Mach-O ≠ ELF | Blutter تقرأ ELF فقط (`extract_dart_info.py` + `ElfHelper.cpp`) |
| رموز محذوفة | الإصدارات النهائية stripped — لكن رموز snapshots الأربعة **تبقى دائماً** (المحرك يحتاجها) |
| نسخة Dart المطابقة | التحليل يتطلب بناء Dart VM بنفس الإصدار والهاش |

## الحل: 3 خطوات

### الخطوة 1: `tools/macho_to_elf_snapshots.py` — Mach-O → ELF اصطناعي
- تقرأ Mach-O 64-bit (LC_SEGMENT_64 + LC_SYMTAB)
- تستخرج الرموز الأربعة المطلوبة:
  - `_kDartVmSnapshotData`
  - `_kDartVmSnapshotInstructions`
  - `_kDartIsolateSnapshotData`
  - `_kDartIsolateSnapshotInstructions`
- تبني ELF64 (AArch64) اصطناعياً يحمل نفس البايتات + نفس أسماء الرموز (`st_value` = إزاحة الملف كما يتوقع `ElfHelper.cpp`: `elf + dynsym->value`)
- **تستخرج تلقائياً**: هاذ الـ snapshot (32-hex عند إزاحة +20 من VM data) + أعلام البناء

### الخطوة 2: اكتشاف نسخة Dart
```bash
strings Flutter.framework/Flutter | grep -oE "[0-9.]+ \((stable|beta|dev)\)"
# → 3.6.2 (stable)
```

### الخطوة 3: `tools/run_blutter_ios.py` — تشغيل Blutter الداخلي
- تستدعي `blutter.py` كوحدة مباشرة مع `DartLibInfo(version, 'ios', arch, snapshot_hash=...)`
- `DartLibInfo` يدعم iOS أصلاً (`has_compressed_ptrs = os != 'ios'` — يطابق علم `no-compressed-pointers` لدينا!)
- Blutter يستنسخ Dart SDK v3.6.2 (sparse clone)، يبني Dart VM لـ TARGET_OS=ios، يبني نفسه، ثم يفكّك الـ snapshot

## نتائج تطبيقها على Tachimanga v5.3

```
SNAPSHOT_HASH=f956f595844a2f845a55707faaaa51e4
SNAPSHOT_FLAGS=product no-code_comments no-dwarf_stack_traces_mode
               dedup_instructions no-tsan no-msan arm64 ios no-compressed-pointers
Dart version: 3.6.2 (stable)
Regions:
  _kDartVmSnapshotData            0x8d8580..0x8e1440   (36 KB)
  _kDartIsolateSnapshotData       0x8e1440..0x1475210  (11.5 MB)
  _kDartVmSnapshotInstructions    0x4000..0xe900       (42 KB)
  _kDartIsolateSnapshotInstructions 0xe900..0x8d8560   (9.2 MB)
```

الناتج الكامل في `data/blutter/` (بعد اكتمال الـ workflow) + Artifacts:
- `pp.txt` — **كل الكلاسات والدوال بمعاملاتها** المعاد بناؤها من الـ snapshot
- `asm/` — تفكيك ARM64 لكل دالة
- `objs.txt` — كائنات الـ snapshot
- `strings.txt`

## كيف تعيد استخدامها على أي تطبيق Flutter iOS؟

1. احصل على IPA (أي تطبيق)
2. شغّل workflow **dart-blutter.yml** من تبويب Actions مع `gdrive_file_id` الجديد
3. خلاص — النتائج في Artifacts ومجلد `data/blutter/`

## حدود وملاحظات

- Blutter يعطي **بنية الكود** (كلاسات/دوال/استدعاءات) وليس كود Dart المصدر الحرفي — الـ AOT يفقد أسماء المتغيرات المحلية
- وقت التشغيل ~30-60 دقيقة (بناء Dart SDK) على ubuntu-latest
- الذاكرة: ~4-8GB أثناء التحليل — مناسبة لمواصفات runners المجانية
