#!/usr/bin/env python3
# ============================================================================
#  gen_music.py — procedural chiptune background loop for Moon Bugs
#
#  Synthesizes a seamless ~8s looping track (bass + arpeggio over a classic
#  Am–F–C–G progression) into assets/music.wav. Pure stdlib, no deps.
#  Re-run: `python3 tools/gen_music.py`
# ============================================================================

import os
import struct
import wave

SR = 44100
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

BEAT = 0.5          # seconds per beat (120 BPM)
BEATS_PER_BAR = 4

# Calm overworld theme — Am-F-C-G, mid tempo, sparkly octave-up arps.
PROG = [
    (110.00, [220.00, 261.63, 329.63]),  # Am
    (87.31, [174.61, 220.00, 261.63]),   # F
    (130.81, [261.63, 329.63, 392.00]),  # C
    (98.00, [196.00, 246.94, 293.66]),   # G
]

# Boss theme — minor, low + fast, with a driving eighth-note bass and a tense
# A-major (dominant) cadence. Roots sit an octave lower for menace.
PROG_BOSS = [
    (73.42, [146.83, 174.61, 220.00]),   # Dm
    (98.00, [196.00, 233.08, 293.66]),   # Gm
    (55.00, [138.59, 220.00, 277.18]),   # A  (C# leading-tone tension)
    (55.00, [138.59, 220.00, 277.18]),   # A
]


def osc(t, freq, kind):
    """One oscillator sample. 'square' for bass punch, 'tri' for soft arps."""
    p = (t * freq) % 1.0
    if kind == "square":
        return 1.0 if p < 0.5 else -1.0
    # triangle
    return 4.0 * abs(p - 0.5) - 1.0


def note(freq, dur, vol, kind):
    """A single note with a short attack and a release tail (click-free)."""
    n = int(SR * dur)
    atk = max(1, int(0.008 * n))
    rel = max(1, int(0.18 * n))
    out = []
    for i in range(n):
        a = min(1.0, i / atk)
        r = min(1.0, (n - i) / rel)
        out.append(osc(i / SR, freq, kind) * vol * a * r)
    return out


def build(prog, beat, arp_mult, driving_bass):
    """Render a looping track from a chord progression to a float buffer."""
    bars = len(prog)
    total = int(SR * beat * bars * BEATS_PER_BAR)
    buf = [0.0] * total

    def add(samples, start):
        for i, s in enumerate(samples):
            j = start + i
            if 0 <= j < total:
                buf[j] += s

    for bar, (root, tones) in enumerate(prog):
        base = bar * BEATS_PER_BAR
        if driving_bass:
            # Relentless eighth-note root pulse for tension.
            for k in range(BEATS_PER_BAR * 2):
                start = int((base * beat + k * beat * 0.5) * SR)
                add(note(root, beat * 0.5 * 0.95, 0.5, "square"), start)
        else:
            # Calm: one root pulse per beat.
            for k in range(BEATS_PER_BAR):
                start = int((base + k) * beat * SR)
                add(note(root, beat * 0.92, 0.48, "square"), start)
        # Arpeggio: eighth notes cycling the chord tones.
        for j in range(BEATS_PER_BAR * 2):
            start = int((base * beat + j * beat * 0.5) * SR)
            freq = tones[j % len(tones)] * arp_mult
            add(note(freq, beat * 0.5 * 0.9, 0.30, "tri"), start)

    # Normalize to avoid clipping, leave a little headroom.
    peak = max(1e-6, max(abs(s) for s in buf))
    scale = 0.85 / peak if peak > 0.85 else 1.0
    return [max(-1.0, min(1.0, s * scale)) for s in buf]


def write_wav(name, buf):
    path = os.path.join(ASSETS, name)
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        for s in buf:
            frames += struct.pack("<h", int(s * 32767))
        w.writeframes(bytes(frames))
    print(f"  wrote {name} ({len(buf) / SR:.1f}s loop)")


def main():
    os.makedirs(ASSETS, exist_ok=True)
    print("Generating Moon Bugs background music ...")
    # Calm theme: mid tempo (120 BPM), octave-up sparkle, gentle bass.
    write_wav("music.wav", build(PROG, 0.5, 2.0, driving_bass=False))
    # Boss theme: fast (~190 BPM), low arps, pounding eighth bass.
    write_wav("music_boss.wav", build(PROG_BOSS, 0.32, 1.0, driving_bass=True))
    print("Done.")


if __name__ == "__main__":
    main()
