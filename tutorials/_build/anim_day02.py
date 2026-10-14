"""Day 2 animation: nickname -> scp up -> scp down -> VNC desktop -> same network / remote-access service. Timed to the narration clips."""
import os, sys, subprocess, re
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, Ellipse

OUT = os.path.join(ROOT, "day02", "animations"); FIG = os.path.join(ROOT, "day02", "figures"); NARR = os.path.join(OUT, "narration")
FPS = 15; W, H = 160, 90
TITLES = ["1  A nickname for each Pi", "2  Laptop to Pi with scp", "3  Pi to laptop with scp", "4  The Pi desktop over VNC", "5  Same network, or a remote-access service"]
DUR = [12.12, 11.89, 9.87, 12.83, 9.95]
LEAD, PAD = 0.4, [1.2, 1.0, 1.0, 1.2, 2.0]
LEN = [LEAD + d + p for d, p in zip(DUR, PAD)]; START = [sum(LEN[:i]) for i in range(5)]; TOTAL = sum(LEN)
TEXTS = ["Typing a long SSH command every time is tedious. Give each Pi a short nickname in a small configuration file, and then you simply type SSH, followed by the nickname.",
         "To send a file from your laptop to the Pi, use SCP. Write the source first, then the destination: the user name, the Pi, a colon, and the folder on the Pi.",
         "To fetch a file from the Pi, swap the order. The file on the Pi comes first, then the folder on your laptop. A single dot means the current folder.",
         "For a full graphical desktop, enable VNC on the Pi, open a VNC viewer on your laptop, and sign in. You then see the Pi's desktop in a window, and you can use your mouse and keyboard on it.",
         "Remember: all of these need your laptop and the Pi to reach each other, either on the same network, or through a remote-access service when they are in different places."]
MONO = "DejaVu Sans Mono"
def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))
def rb(ax, x, y, w, h, fc, ec=None, r=1.2, lw=1.5, z=2, **kw): ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec or fc, lw=lw, zorder=z, **kw))
def typed(s, t, t0, cps=15): return s[:max(0, min(len(s), int((t - t0) * cps)))]
def txt(ax, x, y, s, size=10, **k): return ax.text(x, y, s, fontsize=size * 1.5, **k)

def laptop(ax, x, y, screen_fc="#F4F6F8"):
    rb(ax, x, y + 4, 52, 34, "#2D3748", r=2, z=3); ax.add_patch(Polygon([(x - 4, y + 4), (x + 56, y + 4), (x + 52, y), (x, y)], fc="#556", ec="none", zorder=3))
    rb(ax, x + 2.5, y + 6.5, 47, 29, screen_fc, r=0.8, z=4); return (x + 2.5, y + 6.5, 47, 29)
def pi(ax, x, y, powered=True):
    rb(ax, x, y, 40, 26, PCB, "#14532F", r=2, lw=2, z=2.5)
    for hx, hy in ((2.2, 2.2), (37.8, 2.2), (2.2, 23.8), (37.8, 23.8)): ax.add_patch(Circle((x + hx, y + hy), 1, fc="#0E3D22", ec="#C9D6CE", lw=1, zorder=3))
    rb(ax, x + 14, y + 8, 8, 8, "#B8BEC4", "#7C858D", r=0.5, z=3); rb(ax, x + 26, y + 3, 12, 9, "#C9CED3", "#8B949C", r=0.6, z=3); rb(ax, x + 26, y + 14, 12, 9, "#3C6FD1", "#264D99", r=0.6, z=3)
    ax.add_patch(Circle((x + 5, y + 7), 1, fc="#FF3B3B" if powered else "#5b2a2a", ec="none", zorder=4)); ax.add_patch(Circle((x + 5, y + 4), 1, fc="#3BFF6B" if powered else "#27472f", ec="none", zorder=4))
def fileicon(ax, x, y, name, col="#FFFFFF", z=7):
    ax.add_patch(Polygon([(x, y), (x + 8, y), (x + 8, y + 8), (x + 6, y + 10), (x, y + 10)], fc=col, ec="#333", lw=1.4, zorder=z)); txt(ax, x + 4, y - 2, name, 7, ha="center", va="top", family=MONO, zorder=z)
def foldericon(ax, x, y, name, z=5):
    ax.add_patch(Polygon([(x, y), (x + 12, y), (x + 12, y + 8), (x + 5, y + 8), (x + 4, y + 10), (x, y + 10)], fc="#F3C969", ec="#B07D00", lw=1.4, zorder=z)); txt(ax, x + 6, y - 2, name, 7, ha="center", va="top", family=MONO, zorder=z)
