# 07 — iOS Build Guide / دليل البناء للآيفون

## المتطلبات
- macOS مع Xcode 15+ (للبناء النهائي) — الإجراءات على CI تُنفَّذ عبر GitHub Actions macOS runner
- Flutter SDK مستقر حديث
- حساب Apple ID (مجاني للتجربة / 99$ سنوياً للتوزيع)

## 1. تجهيز بيئة iOS

```bash
sudo xcode-select -s /Applications/Xcode.app
sudo xcodebuild -runFirstLaunch
flutter doctor --android-licenses
flutter config --enable-ios
cd my-manga   # نسختك من Sorayomi
flutter pub get
cd ios && pod install && cd ..
```

## 2. إعدادات المشروع الأساسية

`ios/Runner/Info.plist` — انسخ الأنماط المكتشفة في Tachimanga:

```xml
<!-- صلاحيات مطلوبة (مطابقة لما اكتشفناه) -->
<key>NSFaceIDUsageDescription</key>
<string>قفل التطبيق بحماية وجهك</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>لاستيراد المانجا المحلية</string>
<key>NSLocalNetworkUsageDescription</key>
<string>للاتصال بخادم Suwayomi على شبكتك المحلية</string>
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSAllowsArbitraryLoads</key><true/>  <!-- بعض المصادر HTTP -->
</dict>

<!-- URL Schemes (مطلوبة لـ OAuth التتبع) -->
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLName</key><string>com.yourname.mymanga</string>
    <key>CFBundleURLSchemes</key>
    <array><string>mymanga</string><string>mihon</string></array>
  </dict>
</array>
```

## 3. البناء والتشغيل

```bash
# على المحاكي
flutter run -d "iPhone 15"

# على جهازك (توقيع شخصي مجاني)
flutter build ios --release
# ثم افتح ios/Runner.xcworkspace في Xcode → اختر Team → Run

# IPA للتحميل الجانبي
flutter build ipa --release --no-codesign
```

## 4. التوقيع والتوزيع

| الطريقة | التكلفة | المدة | مناسب لـ |
|---|---|---|---|
| Xcode Personal Team | مجاني | 7 أيام | تجربة سريعة |
| AltStore / SideStore | مجاني | 7 أيام (تجديد تلقائي) | استخدام يومي لنفسك |
| TestFlight | 99$/سنة | 90 يوم | أجهزتك كلها + أصدقاء |
| App Store | 99$/سنة | دائم | الجمهور |

## 5. متطلبات خاصة إن قلّدت JVM المدمج (الخيار B)

1. **Entitlements** — Tachimanga يستخدم `cyan.entitlements` مخصصة. قد تحتاج:
   - `com.apple.security.get-task-allow` (للتطوير)
   - تقنيات JIT: iOS يمنع JIT افتراضياً — OpenJ9 قد يحتاج JIT أو وضع Interpreter (أبطأ لكن يعمل) — OpenJDK Mobile يوفر وضع interpreter آمن
2. **حجم التطبيق:** +100MB لملفات JVM → استخدم App Thinning أو اقبل الحجم (حد iOS Cellulaire download = 200MB+ الآن)
3. **الذاكرة:** اضبط `-Xmx512m` كحد أقصى للخادم المدمج لتفادي إغلاق iOS للتطبيق

## 6. استكشاف أخطاء شائعة

| المشكلة | الحل |
|---|---|
| `pod install` يفشل | `pod repo update` ثم أعد المحاولة |
| تعارض إصدار Dart | طابق إصدار Flutter مع `pubspec.yaml` (environment: sdk) |
| الاتصال بالخادم يفشل على الجهاز الحقيقي | استخدم IP الحقيقي للخادم في إعدادات التطبيق (وليس 127.0.0.1) + اسمح بالشبكة المحلية (Local Network permission) |
| فشل بناء على CI | راجع workflow `build-ios.yml` في هذا المستودع |
