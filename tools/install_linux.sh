#!/usr/bin/env bash
# ============================================================================
#  install_linux.sh — install Moon Bugs with a desktop launcher + icon
#
#  On Linux an executable carries no icon itself; the desktop environment shows
#  an icon via a .desktop entry that references an icon installed in the
#  hicolor icon theme. This script:
#    1. builds the release binary,
#    2. installs it to $PREFIX/bin,
#    3. installs the icon into the hicolor theme,
#    4. installs the .desktop launcher and refreshes the caches.
#
#  Usage:  ./tools/install_linux.sh           # installs into ~/.local
#          sudo PREFIX=/usr/local ./tools/install_linux.sh   # system-wide
# ============================================================================
set -euo pipefail

cd "$(dirname "$0")/.."
PREFIX="${PREFIX:-$HOME/.local}"

echo "==> Building release binary"
cargo build --release

echo "==> Installing to $PREFIX"
install -Dm755 target/release/moonbugs "$PREFIX/bin/moonbugs"
install -Dm644 assets/icon.png \
  "$PREFIX/share/icons/hicolor/512x512/apps/moonbugs.png"
install -Dm644 packaging/moonbugs.desktop \
  "$PREFIX/share/applications/moonbugs.desktop"

# Best-effort cache refresh so the launcher/icon appear immediately.
update-desktop-database "$PREFIX/share/applications" 2>/dev/null || true
gtk-update-icon-cache -f -t "$PREFIX/share/icons/hicolor" 2>/dev/null || true

echo "==> Done."
echo "    Make sure $PREFIX/bin is on your PATH, then launch 'Moon Bugs'"
echo "    from your app menu or run: moonbugs"
