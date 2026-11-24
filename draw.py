#!/usr/bin/env python3
"""news-23 b23 front-page-dense: draws THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 246, 235)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (16, 36, 64)
GRAY = (110, 110, 110)
GREEN = (31, 122, 31)
AMBER = (176, 112, 0)
BLUE = (31, 78, 121)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, font, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, font, max_w, max_lines):
    """Wrap text, truncating with ellipsis if it exceeds max_lines."""
    lines = wrap(text, font, max_w)
    while len(lines) > max_lines:
        words = lines[max_lines - 1].split(" ")[:-1]
        if not words:
            lines = lines[:max_lines]
            break
        lines[max_lines - 1] = " ".join(words) + " ..."
        lines = lines[:max_lines]
        # re-wrap the shortened tail is unnecessary; ellipsis marks the cut
        break
    return lines[:max_lines]


def draw_chip(d, x, y, label, fill):
    w = int(d.textlength(label, font=f(SANS_B, 9))) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f(SANS_B, 9), fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- top red rule ----
d.rectangle([0, 0, W, 6], fill=RED)

# ---- masthead ----
d.text((24, 14), "THE WORLD TODAY", font=f(SERIF_B, 46), fill=INK)
d.text((1000, 16), "31 STORIES", font=f(SANS_B, 16), fill=INK, anchor="ra")
d.text((1000, 38), "6 REGIONS", font=f(SANS_B, 16), fill=INK, anchor="ra")
d.text((24, 70), "MONDAY 23 NOVEMBER 2026", font=f(SANS_B, 20), fill=RED)
d.text((1000, 74), "AI ROUT  \u00b7  AI RULES  \u00b7  POWER SHIFT",
       font=f(SANS, 13), fill=GRAY, anchor="ra")
d.line([24, 96, 1000, 96], fill=INK, width=2)

# ---- number strip ----
nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"), ("11,762", "EBOLA CASES"),
        ("10T WON", "SEOUL FUND"), ("$450M", "SKUBAL DEAL"), ("$107.3B", "ANTHROPIC IPO")]
cell_w = 976 / 6
for i, (n, lab) in enumerate(nums):
    x = 24 + i * cell_w
    d.text((x + cell_w / 2, 102), n, font=f(SANS_B, 25), fill=RED, anchor="ma")
    d.text((x + cell_w / 2, 132), lab, font=f(SANS_B, 10), fill=INK, anchor="ma")
    if i:
        d.line([x, 104, x, 142], fill=(200, 190, 175), width=1)
d.line([24, 150, 1000, 150], fill=(200, 190, 175), width=1)

# ---- region bar ----
regions = [("NORTH AMERICA 8", 8, (31, 78, 121)), ("EUROPE 6", 6, (197, 90, 17)),
           ("MIDDLE EAST 6", 6, (112, 48, 160)), ("ASIA-PACIFIC 6", 6, (15, 123, 108)),
           ("AFRICA 3", 3, (127, 96, 0)), ("WORLD 2", 2, (89, 89, 89))]
x = 24
for lab, cnt, col in regions:
    w = 976 * cnt / 31
    d.rectangle([x, 154, x + w - 1, 172], fill=col)
    d.text((x + w / 2, 158), lab, font=f(SANS_B, 11), fill=(255, 255, 255), anchor="ma")
    x += w

# ---- UTC strip ----
d.rectangle([24, 176, 1000, 196], fill=NAVY)
d.text((32, 181), "THE DAY IN UTC", font=f(SANS_B, 11), fill=(255, 210, 63))
d.text((150, 181),
       "~00:00 ASIA OPENS  \u00b7  06:30 KOSPI -3.3%  \u00b7  ~09:00 SEOUL FUND  \u00b7  "
       "14:30 WALL ST +3%  \u00b7  ~16:00 GUTERRES  \u00b7  ~21:00 FBI HACK   (~ = APPROX.)",
       font=f(SANS, 11), fill=(255, 255, 255))

# ---- hero scenes ----
HX = [24, 352, 680]
HW = 320
HY = 202
SC_H = 104


def scene_kospi(x0, y0):
    d.rectangle([x0, y0, x0 + HW, y0 + SC_H], fill=NAVY)
    # skyline
    import random
    rnd = random.Random(7)
    bx = x0 + 8
    while bx < x0 + HW - 14:
        bw = rnd.randint(16, 30)
        bh = rnd.randint(28, 62)
        d.rectangle([bx, y0 + SC_H - bh, bx + bw, y0 + SC_H], fill=(38, 58, 92))
        for wy in range(y0 + SC_H - bh + 5, y0 + SC_H - 4, 9):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 63))
        bx += bw + 4
    # falling chart
    pts = [(x0 + 14, y0 + 30), (x0 + 70, y0 + 40), (x0 + 120, y0 + 34),
           (x0 + 175, y0 + 52), (x0 + 225, y0 + 60), (x0 + 275, y0 + 80),
           (x0 + 308, y0 + 96)]
    d.line(pts, fill=(255, 80, 80), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
    d.text((x0 + 10, y0 + 8), "intraday -5.8%", font=f(SANS, 11), fill=(255, 255, 255))
    d.text((x0 + HW - 10, y0 + 6), "-3.3%", font=f(SANS_B, 26), fill=(255, 80, 80), anchor="ra")


def scene_guterres(x0, y0):
    d.rectangle([x0, y0, x0 + HW, y0 + SC_H], fill=NAVY)
    # globe
    cx, cy, r = x0 + 62, y0 + 56, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 200))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(180, 210, 240), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(180, 210, 240), width=1)
    d.ellipse([cx - 18, cy - r, cx + 18, cy + r], outline=(180, 210, 240), width=1)
    d.ellipse([cx - r, cy - 20, cx + r, cy + 20], outline=(180, 210, 240), width=1)
    # network
    import random
    rnd = random.Random(11)
    nodes = [(x0 + 150, y0 + 22), (x0 + 195, y0 + 40), (x0 + 235, y0 + 18),
             (x0 + 170, y0 + 68), (x0 + 220, y0 + 78), (x0 + 260, y0 + 52),
             (x0 + 285, y0 + 88), (x0 + 205, y0 + 100)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if rnd.random() < 0.45:
                d.line([nodes[i], nodes[j]], fill=(140, 180, 220), width=1)
    for nx, ny in nodes:
        d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(255, 210, 63))
    # podium silhouette
    d.polygon([(x0 + 268, y0 + SC_H), (x0 + 276, y0 + 84), (x0 + 292, y0 + 84),
               (x0 + 300, y0 + SC_H)], fill=(10, 10, 10))
    d.ellipse([x0 + 278, y0 + 66, x0 + 290, y0 + 82], fill=(10, 10, 10))
    d.rectangle([x0 + 8, y0 + 8, x0 + 118, y0 + 26], fill=(255, 210, 63))
    d.text((x0 + 13, y0 + 11), "150 DELEGATES", font=f(SANS_B, 11), fill=INK)


def scene_power(x0, y0):
    d.rectangle([x0, y0, x0 + HW, y0 + SC_H], fill=(245, 240, 228))
    d.text((x0 + 12, y0 + 8), "ASIA POWER INDEX 2026", font=f(SANS_B, 13), fill=INK)
    bars = [("US", 78.9, (31, 78, 121)), ("CHINA", 73.6, RED), ("INDIA", 40.5, (128, 128, 128))]
    by = y0 + 30
    for lab, val, col in bars:
        d.text((x0 + 12, by), lab, font=f(SANS_B, 12), fill=INK)
        d.rectangle([x0 + 78, by + 2, x0 + 78 + 190 * val / 100, by + 14], fill=col)
        d.text((x0 + 78 + 190 * val / 100 + 6, by), f"{val}", font=f(SANS_B, 12), fill=INK)
        by += 20
    d.text((x0 + 12, y0 + SC_H - 18), "GAP 5.3", font=f(SANS_B, 15), fill=RED)
    d.text((x0 + 92, y0 + SC_H - 14), "narrowest since 2018", font=f(SANS, 11), fill=INK)


heroes = [
    ("#1 ASIA \u00b7 MARKETS", "AI ROUT HITS ASIA",
     "Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, SK Hynix -2.5%.",
     "Source: Yonhap \u00b7 Korea JoongAng", "REPORTED", GREEN, scene_kospi),
    ("#2 WORLD \u00b7 UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; "
     "150 delegates back a risk framework.",
     "Source: UN News \u00b7 Reuters", "REPORTED", GREEN, scene_guterres),
    ("#3 ASIA-PACIFIC \u00b7 POWER", "US LEAD OVER CHINA AT RECORD LOW",
     "Gap 5.3 narrowest since 2018. US diplomatic influence -6 to 76.7. "
     "India third at 40.5.",
     "Source: Lowy Institute", "REPORTED", GREEN, scene_power),
]
for i, (kick, title, body, src, chip, fill, scene) in enumerate(heroes):
    x0 = HX[i]
    scene(x0, HY)
    ty = HY + SC_H + 6
    d.text((x0, ty), kick, font=f(SANS_B, 10), fill=RED)
    ty += 14
    for ln in fit_lines(title, f(SANS_B, 15), HW, 2):
        d.text((x0, ty), ln, font=f(SANS_B, 15), fill=INK)
        ty += 18
    for ln in fit_lines(body, f(SANS, 11), HW, 2):
        d.text((x0, ty), ln, font=f(SANS, 11), fill=INK)
        ty += 14
    d.text((x0, ty + 2), src, font=f(SANS, 9), fill=GRAY)
    draw_chip(d, x0 + HW - 62, ty, chip, fill)

# ---- 10 small cards ----
cards = [
    (4, "SPORT \u00b7 US", (31, 78, 121), "Skubal signs $450M Mets deal",
     "Two-time Cy Young winner, nine years \u2014 the largest ever for a pitcher.",
     "ESPN", "REPORTED", GREEN),
    (5, "TECH \u00b7 US", (31, 78, 121), "Anthropic IPO: $107.3B, largest ever",
     "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.",
     "Bloomberg", "REPORTED", GREEN),
    (6, "EUROPE \u00b7 WAR", (197, 90, 17), "Poland: 3 Russian missiles crossed airspace",
     "Kyiv says three Kh-101 entered Poland on Friday; Tusk: provocation.",
     "AP", "CLAIM", AMBER),
    (7, "EUROPE \u00b7 SECURITY", (197, 90, 17), "Intel warns of Russian nuclear satellite",
     "Moscow built a satellite to carry a nuclear warhead.",
     "Bloomberg", "CLAIM", AMBER),
    (8, "EUROPE \u00b7 ECONOMY", (197, 90, 17), "Paris: 100+ back 2% billionaire tax",
     "Economists, politicians, unions rally behind France's 2% wealth tax.",
     "AFP", "REPORTED", GREEN),
    (9, "EUROPE \u00b7 UK", (197, 90, 17), "Manchester: 12,000 cleared after scare",
     "Substance scare empties arena district; no casualties reported.",
     "AP", "REPORTED", GREEN),
    (10, "EUROPE \u00b7 WAR", (197, 90, 17), "Zelenskyy: 165 Russian missiles in a week",
     "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.",
     "Kyiv", "CLAIM", AMBER),
    (11, "WORLD \u00b7 CLIMATE", (89, 89, 89), "COP31: the day after",
     "Sunday's collapse \u2014 194 nations reject the Antalya pact \u2014 draws fury.",
     "CNN", "REPORTED", GREEN),
    (12, "AFRICA \u00b7 LIBYA", (127, 96, 0), "Benghazi: UN demands probe of port attacks",
     "Drones hit two Russian ships; UN calls for an investigation.",
     "UN News", "CLAIM", AMBER),
    (13, "MIDDLE EAST \u00b7 ISRAEL", (112, 48, 160), "Israel unity talks resume",
     "Likud and Gantz's Yesh Atid return to the table after Sunday's stall.",
     "Reuters", "ONGOING", BLUE),
]
CW = 188
CG = 9
CY = [408, 508]
CH = 92
for idx, (num, kick, kcol, title, body, src, chip, cfill) in enumerate(cards):
    row, col = divmod(idx, 5)
    x0 = 24 + col * (CW + CG)
    y0 = CY[row]
    d.rectangle([x0, y0, x0 + CW, y0 + CH], outline=(200, 190, 175), width=1, fill=(255, 255, 255))
    d.rectangle([x0, y0, x0 + CW, y0 + 15], fill=kcol)
    d.text((x0 + 5, y0 + 2), f"#{num}", font=f(SANS_B, 9), fill=(255, 255, 255))
    d.text((x0 + 28, y0 + 2), kick, font=f(SANS_B, 9), fill=(255, 255, 255))
    ty = y0 + 19
    for ln in fit_lines(title, f(SANS_B, 11), CW - 10, 2):
        d.text((x0 + 5, ty), ln, font=f(SANS_B, 11), fill=INK)
        ty += 13
    for ln in fit_lines(body, f(SANS, 9), CW - 10, 2):
        d.text((x0 + 5, ty), ln, font=f(SANS, 9), fill=INK)
        ty += 11
    d.text((x0 + 5, y0 + CH - 13), src, font=f(SANS, 8), fill=GRAY)
    draw_chip(d, x0 + CW - 62, y0 + CH - 15, chip, cfill)

# ---- map + ALSO list ----
MY = 612
d.text((24, MY), "THE WORLD \u2014 WHERE IT HAPPENED", font=f(SANS_B, 13), fill=RED)
d.text((24, MY + 16), "PIN = STORY NUMBER", font=f(SANS, 9), fill=GRAY)
MAP_X, MAP_Y, MAP_W, MAP_H = 24, MY + 30, 536, 176
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(214, 232, 240),
            outline=(180, 190, 200), width=1)
# graticule
for gx in range(MAP_X + 60, MAP_X + MAP_W, 60):
    d.line([gx, MAP_Y, gx, MAP_Y + MAP_H], fill=(190, 205, 215), width=1)
for gy in range(MAP_Y + 44, MAP_Y + MAP_H, 44):
    d.line([MAP_X, gy, MAP_X + MAP_W, gy], fill=(190, 205, 215), width=1)

CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
           (-75, 72), (-60, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 25),
           (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
           (-140, 60), (-155, 58), (-165, 60)],
    "SA": [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
           (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-75, -40), (-75, -20), (-80, -5)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
           (40, 15), (43, 11), (48, 5), (40, -5), (35, -18), (30, -30), (20, -35),
           (12, -18), (8, 4), (-8, 5)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
           (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (25, 71),
           (18, 69), (12, 65), (5, 60), (5, 58), (-5, 50)],
    "AS": [(30, 70), (40, 68), (50, 70), (60, 70), (70, 73), (80, 73), (90, 75),
           (100, 77), (110, 76), (120, 73), (130, 72), (140, 72), (150, 70),
           (160, 66), (162, 60), (158, 52), (150, 59), (142, 50), (140, 40),
           (135, 35), (130, 33), (127, 35), (122, 38), (120, 30), (115, 22),
           (110, 20), (108, 12), (105, 8), (100, 8), (97, 15), (92, 21),
           (90, 22), (86, 20), (80, 13), (77, 8), (75, 20), (70, 25), (66, 25),
           (60, 25), (57, 26), (52, 28), (50, 30), (48, 30), (44, 29), (42, 15),
           (40, 15), (35, 28), (30, 36), (28, 41), (30, 45)],
    "AU": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
           (135, -35), (140, -38), (145, -38), (150, -37), (153, -27), (146, -19),
           (142, -11), (137, -12), (135, -15), (132, -11), (130, -13), (126, -14),
           (122, -17), (118, -20)],
    "GL": [(-58, 64), (-50, 60), (-40, 60), (-30, 68), (-22, 70), (-20, 76),
           (-30, 80), (-50, 78), (-58, 74)],
}
LAND = (232, 220, 190)


def proj(lon, lat):
    x = MAP_X + (lon + 180) / 360 * MAP_W
    y = MAP_Y + (90 - lat) / 150 * MAP_H
    return x, y


for poly in CONTINENTS.values():
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
              outline=(190, 180, 160))
d.text((MAP_X + 6, MAP_Y + MAP_H - 14), "N \u2191", font=f(SANS_B, 10), fill=INK)

CLAIM_PINS = {6, 7, 10, 12}
ONGOING_PINS = {13}
# (story, lon, lat, dx, dy)
PINS = [
    (1, 127, 37.5, -16, -10), (2, -30, 20, 0, 0), (3, -150, -30, 0, 0),
    (4, -74, 40.7, 0, 0), (5, -77, 39, 0, 0), (6, 21, 52.2, -14, -10),
    (7, 37.6, 55.8, 16, -12), (8, 2.3, 48.9, -14, -6), (9, -2.2, 53.5, -4, -12),
    (10, 30.5, 50.5, 12, 10), (11, 30.7, 36.9, 20, 4), (12, 20.1, 32.1, -18, 8),
    (13, 34.5, 31.5, -18, 14), (14, 34.5, 31.5, 18, -12), (15, 35.2, 31.9, -20, -14),
    (16, 51.4, 35.7, 14, -10), (17, 35.5, 33.9, 6, 20), (18, 50.6, 26.2, 16, 10),
    (19, 32.5, 15.6, 0, 0), (20, 30, 1.5, 0, 0), (21, 90.4, 23.8, 0, 0),
    (22, 127, 37.5, 6, 8), (23, 127, 37.5, 14, -2), (24, 116.4, 39.9, 0, 0),
    (25, 127, 37.5, -6, 10), (26, -77, 39, -12, 6), (27, -77, 39, 10, -6),
    (28, -77, 39, 12, 8), (29, -74, 40.7, 10, 8), (30, -105, 39.7, 0, 0),
    (31, -97.7, 30.3, 0, 0),
]
for num, lon, lat, dx, dy in PINS:
    px, py = proj(lon, lat)
    px, py = px + dx, py + dy
    if num in CLAIM_PINS:
        col = (232, 160, 32)
    elif num in ONGOING_PINS:
        col = (31, 78, 121)
    else:
        col = RED
    d.ellipse([px - 6.5, py - 6.5, px + 6.5, py + 6.5], fill=col,
              outline=(255, 255, 255), width=1)
    d.text((px, py - 5), str(num), font=f(SANS_B, 8), fill=(255, 255, 255), anchor="ma")

# ALSO list (two columns)
d.text((576, MY), "ALSO ON MONDAY \u2014 18 MORE STORIES", font=f(SANS_B, 13), fill=RED)
also_left = [
    ("MIDDLE EAST", (112, 48, 160), [
        "14 Gaza: two killed in Israeli strike",
        "15 West Bank: settler attacks hit villages",
        "16 Iran war: no deal in sight",
        "17 Lebanon seizes 264 kg of explosives",
        "18 Bahrain: Iranian strike hits plant, 2 hurt"]),
    ("AFRICA", (127, 96, 0), [
        "19 Sudan drones downed over Khartoum",
        "20 DRC: fighting traps Ebola teams"]),
    ("WORLD", (89, 89, 89), [
        "31 States sue SpaceX over AI safety claims"]),
]
also_right = [
    ("ASIA-PACIFIC", (15, 123, 108), [
        "21 Bangladesh: Hasina jailed if she returns",
        "22 Seoul minister quits over AI exam chaos",
        "23 SK Telecom -7.3% as Anthropic hype cools",
        "24 China eases margin rules to calm rout",
        "25 Seoul readies 10T-won stabilisation fund"]),
    ("NORTH AMERICA", (31, 78, 121), [
        "26 Bessent demands Nvidia answers",
        "27 FBI probes hack of police database",
        "28 Trump: Iran strikes may resume in New Year",
        "29 US futures jump 3% holiday week",
        "30 Tom Jackson dies at 75"]),
]


def draw_also(x0, groups, y_start):
    y = y_start
    for lab, col, items in groups:
        d.text((x0, y), lab, font=f(SANS_B, 10), fill=col)
        y += 14
        for it in items:
            for ln in wrap(it, f(SANS, 10), 210):
                d.text((x0, y), ln, font=f(SANS, 10), fill=INK)
                y += 12
        y += 3
    return y


draw_also(576, also_left, MY + 30)
draw_also(792, also_right, MY + 30)

# ---- DATE CHECK ----
DY = 826
d.rectangle([24, DY, 1000, 924], outline=RED, width=2, fill=(255, 245, 245))
d.text((32, DY + 8), "DATE CHECK", font=f(SANS_B, 13), fill=RED)
d.text((32, DY + 26),
       "Every story above happened or was first reported on Monday 23 November 2026.",
       font=f(SANS_B, 11), fill=INK)
d.text((992, DY + 8), "WIRES READ UP TO 23:00 UTC", font=f(SANS_B, 10), fill=RED, anchor="ra")
d.text((32, DY + 46),
       "LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 "
       "El Chapo Isidro captured (22 Nov) \u00b7 EU-Indonesia pact (21 Nov) \u00b7 "
       "Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov).",
       font=f(SANS, 10), fill=INK)
d.text((32, DY + 66),
       "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 "
       "COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff.",
       font=f(SANS, 10), fill=INK)

# ---- footer ----
d.text((24, 934),
       "SOURCES: AP \u00b7 Reuters \u00b7 Bloomberg \u00b7 AFP \u00b7 CNN \u00b7 ESPN \u00b7 UN News \u00b7 "
       "WHO \u00b7 Kyiv \u00b7 Lowy Institute \u00b7 Korea JoongAng \u00b7 Morningstar",
       font=f(SANS, 9), fill=GRAY)
d.text((24, 950),
       "CONFIRMED = 2+ outlets \u00b7 REPORTED = carried by a wire \u00b7 CLAIM = one side alleges \u00b7 "
       "ONGOING = developing.  Red pin = reported \u00b7 Amber pin = claim (unverified).",
       font=f(SANS, 9), fill=GRAY)
d.text((24, 972), "THE WORLD TODAY \u00b7 23 NOV 2026", font=f(SANS_B, 10), fill=INK)
d.text((1000, 972), "Scenes are drawn illustrations, not photographs.",
       font=f(SANS, 9), fill=GRAY, anchor="ra")

img.save("entry.png")
print("saved entry.png", img.size)