def cloud(ax, x, y, label="Internet", s=1.0):
    for dx, dy, w, h in ((0, 0, 20, 10), (8, 3, 16, 10), (-8, 2, 14, 8)): ax.add_patch(Ellipse((x + dx * s, y + dy * s), w * s, h * s, fc="#D8EBFB", ec="#2B6CB0", lw=1.3, zorder=2))
    txt(ax, x, y + 1, label, 8, ha="center", va="center", zorder=5)

def draw(ax, i, t):
    """i = scene index, t = seconds since scene start."""
    ax.clear(); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, fc="#F7F9FB", ec="none", zorder=0)); rb(ax, 0, 0, W, 10, NAVY, r=0, z=1)
    txt(ax, 4, 5, TITLES[i], 12.5, color="white", fontweight="bold", va="center", zorder=5)
    for k in range(5): ax.add_patch(Circle((W - 30 + k * 6, 5), 1.5, fc="white" if k == i else "#4C6485", ec="none", zorder=5))
    txt(ax, 4, 85, "Edge AI with the Raspberry Pi - Day 02", 8.5, color=GREY, va="center")
    f = t / LEN[i]
    if i == 0:
        sx, sy, sw, sh = laptop(ax, 8, 30, screen_fc="#0B1620"); pi(ax, 108, 34)
        txt(ax, sx + 2, sy + sh - 3, "PowerShell", 7, color="#7C8B99", va="center", zorder=6)
        # config card appears first
        a = seg(t, 0.4, 1.6)
        if a > 0.02:
            rb(ax, 62, 46, 50, 34, "#FFF8E1", AMBER, r=1.5, z=6, lw=2, alpha=a)
            txt(ax, 64.5, 76, "~/.ssh/config", 8.5, fontweight="bold", va="center", zorder=7, alpha=a)
            for k, l in enumerate(["Host lab", "  HostName raspi-lab.local", "  User piuser"]): txt(ax, 64.5, 70 - k * 5, l, 7.8, family=MONO, va="center", zorder=7, alpha=a)
        l1 = typed("PS C:\\> ssh lab", t, 5.5, 11); txt(ax, sx + 2, sy + 21, l1, 8.2, color="#E7EEF5", family=MONO, va="center", zorder=6)
        if t > 7.4: txt(ax, sx + 2, sy + 15, "Linux raspi-lab ... aarch64", 6.4, color="#9BB4CC", family=MONO, va="center", zorder=6); txt(ax, sx + 2, sy + 9.5, "piuser@raspi-lab:~ $" + (" _" if int(t * 2) % 2 == 0 else ""), 8.2, color="#7CE0A3", family=MONO, va="center", zorder=6)
        if t > 7.4:
            ax.plot([60, 106], [36, 44], color="#9AA5B1", lw=1.6, ls=(0, (4, 3)), zorder=1)
            for k in range(3): u = (t * 0.6 + k / 3) % 1; ax.add_patch(Circle((60 + 46 * u, 36 + 8 * u), 1.1, fc=GREEN, ec="none", zorder=6))
        txt(ax, 134, 30, "raspi-lab", 9, ha="center", va="center", fontweight="bold")
    elif i in (1, 2):
        sx, sy, sw, sh = laptop(ax, 8, 28, screen_fc="#EEF3F8"); pi(ax, 108, 27)
        foldericon(ax, sx + 4, sy + 6, "Documents"); txt(ax, 128, 22, "Pi: home folder  ~", 8.5, ha="center", va="center", fontweight="bold")
        foldericon(ax, 114, 62, "Documents", z=7) if False else None
        up = (i == 1); cmd = "scp file.txt piuser@raspi-lab.local:~/" if up else "scp piuser@raspi-lab.local:file.txt ."
        rb(ax, 30, 70, 100, 11, "#0F1C2B", NAVY, r=1.2, z=6); txt(ax, 33, 75.5, "PS C:\\> " + typed(cmd, t, 1.2, 15), 8.6, color="#E7EEF5", family=MONO, va="center", zorder=7)
        if up:
            fileicon(ax, sx + 22, sy + 8, "file.txt") if t < 5.0 else fileicon(ax, sx + 22, sy + 8, "file.txt", col="#EEE")
            mv = seg(t, 5.0, 8.0)
            if 5.0 <= t < 8.1:
                x = sx + 22 + (122 - sx - 22) * mv; y = sy + 8 + (59 - sy - 8) * mv + 10 * np.sin(np.pi * mv); fileicon(ax, x, y, "file.txt")
            if t >= 8.0: fileicon(ax, 122, 59, "file.txt", col="#DDF5DD"); txt(ax, 140, 63, "arrived!", 9, color=GREEN, ha="left", va="center", fontweight="bold")
            ax.annotate("", xy=(104, 60), xytext=(62, 60), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.2), zorder=3)
        else:
            fileicon(ax, 122, 59, "file.txt") if t < 4.2 else fileicon(ax, 122, 59, "file.txt", col="#EEE")
            mv = seg(t, 4.2, 7.2)
            if 4.2 <= t < 7.3:
                x = 122 + (sx + 22 - 122) * mv; y = 59 + (sy + 8 - 59) * mv + 10 * np.sin(np.pi * mv); fileicon(ax, x, y, "file.txt")
            if t >= 7.2: fileicon(ax, sx + 22, sy + 8, "file.txt", col="#DDF5DD"); txt(ax, sx + 25, sy + 25, "here, in my\nfolder (.)", 8, color=GREEN, ha="center", fontweight="bold")
            ax.annotate("", xy=(62, 60), xytext=(104, 60), arrowprops=dict(arrowstyle="-|>", color=RASP, lw=2.2), zorder=3)
    elif i == 3:
        sx, sy, sw, sh = laptop(ax, 8, 26, screen_fc="#EEF3F8"); pi(ax, 108, 30)
        a = seg(t, 3.5, 5.0)
        if a > 0.02:
            rb(ax, sx + 1, sy + 1, sw - 2, sh - 2, "#1E4F8F", r=0.8, z=5, alpha=a)
            ax.add_patch(Polygon([(sx + 18, sy + 8), (sx + 30, sy + 25), (sx + 42, sy + 8)], fc="#12335F", ec="none", zorder=6, alpha=a))
            rb(ax, sx + 1, sy + 1, sw - 2, 3.4, "#C9D6E8", r=0.3, z=6, alpha=a); ax.add_patch(Circle((sx + 4, sy + 2.7), 1.1, fc=RASP, ec="none", zorder=7, alpha=a))
            rb(ax, sx + 8, sy + 12, 24, 14, "white", "#334", r=0.6, z=7, alpha=a, lw=1); txt(ax, sx + 20, sy + 21, "Terminal", 6.5, ha="center", va="center", zorder=8, alpha=a); txt(ax, sx + 20, sy + 16.5, "$ htop", 6.5, ha="center", va="center", family=MONO, zorder=8, alpha=a)
            cx = sx + 14 + 20 * seg(t, 6.0, 9.0); cy = sy + 10 + 8 * seg(t, 6.0, 9.0)
            if t > 5.5: ax.add_patch(Polygon([(cx, cy), (cx, cy - 5), (cx + 1.6, cy - 3.6), (cx + 3.4, cy - 6.2), (cx + 4.4, cy - 5.6), (cx + 2.7, cy - 3.0), (cx + 4.6, cy - 2.6)], fc="white", ec="black", lw=1, zorder=9))
        else: txt(ax, sx + sw / 2, sy + sh / 2, "VNC Viewer", 12, ha="center", va="center", color=GREY, zorder=6)
        if t > 1.0:
            ax.annotate("", xy=(58, 52), xytext=(106, 52), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.2), zorder=3); txt(ax, 82, 56, "pictures of the Pi's screen", 8.5, color=GREEN, ha="center")
            ax.annotate("", xy=(106, 44), xytext=(58, 44), arrowprops=dict(arrowstyle="-|>", color=RASP, lw=2.2), zorder=3); txt(ax, 82, 39.5, "mouse + keyboard", 8.5, color=RASP, ha="center")
        txt(ax, 130, 26, "VNC server enabled", 8, ha="center", va="center", fontweight="bold"); txt(ax, 130, 22, "(raspi-config)", 7.5, ha="center", va="center", color=GREY)
    else:
        b = seg(t, 5.5, 7.0)
        rb(ax, 6, 24, 148, 56, "#FFFFFF", GREY, r=2, lw=1, z=1)
        rb(ax, 10, 28, 62, 46, "#F3F8F2", GREEN, r=2, lw=2, z=2, ls=(0, (5, 3))); txt(ax, 13, 70, "one network", 9, color=GREEN, fontweight="bold", va="center")
        ax.add_patch(Rectangle((20, 40), 14, 10, fc="#CFE8FB", ec=NAVY, lw=1.6, zorder=4)); txt(ax, 27, 36, "Laptop", 8, ha="center", fontweight="bold")
        rb(ax, 46, 40, 20, 12, PCB, "#14532F", r=1, z=4); txt(ax, 56, 36, "Pi", 8, ha="center", fontweight="bold")
        ax.annotate("", xy=(45, 46), xytext=(35, 46), arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=2), zorder=5); txt(ax, 40, 54, "works", 8, color=GREEN, ha="center")
        if b > 0.02:
            rb(ax, 84, 28, 66, 46, "#FFF5F5", RASP, r=2, lw=2, z=2, ls=(0, (5, 3)), alpha=b); txt(ax, 87, 70, "another place", 9, color=RASP, fontweight="bold", va="center", alpha=b)
            rb(ax, 112, 40, 22, 12, "#CFE8FB", NAVY, r=1, z=4, alpha=b); txt(ax, 123, 36, "Laptop", 8, ha="center", fontweight="bold", alpha=b)
            if t > 7.0:
                rb(ax, 52, 13, 50, 8, "#FFF4DB", AMBER, r=1.2, z=6, lw=2); txt(ax, 77, 17, "remote-access service", 8.5, ha="center", va="center", fontweight="bold", zorder=7)
                ax.annotate("", xy=(70, 22), xytext=(58, 38), arrowprops=dict(arrowstyle="<|-|>", color=AMBER, lw=2), zorder=5); ax.annotate("", xy=(86, 22), xytext=(116, 38), arrowprops=dict(arrowstyle="<|-|>", color=AMBER, lw=2), zorder=5)
            else:
                txt(ax, 78, 50, "?", 40, color=RASP, ha="center", va="center", fontweight="bold")

