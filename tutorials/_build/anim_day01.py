"""Day 1 animation: write the card -> insert -> power on -> Wi-Fi -> SSH.  Output: MP4 (1280x720) + GIF + filmstrip."""
import os, sys, subprocess, math, random
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, Arc

OUT = os.path.join(ROOT, "day01", "animations")
FIG = os.path.join(ROOT, "day01", "figures")
os.makedirs(OUT, exist_ok=True)
FPS = 15
SCENES = [(0, 6, "1  Write the OS image to the microSD card"),
          (6, 10, "2  Put the card into the Pi"),
          (10, 16, "3  Plug in power: first boot"),
          (16, 20, "4  The Pi joins your Wi-Fi"),
          (20, 27, "5  Connect from the laptop with SSH")]
NARR = os.path.join(ROOT, "day01", "animations", "narration")
NARR_DUR = [14.03, 3.97, 13.87, 5.64, 24.61]          # measured with ffprobe
PAD = [1.2, 1.0, 1.2, 1.0, 2.0]                        # silence after each clip
LEAD = 0.4                                              # silence before each clip
OUT_LEN = [LEAD + d + p for d, p in zip(NARR_DUR, PAD)]
OUT_START = [sum(OUT_LEN[:i]) for i in range(len(OUT_LEN))]
ORIG_END = [b for (_, b, _) in SCENES]; ORIG_END[-1] = 28.5   # last scene keeps its 1.5 s tail
TOTAL = sum(OUT_LEN)
TOUT = 0.0
def warp(t):
    for i, L in enumerate(OUT_LEN):
        if t < OUT_START[i] + L or i == len(OUT_LEN) - 1:
            a = SCENES[i][0]; b = ORIG_END[i]
            return a + min(max((t - OUT_START[i]) / L, 0.0), 1.0) * (b - a)
W, H = 160, 90
rnd = random.Random(4)
flick = [rnd.random() for _ in range(2000)]

def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))
def rb(ax, x, y, w, h, fc, ec=None, r=1.2, lw=1.5, z=2, **kw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec or fc, lw=lw, zorder=z, **kw))
def typed(s, t, t0, cps=14): return s[:max(0, min(len(s), int((t - t0) * cps)))]

