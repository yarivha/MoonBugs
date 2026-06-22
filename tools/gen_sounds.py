#!/usr/bin/env python3
# ============================================================================
#  gen_sounds.py — procedural chiptune SFX generator for Moon Bugs
#
#  Synthesizes the game's sound effects as 16-bit mono 44.1kHz WAV files into
#  ../assets/. No external dependencies — pure stdlib (wave/struct/math/random).
#  Re-run any time to regenerate: `python3 tools/gen_sounds.py`
# ============================================================================

import math
import os
import random
import struct
import wave

SR = 44100  # sample rate
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")


def square(t, freq, duty=0.5):
    """A square-wave sample at time t (seconds)."""
    return 1.0 if (t * freq) % 1.0 < duty else -1.0


def write_wav(name, samples):
    """Clamp, convert to int16, and write a mono WAV."""
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        for s in samples:
            v = max(-1.0, min(1.0, s))
            frames += struct.pack("<h", int(v * 32767))
        w.writeframes(bytes(frames))
    print(f"  wrote {name} ({len(samples)/SR:.2f}s)")


def tone(freq_start, freq_end, dur, vol=0.35, duty=0.5, decay=True):
    """A pitch-swept square tone with optional exponential decay envelope."""
    n = int(SR * dur)
    out = []
    for i in range(n):
        t = i / SR
        prog = i / n
        freq = freq_start + (freq_end - freq_start) * prog
        env = (1.0 - prog) if decay else 1.0
        out.append(square(t, freq, duty) * vol * env)
    return out


def arp(freqs, note_dur, vol=0.32, duty=0.5):
    """A quick arpeggio: one short square note per frequency."""
    out = []
    for f in freqs:
        n = int(SR * note_dur)
        for i in range(n):
            t = i / SR
            env = min(1.0, (n - i) / (0.3 * n))  # short fade-out tail
            out.append(square(t, f, duty) * vol * env)
    return out


def noise_burst(dur, vol=0.4, lp=0.5):
    """White noise with a one-pole low-pass and exponential decay — explosions."""
    n = int(SR * dur)
    out = []
    prev = 0.0
    for i in range(n):
        prog = i / n
        env = math.exp(-4.0 * prog)
        white = random.uniform(-1.0, 1.0)
        prev = prev + lp * (white - prev)  # simple low-pass
        out.append(prev * vol * env)
    return out


def main():
    random.seed(1983)  # nod to the original release year — stable output
    print("Generating Moon Bugs SFX into assets/ ...")

    # Laser pew — fast downward sweep.
    write_wav("shoot.wav", tone(1300, 420, 0.10, vol=0.28, duty=0.35))

    # Bug explosion — filtered noise burst.
    write_wav("explosion.wav", noise_burst(0.34, vol=0.45, lp=0.45))

    # Armored glancing hit — tiny metallic blip.
    write_wav("hit.wav", tone(900, 700, 0.05, vol=0.3, duty=0.25))

    # Power-up collected — bright ascending arpeggio (C-E-G-C).
    write_wav("powerup.wav", arp([523, 659, 784, 1046], 0.06, vol=0.30))

    # Drum hauled off the top — sad descending wail.
    write_wav("drum_lost.wav", tone(600, 150, 0.45, vol=0.32, duty=0.5))

    # Wave start — short rising triad fanfare.
    write_wav("wave.wav", arp([392, 523, 659, 880], 0.07, vol=0.30))

    # Game over — slow descending dirge.
    write_wav("gameover.wav", arp([392, 330, 262, 196], 0.18, vol=0.32, duty=0.5))

    # Player hit — harsh low buzz with a touch of noise.
    buzz = tone(160, 110, 0.22, vol=0.34, duty=0.5)
    noise = noise_burst(0.22, vol=0.12, lp=0.7)
    write_wav("hurt.wav", [a + b for a, b in zip(buzz, noise)])

    print("Done.")


if __name__ == "__main__":
    main()
