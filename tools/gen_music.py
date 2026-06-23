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
BARS = 4
BEATS_PER_BAR = 4
TOTAL = int(SR * BEAT * BARS * BEATS_PER_BAR)

# Am – F – C – G : (bass root, [chord tones])
PROG = [
    (110.00, [220.00, 261.63, 329.63]),  # Am
    (87.31, [174.61, 220.00, 261.63]),   # F
    (130.81, [261.63, 329.63, 392.00]),  # C
    (98.00, [196.00, 246.94, 293.66]),   # G
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


def main():
    os.makedirs(ASSETS, exist_ok=True)
    print("Generating Moon Bugs background music ...")
    buf = [0.0] * TOTAL

    def add(samples, start):
        for i, s in enumerate(samples):
            j = start + i
            if 0 <= j < TOTAL:
                buf[j] += s

    for bar in range(BARS):
        root, tones = PROG[bar]
        bar_beat0 = bar * BEATS_PER_BAR
        # Bass: a root pulse on every beat.
        for k in range(BEATS_PER_BAR):
            start = int((bar_beat0 + k) * BEAT * SR)
            add(note(root, BEAT * 0.92, 0.48, "square"), start)
        # Arpeggio: eighth notes climbing the chord, one octave up for sparkle.
        for j in range(BEATS_PER_BAR * 2):
            start = int((bar_beat0 * BEAT + j * BEAT * 0.5) * SR)
            freq = tones[j % len(tones)] * 2.0
            add(note(freq, BEAT * 0.5 * 0.9, 0.30, "tri"), start)

    # Normalize to avoid clipping, leave a little headroom.
    peak = max(1e-6, max(abs(s) for s in buf))
    scale = 0.85 / peak if peak > 0.85 else 1.0

    path = os.path.join(ASSETS, "music.wav")
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        for s in buf:
            v = max(-1.0, min(1.0, s * scale))
            frames += struct.pack("<h", int(v * 32767))
        w.writeframes(bytes(frames))
    print(f"  wrote music.wav ({TOTAL / SR:.1f}s loop)")
    print("Done.")


if __name__ == "__main__":
    main()