def draw(ax, t):
    T = lambda *a, **k: ax.text(*a, **{**k, 'fontsize': k.get('fontsize', 10) * 1.5})
    ax.clear(); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    scene = max(i for i, (a, b, _) in enumerate(SCENES) if t >= a) if t >= 0 else 0
    # ---- background + caption bar
    ax.add_patch(Rectangle((0, 0), W, H, fc="#F7F9FB", ec="none", zorder=0))
    rb(ax, 0, 0, W, 10, NAVY, r=0, z=1)
    T(4, 5, SCENES[scene][2], color="white", fontsize=12.5, fontweight="bold", va="center", zorder=5)
    for i in range(len(SCENES)):
        ax.add_patch(Circle((W - 30 + i * 6, 5), 1.5, fc=("white" if i == scene else "#4C6485"), ec="none", zorder=5))
    # ---- laptop
    rb(ax, 6, 31, 56, 38, "#2D3748", r=2, z=3)
    ax.add_patch(Polygon([(2, 31), (66, 31), (62, 26), (6, 26)], fc="#556", ec="none", zorder=3))
    sc_x, sc_y, sc_w, sc_h = 8.5, 34, 51, 32
    term = t >= 20
    rb(ax, sc_x, sc_y, sc_w, sc_h, "#0B1620" if term else "#F4F6F8", r=0.8, z=4)
    if not term:
        T(sc_x + 2, sc_y + sc_h - 3, "Raspberry Pi Imager", fontsize=8, fontweight="bold", color=RASP, va="center", zorder=5)
        prog = seg(t, 0.8, 5.2) if t < 6 else 1.0
        rb(ax, sc_x + 3, sc_y + 13, sc_w - 6, 4, "#D9DEE4", r=0.8, z=5)
        if prog > 0.01: rb(ax, sc_x + 3, sc_y + 13, (sc_w - 6) * prog, 4, RASP, r=0.8, z=6)
        lab = "Writing...  %d%%" % int(prog * 100) if prog < 1 else "Write successful - safe to remove"
        T(sc_x + 3, sc_y + 20, lab, fontsize=9, color=INK, va="center", zorder=6)
        T(sc_x + 3, sc_y + 8, "OS: Raspberry Pi OS (64-bit)\nhostname: raspi4   Wi-Fi: set   SSH: on", fontsize=6.6, color=GREY, va="top", zorder=6, linespacing=1.4)
    else:
        mono = dict(family="DejaVu Sans Mono", fontsize=8.2, va="center", zorder=6)
        T(sc_x + 2, sc_y + sc_h - 3, "PowerShell", fontsize=7.5, color="#7C8B99", va="center", zorder=6)
        l1 = typed("PS C:\\> ssh user@raspi4.local", t, 20.4, 16)
        T(sc_x + 2, sc_y + 23, l1, color="#E7EEF5", **mono)
        if t > 22.0: T(sc_x + 2, sc_y + 18, "password: " + "*" * min(8, int((t - 22.0) * 6)), color="#E7EEF5", **mono)
        if t > 23.6:
            T(sc_x + 2, sc_y + 12.5, "Linux raspi4 ... aarch64", color="#9BB4CC", **{**mono, "fontsize": 6.8})
            T(sc_x + 2, sc_y + 7.5, "user@raspi4:~ $" + (" _" if int(TOUT * 2) % 2 == 0 else ""), color="#7CE0A3", **mono)
        if t > 25.0: T(sc_x + 2, sc_y + 3, "hostname -I  ->  192.168.1.57", color="#E7EEF5", **{**mono, "fontsize": 6.6})
    # ---- router
    rb(ax, 120, 66, 30, 9, "#4A5568", r=1.2, z=3)
    ax.plot([124, 122], [75, 82], color="#4A5568", lw=3, zorder=3); ax.plot([146, 148], [75, 82], color="#4A5568", lw=3, zorder=3)
    T(135, 70.5, "Wi-Fi router", color="white", fontsize=9, ha="center", va="center", zorder=4)
    # ---- Pi board
    px, py, pw, ph = 98, 22, 46, 30
    # sd card position
    reader = (66, 44)
    slot = (px - 2, py + ph / 2 - 3.2)
    if t < 6: sd = (reader[0] + 3, reader[1]); sd_vis = 1.0
    elif t < 10:
        k = seg(t, 6.6, 9.0); sd = (reader[0] + 3 + (slot[0] + 4 - reader[0] - 3) * k, reader[1] + (slot[1] - reader[1]) * k)
    else: sd = (slot[0] + 4, slot[1])
    sd_into_board = t >= 9.0
    sd_z = 1.5 if sd_into_board else 6
    # reader
    if t < 9:
        rb(ax, 62.5, 40, 12, 12, "#5C6B7A", r=1, z=3)
        T(68.5, 38, "reader", fontsize=7, color=GREY, ha="center", va="top")
    # card
    sdw, sdh = 8, 11
    ax.add_patch(Polygon([(sd[0] - sdw / 2, sd[1] - sdh / 2 + 3), (sd[0] + sdw / 2, sd[1] - sdh / 2 + 3), (sd[0] + sdw / 2, sd[1] + sdh / 2 + 3),
                          (sd[0] - sdw / 2 + 2, sd[1] + sdh / 2 + 3), (sd[0] - sdw / 2, sd[1] + sdh / 2 - 0.5 + 3)], fc=NAVY, ec="none", zorder=sd_z))
    # flow of data blocks laptop -> card (scene 1)
    fillp = seg(t, 0.8, 5.2) if t < 6 else 1.0
    for i in range(4):
        for j in range(5):
            on = (i * 5 + j) / 20.0 < fillp
            ax.add_patch(Rectangle((sd[0] - 2.8 + i * 1.5, sd[1] - 3.2 + 3 + j * 1.8), 1.0, 1.1, fc=("#F3C969" if on else "#27406A"), ec="none", zorder=sd_z + 0.1))
    if 0.8 < t < 5.4:
        for k in range(5):
            ph_ = ((t * 1.6 + k / 5.0) % 1.0)
            ax.add_patch(Rectangle((60 + ph_ * 10, 46.5 - 0.1), 1.6, 1.6, fc=RASP, ec="none", zorder=6, alpha=0.9))
    # board
    rb(ax, px, py, pw, ph, PCB, "#14532F", r=2, lw=2, z=2.5)
    for hx, hy in [(px + 2.5, py + 2.5), (px + pw - 2.5, py + 2.5), (px + 2.5, py + ph - 2.5), (px + pw - 2.5, py + ph - 2.5)]:
        ax.add_patch(Circle((hx, hy), 1.0, fc="#0E3D22", ec="#C9D6CE", lw=1, zorder=3))
    rb(ax, px + 5, py + ph - 5.2, 28, 3.2, "#2B2B2B", r=0.3, z=3)
    rb(ax, px + 16, py + 10, 8, 8, "#B8BEC4", "#7C858D", r=0.5, z=3)
    T(px + 20, py + 14, "CPU", fontsize=6.5, ha="center", va="center", fontweight="bold", zorder=4, color="#2B3138")
    rb(ax, px + pw - 13, py + 3, 13, 9, "#C9CED3", "#8B949C", r=0.6, z=3)
    rb(ax, px + pw - 13, py + 14, 13, 9, "#3C6FD1", "#264D99", r=0.6, z=3)
    T(px + pw / 2, py - 2.2, "Raspberry Pi 4", fontsize=9, ha="center", va="top", color=NAVY, fontweight="bold")
    # USB-C and plug (scene 3)
    uc = (px + 8, py - 0.6)
    rb(ax, uc[0] - 3, uc[1] - 0.2, 6, 2.2, "#C9CED3", "#8B949C", r=0.4, z=3)
    if t >= 10:
        k = seg(t, 10.2, 11.5)
        yy = uc[1] - 9 + 9 * k
        ax.plot([uc[0], uc[0]], [yy - 9, yy], color="#2B2B2B", lw=4, zorder=2)
        rb(ax, uc[0] - 2.2, yy - 1.4, 4.4, 3.2, "#2B2B2B", r=0.4, z=3.2)
    # LEDs
    powered = t >= 11.4
    red_on = powered
    green_on = powered and (t < 15.2 and flick[int(TOUT * FPS) % len(flick)] > 0.35 or (t >= 15.2 and flick[int(TOUT * FPS) % len(flick)] > 0.85))
    ax.add_patch(Circle((px + 6, py + 8.2), 1.0, fc=("#FF3B3B" if red_on else "#5b2a2a"), ec="none", zorder=4))
    ax.add_patch(Circle((px + 6, py + 5.2), 1.0, fc=("#3BFF6B" if green_on else "#27472f"), ec="none", zorder=4))
    if powered:
        T(px + 8.2, py + 8.2, "power", fontsize=6.3, color="white", va="center", zorder=4)
        T(px + 8.2, py + 5.2, "activity", fontsize=6.3, color="white", va="center", zorder=4)
    # boot checklist (scene 3)
    if 10 <= t < 16:
        items = ["resizing the card's file system", "applying hostname, user, Wi-Fi", "starting the SSH service"]
        rb(ax, 70, 60, 46, 22, "white", "#D9DEE4", r=1.5, z=4)
        T(73, 78, "First boot (1-3 minutes)", fontsize=9, fontweight="bold", color=AMBER, va="center", zorder=5)
        for i, it in enumerate(items):
            t0 = 12.0 + i * 1.3
            if t > t0:
                done = t > t0 + 1.2
                T(73, 72 - i * 5, ("v " if done else ". ") + it, fontsize=7.8, color=(GREEN if done else INK), va="center", zorder=5)
    # Wi-Fi (scene 4+)
    if t >= 16:
        for i in range(3):
            a = seg(t, 16.2 + i * 0.6, 17.2 + i * 0.6)
            if a > 0:
                r_ = 8 + i * 8
                ax.add_patch(Arc((px + 34, py + ph - 3), 2 * r_, 2 * r_, theta1=30, theta2=90, color=RASP, lw=3.2, alpha=min(1, a), zorder=2, capstyle="round"))
        if t > 18.2:
            rb(ax, 70, 76, 46, 10, "white", "#D9DEE4", r=1.2, z=4)
            T(93, 83, "joined your Wi-Fi", fontsize=8.5, color=GREEN, fontweight="bold", ha="center", va="center", zorder=5)
            T(93, 79, "name: raspi4.local   IP: 192.168.1.57", fontsize=7.2, color=INK, ha="center", va="center", zorder=5)
    # SSH link (scene 5)
    if t >= 20.2:
        xs = np.linspace(62, 120, 40)
        pts = [(62, 52), (90, 58), (120, 66)]
        ax.plot([62, 120], [48, 66], color="#9AA5B1", lw=1.6, ls=(0, (4, 3)), zorder=1)
        ax.plot([120, 98], [66, 48], color="#9AA5B1", lw=1.6, ls=(0, (4, 3)), zorder=1)
        for k in range(4):
            f = (TOUT * 0.7 + k / 4.0) % 1.0
            ax.add_patch(Circle((62 + 58 * f, 48 + 18 * f), 1.1, fc=GREEN, ec="none", zorder=6))
            f2 = (TOUT * 0.7 + k / 4.0 + 0.5) % 1.0
            ax.add_patch(Circle((120 - 22 * f2, 66 - 18 * f2), 1.1, fc=NAVY, ec="none", zorder=6))
        T(88, 56, "encrypted SSH tunnel", fontsize=8.2, color=GREEN, fontweight="bold", ha="center", zorder=7, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=GREEN, lw=1))
    # title top-left
    T(4, 85, "Edge AI with the Raspberry Pi - Day 01", fontsize=8.5, color=GREY, va="center")

