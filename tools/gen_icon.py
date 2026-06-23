#!/usr/bin/env python3
# ============================================================================
#  gen_icon.py — procedural app icon generator for Moon Bugs
#
#  Draws a little green moon-bug on a starry rounded-square and writes:
#    assets/icon.png        — 512px PNG (source for the macOS .icns bundle)
#    assets/icon_16.rgba    — raw RGBA, embedded for the in-game window icon
#    assets/icon_32.rgba    -  "
#    assets/icon_64.rgba    -  "
#
#  Pure stdlib (zlib/struct/math) — no PIL. Shapes are rendered with 3x
#  supersampling for smooth edges. Re-run: `python3 tools/gen_icon.py`
# ============================================================================

import math
import os
import struct
import zlib

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
SS = 3  # supersampling factor for anti-aliasing


def blend(dst, i, r, g, b, a):
    """Alpha-blend an (r,g,b,a) float color over dst[i..i+4] (bytearray)."""
    if a <= 0:
        return
    inv = 1.0 - a
    dst[i] = int(r * 255 * a + dst[i] * inv)
    dst[i + 1] = int(g * 255 * a + dst[i + 1] * inv)
    dst[i + 2] = int(b * 255 * a + dst[i + 2] * inv)
    dst[i + 3] = int(a * 255 + dst[i + 3] * inv)


