from __future__ import annotations

import math
import random
import subprocess
import sys
from pathlib import Path


def ensure_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont

        return Image, ImageDraw, ImageFilter, ImageFont
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image, ImageDraw, ImageFilter, ImageFont

        return Image, ImageDraw, ImageFilter, ImageFont


Image, ImageDraw, ImageFilter, ImageFont = ensure_pillow()

ROOT = Path(__file__).resolve().parents[1]
ICON_PATH = ROOT / "ShokuninWatchFace" / "Assets.xcassets" / "AppIcon.appiconset" / "icon.png"
SCREENSHOT_ROOT = ROOT / "screenshots"

AMBER = (212, 134, 10)
AMBER_LIGHT = (255, 188, 67)
IRON_TOP = (44, 44, 46)
IRON_BOTTOM = (28, 28, 30)
WHITE = (244, 244, 246)
MUTED = (168, 168, 172)
BLACK = (8, 8, 10)

DEVICES = {
    "apple_watch_ultra": (410, 502),
    "apple_watch_series_10": (396, 484),
}

TEXT = {
    "ja": {
        "app": "職人ウォッチ",
        "angle": "角度を精密に計測",
        "level": "水平をすばやく確認",
        "slope": "傾斜を一目で読む",
        "unit": "度",
    },
    "en": {
        "app": "Shokunin Watch",
        "angle": "Precise Angle Measurement",
        "level": "Fast Level Check",
        "slope": "Read Slope at a Glance",
        "unit": "deg",
    },
}


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/YuGothB.ttc" if bold else "C:/Windows/Fonts/YuGothR.ttc",
        "C:/Windows/Fonts/meiryob.ttc" if bold else "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for item in candidates:
        path = Path(item)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def text_size(draw, text: str, face) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=face)
    return box[2] - box[0], box[3] - box[1]


def centered_text(draw, xy, text: str, face, fill, anchor="mm"):
    draw.text(xy, text, font=face, fill=fill, anchor=anchor)


def gradient(size: tuple[int, int], top=IRON_TOP, bottom=IRON_BOTTOM):
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def add_texture(img, seed: int = 7, strength: int = 16):
    rng = random.Random(seed)
    w, h = img.size
    noise = Image.new("L", img.size, 0)
    npx = noise.load()
    for y in range(h):
        row_bias = rng.randint(-strength, strength)
        for x in range(w):
            npx[x, y] = 128 + max(-strength, min(strength, row_bias + rng.randint(-strength, strength)))
    noise = noise.filter(ImageFilter.GaussianBlur(0.55))
    overlay = Image.new("RGB", img.size, (128, 128, 128))
    overlay.putalpha(noise.point(lambda p: abs(p - 128) * 2))
    img = Image.blend(img, Image.composite(Image.new("RGB", img.size, (60, 60, 62)), img, noise), 0.22)
    draw = ImageDraw.Draw(img, "RGBA")
    for y in range(0, h, 9):
        alpha = 14 if y % 18 == 0 else 8
        draw.line((0, y, w, y), fill=(255, 255, 255, alpha), width=1)
    return img


def rounded_mask(size: tuple[int, int], radius: int):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def amber_glow(base, center, radius):
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow, "RGBA")
    cx, cy = center
    for i in range(7, 0, -1):
        rr = radius + i * 14
        gd.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(212, 134, 10, 6 * i))
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))


def draw_icon():
    size = 1024
    img = add_texture(gradient((size, size)), seed=42, strength=18).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    cx = cy = size // 2

    for r, alpha in [(390, 26), (330, 32), (270, 26)]:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, alpha), width=3)

    amber_glow(img, (cx, cy), 230)
    draw.ellipse((266, 266, 758, 758), fill=(18, 18, 20, 230), outline=AMBER + (255,), width=18)
    draw.ellipse((320, 320, 704, 704), outline=(255, 188, 67, 128), width=4)

    for deg in range(-120, 121, 15):
        rad = math.radians(deg - 90)
        outer = 218
        inner = 184 if deg % 30 == 0 else 199
        x1, y1 = cx + math.cos(rad) * inner, cy + math.sin(rad) * inner
        x2, y2 = cx + math.cos(rad) * outer, cy + math.sin(rad) * outer
        draw.line((x1, y1, x2, y2), fill=AMBER_LIGHT + (230,), width=7 if deg % 30 == 0 else 4)

    draw.rounded_rectangle((292, 471, 732, 553), radius=41, fill=(5, 5, 6, 230), outline=AMBER + (255,), width=12)
    draw.ellipse((482, 487, 542, 547), fill=AMBER_LIGHT + (255,))
    draw.ellipse((494, 499, 530, 535), fill=(255, 226, 143, 245))

    draw.line((cx, cy, cx + 130, cy - 72), fill=AMBER_LIGHT + (255,), width=14)
    draw.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=AMBER + (255,))
    draw.arc((226, 226, 798, 798), 205, 335, fill=(255, 255, 255, 34), width=12)

    ICON_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(ICON_PATH)
    return ICON_PATH


