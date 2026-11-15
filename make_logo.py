from pathlib import Path
from math import cos, sin, pi
from PIL import Image, ImageDraw, ImageFont, ImageOps

S = 512
OUT = Path(__file__).with_name("logo.png")

INK = (10, 14, 32)
NAVY = (24, 31, 62)
NAVY_2 = (33, 43, 80)
GOLD = (255, 201, 66)
GOLD_D = (176, 117, 22)
GREEN = (110, 216, 124)
GREEN_D = (42, 121, 77)
GREEN_L = (163, 238, 166)
PAPER = (255, 249, 228)
RED = (235, 72, 72)
PURPLE = (74, 48, 128)
WHITE = (255, 255, 255)

IMPACT = "C:/Windows/Fonts/impact.ttf"
ARIALBD = "C:/Windows/Fonts/arialbd.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, box, text, fnt, fill, stroke=0, stroke_fill=INK):
    draw.text(box, text, font=fnt, fill=fill, anchor="mm",
              stroke_width=stroke, stroke_fill=stroke_fill)


def main():
    base = Image.new("RGB", (S, S), INK)
    glow_mask = ImageOps.invert(Image.radial_gradient("L").resize((S, S)))
    glow_mask = glow_mask.point(lambda v: int(v * 0.55))
    base.paste(Image.new("RGB", (S, S), (38, 96, 72)), (0, 0), glow_mask)

    disc = Image.new("RGB", (S, S), NAVY)
    d = ImageDraw.Draw(disc)
    d.ellipse((20, 20, 492, 492), fill=NAVY)
    cx = cy = S / 2
    for i in range(28):
        a0 = 2 * pi * i / 28
        a1 = a0 + 2 * pi / 56
        d.polygon([(cx, cy),
                   (cx + 250 * cos(a0), cy + 250 * sin(a0)),
                   (cx + 250 * cos(a1), cy + 250 * sin(a1))], fill=NAVY_2)
    d.ellipse((44, 44, 468, 468), fill=NAVY)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse((20, 20, 492, 492), fill=255)
    base.paste(disc, (0, 0), mask)

    d = ImageDraw.Draw(base)
    d.ellipse((20, 20, 492, 492), outline=GOLD_D, width=20)
    d.ellipse((20, 20, 492, 492), outline=GOLD, width=11)
    d.ellipse((44, 44, 468, 468), outline=GOLD_D, width=4)

    d.rounded_rectangle((86, 60, 426, 122), radius=18, fill=INK,
                        outline=GOLD, width=5)
    centered(d, (256, 91), "ESCROW GOBLIN", font(IMPACT, 46), GOLD)

    d.ellipse((112, 118, 400, 396), fill=PURPLE, outline=INK, width=10)
    d.polygon([(160, 222), (44, 158), (126, 292)], fill=GREEN_D, outline=INK)
    d.line([(160, 222), (44, 158), (126, 292)], fill=INK, width=10, joint="curve")
    d.polygon([(352, 222), (468, 158), (386, 292)], fill=GREEN_D, outline=INK)
    d.line([(352, 222), (468, 158), (386, 292)], fill=INK, width=10, joint="curve")
    d.polygon([(150, 232), (76, 190), (128, 278)], fill=GREEN)
    d.polygon([(362, 232), (436, 190), (384, 278)], fill=GREEN)

    d.ellipse((132, 158, 380, 392), fill=GREEN, outline=INK, width=11)
    d.arc((132, 158, 380, 392), 195, 345, fill=GREEN_L, width=7)
    d.line((166, 224, 234, 208), fill=GREEN_D, width=10)
    d.line((278, 208, 346, 224), fill=GREEN_D, width=10)
    for box in ((172, 222, 234, 288), (278, 222, 340, 288)):
        d.ellipse(box, fill=PAPER, outline=INK, width=7)
    d.ellipse((196, 242, 224, 278), fill=INK)
    d.ellipse((288, 242, 316, 278), fill=INK)
    d.ellipse((202, 244, 212, 256), fill=WHITE)
    d.ellipse((294, 244, 304, 256), fill=WHITE)
    d.ellipse((240, 282, 272, 316), fill=GREEN_D, outline=INK, width=5)
    d.pieslice((178, 282, 334, 376), 8, 172, fill=INK)
    d.rectangle((202, 328, 310, 350), fill=PAPER, outline=INK, width=4)
    for x in (228, 254, 280):
        d.line((x, 328, x, 350), fill=INK, width=3)
    d.rectangle((254, 328, 278, 350), fill=GOLD)

    d.rounded_rectangle((70, 344, 442, 444), radius=20, fill=(38, 48, 92),
                        outline=GOLD, width=8)
    d.line((78, 360, 434, 360), fill=GOLD_D, width=6)
    for x in (118, 394):
        d.ellipse((x - 24, 330, x + 24, 374), fill=GREEN, outline=INK, width=7)
        d.line((x - 12, 350, x + 12, 350), fill=GREEN_D, width=4)
    d.ellipse((216, 362, 296, 434), fill=INK, outline=GOLD, width=6)
    d.ellipse((238, 382, 274, 418), fill=GOLD)
    d.rectangle((250, 398, 262, 428), fill=INK)
    for y in (408, 396, 384):
        d.ellipse((92, y, 164, y + 22), fill=GOLD, outline=GOLD_D, width=4)

    stamp = Image.new("RGBA", (168, 62), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle((2, 2, 166, 60), radius=9, outline=RED, width=5)
    sd.text((84, 31), "LOCKED", font=font(IMPACT, 30), fill=RED, anchor="mm")
    stamp = stamp.rotate(-12, resample=Image.BICUBIC, expand=True)
    base.paste(stamp, (300, 132), stamp)

    d.rounded_rectangle((86, 434, 426, 482), radius=16, fill=INK,
                        outline=GOLD, width=4)
    centered(d, (256, 458), "$GOBLIN  -  $1,000 IN ESCROW", font(ARIALBD, 21), GOLD)

    base.save(OUT, format="PNG", optimize=False)
    print(OUT)


if __name__ == "__main__":
    main()
