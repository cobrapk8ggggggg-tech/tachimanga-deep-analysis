# 05 — Tech Stack / الحزمة التقنية الكاملة

## Dart Packages (108 package — مستخرجة من AOT snapshot)

### التطبيق والبنية
| الحزمة | الدور |
|---|---|
| `tachidesk_sorayomi` | **التطبيق نفسه** (أساس Sorayomi المفتوح) |
| `flutter_riverpod` + `hooks_riverpod` + `riverpod` | إدارة الحالة |
| `go_router` | التنقل |
| `freezed_annotation` + `json_annotation` | نماذج مجمدة + JSON |
| `flutter_hooks` | خطافات Widgets |
| `rxdart` + `stream_transform` + `queue` | بث ومهام |
| `flutter_localizations` + `intl` | 29 لغة (العربية بينها!) |

### الشبكات والبيانات
| الحزمة | الدور |
|---|---|
| `dio` + `http` + `cupertino_http` | عملاء HTTP |
| `web_socket_channel` + `web_socket` | مزامنة realtime |
| `sqflite_darwin` + `sqflite_common` | SQLite |
| `shared_preferences_foundation` | إعدادات |
| `crypto` + `uuid` + `mime` | أدوات |
| `system_proxy` | بروكسي النظام |

### الواجهة والصور
| الحزمة | الدور |
|---|---|
| `flex_color_scheme` + `flex_seed_scheme` | محرك السمات |
| `cupertino_native` + `cupertino_modal_sheet` | مكونات iOS أصلية |
| `cached_network_image` + `flutter_cache_manager` + `octo_image` | كاش الصور |
| `photo_view` | تكبير الصور |
| `palette_generator` | استخراج ألوان من الأغلفة! |
| `infinite_scroll_pagination` + `scrollable_positioned_list` + `scroll_to_index` + `infinite_listview` | قوائم متقدمة |
| `visibility_detector` | تحسين الأداء |
| `numberpicker` + `markdown_widget` + `highlight` + `markdown` | عناصر واجهة |
| `flutter_perf_monitor` | مراقب أداء |

### iOS/المنصة
| الحزمة | الدور |
|---|---|
| `sign_in_with_apple` | Apple ID |
| `local_auth_darwin` | Face ID |
| `in_app_purchase_storekit` | اشتراكات |
| `flutter_web_auth_2` | OAuth (التتبع) |
| `webview_flutter_wkwebview` | WebViews (تجاوز Cloudflare) |
| `apple_pencil_double_tap` | قلم Apple Pencil! |
| `image_picker_ios` + `file_picker` | اختيار ملفات |
| `url_launcher_ios` + `package_info_plus` + `device_info_plus` + `connectivity_plus` | أدوات منصة |
| `flutter_path_provider_plus` + `path_provider_foundation` | مسارات |
| `in_app_review` | طلب تقييم |
| `fluttertoast` | إشعارات |
| `google_mobile_ads` | إعلانات |
| `flutter_nsfw` | كشف NSFW |
| `libzstd` | ضغط zstd |
| `cupertino_http` | URLSession الأصلي |

### أدوات
`async · characters · clock · collection · convert · cross_file · ffi · file · http_parser · http_status · logging · material_color_utilities · meta · path · source_span · stack_trace · stream_channel · string_scanner · synchronized · term_glyph · typed_data · vector_math`

## Native iOS Frameworks (40+)

### Flutter الأساس
`Flutter.framework` (المحرك) · `App.framework` (Dart AOT 21.7MB)

### المكونات الأصلية (Objective-C/Swift)
| Framework | الاستخدام |
|---|---|
| SDWebImage | تحميل صور عالي الأداء |
| SSZipArchive | أرشفة ZIP (ملفات التنزيل) |
| FMDB | SQLite wrapper |
| SAMKeychain | Keychain آمن |
| NSFWDetector + flutter_nsfw | كشف محتوى +18 (CoreML!) |
| HCSStarRatingView | نجوم التقييم |
| SVProgressHUD | HUD تحميل |
| DWAlertController | تنبيهات iOS |
| Mantle + Masonry | إرث من الطبقة القديمة Swift |
| FileMD5Hash | فحص ملفات |
| Promises/FBLPromises + GoogleDataTransport + GoogleUtilities + nanopb | بنية Firebase |
| libzstd | ضغط |

### Firebase Suite
`FirebaseCore · FirebaseCrashlytics · FirebaseRemoteConfig · FirebaseABTesting · FirebaseInstallations · FirebaseSessions · FirebaseCoreExtension · FirebaseCoreInternal · FirebaseRemoteConfigInterop · FirebaseSharedSwift` + `GoogleMobileAdsResources.bundle` + `UserMessagingPlatformResources.bundle` (GDPR)

### السحابة
- `GoogleService-Info.plist` — تكوين Firebase (Crashlytics + RemoteConfig + Analytics)
- خادم مزامنة Tachimanga (خاص بالمغلق)
- خادم حساب MangaCrush (خاص بالمغلق)

## نظام JVM المدمج (الابتكار الأهم)

| الملف | الحجم | الوظيفة |
|---|---|---|
| `jre/lib/modules` | 96.6 MB | صورة وحدات Java كاملة (OpenJ9 — Eclipse OpenJ9 JVM حسب رسائل الخطأ J9VM) |
| `jre/lib/jrt-fs.jar` | — | نظام ملفات الوحدات |
| `jre/lib/security/` | — | مزودات الأمان + شهادات CA |
| `jre/lib/tzdb.dat` | — | قاعدة مناطق زمنية |
| `jre/lib/java.properties` | 145 KB | رسائل JVM |
| `jre/conf/` + `options.default` | — | تكوين |
| `Tachimanga.dylib` | 6 MB | **الجسر** — يضمّن JVM داخل عملية iOS ويدير دورة حياة الخادم |

> **بديل مفتوح المصدر لهذا الجزء:** [OpenJDK Mobile](https://github.com/openjdk/mobile) (رسمي من OpenJDK، يدعم iOS) أو تشغيل Suwayomi-Server على خادم خارجي/منزلي.

## كيف اكتُشفت هذه القوائم؟
كل الأسماء أعلاه مستخرجة حرفياً من:
1. `Frameworks/App.framework/App` — Dart AOT snapshot (أسماء الحزم والملفات محفوظة كنص)
2. `Frameworks/` — قائمة الديبلات
3. `jre/` — فحص ملفات JVM
4. `Info.plist` — البيانات الوصفية

الأدوات: `strings`, `unzip`, `file`, Python plistlib — كلها في [`tools/`](../tools/)
