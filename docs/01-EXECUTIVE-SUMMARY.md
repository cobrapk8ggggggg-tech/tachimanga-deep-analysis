# 01 — Executive Summary / الملخص التنفيذي

## الملف المفحوص

| الخاصية | القيمة |
|---|---|
| اسم الملف | `Tachimanga v5.3 Premium Unlocked blatant Patched.zip` |
| الحجم | 124 MB → يحتوي IPA بحجم 135 MB |
| النوع | iOS App Package (IPA) — Mach-O arm64 |
| Bundle ID | `com.mangacrush.ios` |
| الاسم المعروض | Tachimanga |
| الإصدار | 5.3 (build 533) |
| أدنى إصدار iOS | 15.0 |
| SDK البناء | iphoneos27.1 |
| URL Schemes | `app.tachimanga`, `tachimanga`, `mihon` |
| المحليّات | ar, de, en, es, fr, hu, id, it, ms, pt-BR, pt-PT, ru, th, tr, uk, vi, zh-Hans, zh-Hant (**العربية مدعومة رسمياً**) |
| ملف الكراك | `Frameworks/blatantsPatch.dylib` (70KB) — الديبل library المُحقونة لفتح Premium |

## هل التطبيق مفتوح المصدر؟ (Open-Source Verdict)

### الحكم: التطبيق مغلق المصدر لكنه مشتق من مشروع مفتوح

1. **كود MangaCrush الخاص (مغلق):** نظام الحسابات، الاشتراكات Premium، الإعلانات، جسر الـ JVM، تخصيصات الواجهة (Liquid Glass)، مزامنة Tachimanga السحابية.
2. **الأساس المفتوح المصدر (قابل للاستنساخ قانونياً):**
   - [**Suwayomi/Tachidesk-Sorayomi**](https://github.com/Suwayomi/Tachidesk-Sorayomi) — 1574★ — **MPL-2.0** — Dart/Flutter
     - اسم الحزمة داخل التطبيق حرفياً: `package:tachidesk_sorayomi/` — دليل قاطع
     - كل بنية `src/features/...` في التطبيق مطابقة لبنية Sorayomi مع إضافات
   - [**Suwayomi/Suwayomi-Server**](https://github.com/Suwayomi/Suwayomi-Server) — Kotlin — **MPL-2.0**
     - اكتُشف `http://127.0.0.1:4567` في كود Dart — هذا هو المنفذ الافتراضي لـ Suwayomi-Server
   - إضافات المصادر: منتجات مجتمع Tachiyomi/Mihon (Keiyoushi) — Apache-2.0/مفتوحة

### الدليل على النسخ من Sorayomi (Evidence)
- `package:tachidesk_sorayomi/main.dart` — نقطة دخول التطبيق نفسها
- 649 ملف Dart مطابقون لبنية Sorayomi: `src/features/{library,browse_center,manga_book,settings,...}`
- نفس نمط المعمارية: `data/ domain/ presentation/ controllers/` لكل ميزة
- نفس أسماء الملفات مثل `library_manga_filter.dart`, `extension_list_tile.dart` وغيرها

## ما الذي أضافه MangaCrush فوق Sorayomi؟ (الجزء المغلق)

| الميزة المضافة | الدليل من التحليل |
|---|---|
| 🔐 نظام حساب MangaCrush | `src/features/account/` — login/register/verify/reset/change-password + `signin_with_apple.dart` |
| 💎 اشتراكات Premium | `src/features/custom/inapp/` — purchase_screen2, premium_features_screen, purchase_check, promotion, TestFlight alert |
| 📺 إعلانات AdMob + Reward Ads | `src/features/custom/ads/` + GoogleMobileAds.framework + `download_reward_ad_dialog.dart` |
| 🧊 واجهة iOS حقيقية (Liquid Glass) | `liquid_glass_controller.dart`, `cupertino_native`, `cupertino_modal_sheet` |
| ☁️ مزامنة سحابية realtime | `src/features/sync/` — realtime_sync_hero, sync_settings |
| ⚙️ JVM مدمج لتشغيل إضافات Tachiyomi | مجلد `jre/` (OpenJ9, 96MB modules) + `Tachimanga.dylib` (6MB — الجسر) |
| 🛡️ كشف NSFW | `flutter_nsfw` + `NSFWDetector.framework` |

## الأرقام الكاملة

- **108** حزمة Dart مميزة (بما فيها flutter/dart core)
- **649** ملف Dart في التطبيق الأساسي
- **15** وحدة ميزات رئيسية (features)
- **40+** إطار/مكتبة أصلي (native) داخل التطبيق
- **JVM OpenJ9** كامل: 96MB modules + jrt-fs.jar + security + tzdb
- **29** لغة واجهة عبر ملفات `.lproj`

## القرار الاستراتيجي الموصى به

> **لا تعِد اختراع العجلة.** بدلاً من إعادة كتابة التطبيق من الصفر:
> 1. اعمل **Fork** لمستودع `Suwayomi/Tachidesk-Sorayomi` (MPL-2.0 — يسمح بذلك كلياً)
> 2. اتبع خارطة الطريق في [06-OPEN-SOURCE-ROADMAP.md](06-OPEN-SOURCE-ROADMAP.md)
> 3. ستحصل على: المكتبة، المصادر، القارئ، التنزيلات، التتبع، النسخ الاحتياطي، الترحيل، وكل ما رأيته في Tachimanga — بنفس الواجهة تقريباً لأن Tachimanga نفسه مبني عليها
> 4. أضف تحسيناتك الخاصة (سطح سحابي اختياري، واجهة عربية محسّنة، إلخ)
