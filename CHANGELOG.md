# Changelog

All notable changes to Moon Bugs are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.6.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.6.0
[0.5.2]: https://github.com/yarivha/MoonBugs/releases/tag/v0.5.2
[0.5.1]: https://github.com/yarivha/MoonBugs/releases/tag/v0.5.1
[0.5.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.5.0
[0.4.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.4.0
[0.3.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.3.0
[0.2.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.2.0
[0.1.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.1.0
