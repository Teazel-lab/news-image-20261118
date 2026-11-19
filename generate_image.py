#!/usr/bin/env python3
"""Editorial world-news front page for 18 November 2026."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (11, 16, 32)
NAVY_CARD = (18, 26, 48)
GOLD = (212, 175, 90)
GOLD_DIM = (160, 132, 68)
CREAM = (236, 230, 214)
MUTED = (168, 174, 190)
RULE = (58, 68, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    f_mast = font(SERIF_B, 54)
    f_date = font(SANS, 18)
    f_kicker = font(SANS_B, 13)
    f_head_l = font(SERIF_B, 32)
    f_head = font(SERIF_B, 22)
    f_deck = font(SERIF, 16)
    f_foot = font(SANS, 15)
    f_num = font(SANS_B, 14)

    # Masthead
    d.rectangle((0, 0, W, 128), fill=(8, 12, 24))
    d.rectangle((0, 124, W, 128), fill=GOLD)
    mast = "WORLD NEWS"
    mw = d.textlength(mast, font=f_mast)
    d.text(((W - mw) / 2, 22), mast, font=f_mast, fill=GOLD)
    date = "WEDNESDAY 18 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 86), date, font=f_date, fill=CREAM)

    stories = [
        {
            "kicker": "LEAD",
            "title": "Trump lands in Shenzhen for APEC",
            "deck": "Xi welcomes him; Xi and Putin blast Western protectionism and sanctions; Xi–Trump–Putin talks set for Thursday",
            "lead": True,
        },
        {
            "kicker": "EUROPE",
            "title": "EU proposes €45bn loan for Ukraine",
            "deck": "repaid only after Russia pays reparations — von der Leyen",
        },
        {
            "kicker": "AMERICAS",
            "title": "US and Venezuela sign military pact",
            "deck": "training and intelligence sharing, Hegseth in Caracas",
        },
        {
            "kicker": "GULF",
            "title": "Iran fires at Kuwait after US strike on Qeshm",
            "deck": "Bahrain intercepts Iranian attacks for third time in a week",
        },
        {
            "kicker": "MARKETS",
            "title": "Wall St mixed after Nvidia earnings",
            "deck": "Dow −1.1%, S&P −0.2%, Nasdaq +0.4%; Anthropic IPO priced at $83",
        },
        {
            "kicker": "AFRICA",
            "title": "Ethiopia, Eritrea mass troops on border",
            "deck": "war fears rise in the Horn of Africa",
        },
    ]

    margin = 28
    gap = 10
    top = 144
    bottom = 980
    lead = stories[0]
    rest = stories[1:]

    lead_h = 196
    card_w = W - margin * 2
    inner = 16

    # Lead card
    d.rounded_rectangle(
        (margin, top, margin + card_w, top + lead_h),
        radius=10,
        fill=NAVY_CARD,
        outline=GOLD,
        width=2,
    )
    lx = margin + inner
    ly = top + 12
    d.text((lx, ly), "LEAD", font=f_kicker, fill=GOLD)
    ly += 22
    title_lines = wrap(d, lead["title"], f_head_l, card_w - inner * 2)
    ly = draw_lines(d, title_lines, f_head_l, lx, ly, CREAM, 38)
    ly += 4
    deck_lines = wrap(d, lead["deck"], f_deck, card_w - inner * 2)
    draw_lines(d, deck_lines, f_deck, lx, ly, MUTED, 22)

    # Five smaller cards in a column
    y0 = top + lead_h + gap
    n = len(rest)
    avail = bottom - y0 - gap
    ch = (avail - gap * (n - 1)) // n

    for i, s in enumerate(rest):
        y = y0 + i * (ch + gap)
        d.rounded_rectangle(
            (margin, y, margin + card_w, y + ch),
            radius=8,
            fill=NAVY_CARD,
            outline=RULE,
            width=1,
        )
        # gold accent bar
        d.rectangle((margin, y, margin + 5, y + ch), fill=GOLD)
        x = margin + 18
        yy = y + 10
        label = f"{i + 2:02d}  {s['kicker']}"
        d.text((x, yy), label, font=f_num, fill=GOLD_DIM)
        yy += 20
        tlines = wrap(d, s["title"], f_head, card_w - 36)
        yy = draw_lines(d, tlines, f_head, x, yy, CREAM, 26)
        yy += 2
        dlines = wrap(d, s["deck"], f_deck, card_w - 36)
        draw_lines(d, dlines, f_deck, x, yy, MUTED, 20)

    # Footer
    d.rectangle((0, 992, W, 1024), fill=(8, 12, 24))
    d.rectangle((0, 992, W, 995), fill=GOLD)
    foot = "make.fun · world news of 18 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 1000), foot, font=f_foot, fill=GOLD)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out)


if __name__ == "__main__":
    main()
