"""
Generates color.png (192x192) and outline.png (32x32) for the Teams app manifest.
Uses only the Python standard library — no Pillow required.
Run once:  python make_icons.py
"""
import struct, zlib, math

NAVY   = (13, 35, 84)      # #0D2354 Certis navy
ORANGE = (247, 148, 29)    # #F7941D Certis orange
WHITE  = (255, 255, 255)

def png_bytes(pixels, width, height):
    """Encode an RGBA pixel array as a minimal PNG."""
    def u32(n): return struct.pack(">I", n)
    def chunk(tag, data):
        c = zlib.crc32(tag + data) & 0xFFFFFFFF
        return u32(len(data)) + tag + data + u32(c)

    raw = b""
    for y in range(height):
        raw += b"\x00"  # filter byte
        for x in range(width):
            raw += bytes(pixels[y][x])

    ihdr = chunk(b"IHDR", u32(width) + u32(height) + b"\x08\x06\x00\x00\x00")
    idat = chunk(b"IDAT", zlib.compress(raw, 9))
    iend = chunk(b"IEND", b"")
    return b"\x89PNG\r\n\x1a\n" + ihdr + idat + iend


def make_color_icon(size=192):
    """Navy circle on navy background with an orange 'H' letterform."""
    cx, cy, r = size // 2, size // 2, size // 2 - 2
    pixels = []
    for y in range(size):
        row = []
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > r:
                row.append((*NAVY, 255))
            else:
                # Draw a simple bold 'H' in orange
                rel_x = (x - cx) / r   # -1 .. 1
                rel_y = (y - cy) / r
                lw = 0.18   # stroke width
                h_top, h_bot = -0.55, 0.55
                h_mid_t, h_mid_b = -0.08, 0.08
                left_x, right_x = -0.30, 0.30

                on_left  = abs(rel_x - left_x)  < lw and h_bot >= rel_y >= h_top
                on_right = abs(rel_x - right_x) < lw and h_bot >= rel_y >= h_top
                on_cross = abs(rel_y) < lw * 0.9 and left_x <= rel_x <= right_x

                if on_left or on_right or on_cross:
                    row.append((*ORANGE, 255))
                else:
                    row.append((*NAVY, 255))
        pixels.append(row)
    return png_bytes(pixels, size, size)


def make_outline_icon(size=32):
    """White circle outline with a white 'H' on transparent background."""
    cx, cy, r_outer, r_inner = size//2, size//2, size//2-1, size//2-3
    pixels = []
    for y in range(size):
        row = []
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            rel_x = (x - cx) / (r_inner or 1)
            rel_y = (y - cy) / (r_inner or 1)
            lw = 0.28
            h_top, h_bot = -0.6, 0.6
            left_x, right_x = -0.32, 0.32

            on_ring  = r_inner < dist <= r_outer
            on_left  = abs(rel_x - left_x)  < lw and h_bot >= rel_y >= h_top and dist <= r_inner
            on_right = abs(rel_x - right_x) < lw and h_bot >= rel_y >= h_top and dist <= r_inner
            on_cross = abs(rel_y) < lw * 0.8 and left_x <= rel_x <= right_x and dist <= r_inner

            if on_ring or on_left or on_right or on_cross:
                row.append((*WHITE, 255))
            else:
                row.append((0, 0, 0, 0))   # transparent
        pixels.append(row)
    return png_bytes(pixels, size, size)


if __name__ == "__main__":
    import os
    out = os.path.dirname(os.path.abspath(__file__))

    color_path   = os.path.join(out, "color.png")
    outline_path = os.path.join(out, "outline.png")

    with open(color_path,   "wb") as f: f.write(make_color_icon(192))
    with open(outline_path, "wb") as f: f.write(make_outline_icon(32))

    print(f"Created: {color_path}")
    print(f"Created: {outline_path}")
