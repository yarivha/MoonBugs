# Changelog

All notable changes to Moon Bugs are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] - 2026-08-09

### Fixed
- **On a phone in portrait the score line and the barrels were cut off.** The
  canvas was sized with `100vh`, which on iOS Safari is the viewport *without*
  the browser toolbars — so the canvas stood taller than the visible area and
  the centred layout cropped an equal slice off the top (the HUD) and the
  bottom (the drums and the ground). It is now pinned to `visualViewport`, the
  one measurement that excludes the toolbars, and re-fitted on resize,
  rotation, and the toolbar collapsing. The web caption is also hidden on
  touch devices, where it lay across the drums.
- **The version stamp sat under the iPhone home indicator.** `viewport-fit=cover`
  lets the page reach into the safe areas, burying the bottom row of the game.
  The canvas now subtracts the safe-area insets and is anchored to the top, so
  the leftover strip falls where the indicator actually is, and the version is
  a little higher and brighter.

### Added
- **A big moon over the top-left of the sky**, as in the 1983 original —
  a cratered disc with a lit limb and a faint halo, drawn behind everything
  and sized from the screen so it looks the same on a phone as on a monitor.
  It sits below the HUD block rather than under it, and is deliberately dim,
  so the score and drum counts stay readable.

## [0.7.1] - 2026-08-08

### Fixed
- **A redeployed web build could keep running the old code.** The wasm filename
  never changes between releases, so a browser (or a caching proxy) held the
  previous binary until it expired, even though the HTML around it updated —
  and the sample Apache config caches `.wasm` for an hour, making that a
  guaranteed hour of confusion after every deploy. The page now loads
  `moonbugs.wasm?v=<version>`, stamped by `tools/build_web.sh`, so each release
  requests a URL no cache has seen.

## [0.7.0] - 2026-08-08

### Changed
- **Touch is now one-thumb: hold anywhere to steer and fire.** The buggy drives
  toward your finger and the cannon fires while you hold, replacing the
  separate move/fire pads — you point at where you want to be and it shoots on
  the way. The bomb keeps a button (bottom right, with its count) since it is a
  discrete action.

### Added
- The build version is stamped in the bottom-left corner of the main menu,
  dim and out of the way, so you can tell at a glance which build a machine
  or phone is actually running. Taken from `Cargo.toml` at compile time, so
  it cannot drift from the release.

### Fixed
- **Esc killed the web build.** It broke out of the game loop, which closes the
  window on desktop but in a browser simply abandons the canvas — leaving a
  blank page with only the HTML caption underneath and no way back. In the
  browser Esc now returns to the start screen (keeping your best score); on
  desktop it still quits.
- **The web build could hang before its first frame.** macroquad's wasm loader
  parks in `while !sound.is_loaded() { next_frame().await }`, so awaiting all
  twelve audio clips up front meant nothing was drawn until every decode
  finished — and on a browser that never finishes (iOS Safari keeps its
  AudioContext suspended until a user gesture) the page stayed a black screen
  with nothing to tap. Audio now loads in a coroutine alongside the game loop:
  the menu is up and playable on the first frame, and the sound joins when it
  is ready.

## [0.6.0] - 2026-08-08

### Added
- **Touch controls** — the game is fully playable on a phone or tablet with no
  keyboard. Tap anywhere to start or restart (the stand-in for `Enter`), and
  play with on-screen thumb pads: move left/right, fire, and bomb. The pads
  appear only after the first touch, so desktop play is untouched, and the
  audio buttons now respond to taps as well as clicks.
- **The interface scales to the display** — every HUD offset, text size and
  button was authored for the 900x640 design size and is now scaled to fit
  both axes, so the menu no longer overflows or overlaps on a small phone
  canvas (and stays proportional on a large monitor).

### Fixed
- Touch positions were out by the device pixel ratio: macroquad reports screen
  size in logical pixels but stores touch positions in physical ones, so on a
  2x phone screen every tap landed at double coordinates and missed every
  button. Converted once, at the input boundary.
- The web shell now fills the viewport and sets `touch-action: none`, so
  browser scroll and double-tap zoom no longer fight the controls.

## [0.5.2] - 2026-08-07

### Fixed
- The boss-wave banner showed a tofu box instead of a dash — it used an em
  dash, which macroquad's default font has no glyph for. Now plain ASCII.

### Removed
- **The GitHub Pages deployment** — the `Web` workflow is gone; the browser
  build is no longer auto-published to a URL. It still builds via
  `tools/build_web.sh` and ships as a release zip, to be hosted wherever you
  like.

## [0.5.1] - 2026-08-07

### Added
- **Web build attached to GitHub Releases** — each `v*` tag now also publishes
  `moonbugs-<version>-web.zip` (wasm + macroquad's JS glue + the HTML shell),
  so the browser version can be self-hosted or played offline instead of only
  the Pages URL. v0.5.0 shipped before this job existed, so it carries the
  three desktop archives only.

## [0.5.0] - 2026-08-07

### Added
- **Play in a browser** — the game now builds to WebAssembly and is published
  to GitHub Pages on every push to `main` (new `Web` workflow), so it is
  playable at `yarivha.github.io/MoonBugs` with sound and music intact. No
  game-code changes were needed: `tools/build_web.sh` assembles a static
  `dist/web/` from the wasm, macroquad's JS glue (version-matched to
  `Cargo.lock`), and the new `web/index.html` shell.

