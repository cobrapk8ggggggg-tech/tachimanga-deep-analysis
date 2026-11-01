#!/usr/bin/env bash
# analyze_ipa.sh — استطلاع كامل لأي IPA (iOS App)
# الاستخدام: ./analyze_ipa.sh <path/to/AppName.ipa> <output_dir>
set -euo pipefail

IPA="${1:?Usage: $0 <app.ipa> <out_dir>}"
OUT="${2:-recon_out}"
mkdir -p "$OUT"

echo "==== [1/7] Extract IPA ===="
rm -rf "$OUT/ipa"
unzip -o -q "$IPA" -d "$OUT/ipa"
APP=$(find "$OUT/ipa/Payload" -maxdepth 1 -name "*.app" | head -1)
echo "APP: $APP"

echo "==== [2/7] Info.plist ===="
python3 - "$APP/Info.plist" <<'PYEOF'
import plistlib, sys, json
with open(sys.argv[1], 'rb') as f:
    p = plistlib.load(f)
interesting = {k: v for k, v in p.items() if not k.startswith('DT')}
print(json.dumps(interesting, indent=2, default=str))
PYEOF

echo "==== [3/7] Frameworks inventory ===="
du -sh "$APP"/Frameworks/* 2>/dev/null | sort -rh | tee "$OUT/frameworks.txt"

echo "==== [4/7] Dart AOT structure ===="
AOT="$APP/Frameworks/App.framework/App"
if [ -f "$AOT" ]; then
  strings -a "$AOT" > "$OUT/dart_aot_strings.txt"
  grep -oE "package:[a-zA-Z_0-9]+/" "$OUT/dart_aot_strings.txt" | sort -u > "$OUT/dart_packages.txt"
  # التطبيق الأساسي: ابحث عن package غير معروف كحزمة طرف ثالث
  grep -oE "package:[a-zA-Z_0-9/]+\.dart" "$OUT/dart_aot_strings.txt" | sort -u > "$OUT/dart_files.txt"
  echo "Packages: $(wc -l < "$OUT/dart_packages.txt") | Dart files: $(wc -l < "$OUT/dart_files.txt")"
fi

echo "==== [5/7] URLs & endpoints ===="
grep -ohE "(https?|wss?)://[a-zA-Z0-9./_:?=&%-]+" "$OUT"/*.txt 2>/dev/null | sort -u > "$OUT/urls.txt" || true

echo "==== [6/7] Mach-O report ===="
for f in "$APP/Tachimanga" "$APP"/Frameworks/*.dylib "$APP"/Frameworks/*.framework/*; do
  [ -f "$f" ] && file "$f"
done | tee "$OUT/macho.txt"

echo "==== [7/7] JVM check ===="
if [ -d "$APP/jre" ]; then
  echo "Embedded JVM found (OpenJ9-style):" | tee "$OUT/jvm.txt"
  du -sh "$APP/jre/lib/modules" | tee -a "$OUT/jvm.txt"
fi

echo ""
echo "✅ DONE — النتائج في: $OUT/"
echo "   أهم ملف: $OUT/dart_files.txt (بنية ملفات التطبيق)"
