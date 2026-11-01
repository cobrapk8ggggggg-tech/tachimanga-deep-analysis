# 06 — Open-Source Roadmap / 🚀 خارطة طريق بناء نسختك الخاصة

> **الهدف:** نسخة خاصة بك من "Tachimanga" بكل ميزاته، تدعم الآيفون، مبنية على مصادر مفتوحة قانونياً.

## القرار الهندسي الأول: أين يعمل "الخادم"؟

Tachimanga يشغّل Suwayomi-Server **داخل التطبيق** (JVM مدمج). أنت أمام 3 خيارات:

| الخيار | الصعوبة | التكلفة | الموثوقية | متى تختاره |
|---|---|---|---|---|
| **A. خادم سحابي/منزلي + تطبيق عميل** | ⭐ سهل | 0–5$/شهر | ممتازة | **ابدأ هنا** — يعمل أسبوعياً |
| B. JVM مدمج في التطبيق (نسخ Tachimanga الحرفية) | ⭐⭐⭐⭐ صعب جداً | 0 | متوسطة | لاحقاً كمرحلة ثانية |
| C. نصف مدمج: الجهاز يشغّل JVM عبر OpenJDK Mobile | ⭐⭐⭐ متوسط-صعب | 0 | متوسطة | بعد إتقان A |

> 💡 **نصيحة:** ابدأ بالخيار A اليوم — ستحصل على تجربة شبه مطابقة (الفرق الوحيد: تحتاج خادماً يعمل). ثم انتقل إلى B عندما يصبح كل شيء مستقراً.

---

## المرحلة 0: الأساسات (يوم 1)

```bash
# 1) اعمل Fork لمستودع العميل (مطبق في هذا الحساب):
#    github.com/cobrapk8ggggggg-tech/Tachidesk-Sorayomi (fork من Suwayomi)
# 2) استنسخه محلياً
git clone https://github.com/cobrapk8ggggggg-tech/Tachidesk-Sorayomi.git my-manga
cd my-manga
# 3) ثبّت Flutter (نسخة مستقرة حديثة) + Android Studio/Xcode
flutter doctor   # تأكد أن iOS toolchain جاهز
# 4) شغّل الكود — يجب أن يفتح على iOS Simulator فوراً
flutter run -d "iPhone"
# 5) الخادم (الخيار A): على Docker بجهاز آخر أو نفس الشبكة
docker run -d --name suwayomi -p 4567:4567 -v suwayomi-data:/home/suwayomi/.local/share/Tachidesk ghcr.io/suwayomi/suwayomi-server:latest
```

**النتيجة بعد ساعة واحدة:** تطبيق آيفون حقيقي يشبه Tachimanga ويتصل بخادم مانجا كامل فيه 700+ مصدر.

## المرحلة 1: تخصيص الهوية (أسبوع 1)

1. **غيّر الاسم والأيقونة:**
   - `pubspec.yaml`: name + description
   - iOS: `ios/Runner/Info.plist` → CFBundleDisplayName + CFBundleIdentifier
   - الأيقونة: `flutter_launcher_icons`
2. **اربط عنوان الخادم بإعداداتك:** في Sorayomi خيار "Server URL" موجود في الإعدادات — اجعله يحفظ خيارك
3. **غيّر السمة الافتراضية:** `src/constants/app_themes/app_theme.dart`
4. **أضف العربية محسّنة:** `intl_ar.arb` — الأساس موجود أصلاً
5. **غيّر ألوان التطبيق والشعار** في `assets/`

## المرحلة 2: الميزات الجوهرية (أسابيع 2–4)

انسخ سلوكيات Tachimanga واحدة واحدة (الملفات المرجعية في `docs/03-FEATURE-MAP.md`):

| الميزة | من أين تبدأ في Sorayomi |
|---|---|
| تحسين القارئ (Page Curl, تمرير بالضغط المطول) | `reader/widgets/reader_mode/page_curl/` — أضف CustomPainter |
| Liquid Glass للتبويبات | platform channel إلى `UIVisualEffectView` |
| قفل Face ID | أضف `local_auth` + شاشة قفل عند الإقلاع |
| أيقونات بديلة | `flutter_dynamic_icon_plus` أو API أصلي |
| وضع التخفي في السجل | موجود جزئياً — فعّل |
| نسخ احتياطي للسحابة | أضف iCloud Drive عبر `icloud_storage` حزمة |
| إشعارات فصول جديدة | `flutter_local_notifications` + جدولة خلفية |

