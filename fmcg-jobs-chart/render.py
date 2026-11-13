import json, sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(f"{D}/data.json"))
years, doms, HL = d["years"], d["domains"], d["highlight"]
names = list(doms)
W, H, S = 1080, 1350, 1
F = "/usr/share/fonts/opentype/inter/"
f = lambda n, s: ImageFont.truetype(F + n, s)
BG, INK, MUTE, BAR, ACC, ACC_T = "#F7F6F2", "#14141F", "#8A8A99", "#C9C8D6", "#5B3FE0", "#5B3FE0"
def share(t):  # t in year-index units, smooth between snapshots
    i = min(int(t), len(years) - 2); u = t - i; u = u*u*(3 - 2*u)
    v = {n: doms[n][i]*(1-u) + doms[n][i+1]*u for n in names}
    s = sum(v.values()); return {n: v[n]/s*100 for n in names}
def rank_of(v, n): return sorted(v, key=v.get, reverse=True).index(n) + 1
FPS, SEG, HOLD = 30, 36, 60
ts = []
for i in range(len(years)-1):
    ts += [i + k/SEG for k in range(SEG)]
ts += [len(years)-1]*HOLD
def frame(t, pos):
    im = Image.new("RGB", (W, H), BG); g = ImageDraw.Draw(im)
    v = share(t); yr = years[0] + (years[-1]-years[0])*t/(len(years)-1)
    g.text((60, 70), "FMCG JOBS HAVE", font=f("Inter-Bold.otf", 64), fill=INK)
    g.text((60, 142), "REINVENTED THEMSELVES", font=f("Inter-Bold.otf", 64), fill=ACC)
    g.text((60, 232), "Share of FMCG corporate openings by function, %", font=f("Inter-Regular.otf", 28), fill=MUTE)
    x0, x1, top, row = 380, 960, 330, 76
    mx = 36
    for gx in range(0, 36, 10):
        X = x0 + (x1-x0)*gx/mx
        g.line([(X, top-10), (X, top+row*10)], fill="#E4E3EC", width=2)
        g.text((X, top-40), f"{gx}%", font=f("Inter-Regular.otf", 22), fill=MUTE, anchor="mm")
    for n in names:
        y = top + pos[n]*row
        hl = n == HL
        w = max(4, (x1-x0)*v[n]/mx)
        g.rounded_rectangle([x0, y+8, x0+w, y+row-14], radius=6, fill=ACC if hl else BAR)
        g.text((x0-16, y+row/2-3), n, font=f("Inter-Bold.otf" if hl else "Inter-Medium.otf", 26), fill=ACC_T if hl else INK, anchor="rm")
        g.text((x0+w+12, y+row/2-3), f"{v[n]:.1f}%", font=f("Inter-Bold.otf", 24), fill=ACC_T if hl else MUTE, anchor="lm")
    g.text((60, 1170), f"{HL} rank", font=f("Inter-Regular.otf", 24), fill=MUTE)
    g.text((60, 1195), f"#{rank_of(v, HL)}", font=f("Inter-Bold.otf", 84), fill=ACC)
    g.text((1020, 1225), f"{int(round(yr))}", font=f("Inter-Bold.otf", 150), fill=ACC, anchor="rm")
    p = t/(len(years)-1); g.line([(60, 1318), (1020, 1318)], fill="#DAD9E3", width=4)
    g.line([(60, 1318), (60+960*p, 1318)], fill=ACC, width=4)
    if t >= len(years)-1:
        g.text((60, 1128), "Digital, Data & ESG roles grew 6x+; plant & field-heavy roles shrank.", font=f("Inter-SemiBold.otf", 26), fill=INK)
    g.text((60, 1335-8), "Illustrative estimates, not official data.", font=f("Inter-Regular.otf", 17), fill=MUTE)
    return im
out = f"{D}/frames"; os.makedirs(out, exist_ok=True)
pos = {n: float(rank_of(share(0), n)-1) for n in names}
for k, t in enumerate(ts):
    v = share(t)
    for n in names: pos[n] += (rank_of(v, n)-1 - pos[n])*0.25
    im = frame(t, pos); im.save(f"{out}/{k:04d}.png")
    if t >= len(years)-1 and k == len(ts)-1: im.save(f"{D}/fmcg-jobs-evolution.png")
subprocess.run(["ffmpeg","-y","-v","error","-framerate",str(FPS),"-i",f"{out}/%04d.png","-c:v","libx264","-pix_fmt","yuv420p","-crf","18",f"{D}/fmcg-jobs-evolution.mp4"],check=True)
import shutil; shutil.rmtree(out)