def draw_header_footer(draw, w, h, lang: str, screen: str):
    title_face = font(max(24, int(w * 0.073)), bold=True)
    cap_face = font(max(18, int(w * 0.05)), bold=True)
    centered_text(draw, (w / 2, int(h * 0.095)), TEXT[lang]["app"], title_face, WHITE + (255,))
    centered_text(draw, (w / 2, int(h * 0.91)), TEXT[lang][screen], cap_face, WHITE + (255,))


def draw_angle(draw, w, h, lang):
    cx, cy = w / 2, h * 0.48
    r = w * 0.31
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(12, 12, 14, 225), outline=AMBER + (255,), width=5)
    for deg in range(-120, 121, 20):
        rad = math.radians(deg - 90)
        inner = r * (0.82 if deg % 40 == 0 else 0.9)
        outer = r * 0.98
        draw.line((cx + math.cos(rad) * inner, cy + math.sin(rad) * inner, cx + math.cos(rad) * outer, cy + math.sin(rad) * outer), fill=AMBER_LIGHT + (220,), width=3)
    angle = -32
    rad = math.radians(angle - 90)
    draw.line((cx, cy, cx + math.cos(rad) * r * 0.68, cy + math.sin(rad) * r * 0.68), fill=AMBER_LIGHT + (255,), width=7)
    draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=AMBER + (255,))
    face = font(int(w * 0.12), bold=True)
    centered_text(draw, (cx, cy + r * 0.45), "32°" if lang == "ja" else "32 deg", face, WHITE + (255,))


def draw_level(draw, w, h, lang):
    cx, cy = w / 2, h * 0.49
    tube_w, tube_h = w * 0.72, h * 0.15
    x0, y0 = cx - tube_w / 2, cy - tube_h / 2
    x1, y1 = cx + tube_w / 2, cy + tube_h / 2
    draw.rounded_rectangle((x0, y0, x1, y1), radius=int(tube_h / 2), fill=(10, 10, 12, 235), outline=AMBER + (255,), width=5)
    draw.rounded_rectangle((x0 + 16, y0 + 16, x1 - 16, y1 - 16), radius=int(tube_h / 2), outline=(255, 255, 255, 48), width=2)
    mark_gap = 34
    draw.line((cx - mark_gap, y0 + 12, cx - mark_gap, y1 - 12), fill=AMBER_LIGHT + (220,), width=3)
    draw.line((cx + mark_gap, y0 + 12, cx + mark_gap, y1 - 12), fill=AMBER_LIGHT + (220,), width=3)
    bubble_w = w * 0.22
    bubble = (cx - bubble_w / 2 + 9, cy - tube_h * 0.28, cx + bubble_w / 2 + 9, cy + tube_h * 0.28)
    draw.ellipse(bubble, fill=(255, 194, 64, 230), outline=(255, 228, 146, 245), width=3)
    face = font(int(w * 0.08), bold=True)
    centered_text(draw, (cx, cy + h * 0.18), "0.4°" if lang == "ja" else "0.4 deg", face, WHITE + (255,))


def draw_slope(draw, w, h, lang):
    cx, cy = w / 2, h * 0.49
    bar_w, bar_h = w * 0.68, h * 0.1
    angle = math.radians(-13)
    corners = [(-bar_w / 2, -bar_h / 2), (bar_w / 2, -bar_h / 2), (bar_w / 2, bar_h / 2), (-bar_w / 2, bar_h / 2)]
    pts = []
    for x, y in corners:
        pts.append((cx + x * math.cos(angle) - y * math.sin(angle), cy + x * math.sin(angle) + y * math.cos(angle)))
    draw.polygon(pts, fill=(10, 10, 12, 235), outline=AMBER + (255,))
    draw.line((w * 0.16, cy + h * 0.12, w * 0.84, cy + h * 0.12), fill=(255, 255, 255, 55), width=3)
    draw.arc((cx - w * 0.24, cy - w * 0.04, cx + w * 0.24, cy + w * 0.44), 200, 340, fill=AMBER_LIGHT + (230,), width=5)
    face = font(int(w * 0.12), bold=True)
    centered_text(draw, (cx, cy - h * 0.17), "-13°" if lang == "ja" else "-13 deg", face, WHITE + (255,))
    small = font(int(w * 0.045), bold=True)
    centered_text(draw, (cx, cy + h * 0.2), "23.1%" if lang == "ja" else "23.1%", small, MUTED + (255,))


def draw_screenshot(device: str, size: tuple[int, int], lang: str, screen: str):
    w, h = size
    seed = sum(ord(ch) for ch in f"{device}:{lang}:{screen}")
    img = add_texture(gradient(size), seed=seed, strength=13).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((10, 10, w - 10, h - 10), radius=42, outline=(255, 255, 255, 24), width=2)
    draw_header_footer(draw, w, h, lang, screen)
    if screen == "angle":
        draw_angle(draw, w, h, lang)
    elif screen == "level":
        draw_level(draw, w, h, lang)
    else:
        draw_slope(draw, w, h, lang)
    out = SCREENSHOT_ROOT / device / lang / f"{screen}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    generated = [draw_icon()]
    for device, size in DEVICES.items():
        for lang in ("ja", "en"):
            for screen in ("angle", "level", "slope"):
                generated.append(draw_screenshot(device, size, lang, screen))

    for path in generated:
        print(path)


if __name__ == "__main__":
    main()
