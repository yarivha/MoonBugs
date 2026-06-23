#!/usr/bin/env bash
# ============================================================================
#  bundle_macos.sh — package Moon Bugs as a macOS .app with a Finder/Dock icon
#
#  On macOS a bare Unix executable has no icon; the icon comes from a .app
#  bundle whose Info.plist points at an .icns in Resources/. This script:
#    1. builds the release binary,
#    2. turns assets/icon.png into AppIcon.icns (sips + iconutil),
#    3. assembles dist/MoonBugs.app.
#
#  Usage:  ./tools/bundle_macos.sh
#  Output: dist/MoonBugs.app  (double-click it, or drag to /Applications)
# ============================================================================
set -euo pipefail

cd "$(dirname "$0")/.."   # project root
ROOT="$(pwd)"
APP="$ROOT/dist/MoonBugs.app"
NAME="MoonBugs"

# Use a prebuilt binary if MOONBUGS_BIN is set (e.g. a universal binary from
# CI); otherwise build a release binary for the host architecture.
if [ -n "${MOONBUGS_BIN:-}" ]; then
  echo "==> Using prebuilt binary: $MOONBUGS_BIN"
  BIN="$MOONBUGS_BIN"
else
  echo "==> Building release binary"
  cargo build --release
  BIN="$ROOT/target/release/moonbugs"
fi

echo "==> Generating AppIcon.icns from assets/icon.png"
ICONSET="$(mktemp -d)/AppIcon.iconset"
mkdir -p "$ICONSET"
# Standard macOS icon sizes (point size + @2x retina variant).
for spec in "16:16x16" "32:16x16@2x" "32:32x32" "64:32x32@2x" \
            "128:128x128" "256:128x128@2x" "256:256x256" "512:256x256@2x" \
            "512:512x512" "1024:512x512@2x"; do
  px="${spec%%:*}"; label="${spec##*:}"
  sips -z "$px" "$px" "$ROOT/assets/icon.png" --out "$ICONSET/icon_${label}.png" >/dev/null
done
mkdir -p "$APP/Contents/Resources"
iconutil -c icns "$ICONSET" -o "$APP/Contents/Resources/AppIcon.icns"

echo "==> Assembling bundle structure"
mkdir -p "$APP/Contents/MacOS"
cp "$BIN" "$APP/Contents/MacOS/$NAME"

cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key>            <string>${NAME}</string>
  <key>CFBundleDisplayName</key>     <string>Moon Bugs</string>
  <key>CFBundleIdentifier</key>      <string>com.yariv.moonbugs</string>
  <key>CFBundleVersion</key>         <string>0.2.0</string>
  <key>CFBundleShortVersionString</key><string>0.2.0</string>
  <key>CFBundlePackageType</key>     <string>APPL</string>
  <key>CFBundleExecutable</key>      <string>${NAME}</string>
  <key>CFBundleIconFile</key>        <string>AppIcon</string>
  <key>NSHighResolutionCapable</key> <true/>
  <key>LSMinimumSystemVersion</key>  <string>10.12</string>
</dict>
</plist>
PLIST

# Refresh Finder's icon cache for this bundle.
touch "$APP"

echo "==> Done: $APP"
