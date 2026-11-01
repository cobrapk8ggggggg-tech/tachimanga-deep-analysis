# 03 — Complete Feature Map / خريطة الميزات الكاملة

> مستخرجة حرفياً من كود Dart AOT — **649 ملف** موزعة على **15 وحدة ميزات**
> القائمة الكاملة بالملفات: [`data/extracted/app_dart_files_full.txt`](../data/extracted/app_dart_files_full.txt)

---

## 🗂️ الوحدات الـ 15

| # | الوحدة | الملفات | الوصف |
|---|---|---|---|
| 1 | `library` | 25 | المكتبة: التصنيفات، الفلاتر، الفرز، التحديد الجماعي |
| 2 | `browse_center` | 90+ | الاستكشاف: المصادر، الإضافات، البحث الشامل، الترحيل |
| 3 | `manga_book` | 120+ | المانجا: التفاصيل، الفصول، **القارئ**، التنزيلات، السجل، التحديثات |
| 4 | `settings` | 100+ | الإعدادات الكاملة (8 أقسام فرعية) |
| 5 | `account` | 11 | حساب MangaCrush: تسجيل/دخول/تحقق/استعادة + Apple |
| 6 | `sync` | 11 | المزامنة السحابية realtime |
| 7 | `stats` | — | إحصائيات القراءة |
| 8 | `bulk_tracking` | 12 | تتبع جماعي (MAL/AniList/Kitsu...) |
| 9 | `bulk_migrate` | 8 | ترحيل جماعي بين المصادر |
| 10 | `custom` | 25+ | **إضافات MangaCrush:** الإعلانات، In-App Purchases، ألوان HEX |
| 11 | `about` | 10+ | حول التطبيق + شاشة الشكر |
| 12 | `help` | 9 | أدلة مساعدة (Markdown pages) |
| 13 | `app_update` | 3 | تحديثات التطبيق |
| 14 | `remote_notice` | — | إشعارات بعيدة (RemoteConfig) |
| 15 | `whats_new` | — | ما الجديد |

---

## 📚 1. المكتبة (Library) — `src/features/library/`

```
library_screen.dart                 → الشاشة الرئيسية (Tab 1)
├── library_app_bar.dart            → شريط علوي: بحث، فلتر، فرز، عرض شبكي/قائمة
├── library_category_tab.dart       → تبويب لكل تصنيف
├── category_manga_list.dart        → قائمة مانجا التصنيف
├── library_manga_display.dart      → عرض الأغلفة (شبكة/قائمة/شبكة مضغوطة)
├── library_manga_filter.dart       → ورقة الفلاتر: مكتمل، قيد التنزيل، غير مقروء...
├── library_manga_organizer.dart    → الفرز: عنوان، آخر قراءة، تاريخ إضافة، غير مقروء...
├── library_select_icon_button.dart → وضع التحديد الجماعي
├── multi_manga_action_bar.dart     → شريط إجراءات جماعية (نقل تصنيف، تتبع، حذف، ترحيل)
├── batch_edit_manga_category_dialog.dart
├── edit_category_screen.dart       → إدارة التصنيفات (إنشاء/ترتيب/حذف)
└── category_create_fab.dart
```

**نموذج البيانات:** `category_model.dart` (id, name, order, flags)

## 🔎 2. الاستكشاف (Browse) — `src/features/browse_center/`

```
browse_screen.dart            → الشاشة الرئيسية (Tab 2)
├── extension_screen.dart     → متجر الإضافات (تنزيل من مستودعات)
│   ├── extension_list_tile.dart          → بطاقة إضافة (اسم، لغة، نجمة، حالة)
│   ├── extension_language_filter_dialog  → فلترة باللغات
│   ├── extension_info_screen             → صفحة تفاصيل الإضافة + مصادرها
│   └── install_extension_file.dart       → تثبيت إضافة من ملف محلي (.apk/.tup)!
├── source_screen (controller: source_controller.dart)
│   ├── sources grid حسب اللغة
│   ├── source_query_controller.dart      → بحث داخل المصدر
│   └── source_custom_filter_controller.dart → فلاتر المصدر الديناميكية!
├── global_search_screen.dart → بحث في كل المصادر المفعلة دفعة واحدة
│   └── source_quick_search.dart          → نتائج سريعة لكل مصدر
└── migrate_screen.dart       → الترحيل بين المصادر
    ├── migrate_source_detail_screen      → مقارنة المصدر القديم/الجديد
    └── migration_target_preview.dart     → معاينة قبل الترحيل
```

