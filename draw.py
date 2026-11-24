#!/usr/bin/env python3
"""news-23 b23 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories. All drawn with PIL. Output: entry.png 1024x1024."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 227)
INK = (22, 22, 22)
BLACK = (8, 8, 8)
GOLD = (212, 175, 55)
GOLD_D = (176, 141, 0)
RED = (178, 34, 34)
RED_B = (205, 45, 45)
NAVY = (16, 42, 90)
TEAL = (15, 118, 110)
GREEN = (46, 110, 46)
PURPLE = (120, 60, 140)
MAGENTA = (180, 0, 120)
BROWN = (120, 72, 20)
GREY = (90, 90, 90)
GREY_T = (110, 110, 110)
MAP_BG = (214, 228, 235)
LAND = (139, 178, 120)
CREAM = (250, 246, 232)

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)


def wrap(text, font, max_w, draw):
    """Wrap text into lines fitting max_w. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(draw, x, y, label, bg):
    """Right-aligned chip ending at x. Returns left edge."""
    f = SANS_B(9)
    w = int(draw.textlength(label, font=f)) + 12
    draw.rounded_rectangle([x - w, y, x, y + 14], radius=7, fill=bg)
    draw.text((x - w + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return x - w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 56], fill=BLACK)
    d.text((14, 6), "THE WORLD TODAY", font=SERIF_B(42), fill=(255, 255, 255))
    dt = "MONDAY 23 NOVEMBER 2026"
    d.text((W - 14 - d.textlength(dt, font=SANS_B(19)), 18), dt,
           font=SANS_B(19), fill=GOLD)

    # ---------- kicker ----------
    d.text((14, 62), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  "
           "US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
           font=SERIF_B(15), fill=RED)

    # ---------- number strip ----------
    nums = [
        ("-3.3%", "KOSPI CLOSES 4,708.54", RED_B),
        ("5.3", "US-CHINA POWER GAP", NAVY),
        ("11,762", "EBOLA CASES, DRC", GREEN),
        ("$450M", "SKUBAL DEAL", PURPLE),
        ("$107.3B", "ANTHROPIC IPO", MAGENTA),
    ]
    col_w = 204
    for i, (num, lab, col) in enumerate(nums):
        x = 14 + i * col_w
        d.text((x, 82), num, font=SANS_B(30), fill=col)
        d.text((x, 116), lab, font=SANS_B(10), fill=INK)
        if i:
            d.line([(x - 8, 84), (x - 8, 126)], fill=(200, 192, 170), width=1)

    # ---------- THE DAY IN NUMBERS strip ----------
    d.rectangle([0, 130, W, 148], fill=NAVY)
    d.text((14, 134), "THE DAY IN NUMBERS", font=SANS_B(11), fill=GOLD)
    d.text((210, 134), "-5.8% intraday low   \u00b7   165 missiles in a week   "
           "\u00b7   12,000 cleared   \u00b7   264 kg seized   \u00b7   2% tax backed",
           font=SANS(11), fill=(255, 255, 255))

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", TEAL, 200), ("AMERICAS 8", NAVY, 210),
               ("MIDDLE EAST 6", GOLD_D, 180), ("EUROPE 5", PURPLE, 160),
               ("AFRICA 3", BROWN, 130), ("WORLD 2", GREY, 144)]
    x = 0
    for name, col, w in regions:
        d.rectangle([x, 150, x + w, 166], fill=col)
        tw = d.textlength(name, font=SANS_B(11))
        d.text((x + (w - tw) / 2, 153), name, font=SANS_B(11),
               fill=(255, 255, 255))
        x += w

    # ---------- hero scenes ----------
    hy, hh = 168, 184
    cols = [(10, 338), (348, 676), (686, 1014)]

    # --- scene 1: Kospi chart (navy) ---
    x0, x1 = cols[0]
    d.rectangle([x0, hy, x1, hy + hh], fill=(14, 30, 58))
    # skyline
    import random
    random.seed(23)
    bx = x0 + 6
    while bx < x1 - 14:
        bw = random.randint(14, 26)
        bh = random.randint(18, 52)
        d.rectangle([bx, hy + hh - 34 - bh, bx + bw, hy + hh - 34],
                    fill=(30, 52, 96))
        for wy in range(hy + hh - 30 - bh, hy + hh - 38, 9):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if random.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # descending chart
    pts = [(x0 + 14, hy + 62), (x0 + 60, hy + 52), (x0 + 105, hy + 74),
           (x0 + 150, hy + 66), (x0 + 195, hy + 92), (x0 + 240, hy + 84),
           (x0 + 285, hy + 108), (x0 + 318, hy + 118)]
    d.line(pts, fill=RED_B, width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 214, 90))
    d.text((x0 + 10, hy + 8), "-3.3%", font=SANS_B(34), fill=RED_B)
    d.rectangle([x0, hy + hh - 26, x1, hy + hh], fill=BLACK)
    d.text((x0 + 10, hy + hh - 22), "KOSPI  4,708.54   \u00b7   -161 PTS",
           font=SANS_B(12), fill=(255, 255, 255))

    # --- scene 2: Guterres globe (teal) ---
    x0, x1 = cols[1]
    d.rectangle([x0, hy, x1, hy + hh], fill=TEAL)
    d.text((x0 + 12, hy + 10), "150 DELEGATES", font=SANS_B(30),
           fill=(255, 214, 90))
    d.text((x0 + 12, hy + 46), "BACK A RISK FRAMEWORK", font=SANS_B(16),
           fill=(255, 255, 255))
    # globe, right side, clear of text
    gx, gy, gr = x1 - 52, hy + 108, 34
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(178, 222, 214))
    d.ellipse([gx - 18, gy - 22, gx + 2, gy - 2], fill=(46, 140, 90))
    d.ellipse([gx - 4, gy + 4, gx + 20, gy + 24], fill=(46, 140, 90))
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(255, 255, 255),
              width=2)
    # flags
    for fx, fcol in [(x0 + 22, RED_B), (x0 + 62, (40, 90, 200)),
                     (x0 + 102, (255, 214, 90))]:
        d.line([(fx, hy + 96), (fx, hy + 138)], fill=(255, 255, 255), width=2)
        d.polygon([(fx, hy + 96), (fx + 26, hy + 104), (fx, hy + 112)],
                  fill=fcol)
    # podium
    d.polygon([(x0 + 130, hy + 158), (x0 + 190, hy + 158), (x0 + 178, hy + 138),
               (x0 + 142, hy + 138)], fill=(120, 72, 20))
    d.rectangle([x0, hy + hh - 26, x1, hy + hh], fill=BLACK)
    d.text((x0 + 10, hy + hh - 22), "UN  \u00b7  BRIDGETOWN", font=SANS_B(12),
           fill=(255, 255, 255))

    # --- scene 3: power bars (cream) ---
    x0, x1 = cols[2]
    d.rectangle([x0, hy, x1, hy + hh], outline=INK, width=1, fill=CREAM)
    d.text((x0 + 10, hy + 8), "NARROWEST SINCE 2018", font=SANS_B(13),
           fill=INK)
    d.text((x1 - 10 - d.textlength("GAP 5.3", font=SANS_B(13)), hy + 8),
           "GAP 5.3", font=SANS_B(13), fill=GOLD_D)
    bars = [("US", 78.9, NAVY), ("CHINA", 73.6, RED_B), ("INDIA", 40.5, GOLD_D)]
    base_y = hy + hh - 34
    max_h = 92
    bw = 62
    gap = (x1 - x0 - 3 * bw) / 4
    for i, (name, val, col) in enumerate(bars):
        bx = x0 + gap + i * (bw + gap)
        bh = max_h * val / 78.9
        d.text((bx + bw / 2 - d.textlength(f"{val}", font=SANS_B(14)) / 2,
                base_y - bh - 20), f"{val}", font=SANS_B(14), fill=col)
        d.rectangle([bx, base_y - bh, bx + bw, base_y], fill=col)
        d.text((bx + bw / 2 - d.textlength(name, font=SANS_B(11)) / 2,
                base_y + 4), name, font=SANS_B(11), fill=INK)

    # ---------- hero headlines ----------
    heroes = [
        ("1", "AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
         "Samsung -3.1%, SK Hynix -2.5%.", "KOREA EXCHANGE"),
        ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; "
         "150 delegates back a risk framework.", "UNITED NATIONS"),
        ("3", "US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, "
         "narrowest since 2018. India third at 40.5.", "LOWY INSTITUTE"),
    ]
    hy2 = 358
    for (num, head, body, src), (x0, x1) in zip(heroes, cols):
        d.ellipse([x0, hy2 + 2, x0 + 20, hy2 + 22], fill=RED)
        d.text((x0 + 7, hy2 + 4), num, font=SANS_B(12), fill=(255, 255, 255))
        hl = wrap(head, SERIF_B(15), x1 - x0 - 28, d)
        y = draw_lines(d, x0 + 28, hy2, hl[:2], SERIF_B(15), INK, 18)
        bl = wrap(body, SANS(11), x1 - x0 - 28, d)
        y = draw_lines(d, x0 + 28, y + 3, bl[:3], SANS(11), (60, 60, 60), 14)
        d.text((x0 + 28, hy2 + 92), src, font=SANS(9), fill=GREY_T)
        chip(d, x1, hy2 + 90, "REPORTED", NAVY)

    # ---------- MORE OF THE DAY ----------
    d.text((10, 462), "MORE OF THE DAY \u2014 10 STORIES", font=SANS_B(14),
           fill=INK)
    d.line([(10, 480), (W - 10, 480)], fill=INK, width=2)

    # ---------- 10 cards ----------
    cards = [
        ("AMERICAS", "4", "BESSENT: NVIDIA ANSWERS",
         "Treasury chief wants to know of violations over China sales.",
         "Reuters", "REPORTED", NAVY),
        ("FBI", "5", "FBI PROBES NCIC HACK",
         "Hackers hit the NCIC system used by police nationwide.",
         "AP", "REPORTED", NAVY),
        ("WHITE HOUSE", "6", "TRUMP: IRAN STRIKES MAY RESUME",
         "Strikes could resume in the New Year.",
         "Reuters", "REPORTED", NAVY),
        ("MARKETS", "7", "US FUTURES JUMP 3%",
         "Holiday-week rally lifts Nasdaq futures as the AI rout cools.",
         "Bloomberg", "REPORTED", NAVY),
        ("SPORT", "8", "SKUBAL'S $450M METS DEAL",
         "Two-time Cy Young winner signs nine years, largest ever for a pitcher.",
         "ESPN", "REPORTED", NAVY),
        ("SPORT", "9", "TOM JACKSON DIES AT 75",
         "Broncos linebacker turned ESPN voice dies.",
         "ESPN", "REPORTED", NAVY),
        ("LEGAL", "10", "STATES SUE SPACEX",
         "Ten states challenge AI safety claims.",
         "AP", "REPORTED", NAVY),
        ("TECH", "11", "ANTHROPIC IPO: $107.3B",
         "Claude maker raises at $83 a share; debut closes $97.17.",
         "WSJ", "REPORTED", NAVY),
        ("EUROPE", "12", "POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE",
         "Kyiv: three Kh-101s crossed airspace.",
         "AP", "CLAIM", RED),
        ("SPACE", "13", "RUSSIAN NUCLEAR SATELLITE",
         "Intel claims a nuclear-armed satellite.",
         "Reuters", "CLAIM", RED),
    ]
    cw, chh, cg = 198, 80, 6
    cat_cols = {"AMERICAS": (120, 40, 40), "FBI": (90, 40, 120),
                "WHITE HOUSE": (150, 110, 0), "MARKETS": (0, 110, 110),
                "SPORT": (40, 120, 60), "LEGAL": (140, 40, 110),
                "TECH": (0, 90, 140), "EUROPE": (160, 60, 30),
                "SPACE": (90, 90, 90)}
    for i, (cat, num, head, body, src, lab, labcol) in enumerate(cards):
        r, c = divmod(i, 5)
        x0 = 10 + c * (cw + cg)
        y0 = 486 + r * (chh + cg)
        d.rectangle([x0, y0, x0 + cw, y0 + chh], outline=(180, 172, 150),
                    width=1, fill=(255, 255, 255))
        d.rectangle([x0, y0, x0 + cw, y0 + 16], fill=cat_cols[cat])
        d.text((x0 + 5, y0 + 3), cat, font=SANS_B(9), fill=(255, 255, 255))
        d.text((x0 + cw - 5 - d.textlength(num, font=SANS_B(10)), y0 + 3),
               num, font=SANS_B(10), fill=(255, 255, 255))
        hl = wrap(head, SERIF_B(11), cw - 10, d)
        y = draw_lines(d, x0 + 5, y0 + 19, hl[:2], SERIF_B(11), INK, 13)
        # body lines capped so they never reach the source/chip row:
        # 2-line headline -> 1 body line; 1-line headline -> 2 body lines
        max_body = 1 if len(hl) > 1 else 2
        bl = wrap(body, SANS(9), cw - 10, d)
        draw_lines(d, x0 + 5, y + 1, bl[:max_body], SANS(9), (70, 70, 70), 11)
        d.text((x0 + 5, y0 + chh - 13), src, font=SANS(8), fill=GREY_T)
        chip(d, x0 + cw - 4, y0 + chh - 15, lab, labcol)

    # ---------- map + ALSO headers ----------
    d.text((10, 658), "WHERE IT HAPPENED", font=SANS_B(14), fill=INK)
    d.text((520, 658), "ALSO ON MONDAY", font=SANS_B(14), fill=INK)
    d.line([(10, 676), (W - 10, 676)], fill=INK, width=2)

    # ---------- map ----------
    mx0, my0, mx1, my1 = 10, 682, 500, 868
    d.rectangle([mx0, my0, mx1, my1], fill=MAP_BG)
    for gx in range(mx0 + 20, mx1, 20):
        d.line([(gx, my0), (gx, my1)], fill=(196, 212, 220), width=1)
    for gy in range(my0 + 20, my1, 20):
        d.line([(mx0, gy), (mx1, gy)], fill=(196, 212, 220), width=1)
    # continents (kept inside the map box)
    d.polygon([(30, 690), (120, 675), (170, 690), (150, 730), (110, 745),
               (60, 740), (35, 720)], fill=LAND)
    d.polygon([(120, 755), (160, 750), (165, 790), (140, 830), (120, 800)],
              fill=LAND)
    d.polygon([(250, 680), (300, 672), (320, 690), (300, 705), (260, 705)],
              fill=LAND)
    d.polygon([(255, 720), (300, 715), (315, 745), (295, 790), (265, 775)],
              fill=LAND)
    d.polygon([(330, 675), (430, 665), (470, 690), (450, 730), (400, 745),
               (350, 730), (330, 700)], fill=LAND)
    d.polygon([(400, 800), (450, 795), (455, 820), (410, 825)], fill=LAND)
    pins = [(445, 690), (150, 760), (430, 675), (95, 700), (120, 695),
            (360, 705), (75, 705), (45, 715), (70, 725), (85, 740),
            (290, 685), (315, 695), (350, 680)]
    for i, (px, py) in enumerate(pins, start=1):
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        lab = str(i)
        d.text((px - d.textlength(lab, font=SANS_B(9)) / 2, py - 6),
               lab, font=SANS_B(9), fill=(255, 255, 255))

    # ---------- ALSO list ----------
    also = [
        "14. Paris: 100+ back 2% billionaire tax",
        "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week",
        "17. COP31: the day after pact rejected",
        "18. Benghazi: UN demands port probe",
        "19. Israel unity talks resume",
        "20. Gaza: two killed in Israeli strike",
        "21. West Bank settler attacks",
        "22. Iran war: no deal in sight",
        "23. Lebanon seizes 264 kg explosives",
        "24. Bahrain: strike hits plant, 2 hurt",
        "25. Sudan: defences down drones",
        "26. DRC: fighting traps Ebola teams",
        "27. Bangladesh: Hasina jailed if she returns",
        "28. Seoul minister quits in exam row",
        "29. SK Telecom -7.3% as hype cools",
        "30. China eases margin rules",
        "31. Seoul readies 10T-won fund",
    ]
    for i, item in enumerate(also):
        col = i // 9
        row = i % 9
        ax = 520 + col * 250
        ay = 688 + row * 22
        d.text((ax, ay), item, font=SANS(10), fill=INK)

    # pin legend (2 lines, below map)
    leg = ("Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 "
           "4 Washington \u00b7 5 New York \u00b7 6 Tehran \u00b7 7 Chicago \u00b7 "
           "8 San Francisco")
    leg2 = "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow"
    d.text((10, 872), leg, font=SANS(9), fill=GREY_T)
    d.text((10, 884), leg2, font=SANS(9), fill=GREY_T)

    # ---------- DATE CHECK ----------
    d.rectangle([10, 898, W - 10, 962], outline=RED, width=3, fill=(255, 240, 240))
    d.text((20, 904), "DATE CHECK", font=SANS_B(13), fill=RED)
    d.text((150, 906),
           "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
           font=SANS_B(11), fill=INK)
    dc = ("LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 (22 Nov) \u00b7 "
          "Sparta II fire (22 Nov) \u00b7 El Chapo captured (22 Nov) \u00b7 "
          "EU-Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 "
          "ICJ Myanmar ruling (19 Nov)")
    dl = wrap(dc, SANS(10), W - 40, d)
    draw_lines(d, 20, 926, dl[:1], SANS(10), INK, 13)
    d.text((20, 944),
           "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races "
           "uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped "
           "Ebola staff", font=SANS(10), fill=INK)

    # ---------- footer ----------
    d.text((10, 968), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 "
           "Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute "
           "(Asia Power Index 2026).", font=SANS(9), fill=GREY_T)
    d.text((10, 980), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one "
           "side's claim, not independently confirmed \u00b7 ONGOING = still "
           "developing", font=SANS(9), fill=GREY_T)
    d.rectangle([0, 996, W, H], fill=BLACK)
    foot = ("Scenes are drawn illustrations, not photographs.  \u00b7  "
            "THE WORLD TODAY \u2014 Monday 23 November 2026  \u00b7  31 stories  "
            "\u00b7  6 regions")
    d.text(((W - d.textlength(foot, font=SANS_B(11))) / 2, 1006), foot,
           font=SANS_B(11), fill=GOLD)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
