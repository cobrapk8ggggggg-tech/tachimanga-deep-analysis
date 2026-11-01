# 🔬 Tachimanga v5.3 — Deep Reverse-Engineering Analysis
# 🔬 تحليل تفكيكي عميق لتطبيق Tachimanga v5.3

> **الهدف (Goal):** فهم بنية تطبيق Tachimanga v5.3 بالكامل (كل ميزة، كل واجهة، كل منطق) وبناء نسخة خاصة مفتوحة المصدر تدعم iOS، مبنية على أساس مفتوح المصدر قانوني 100%.
>
> **Verdict / الخلاصة المهمة:** التطبيق **مبني على مشروع مفتوح المصدر بالكامل** — يمكن استنساخ 95%+ من ميزاته من مصادر مفتوحة قانونية.

---

## 🎯 TL;DR — النتيجة النهائية في سطرين

| السؤال | الجواب |
|---|---|
| هل Tachimanga v5.3 مفتوح المصدر؟ | ❌ لا — كود MangaCrush مغلق، **لكن** التطبيق مبنٍ بالكامل على |
| الأساس المفتوح | ✅ [Suwayomi/Tachidesk-Sorayomi](https://github.com/Suwayomi/Tachidesk-Sorayomi) (Flutter, MPL-2.0) + [Suwayomi-Server](https://github.com/Suwayomi/Suwayomi-Server) (Kotlin, MPL-2.0) |
| إطار العمل | ✅ **Flutter** (Dart AOT) — وليس Swift أصلي |
| يدعم iOS؟ | ✅ Flutter يدعم iOS بشكل ممتاز — وهذا التطبيق نفسه دليل حي |
| خطة البناء الخاصة | ✅ Fork السورايومي + خادم Suwayomi مدمج محلياً أو سحابي — [الخطة الكاملة](docs/06-OPEN-SOURCE-ROADMAP.md) |

---

## 📐 المعمارية المكتشفة (Discovered Architecture)

```
┌──────────────────────────────────────────────────────────┐
│                 Tachimanga.app (iOS, arm64)              │
│                 Bundle: com.mangacrush.ios               │
│                 Min iOS 15.0 · Flutter Engine            │
│                                                          │
│  ┌─────────────────────────┐    HTTP  ┌───────────────┐  │
│  │   Flutter UI (Dart AOT) │ ───────▶ │ OpenJ9 JVM    │  │
│  │   649 ملف Dart          │ 127.0.0.1│ مدمج داخل     │  │
│  │   package:              │  :4567   │ التطبيق (96MB)│  │
│  │   tachidesk_sorayomi    │          │               │  │
│  │                         │          │ يشغّل:         │  │
│  │  Riverpod · go_router   │          │ Suwayomi-     │  │
│  │  freezed · dio · flex_  │          │ Server محلياً │  │
│  │  color_scheme           │          └──────┬────────┘  │
│  └─────────────────────────┘                 │           │
│           │                                  ▼           │
│  ┌────────▼─────────┐            ┌─────────────────────┐ │
│  │ Native iOS layer │            │ Tachiyomi .apk      │ │
│  │ Firebase·AdMob   │            │ extensions (700+)   │ │
│  │ IAP·FaceID·NSFW  │            │ Java/Kotlin sources │ │
│  └──────────────────┘            │ تعمل عبر JVM!       │ │
│                                  └─────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

**السر الهندسي الأهم:** إضافات Tachiyomi هي ملفات APK تعمل على JVM. فريق Tachimanga دمّج **OpenJ9 JVM كاملاً (96MB modules)** داخل تطبيق iOS، وشغّل عليه خادم Suwayomi-Server محلياً على `127.0.0.1:4567`، ثم واجهه تطبيق Flutter (نسخة معدّلة من Sorayomi) — كل هذا **داخل هاتف الآيفون نفسه دون أي خادم خارجي**.

---

## 📂 محتويات المستودع

| المسار | الوصف |
|---|---|
| [`docs/01-EXECUTIVE-SUMMARY.md`](docs/01-EXECUTIVE-SUMMARY.md) | الملخص التنفيذي الكامل |
| [`docs/02-ARCHITECTURE.md`](docs/02-ARCHITECTURE.md) | المعمارية العميقة: Flutter + JVM + Suwayomi |
| [`docs/03-FEATURE-MAP.md`](docs/03-FEATURE-MAP.md) | خريطة كل الميزات الـ 15+ وكل شاشة (649 ملف) |
| [`docs/04-UI-SPEC.md`](docs/04-UI-SPEC.md) | مواصفات الواجهات: السمات، Liquid Glass، أنماط القراءة |
| [`docs/05-TECH-STACK.md`](docs/05-TECH-STACK.md) | كل الحزم (108 حزمة Dart + 40+ إطار أصلي) |
| [`docs/06-OPEN-SOURCE-ROADMAP.md`](docs/06-OPEN-SOURCE-ROADMAP.md) | 🚀 **خارطة طريق بناء نسختك الخاصة خطوة بخطوة** |
| [`docs/07-IOS-BUILD-GUIDE.md`](docs/07-IOS-BUILD-GUIDE.md) | دليل البناء للآيفون + التوقيع + التوزيع |
| [`data/extracted/`](data/extracted/) | البيانات المستخرجة حرفياً من الـ IPA |
| [`.github/workflows/`](.github/workflows/) | GitHub Actions للمهام الثقيلة |
| [`tools/`](tools/) | أدوات التحليل القابلة لإعادة الاستخدام |

---

## 🤖 GitHub Actions — المهام الثقيلة

| Workflow | الوظيفة |
|---|---|
| `ipa-recon.yml` | تفكيك شامل: تفريغ كل الـ strings، الرموز، فحص Mach-O → يرفع النتائج للمستودع |
| `dart-blutter.yml` | بناء **Blutter** (أقوى أداة عالمية لتفكيك Dart AOT) وإعادة بناء هيكل كود Dart الكامل → Artifacts |
| `upstream-sync.yml` | مراقبة أسبوعية لمستودع Sorayomi الأصلي والإبلاغ عن التحديثات |
| `build-ios.yml` | بناء نسختك الخاصة كـ IPA جاهز للتوقيع |

---

## ⚖️ ملاحظات قانونية (Legal Notes)

1. **MPL-2.0** (رخصة Sorayomi وSuwayomi-Server): رخصة *copyleft على مستوى الملف* — يمكنك بناء نسختك الخاصة وحتى بيعها، مع إبقاء تعديلاتك على ملفات MPL مفتوحة، وإضافة بيان الرخصة.
2. الملف المفحوص كان نسخة **"Patched" (مقرصنة)** — لا تُعِد توزيعه. نحن نحلله فقط للفهم وبناء بديل نظيف مفتوح.
3. المحتوى المنشور هنا هو تحليل هندسي عكسي للفهم والتعلم والترابطية (interoperability).

---

## 👤 المالك

- GitHub: `cobrapk8ggggggg-tech`
- المستودع الأساسي للنسخة الخاصة: *(انظر خارطة الطريق)*