### Fixed
- The web shell works around two macroquad 0.4 web gotchas: its
  `mq_js_bundle.js` is `"use strict"` but assigns to an undeclared
  `register_plugin` (so the page pre-declares it, otherwise the tail of the
  bundle is aborted by a ReferenceError), and the bundle declares top-level
  `canvas`/`gl` (so the page's own script is wrapped in an IIFE to avoid a
  fatal redeclaration).

## [0.4.0] - 2026-08-06

### Added
- **Boss projectile attacks** — bosses now shell the surface with plasma
  volleys in three patterns: an aimed 3-shot burst that leads the buggy, a wide
  downward fan (5–7 bolts, wider on later bosses), and a 12-bolt radial ring
  from wave 20. Every volley is telegraphed by a ~0.65s charge-up — a ring
  collapsing into a swelling core under the boss, plus a firing line for aimed
  bursts — with matching charge and launch SFX (`boss_charge.wav`,
  `boss_shot.wav`, both procedurally generated). Volley spacing and bolt speed
  tighten with the wave. Bolts are absorbed by the shield, fizzle out in the
  lunar dust, and are swept away by a bomb or by the boss's own death.
- **Post-hit mercy window** — taking a hit grants ~1.2s of invulnerability
  (the buggy flickers). Applies to every damage source, so a single volley,
  swarm, or falling barrel costs one life instead of several at once.

## [0.3.0] - 2026-06-23

### Added
- **Bombs** — start with 3; press `B` to detonate one and clear the screen of
  bugs (carried drums drop safely; a boss takes heavy damage but isn't
  one-shot). Earn more from a new bomb power-up, capped at 5. HUD shows the
  count and a bright detonation flash plays.

### Changed
- Eased the difficulty: gentler per-wave speed scaling (with a cap), slower
  dives/carries, fewer bugs per wave, slightly longer spawn spacing, and a
  higher power-up drop rate (16% → 20%).
- GitHub Releases now use the matching `CHANGELOG.md` section as their notes.

### Fixed
- Windows `.exe` icon now displays in Explorer and the taskbar: the `.ico`
  stores small sizes (16–128px) as BMP rather than PNG, which Windows renders
  unreliably below 256px.

## [0.2.0] - 2026-06-23

### Added
- **Background music** — a procedurally generated, looping chiptune track
  (`tools/gen_music.py`), embedded in the binary.
- **Boss bug every 10th wave** — a large, horned, high-HP boss (`hp = 20 + wave`)
  with a floating health bar. It weaves across the top, creeps downward, and
  bumps the buggy for damage on a cooldown instead of stealing drums. The wave
  can't clear until it's destroyed; killing it pays a big score, a huge
  explosion, and a guaranteed extra life.
- **Scary boss theme** — a darker, faster track (`music_boss.wav`) that takes
  over when a boss appears and switches back to the calm theme afterward.
- **Independent music / SFX mute** — two clickable buttons (top-right: speaker
  for SFX, note for music) plus keyboard shortcuts `M` (SFX) and `N` (music).
- **Extra-life power-up** — a rare heart drop (~10% of power-ups) that grants
  +1 life, capped at 5.
- **Falling barrels hurt you** — a barrel dropped by a shot carrier now strikes
  the buggy like a bug (costs a life, or bounces off the shield).

### Changed
- Split the single mute control into independent music and SFX mutes.
- Moved the lives hearts below the new audio buttons so they don't overlap.

## [0.1.0] - 2026-06-23

### Added
- Initial playable game: a macroquad homage to Windmill Software's 1983
  *Moon Bugs*. Defend fuel drums from weaving, diving alien bugs across
  escalating waves; shoot a carrier to make it drop its drum.
- Power-ups: rapid fire, spread shot, and shield.
- Procedurally generated chiptune sound effects, embedded in the binary.
- Procedurally generated cross-platform icons: in-app window/dock icon
  (`Conf.icon`), Windows `.exe` icon (`build.rs` + `winresource`), a macOS
  `.app` bundle (`tools/bundle_macos.sh`), and a Linux launcher
  (`tools/install_linux.sh`).
- GitHub Actions release workflow building native binaries for Linux, Windows,
  and a universal macOS binary, publishing them to a GitHub Release on `v*` tags.

### Fixed
- Waves no longer stall: fleeing bugs that leave the top of the screen are
  retired, so the "all bugs cleared" check fires correctly.

[0.8.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.8.0
[0.7.1]: https://github.com/yarivha/MoonBugs/releases/tag/v0.7.1
[0.7.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.7.0
[0.6.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.6.0
[0.5.2]: https://github.com/yarivha/MoonBugs/releases/tag/v0.5.2
[0.5.1]: https://github.com/yarivha/MoonBugs/releases/tag/v0.5.1
[0.5.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.5.0
[0.4.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.4.0
[0.3.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.3.0
[0.2.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.2.0
[0.1.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.1.0
