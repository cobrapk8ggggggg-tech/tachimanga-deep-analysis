# 02 — Deep Architecture / المعمارية العميقة

## 1. نظرة عامة على الطبقات (Layer Stack)

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: iOS Native Frameworks                              │
│  Firebase (Core/Crashlytics/RemoteConfig/ABTesting/Sessions)│
│  GoogleMobileAds · UMP · GoogleService-Info.plist           │
│  SDWebImage · SSZipArchive · FMDB · SAMKeychain             │
│  NSFWDetector · HCSStarRatingView · SVProgressHUD           │
│  DWAlertController · Mantle · Masonry · FileMD5Hash         │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Flutter Engine (Flutter.framework) + App AOT       │
│  App.framework = 21.7MB Dart AOT snapshot                   │
│  flutter_assets: icons(29 app icons!) · data · licenses     │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Flutter Plugins (22 plugin)                        │
│  connectivity_plus · cupertino_http · cupertino_native      │
│  device_info_plus · file_picker · flutter_nsfw              │
│  flutter_path_provider_plus · flutter_web_auth_2            │
│  fluttertoast · image_picker_ios · in_app_purchase_storekit │
│  in_app_review · local_auth_darwin · package_info_plus      │
│  path_provider_foundation · shared_preferences_foundation   │
│  sign_in_with_apple · sqflite_darwin · system_proxy         │
│  url_launcher_ios · webview_flutter_wkwebview · libzstd     │
│  apple_pencil_double_tap (Apple Pencil support!)            │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Bridge (Tachimanga.dylib — 6MB)                    │
│  الجسر بين Dart ←→ JVM (تشغيل/إيقاف الخادم المحلي،          │
│  إدارة ملفات الإضافات، بث أحداث التنزيلات)                  │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Embedded JVM (OpenJ9) — jre/ folder                │
│  jre/lib/modules (96MB) · jrt-fs.jar · security/ · tzdb.dat │
│  java.properties · options.default · jvm.cfg                │
│  يشغّل: Suwayomi-Server (Kotlin) → محلياً 127.0.0.1:4567    │
│    └─ يحمّل إضافات Tachiyomi (.apk) ويشغّل كود Java فيها    │
└─────────────────────────────────────────────────────────────┘
```

## 2. تدفق البيانات (Data Flow) — من المصدر إلى الشاشة

### مثال: فتح شاشة استكشاف "Browse"
```
[Flutter UI: browse_screen.dart]
   │ riverpod → browse_controller
   │ HTTP GET http://127.0.0.1:4567/api/v1/source/list
   ▼
[Tachimanga.dylib bridge] → [OpenJ9 JVM]
   ▼
[Suwwayomi-Server (embedded)] REST API
   ▼
 loads extension .apk → runs Java source code (OkHttp scraping)
   ▼
 returns JSON: sources list
   ▼
[Flutter UI renders grid of source cards]
```

### مثال: قراءة فصل (Reader)
```
reader_screen_v2.dart
   │ reader_controller_v2 (riverpod StateNotifier)
   │ GET /api/v1/manga/{mangaId}/chapter/{chapterIndex}/page/{page}
   ▼
 Suwayomi-Server → extension fetches image URL → downloads → returns page
   ▼
 cached_network_image renders → photo_view zoom → page_scroll_physics
```

## 3. دورة حياة التطبيق (App Lifecycle)

1. **الإقلاع:** `main.dart` → تهيئة Riverpod providers
2. **تشغيل JVM:** الجسر الأصلي (Tachimanga.dylib) يشغّل OpenJ9 JVM داخل العملية
3. **إقلاع Suwayomi-Server:** يبدأ REST server على 127.0.0.1:4567
4. **فحص الخادم:** `connectivity_plus` + ping للخادم المحلي (شاشة انتظار)
5. **تهيئة Firebase:** Crashlytics + RemoteConfig (مزودات الإعدادات البعيدة `update_notice_config.dart`)
6. **فحص الحساب:** `account_controller.dart` → جلسة MangaCrush (sign_in_with_apple اختياري)
7. **فحص Premium:** `purchase_check_controller.dart` → in_app_purchase_storekit (+ تجاوز عبر كراك blatantsPatch في النسخة المقرصنة)
8. **الواجهة الرئيسية:** go_router → شاشة Library/Browse/Updates/History/More

## 4. إدارة الحالة (State Management) — Riverpod

نمط Sorayomi الكامل:
```
data/{x}_repository.dart      ← طبقة الوصول للبيانات (dio → REST API)
domain/{x}_model.dart         ← نماذج مجمدة (freezed + json_serializable)
presentation/{x}/controller/  ← StateNotifier/AsyncNotifier (riverpod)
presentation/{x}/{x}_screen.dart      ← الشاشة
presentation/{x}/widgets/     ← مكونات الشاشة
```

## 5. قاعدة البيانات المحلية

- **sqflite_darwin** (SQLite على iOS) — للبيانات التطبيقية الخفيفة
- **shared_preferences_foundation** — الإعدادات
- **SAMKeychain** — بيانات حساسة (مفاتيح)
- **ملاحظة مهمة:** بيانات المكتبة الفعلية (المانجا، الفصول، التقدم) **تُخزَّن داخل Suwayomi-Server** (H2/SQLite على جانب JVM) — واجهة Flutter مجرد عميل REST!

## 6. الشبكات (Networking)

- **dio** — عميل HTTP الرئيسي للـ API المحلي
- **cupertino_http** — استخدام URLSession الأصلي في iOS (HTTP/2, proxy)
- **flutter_web_auth_2** — OAuth لتتبع MAL/AniList (يفتح متصفح ويعود عبر `tachimanga://` scheme)
- **system_proxy** — دعم بروكسي النظام
- **NSAppTransportSecurity: NSAllowsArbitraryLoads = true** — السماح بمصادر HTTP غير المشفرة (بعض مصادر المانجا قديمة)
- **webview_flutter_wkwebview** — حل Cloudflare/كابتشا داخل تطبيق