def render():
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); n = int(TOTAL * FPS)
    mp4 = os.path.join(OUT, "Day02_silent.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", "1280x720", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", mp4], stdin=subprocess.PIPE)
    keys = {}
    for k in range(n):
        T = k / FPS; i = max(j for j in range(5) if T >= START[j] - 1e-9); t = T - START[i]
        draw(ax, i, t); fig.canvas.draw(); buf = np.asarray(fig.canvas.buffer_rgba()); p.stdin.write(buf.tobytes())
        if t <= LEN[i] - 0.6: keys[i] = buf.copy()
    p.stdin.close(); p.wait(); plt.close(fig); return mp4, keys

def srt_time(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000); return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

if __name__ == "__main__":
    silent, keys = render()
    srt, n = [], 1
    for i, tx in enumerate(TEXTS):
        sents = re.split(r"(?<=[.:;])\s+", tx); tot = sum(len(x) for x in sents); t0 = START[i] + LEAD
        for sn in sents: d = DUR[i] * len(sn) / tot; srt.append(f"{n}\n{srt_time(t0)} --> {srt_time(t0 + d)}\n{sn}\n"); n += 1; t0 += d
    srtp = os.path.join(OUT, "Day02_remote_access_and_files.en.srt"); open(srtp, "w").write("\n".join(srt))
    mp4 = os.path.join(OUT, "Day02_remote_access_and_files.mp4"); ins, fl, labs = [], [], []
    for i in range(5):
        ins += ["-i", os.path.join(NARR, f"s{i+1}.mp3")]; ms = int((START[i] + LEAD) * 1000); fl.append(f"[{i+1}:a]adelay={ms}|{ms}[a{i}]"); labs.append(f"[a{i}]")
    fc = ";".join(fl) + ";" + "".join(labs) + "amix=inputs=5:normalize=0,apad[aout]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, *ins, "-i", srtp, "-filter_complex", fc, "-map", "0:v", "-map", "[aout]", "-map", "6:s", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-t", f"{TOTAL:.2f}", mp4], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-vf", "fps=8,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", os.path.join(OUT, "Day02_remote_access_and_files.gif")], check=True)
    os.replace(silent, os.path.join(OUT, "Day02_remote_access_and_files_silent.mp4"))
    from PIL import Image
    for i in range(5): Image.fromarray(keys[i]).convert("RGB").save(os.path.join(FIG, f"d2_anim_f{i+1}.png"))
    print("anim done; %.1fs" % TOTAL)