def render(path_mp4):
    global TOUT
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100); ax = fig.add_axes([0, 0, 1, 1])
    n = int(TOTAL * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", "1280x720", "-r", str(FPS), "-i", "-",
           "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", path_mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    targets = (5.5, 9.4, 14.5, 18.8, 25.8); best = {k: (9e9, None) for k in targets}
    for i in range(n):
        TOUT = i / FPS; t = warp(TOUT)
        draw(ax, t); fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())
        p.stdin.write(buf.tobytes())
        for kt in targets:
            d = abs(t - kt)
            if d < best[kt][0]: best[kt] = (d, buf.copy())
    p.stdin.close(); p.wait(); plt.close(fig)
    return {k: v[1] for k, v in best.items()}

def srt_time(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

TEXTS = [
    "First, we write the operating system onto the microSD card. Raspberry Pi Imager copies a ready-to-run system onto the card, together with your settings: the computer name, your user, your Wi-Fi, and SSH.",
    "Next, we slide the card into the slot under the Raspberry Pi.",
    "Now plug in the power. The red light stays on, and the green light flickers while the Pi reads the card. The first boot takes a few minutes: the Pi resizes the file system and applies your settings. Do not unplug it.",
    "Then the Pi joins your Wi-Fi network by itself, and receives its own address on the network.",
    "Finally, on your laptop, open PowerShell and type ssh, your user name, at raspi4.local. Type yes the first time, then your password. Nothing appears while you type; that is normal. When you see the Pi's prompt, you are inside the Pi. Check its address with the hostname command. And remember: always shut down properly before you unplug it.",
]

if __name__ == "__main__":
    silent = os.path.join(OUT, "Day01_flash_boot_ssh_silent.mp4")
    key = render(silent)
    # subtitles: split each scene text into sentences, share the clip time by character count
    import re
    srt, n = [], 1
    for i, txt in enumerate(TEXTS):
        sents = re.split(r"(?<=[.:;])\s+", txt); tot = sum(len(x) for x in sents); t0 = OUT_START[i] + LEAD
        for sn in sents:
            d = NARR_DUR[i] * len(sn) / tot
            srt.append(f"{n}\n{srt_time(t0)} --> {srt_time(t0 + d)}\n{sn}\n"); n += 1; t0 += d
    srt_path = os.path.join(OUT, "Day01_flash_boot_ssh.en.srt"); open(srt_path, "w").write("\n".join(srt))
    # audio track: each clip delayed to its scene start
    mp4 = os.path.join(OUT, "Day01_flash_boot_ssh.mp4")
    ins, fl, labs = [], [], []
    for i in range(5):
        ins += ["-i", os.path.join(NARR, f"s{i+1}.mp3")]
        ms = int((OUT_START[i] + LEAD) * 1000); fl.append(f"[{i+1}:a]adelay={ms}|{ms}[a{i}]"); labs.append(f"[a{i}]")
    fc = ";".join(fl) + ";" + "".join(labs) + "amix=inputs=5:normalize=0,apad[aout]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, *ins, "-i", srt_path, "-filter_complex", fc,
                    "-map", "0:v", "-map", "[aout]", "-map", "6:s", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-c:s", "mov_text",
                    "-metadata:s:s:0", "language=eng", "-t", f"{TOTAL:.2f}", mp4], check=True)
    gif = os.path.join(OUT, "Day01_flash_boot_ssh.gif")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-vf", "fps=8,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", gif], check=True)
    from PIL import Image
    for i, k in enumerate(sorted(key)): Image.fromarray(key[k]).convert("RGB").save(os.path.join(FIG, f"d1_anim_f{i+1}.png"))
    print("anim done; total %.1fs" % TOTAL)