def render(size):
    """Render the icon at `size` px (with supersampling); return RGBA bytes."""
    n = size * SS
    buf = bytearray(n * n * 4)  # transparent

    def px(x, y, color):
        if 0 <= x < n and 0 <= y < n:
            r, g, b, a = color
            blend(buf, (y * n + x) * 4, r, g, b, a)

    # --- Rounded-square background with vertical gradient + soft border -----
    radius = 0.20 * n
    for y in range(n):
        ty = y / n
        # gradient top -> bottom
        top = (0.11, 0.10, 0.24)
        bot = (0.03, 0.03, 0.09)
        gr = top[0] + (bot[0] - top[0]) * ty
        gg = top[1] + (bot[1] - top[1]) * ty
        gb = top[2] + (bot[2] - top[2]) * ty
        for x in range(n):
            # rounded-rect mask via distance to the inner corner box
            dx = max(radius - x, x - (n - radius), 0)
            dy = max(radius - y, y - (n - radius), 0)
            if dx * dx + dy * dy <= radius * radius:
                px(x, y, (gr, gg, gb, 1.0))

    def disc(cx, cy, rad, color):
        x0, x1 = int(cx - rad - 1), int(cx + rad + 1)
        y0, y1 = int(cy - rad - 1), int(cy + rad + 1)
        for y in range(max(0, y0), min(n, y1)):
            for x in range(max(0, x0), min(n, x1)):
                d = math.hypot(x - cx, y - cy)
                if d <= rad:
                    # feather the last pixel for a soft edge
                    a = color[3] * min(1.0, rad - d)
                    px(x, y, (color[0], color[1], color[2], a))

    def tri(p0, p1, p2, color):
        xs = [p0[0], p1[0], p2[0]]
        ys = [p0[1], p1[1], p2[1]]
        x0, x1 = int(min(xs)), int(max(xs)) + 1
        y0, y1 = int(min(ys)), int(max(ys)) + 1

        def sign(a, b, c):
            return (a[0] - c[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (a[1] - c[1])

        for y in range(max(0, y0), min(n, y1)):
            for x in range(max(0, x0), min(n, x1)):
                p = (x + 0.5, y + 0.5)
                d1 = sign(p, p0, p1)
                d2 = sign(p, p1, p2)
                d3 = sign(p, p2, p0)
                neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
                pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
                if not (neg and pos):
                    px(x, y, color)

    # --- A scattering of stars ---------------------------------------------
    stars = [(0.18, 0.20, 1.3), (0.80, 0.16, 1.6), (0.72, 0.34, 1.0),
             (0.26, 0.74, 1.1), (0.84, 0.72, 1.4), (0.14, 0.50, 0.9),
             (0.50, 0.13, 1.0)]
    for sx, sy, sr in stars:
        disc(sx * n, sy * n, sr * SS, (1.0, 1.0, 1.0, 0.85))

    cx, cy = 0.5 * n, 0.54 * n
    body_r = 0.26 * n

    # --- Antennae -----------------------------------------------------------
    for ax in (0.40, 0.60):
        tip = (ax * n, 0.20 * n)
        disc(tip[0], tip[1], 0.035 * n, (0.9, 1.0, 0.6, 1.0))
        tri((cx, cy - body_r * 0.6),
            (tip[0] - 0.02 * n, tip[1]),
            (tip[0] + 0.02 * n, tip[1]),
            (0.6, 0.8, 0.45, 1.0))

    # --- Wings (behind body) ------------------------------------------------
    wing = (0.30, 0.55, 0.34, 0.95)
    tri((cx, cy), (cx - body_r * 1.7, cy - body_r * 0.5),
        (cx - body_r * 0.4, cy + body_r * 0.9), wing)
    tri((cx, cy), (cx + body_r * 1.7, cy - body_r * 0.5),
        (cx + body_r * 0.4, cy + body_r * 0.9), wing)

    # --- Body ---------------------------------------------------------------
    disc(cx, cy, body_r + 0.02 * n, (0.05, 0.15, 0.07, 1.0))  # outline
    disc(cx, cy, body_r, (0.50, 0.88, 0.55, 1.0))
    disc(cx - body_r * 0.3, cy - body_r * 0.3, body_r * 0.45,
         (0.66, 0.96, 0.68, 0.6))  # highlight

    # --- Eyes ---------------------------------------------------------------
    for ex in (-0.34, 0.34):
        disc(cx + ex * body_r * 2, cy - 0.18 * body_r, 0.30 * body_r,
             (1.0, 1.0, 1.0, 1.0))
        disc(cx + ex * body_r * 2 + 0.05 * body_r, cy - 0.12 * body_r,
             0.14 * body_r, (0.05, 0.05, 0.1, 1.0))

    # --- Downsample (box filter) -------------------------------------------
    out = bytearray(size * size * 4)
    area = SS * SS
    for y in range(size):
        for x in range(size):
            r = g = b = a = 0
            for sy in range(SS):
                for sx in range(SS):
                    i = ((y * SS + sy) * n + (x * SS + sx)) * 4
                    r += buf[i]; g += buf[i + 1]; b += buf[i + 2]; a += buf[i + 3]
            o = (y * size + x) * 4
            out[o] = r // area
            out[o + 1] = g // area
            out[o + 2] = b // area
            out[o + 3] = a // area
    return out


def png_bytes(size, rgba):
    """Encode an RGBA bytearray as PNG bytes (pure stdlib)."""
    raw = bytearray()
    for y in range(size):
        raw.append(0)  # filter type 0
        raw += rgba[y * size * 4:(y + 1) * size * 4]

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return (sig + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def write_png(path, size, rgba):
    """Write an RGBA bytearray as a PNG file."""
    with open(path, "wb") as f:
        f.write(png_bytes(size, rgba))


def bmp_icon_bytes(size, rgba):
    """Encode an RGBA buffer as a 32-bit BMP/DIB icon image (for an .ico entry).

    Windows Explorer and the taskbar reliably render the small icon sizes only
    from BMP-format entries — PNG-in-ICO is dependable at 256px but flaky at
    16/32/48px, where it shows a blank/generic icon. So small sizes use this.

    The DIB stores a doubled height (XOR color rows + AND mask rows), bottom-up,
    with BGRA pixels. With a 32-bit alpha channel the AND mask is all-zero.
    """
    # BITMAPINFOHEADER: height is doubled to cover the (empty) AND mask.
    header = struct.pack(
        "<IiiHHIIiiII", 40, size, size * 2, 1, 32, 0, 0, 0, 0, 0, 0
    )
    xor = bytearray()
    for y in range(size - 1, -1, -1):  # bottom-up
        row = y * size * 4
        for x in range(size):
            i = row + x * 4
            r, g, b, a = rgba[i], rgba[i + 1], rgba[i + 2], rgba[i + 3]
            xor += bytes((b, g, r, a))  # BGRA
    and_row = ((size + 31) // 32) * 4  # 1bpp, rows padded to 32 bits
    and_mask = bytes(and_row * size)   # all zero = fully opaque
    return header + bytes(xor) + and_mask


def write_ico(path, sizes):
    """Write a multi-resolution Windows .ico.

    Small sizes are stored as BMP (best Explorer/taskbar compatibility); 256px
    is stored as PNG (compact and well supported at that size).
    """
    images = []
    for s in sizes:
        rgba = render(s)
        data = png_bytes(s, rgba) if s >= 256 else bmp_icon_bytes(s, rgba)
        images.append((s, data))
    count = len(images)
    header = struct.pack("<HHH", 0, 1, count)  # reserved, type=icon, count
    entries = b""
    offset = 6 + count * 16
    blob = b""
    for s, data in images:
        dim = s if s < 256 else 0  # 0 encodes 256 in the ICONDIRENTRY
        entries += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
        blob += data
    with open(path, "wb") as f:
        f.write(header + entries + blob)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    print("Generating Moon Bugs icon ...")

    # Base PNG for the macOS .icns bundle and the Linux desktop icon.
    big = render(512)
    write_png(os.path.join(ASSETS, "icon.png"), 512, big)
    print("  wrote icon.png (512px)")

    # Multi-size Windows .ico, embedded into the .exe by build.rs.
    write_ico(os.path.join(ASSETS, "icon.ico"), [16, 32, 48, 64, 128, 256])
    print("  wrote icon.ico (16-256px)")

    # Raw RGBA buffers embedded for the in-game window/dock icon.
    for s in (16, 32, 64):
        data = render(s)
        with open(os.path.join(ASSETS, f"icon_{s}.rgba"), "wb") as f:
            f.write(data)
        print(f"  wrote icon_{s}.rgba ({s}x{s}, {len(data)} bytes)")

    print("Done.")


if __name__ == "__main__":
    main()
