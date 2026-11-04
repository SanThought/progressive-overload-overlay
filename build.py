#!/usr/bin/env python3
"""Build progressive-overload-overlay final.mp4.
Inputs expected next to this script:
  src.mp4            - original vertical video (474x850, not committed: private)
  fonts/SpaceGrotesk-Bold.ttf, fonts/Inter.ttf  (OFL, google/fonts)
Requires: pillow, fonttools, ffmpeg with libass.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 474, 850
VOLT = (216, 255, 63); INK = (12, 12, 14); WHITE = (245, 245, 242); GRAY = (170, 170, 165)
SG = "fonts/SpaceGrotesk-Bold.ttf"; IT = "fonts/Inter.ttf"
os.makedirs("assets", exist_ok=True)

def font(path, size, wght):
    f = ImageFont.truetype(path, size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

def card(fname, headline, lines, src):
    cw, ch = 414, 176
    img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, cw-1, ch-1], radius=14, fill=(10, 10, 12, 215))
    d.rounded_rectangle([0, 0, 7, ch-1], radius=3, fill=VOLT + (255,))
    d.text((26, 16), headline, font=font(SG, 30, 700), fill=VOLT)
    y = 58
    for ln in lines:
        d.text((26, y), ln, font=font(IT, 21, 500), fill=WHITE); y += 29
    d.text((26, ch-34), src, font=font(IT, 17, 400), fill=GRAY)
    img.save("assets/" + fname)

card("cardA.png", "PROGRESSIVE OVERLOAD",
     ["Raise the training stimulus", "gradually, from a load you", "can fully control."],
     "Source: ACSM Position Stand - MSSE 2009")
card("cardB.png", "THE 2-10% RULE",
     ["Hit 1-2 reps over your target,", "then add 2-10% load. That is", "the published progression rule."],
     "Source: ACSM Position Stand - MSSE 2009")
card("cardC.png", "STRENGTH LOVES HEAVY",
     ["Heavy loads beat light loads", "for strength: SMD 0.60", "(95% CI 0.38-0.82)."],
     "Source: Lopez et al. 2021 - 28 studies, 747 adults")
card("cardD.png", "HYPERTROPHY: ANY LOAD",
     ["Sets to failure grow muscle", "equally at light and heavy loads", "(P = 0.11-0.47)."],
     "Source: Lopez et al. 2021 - MSSE")

def wrap(d, text, f, maxw):
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# intro
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
d.rectangle([40, 300, 120, 306], fill=VOLT)
d.text((40, 330), "PROGRESSIVE", font=font(SG, 58, 700), fill=WHITE)
d.text((40, 396), "OVERLOAD", font=font(SG, 58, 700), fill=VOLT)
d.text((40, 480), "One claim, checked against", font=font(IT, 24, 500), fill=GRAY)
d.text((40, 512), "the evidence.", font=font(IT, 24, 500), fill=GRAY)
d.text((40, 780), "EVIDENCE OVERLAY - NOV 2026", font=font(IT, 16, 600), fill=GRAY)
img.save("assets/intro.png")

# outro
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
d.rectangle([40, 120, 120, 126], fill=VOLT)
d.text((40, 146), "SOURCES", font=font(SG, 44, 700), fill=WHITE)
y = 230
for s in [
 "1. ACSM. Progression Models in Resistance Training for Healthy Adults. Med Sci Sports Exerc. 2009;41(3):687-708.",
 "2. Lopez P, et al. Resistance Training Load Effects on Muscle Hypertrophy and Strength Gain. Med Sci Sports Exerc. 2021;53(6):1206-1216.",
 "3. Schoenfeld BJ, et al. Dose-response of weekly training volume to muscle mass. J Sports Sci. 2017;35(11):1073-1082.",
]:
    for ln in wrap(d, s, font(IT, 19, 400), 394):
        d.text((40, y), ln, font=font(IT, 19, 400), fill=WHITE); y += 26
    y += 16
for ln in wrap(d, "Bonus: higher weekly volume -> more growth (graded dose-response, P=0.002 - Schoenfeld 2017)", font(IT, 19, 600), 394):
    d.text((40, y + 10), ln, font=font(IT, 19, 600), fill=VOLT); y += 26
d.text((40, 780), "Rendered with verified sources - no invented data", font=font(IT, 16, 400), fill=GRAY)
img.save("assets/outro.png")

# filtergraph (see timeline.json for the timing derivation)
cards = [  # (input_idx, T0 main-local, dur)
    (3, 3.0, 6.0), (4, 11.5, 9.0), (5, 21.0, 4.6), (6, 25.8, 2.55),
]
lines = ["[0:v]fps=30,scale=474:850,format=rgba[base]"]
prev = "[base]"
for i, (idx, t0, dur) in enumerate(cards):
    lines.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d=0.30:alpha=1,"
                 f"fade=t=out:st={dur-0.3:.2f}:d=0.30:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[c{i}]")
    lines.append(f"{prev}[c{i}]overlay=x=30:y=36-212*max(0\\,1-(t-{t0})/0.35):eof_action=pass[v{i+1}]")
    prev = f"[v{i+1}]"
lines.append(f"{prev}ass='subs.ass',fade=t=in:st=0:d=0.4,fade=t=out:st=27.97:d=0.5,"
             "format=yuv420p,setsar=1[vmain]")
zp = ("scale=948:1700,zoompan=z='1+0.05*on/150':x='iw/2-(iw/zoom/2)':"
      "y='ih/2-(ih/zoom/2)':d=1:s=474x850:fps=30")
lines.append(f"[1:v]{zp},fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5,format=yuv420p,setsar=1[vintro]")
lines.append(f"[2:v]{zp},fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5,format=yuv420p,setsar=1[voutro]")
lines.append("[0:a]aresample=48000,aformat=channel_layouts=stereo[amain]")
for k, lbl in ((7, "aintro"), (8, "aoutro")):
    lines.append(f"[{k}:a]afade=t=in:st=0:d=1.2,afade=t=out:st=3.8:d=1.2,"
                 f"aresample=48000,aformat=channel_layouts=stereo[{lbl}]")
lines.append("[vintro][aintro][vmain][amain][voutro][aoutro]concat=n=3:v=1:a=1[v][a]")
open("graph.txt", "w").write(";\n".join(lines))

tone = "aevalsrc=0.09*sin(2*PI*98*t)+0.05*sin(2*PI*147*t):s=48000"
cmd = ["ffmpeg", "-y", "-loglevel", "warning", "-i", "src.mp4",
       "-loop", "1", "-t", "5", "-i", "assets/intro.png",
       "-loop", "1", "-t", "5", "-i", "assets/outro.png",
       "-loop", "1", "-t", "6.0", "-i", "assets/cardA.png",
       "-loop", "1", "-t", "9.0", "-i", "assets/cardB.png",
       "-loop", "1", "-t", "4.6", "-i", "assets/cardC.png",
       "-loop", "1", "-t", "2.6", "-i", "assets/cardD.png",
       "-f", "lavfi", "-t", "5", "-i", tone,
       "-f", "lavfi", "-t", "5", "-i", tone,
       "-filter_complex_script", "graph.txt", "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "final.mp4"]
subprocess.run(cmd, check=True)
print("final.mp4 built")