**نماذج البيانات:** `source_model`, `extension_info_model`, `filter_model` (فلاتر ديناميكية من المصدر: TriState, Select, Text, Sort!), `language_model`

## 📖 3. المانجا والقارئ (Manga Book) — `src/features/manga_book/`

### 3a. تفاصيل المانجا
```
manga_details_screen.dart      → الغلاف، العنوان، المؤلف، الفنان، الحالة، المصدر
├── manga_details_app_bar      → مشاركة، تتبع، تصنيف، تحميل
├── manga_cover_screen.dart    → عرض الغلاف مكبّراً
├── manga_note_screen.dart     → ملاحظات شخصية للمانجا
├── chapter_list_tile.dart     → صف فصل (رقم، تاريخ، scanned by، غير مقروء، محفوظ)
├── chapter_filter_icon_button → فلاتر الفصول
├── edit_manga_category_dialog
└── big_screen_manga_details   → تخطيط iPad/landscape
```

### 3b. القارئ (أقوى جزء — انظر 02-ARCHITECTURE §9)
```
reader_screen_v2.dart          → شاشة القارئ كاملة الشاشة
├── reader_controller_v2       → منطق التنقل بين الصفحات/الفصول
├── reader_setting_controller  → إعدادات القارئ (تُحفظ لكل قراءة + عالمية)
├── أنماط القراءة:
│   ├── continuous_reader_mode_v2      → Webtoon/متصل
│   ├── single_page_reader_mode_v2     → صفحة صفحة
│   ├── double_page_reader_mode_v2     → صفحتان (spread)
│   └── page_curl                      → قلب واقعي 3D (CustomPainter!)
├── تخطيطات اللمس: edge / kindlish / L-shaped / right_and_left
├── reader_bottom_bar          → شريط سفلي: شريط تمرير صفحات، وضع، إعدادات
├── page_number_slider         → سحب للتنقل السريع
├── long_press_scroll_speed    → تمرير تلقائي بسرعة متغيرة
├── reader_edge_gestures       → نقر/سحب قابل للتخصيص
└── reader_appearance          → خلفية، padding، فاصل فصول، عرض التقدم
```

### 3c. التنزيلات
```
downloads_screen.dart          → طابور التنزيلات (Tab منفصل)
├── download_progress_list_tile → شريط تقدم لكل مانجا
├── downloads_parallel_button   → تنزيل متوازٍ (عدة فصول دفعة واحدة)
├── download_pip_button         → نافذة عائمة (PiP) تُظهر التقدم أثناء التصفح!
├── bgc_download_settings_screen → إعدادات التنزيل الخلفي
└── download_reward_ad_dialog   → (MangaCrush) مشاهدة إعلان = طاقة تنزيل
```

### 3d. السجل والتحديثات
```
history_screen.dart            → سجل القراءة (Tab 4)
├── history_descriptive_list_tile → "قرأت فصل X من Y قبل ساعتين"
├── history_multi_action_bar      → إزالة من السجل جماعياً
└── incognito_icon_button         → وضع التخفي (لا يُسجَّل تقدم!)
updates (updates_repository)   → سجل التحديثات الجديدة من المصادر (Tab 3)
```

## ⚙️ 4. الإعدادات (Settings) — `src/features/settings/` (8 أقسام)