## المرحلة 3: الطبقة الخاصة (اختيارية)

- **حساب خاص بك:** Supabase/Firebase Auth (بدائل جاهزة، تدعم Apple Sign-In)
- **مزامنة خاصة:** خادم Suwayomi واحد يخدم أجهزتك كلها = مزامنة فعلية (نفس التقدم على الآيفون والآيباد)
- **كشف NSFW:** أضف `flutter_nsfw` (نفس حزمة Tachimanga!)
- **شاشة HTTP Dump:** ميزة مميزة في Tachimanga — انسخها (dio interceptor + شاشة قائمة)

## المرحلة 4: التوزيع على الآيفون

1. **لنفسك فقط (مجاناً):** Xcode → Personal Team → `flutter build ipa` → ثبّت عبر Xcode/AltStore/Sidestore
2. **لأجهزتك كلها:** Apple Developer Program (99$/سنة) → TestFlight أو تثبيت مباشر
3. **للعامة:** App Store (انتبه لسياسة المتجر — قارئ المحتوى يُقبل عادة إن لم يكن نفسه يقرصن محتوى مدفوعاً)

---

## الخيار B (متقدم): JVM داخل التطبيق مثل Tachimanga حرفياً

كيف يفعلها Tachimanga (مكتشف من التحليل):
1. **OpenJ9 JVM مدمج** (96MB modules) داخل حزمة التطبيق
2. **Tachimanga.dylib (6MB)** — مكتبة C/C++ تُحمّل JVM داخل عملية التطبيق (JNI Invocation API)
3. يشغّل **Suwayomi-Server كامل** على 127.0.0.1:4567
4. Flutter يتكلم معه REST محلياً — **نفس كود Sorayomi يعمل دون تغيير!**

كيف تفعلها أنت بمصادر مفتوحة:
1. ابنِ [OpenJDK Mobile](https://github.com/openjdk/mobile) لـ iOS (رموز arm64 iOS رسمية) — أو استخدم GraalVM Native Image
2. ابنِ Suwayomi-Server (Kotlin/JVM) كـ fat-jar
3. اكتب Plugin أصلي (Swift/ObjC) يستدعي JNI_CreateJavaVM ويشغّل الخادم في thread خلفي
4. اربطه بدورة حياة التطبيق (إيقاف عند الخروج)
5. توجه Flutter دائماً إلى 127.0.0.1:4567

> ⚠️ تحديات معروفة: حجم التطبيق (+100MB)، توقيع Entitlements خاص (`cyan.entitlements` في Tachimanga يشير لذلك)، إدارة ذاكرة JVM على أجهزة iPhone (استخدم `-Xmx` محدوداً)، ومتجر App Store لن يسمح غالباً بتحميل كود الإضافات ديناميكياً — التوزيع خارج المتجر (TestFlight للاختبار أو AltStore) أنسب.

## مقارنة توقيتات واقعية

| المسار | وقت أول نسخة عاملة | وقت نسخة مكتملة التشابه |
|---|---|---|
| A فقط | 1–2 ساعة | 2–4 أسابيع |
| A ثم B | 1–2 ساعة | 2–4 أشهر |

## مصادر مفتوحة تُساعدك (كلها مجانية)

| المشروع | الرابط | الفائدة |
|---|---|---|
| Tachidesk-Sorayomi (عميل Flutter) | github.com/Suwayomi/Tachidesk-Sorayomi | **أساسك** — MPL-2.0 |
| Suwayomi-Server (خادم) | github.com/Suwayomi/Suwayomi-Server | الخادم — MPL-2.0 |
| Mihon (أندرويد) | github.com/mihonapp/mihon | مرجع الميزات — Apache-2.0 |
| Keiyoushi extensions | github.com/keiyoushi/extensions | 700+ مصدر — مفتوح |
| SoraSquirrel (فرع iOS-focused) | github.com/Molasses4098/SoraSquirrel | مرجع تحسينات iOS — MPL-2.0 |
| OpenJDK Mobile | github.com/openjdk/mobile | JVM للآيفون — GPL+CE |
| Aidoku (iOS أصلي Swift) | github.com/Aidoku/Aidoku | مرجع UI بـ Swift — GPL |
