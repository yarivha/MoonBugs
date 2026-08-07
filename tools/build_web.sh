#!/usr/bin/env bash
# ============================================================================
#  build_web.sh — assemble the WebAssembly build into dist/web/
#
#  Produces a fully static directory (index.html + mq_js_bundle.js +
#  moonbugs.wasm) that can be served by any HTTP server. All game assets are
#  baked into the .wasm via include_bytes!, so nothing else needs hosting.
#
#  Usage:  ./tools/build_web.sh   &&   python3 -m http.server -d dist/web 8080
# ============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist/web"

rustup target add wasm32-unknown-unknown >/dev/null 2>&1 || true

echo "Building moonbugs for wasm32-unknown-unknown ..."
cargo build --release --target wasm32-unknown-unknown --manifest-path "$ROOT/Cargo.toml"

# macroquad ships the JS glue inside the crate; pick the copy matching the
# exact version in Cargo.lock so the bundle can never drift from the binary.
MQ_VER="$(awk '/^name = "macroquad"$/{f=1; next} f && /^version = /{gsub(/[",]/,"",$3); print $3; exit}' "$ROOT/Cargo.lock")"
[ -n "$MQ_VER" ] || { echo "error: could not read the macroquad version from Cargo.lock" >&2; exit 1; }

BUNDLE="$(find "${CARGO_HOME:-$HOME/.cargo}/registry/src" -type f \
  -path "*macroquad-$MQ_VER/js/mq_js_bundle.js" -print -quit)"
[ -n "$BUNDLE" ] || { echo "error: mq_js_bundle.js not found for macroquad $MQ_VER" >&2; exit 1; }

mkdir -p "$OUT"
cp "$ROOT/target/wasm32-unknown-unknown/release/moonbugs.wasm" "$OUT/"
cp "$BUNDLE" "$OUT/"
cp "$ROOT/web/index.html" "$OUT/"

echo "Done -> $OUT"
ls -lh "$OUT"
echo
echo "Serve it (the wasm is fetched, so file:// will not work):"
echo "  python3 -m http.server -d dist/web 8080"