| القسم | المحتوى |
|---|---|
| **Appearance** | 15+ سمة (Midnight Dusk, Tako...)، أسود نقي، مستوى المزج، **Liquid Glass**، أيقونات التطبيق (29!)، تنسيق التاريخ، عدد أعمدة الشبكة، تدوير الشاشة |
| **Library** | سلوك التحديث العالمي، فئات افتراضية |
| **Reader** | كل إعدادات القارئ + رسوميات + حركات الانتقال (`reader_page_animation_preferences`) |
| **Downloads** | مواقع، عدد متزامن، إعادة محاولة |
| **Tracking** | ربط MAL/AniList/Kitsu/Shikimori + `tracking_repository` |
| **Browse** | مستودعات الإضافات (`edit_repo_screen`)، `remote_blacklist` (حجب مصادر عن بعد!) |
| **Backup** | نسخ احتياطي يدوي/تلقائي (frequency, limit, retention) + **نسخ للسحابة** + استيراد `.tachibk` |
| **Sync** | ربط بخادم Tachimanga Sync، مزامنة الآن، إعدادات |
| **Advanced** | User-Agent مخصص، **HTTP Dump** (تسجيل طلبات الشبكة كاملة للتشخيص!)، DHT |

## 👤 5. الحساب (Account) — إضافة MangaCrush المغلقة

```
account_login_screen / account_register_screen / account_register_verify_screen
account_reset_password_screen / account_change_password_screen
signin_with_apple.dart         → دخول بـ Apple ID
account_status_tile.dart       → حالة الاشتراك
login_terms_widget.dart        → شروط الاستخدام
```

## 💎 6. Premium (custom/inapp) — إضافة MangaCrush المغلقة

```
purchase_screen2.dart          → شاشة الاشتراك (خطط، أسعار)
premium_features_screen.dart   → جدول الميزات المدفوعة
premium_features_b.dart        → عرض بديل (A/B)
purchase_check.dart            → التحقق من الاستلام مع App Store
promotion/                     → نوافذ ترويجية + بانرات
testflight_purchase_alert.dart → تنبيه خاص لمستخدمي TestFlight
```
> **لمشروعك الخاص:** هذه الوحدة غير ضرورية — تطبيقك الخاص لا يحتاج اشتراكات (وأنت المالك).

## 📺 7. الإعلانات (custom/ads) — إضافة MangaCrush المغلقة

```
reward_ads_controller.dart     → إعلانات المكافآت (طاقة تنزيل / معاينة القارئ)
reward_ads_config.dart         → تكوين RemoteConfig للإعلانات
ad_controller.dart (reader)    → إعلان بين صفحات القارئ (النسخة المجانية)
```

## 🔄 8. المزامنة (Sync)

```
sync_controller.dart           → منطق المزامنة
sync_repository.dart           → REST للخادم
realtime_sync_hero.dart        → مزامنة فورية (WebSocket!)
sync_now_tile.dart / sync_settings_screen
```

## 📊 9. الإحصائيات (Stats)
إحصائيات القراءة: الوقت المقروء، الفصول، توزيع حسب المصدر.

## 📦 10. التتبع الجماعي والترحيل الجماعي
- `bulk_tracking/` — ربط عشرات المانجا بمواقع التتبع دفعة واحدة مع `rate_config` (حماية من rate-limit)
- `bulk_migrate/` — ترحيل المكتبة كاملة لمصدر آخر مع بحث تلقائي ومطابقة (`matching_in_progress_dialog`)

## 🆘 11. المساعدة + حول
`help_screen.dart` — صفحات Markdown مضمنة: أسئلة النسخ الاحتياطي، أسئلة المصادر المحلية، أسئلة المزامنة، دليل متجر الإضافات.

---

## 🧩 المكونات المشتركة (Common Widgets)
- `cupertino_modal_sheet` — أوراق iOS أصلية بسحب للإغلاق
- `infinite_scroll_pagination` — تحميل لا نهائي
- `scrollable_positioned_list` — قوائم مواضع دقيقة
- `numberpicker` — منتقي أرقام iOS-Style
- `HCSStarRatingView` — تقييم بالنجوم أصلي
- `SVProgressHUD` — مؤشرات تحميل iOS-Style
- `DWAlertController` — تنبيهات بنمط UIAlertController
- `photo_view` — تكبير/تصغير الصور
