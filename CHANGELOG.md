# Changelog

All notable changes to Moon Bugs are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.3.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.3.0
[0.2.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.2.0
[0.1.0]: https://github.com/yarivha/MoonBugs/releases/tag/v0.1.0
