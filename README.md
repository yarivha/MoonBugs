# Moon Bugs — Lunar Defense

A modern, [macroquad](https://macroquad.rs/)-based homage to Windmill Software's
1983 arcade game *Moon Bugs*.

Defend a row of fuel drums on the lunar surface from swooping alien bugs. Bugs
descend in weaving patterns, then dive to grab a drum and haul it off the top of
the screen. Shoot a carrier and it **drops the drum** — which falls safely back
to the ground if it survives the trip. Lose all your drums (or all your lives)
and it's game over.

## Run it

```sh
cargo run --release
```

The first build pulls in macroquad and takes a minute; after that it's instant.

## Controls

| Action | Keys                |
| ------ | ------------------- |
| Move   | `←` / `→` or `A`/`D` |
| Fire   | `Space` or `↑`      |
| Pause  | `P`                 |
| Mute   | `M`                 |
| Start / restart | `Enter`    |
| Quit   | `Esc`               |

## Sound

All SFX (laser, explosions, power-up jingle, wave fanfare, game-over dirge, etc.)
are **procedurally generated chiptune** — no binary assets checked in by hand.
The WAVs in `assets/` are **embedded into the binary at compile time** (via
`include_bytes!`), so the built executable is fully self-contained and needs no
asset folder at runtime.

Regenerate the sounds any time with:

```sh
python3 tools/gen_sounds.py   # writes assets/*.wav, pure stdlib, no deps
```

The `assets/*.wav` files must exist at **build** time (they get baked in); they
are *not* needed alongside the shipped binary. Toggle audio in-game with `M`.

## Icon

The app icon is procedurally drawn (a green moon-bug on a starry rounded square):

```sh
python3 tools/gen_icon.py   # writes assets/icon.png + assets/icon_*.rgba
```

- **All platforms (running window):** the 16/32/64px raw-RGBA buffers are
  embedded in the binary and used as the window / taskbar / dock icon
  (`Conf.icon`). Nothing extra needed.
- **Windows (.exe file icon):** `assets/icon.ico` is embedded into the
  executable by `build.rs` (via the `winresource` build-dependency). Building
  for a Windows target just works on Windows; cross-compiling needs a resource
  compiler (`llvm-rc` or mingw `windres`) on PATH, otherwise the build still
  succeeds without the embedded icon.
- **macOS (Finder/Dock file icon):** a bare executable has no Finder icon — that
  comes from a `.app` bundle. Build one (with `icon.png` → `AppIcon.icns`) via:

  ```sh
  ./tools/bundle_macos.sh    # produces dist/MoonBugs.app
  ```

  Then double-click `dist/MoonBugs.app` or drag it to `/Applications`.
- **Linux (launcher icon):** executables carry no icon; the desktop environment
  shows one via a `.desktop` entry plus an icon in the hicolor theme. Install
  both with:

  ```sh
  ./tools/install_linux.sh   # installs binary + icon + launcher into ~/.local
  ```

## Modern twists over the 1983 original

- **Escalating waves** — more bugs, faster, with armored variants from wave 3.
- **Carrier mechanic** — shoot a bug mid-heist and the drum drops back down.
- **Power-ups** dropped by killed bugs: Rapid fire (R), Spread shot (S), Shield (+).
- **Player lives + shield**, particle explosions, starfield, and a session high score.

## Ideas for later

- Background music loop (the `audio` module supports looped playback).
- Persistent high score to disk.
- Boss bug every N waves; bombs/smart-bomb power-up.
- Gamepad support.
- WebAssembly build (`cargo build --target wasm32-unknown-unknown`) to play in a browser.
