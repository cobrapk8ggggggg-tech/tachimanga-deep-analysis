# tools / أدوات التحليل

| الأداة | الوصف | الاستخدام |
|---|---|---|
| `analyze_ipa.sh` | استطلاع شامل لأي IPA: بنية Dart، الحزم، الروابط، الأطر، JVM | `./analyze_ipa.sh app.ipa out/` |
| `../.github/workflows/ipa-recon.yml` | نفس الاستطلاع لكن على GitHub Actions (موارد أكبر) | شغّل يدوياً من تبويب Actions |
| `../.github/workflows/dart-blutter.yml` | **Blutter + جسر iOS** — إعادة بناء كود Dart كامل (كلاسات + دوال + assembly) | شغّل يدوياً — ~40 دقيقة |
| `macho_to_elf_snapshots.py` | **جسر iOS**: تحويل ثنائي App (Mach-O) إلى ELF اصطناعي + استخراج هاش snapshot | `python3 macho_to_elf_snapshots.py App out.so` |
| `run_blutter_ios.py` | تشغيل Blutter على iOS (بناء Dart SDK المطابق + تحليل) | `DART_VERSION=3.6.2 SNAPSHOT_HASH=... python3 run_blutter_ios.py libapp.so out/` |
| `../.github/workflows/build-ios.yml` | بناء نسختك كـ IPA غير موقّع | Actions → Build iOS → Run |
| `../.github/workflows/upstream-sync.yml` | مراقبة Sorayomi الأصلي أسبوعياً | تلقائي |

## أدوات خارجية موصى بها (متاحة على GitHub Actions مجاناً)
- **Blutter** — github.com/worawit/blutter — تفكيك Dart AOT (الأهم لتطبيقات Flutter)
- **jimage** (JDK) — سرد محتويات `jre/lib/modules`
- **Hopper/IDA** على macOS — تفكيك الديبل الأصلي `Tachimanga.dylib`
- **Frida** — تحليل ديناميكي على جهاز آيفون مكسور الحماية (اختياري متقدم)