## 7. تنزيل الملفات والقراءة دون اتصال

- **flutter_cache_manager + cached_network_image + octo_image** — كاش الصور
- **SSZipArchive (native)** — فك ضغط CBZ/الأرشيفات
- **downloads_repository + download_ticket_service** — طابور تنزيلات بمهام متوازية (`downloads_parallel_button`)
- **download_pip_button** — تنزيل في الخلفية مع مؤشر PiP (نافذة عائمة صغيرة تُظهر التقدم!)

## 8. نظام السمات والمظهر (التطبيق الأصلي للـ UI)

- **flex_color_scheme** — محرك السمات الأساسي
- `src/constants/app_themes/app_theme.dart` — تعريفات السمات (Midnight Dusk, Tako, ...)
- **ThemeDefine + ThemeSchemeColor + ThemePureBlack** — امتدادات مخصصة (أسود نقي للـ OLED)
- **liquid_glass_controller** — تأثيرات iOS 26 Liquid Glass (`cupertino_native` يوفر مكونات UIKit حقيقية)
- **ThemeBlendLevel** — مزج ألوان قابل للضبط
- **app_icon_controller + 29 أيقونة بديلة** — تغيير أيقونة التطبيق (شائع في iOS)
- **grid_count_controller + grid_cover_min_width** — تحكم كامل بكثافة الشبكة

## 9. القارئ (Reader) — أعمق وحدة فنية

| النمط | الملف |
|---|---|
| Continuous (Webtoon) | `continuous_reader_mode_v2.dart` |
| Single Page | `single_page_reader_mode_v2.dart` |
| Double Page ( spread) | `double_page_reader_mode_v2.dart` |
| Page Curl (قلب صفحات واقعي كـ iBooks!) | `page_curl/reader_page_curl_painter.dart` + CustomPainter |
| تخطيطات اللمس للتنقل | `edge_layout`, `kindlish_layout`, `l_shaped_layout`, `right_and_left_layout` |
| فيزياء تمرير مخصصة | `page_scroll_physics.dart` |
| تمرير بالضغط المطوّل | `long_press_scroll_speed.dart` + indicator |
| فاصل الفصول | `chapter_separator.dart` |
| خلفية تلقائية من الصورة | `reader_automatic_page_background.dart` |
| لون خلفية قابل للاختيار | `manga_reader_background_color_popup.dart` |
| Padding للصفحات | `manga_reader_padding_popup.dart` |
| شريط أدوات سفلي/علوي قابل للتخصيص | `reader_toolbar_preferences.dart`, `duo_reader_toolbar_layout.dart` |
| إيماءات الحواف | `reader_edge_gestures.dart` |

## 10. الأمان والخصوصية

- **local_auth_darwin** — قفل Face ID
- **NSFaceIDUsageDescription** — صلاحية FaceID
- **NSUserTrackingUsageDescription** — تتبع الإعلانات (ATT)
- **NSPhotoLibraryUsageDescription** — استيراد ملفات محلية
- **NSLocalNetworkUsageDescription** — اتصال محلي (Suwayomi عن بُعد؟)
- **flutter_web_auth_2** — مصادقة ويب آمنة
- **NSFWDetector** — كشف محتوى +18 تلقائي (يطمس الأغلفة في الاستكشاف!)

## 11. الأداء

- **flutter_perf_monitor** — مراقب أداء مدمج (FPS/RAM) — ميزة موثقة في الإعدادات
- **visibility_detector** — إيقاف الأشياء غير المرئية (توفير بطارية)
- **rxdart + stream_transform + queue** — بث وإدارة مهام متقدمة
- **AOT compiled** — لا JIT = إقلاع سريع وأداء ثابت
