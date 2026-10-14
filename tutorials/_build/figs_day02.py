import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, Ellipse, FancyArrowPatch
OUT = os.path.join(ROOT, "day02", "figures"); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": SANS, "savefig.dpi": 300})
MONO = "DejaVu Sans Mono"

def newax(w, h, xl, yl):
    fig = plt.figure(figsize=(w, h)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, xl); ax.set_ylim(0, yl); ax.axis("off"); return fig, ax
def rbox(ax, x, y, w, h, fc, ec=None, r=1.0, lw=1.4, z=2, **kw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec or fc, lw=lw, zorder=z, **kw))
def arrow(ax, a, b, color=GREY, lw=2, ms=14, rad=0.0, z=3, style="-|>"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=ms, lw=lw, color=color, connectionstyle=f"arc3,rad={rad}", zorder=z))
def laptop(ax, x, y, label="Laptop", col=NAVY_L, ec=NAVY):
    rbox(ax, x, y + 3, 18, 12, col, ec, r=1); rbox(ax, x + 1.6, y + 4.4, 14.8, 9, "#CFE8FB", ec, r=0.5, lw=0.8, z=3)
    ax.add_patch(Polygon([(x - 2, y + 3), (x + 20, y + 3), (x + 18.5, y), (x - 0.5, y)], fc="#8896A8", ec=ec, lw=1, zorder=2))
    ax.text(x + 9, y - 2.8, label, ha="center", fontsize=8.8, fontweight="bold", color=INK)
def pi(ax, x, y, label="Raspberry Pi", w=16):
    rbox(ax, x, y, w, 10.5, "#1E7B4A", "#14532F", r=1.2, lw=1.4)
    for dx, dy in ((1.2, 1.2), (w - 1.2, 1.2), (1.2, 9.3), (w - 1.2, 9.3)): ax.add_patch(Circle((x + dx, y + dy), 0.55, fc="#CFE", ec="none", zorder=4))
    rbox(ax, x + 4.5, y + 3, 5, 4.5, "#B8BEC4", "#7C858D", r=0.4, z=4)
    ax.text(x + w / 2, y - 2.8, label, ha="center", fontsize=8.8, fontweight="bold", color=INK)
def term(ax, x, y, w, h, lines, title="", fs=7.8):
    rbox(ax, x, y, w, h, "#0F1C2B", NAVY, r=1, lw=1.2)
    if title: ax.text(x + 1.4, y + h - 2.2, title, color="#9BB4CC", fontsize=6.8, va="center")
    for i, (t, c) in enumerate(lines): ax.text(x + 1.6, y + h - 5.8 - i * 3.5, t, color=c, fontsize=fs, family=MONO, va="center")
W_, G_, D_ = "#E7EEF5", "#7CE0A3", "#8DA0B5"

def fig_roadmap():
    fig, ax = newax(7.2, 2.5, 126, 42); ax.set_xlim(-3, 123)
    segs = [("A", "Review and\nplan", 10, NAVY), ("B", "Smarter SSH", 25, "#7A4FA0"), ("C", "Moving files", 25, RASP), ("D", "Remote\ndesktop", 25, "#2B6CB0"), ("E", "More than one\nnetwork", 20, AMBER), ("F", "Security and\nwrap-up", 15, GREEN)]
    t = 0
    for k, name, m, c in segs:
        rbox(ax, t + 0.6, 17, m - 1.2, 13, c, r=1.5)
        ax.text(t + m / 2, 25.5, k, ha="center", va="center", color="white", fontsize=17, fontweight="bold"); ax.text(t + m / 2, 20.2, f"{m} min", ha="center", va="center", color="white", fontsize=9)
        ax.text(t + m / 2, 13.2, name, ha="center", va="top", color=INK, fontsize=8.6, linespacing=1.1); t += m
    ax.plot([0, 120], [36, 36], color=GREY, lw=1.2)
    for x in (0, 10, 35, 60, 85, 105, 120): ax.plot([x, x], [35, 37], color=GREY, lw=1.2); ax.text(x, 39.8, f"{x//60}:{x%60:02d}", ha="center", fontsize=8.5, color=GREY)
    fig.savefig(f"{OUT}/d2_roadmap.png", pad_inches=0); plt.close(fig)

def fig_sshconfig():
    fig, ax = newax(7.2, 2.9, 120, 48)
    term(ax, 2, 20, 46, 24, [("PS C:\\> ssh piuser@192.168.1.57", W_), ("# long, easy to mistype", D_), ("", W_), ("PS C:\\> ssh lab", G_), ("# short; same result", D_)], "Without and with a nickname")
    rbox(ax, 56, 4, 62, 40, "#FFF8E1", AMBER, r=1.2, lw=1.4); ax.text(59, 40, "the file  C:\\Users\\you\\.ssh\\config", fontsize=8.6, fontweight="bold", va="center")
    cfg = ["Host lab", "    HostName raspi-lab.local", "    User piuser", "", "Host home", "    HostName raspi-home.local", "    User piuser"]
    for i, l in enumerate(cfg): ax.text(60, 34 - i * 3.9, l, fontsize=8.2, family=MONO, va="center", color=INK)
    arrow(ax, (50, 28), (55, 28), color=AMBER, lw=2)
    ax.text(2, 12, "Each 'Host' block gives a nickname to a Pi:\nwhere it is (HostName) and who you are (User).\nThen ssh, scp and SFTP all accept the nickname.", fontsize=8.6, va="center", linespacing=1.35, color=INK)
    fig.savefig(f"{OUT}/d2_sshconfig.png", pad_inches=0); plt.close(fig)

def fig_keys():
    fig, ax = newax(7.2, 3.3, 120, 55)
    laptop(ax, 6, 22); pi(ax, 92, 24)
    rbox(ax, 2, 40, 30, 12, "#E3EAF4", NAVY, r=1); ax.text(17, 48, "private key", ha="center", fontsize=9, fontweight="bold"); ax.text(17, 43.6, "id_ed25519  (secret,\nnever leaves the laptop)", ha="center", fontsize=7.2, va="center", linespacing=1.2)
    rbox(ax, 86, 40, 32, 12, "#FFF4DB", AMBER, r=1); ax.text(102, 48, "public key", ha="center", fontsize=9, fontweight="bold"); ax.text(102, 43.6, "~/.ssh/authorized_keys\n(safe to share)", ha="center", fontsize=7.2, va="center", linespacing=1.2)
    arrow(ax, (40, 30), (90, 30), color=GREEN, lw=2); ax.text(65, 33, "1  'I am the owner of this key pair'", ha="center", fontsize=8, color=GREEN)
    arrow(ax, (90, 25), (40, 25), color=NAVY, lw=2); ax.text(65, 21.2, "2  Pi sends a random challenge", ha="center", fontsize=8, color=NAVY)
    arrow(ax, (40, 20), (90, 20), color=RASP, lw=2); ax.text(65, 15.6, "3  laptop signs it with the private key; Pi checks with the public key: access, no password", ha="center", fontsize=7.4, color=RASP)
    ax.text(60, 5.5, "Keys prove who you are without sending a secret over the network.", ha="center", fontsize=8.6, color=GREY, style="italic")
    fig.savefig(f"{OUT}/d2_keys.png", pad_inches=0); plt.close(fig)

def fig_scp():
    fig, ax = newax(7.2, 3.4, 120, 57)
    laptop(ax, 4, 26); pi(ax, 98, 28)
    rbox(ax, 30, 37, 60, 12, "#E3F4DC", GREEN, r=1); ax.text(60, 45.2, "laptop  ->  Pi", ha="center", fontsize=9, fontweight="bold", color=GREEN)
    ax.text(60, 40.2, "scp  file.txt  piuser@raspi-lab.local:~/", ha="center", fontsize=7.8, family=MONO)
    arrow(ax, (26, 53), (96, 53), color=GREEN, lw=2.2)
    rbox(ax, 30, 19, 60, 12, "#FBE3EA", RASP, r=1); ax.text(60, 27.2, "Pi  ->  laptop", ha="center", fontsize=9, fontweight="bold", color=RASP)
    ax.text(60, 22.2, "scp  piuser@raspi-lab.local:file.txt  .", ha="center", fontsize=7.8, family=MONO)
    arrow(ax, (96, 15.5), (26, 15.5), color=RASP, lw=2.2)
    for x, t, c, d in ((2, "scp", NAVY, "the copy program"), (20, "SOURCE", GREEN, "what to copy"), (44, "DESTINATION", RASP, "where it goes")):
        ax.text(x, 9, t, fontsize=9.5, fontweight="bold", color=c, va="center"); ax.text(x, 5.2, d, fontsize=7.6, color=GREY, va="center")
    ax.text(118, 7, "user@host:path  means 'on the Pi'.\nNo 'user@host:' means 'on this computer'.", ha="right", fontsize=7.8, va="center", linespacing=1.3, color=INK)
    fig.savefig(f"{OUT}/d2_scp.png", pad_inches=0); plt.close(fig)

def fig_sftp():
    fig, ax = newax(7.2, 3.2, 120, 53)
    rbox(ax, 2, 4, 116, 46, "#F7F9FB", GREY, r=1.2, lw=1.2); rbox(ax, 2, 44, 116, 6, "#DDE3EA", GREY, r=1.2); ax.text(5, 47, "SFTP program (FileZilla / WinSCP): two panes", fontsize=8.6, va="center", fontweight="bold")
    rbox(ax, 4, 38, 82, 4.5, "white", GREY, r=0.5, lw=0.8); ax.text(6, 40.2, "Host: sftp://raspi-lab.local    User: piuser    Password: ********    Port: 22", fontsize=7.4, va="center", family=MONO)
    rbox(ax, 88, 38, 28, 4.5, "#2B6CB0", "#2B6CB0", r=0.5); ax.text(102, 40.2, "Quickconnect", color="white", ha="center", fontsize=7.6, va="center")
    for x0, title, items, c in ((4, "Local site (your laptop)", ["Documents/", "Downloads/", "photos.zip", "model.tflite"], NAVY), (62, "Remote site (the Pi)", ["Documents/", "images/", "test.jpg", "notes.txt"], GREEN)):
        rbox(ax, x0, 7, 54, 28, "white", c, r=0.8, lw=1.2); rbox(ax, x0, 31, 54, 4, c, c, r=0.5); ax.text(x0 + 2, 33, title, color="white", fontsize=7.8, va="center", fontweight="bold")
        for i, t in enumerate(items): ax.text(x0 + 3, 27 - i * 5, ("[folder] " if t.endswith("/") else "[file]    ") + t, fontsize=7.6, va="center", family=MONO)
    arrow(ax, (55.5, 22), (62.5, 22), color=GREEN, lw=2); arrow(ax, (62.5, 16), (55.5, 16), color=RASP, lw=2)
    ax.text(59, 2, "drag and drop between the panes", ha="center", fontsize=7.4, color=GREY)
    fig.savefig(f"{OUT}/d2_sftp.png", pad_inches=0); plt.close(fig)

def fig_vnc():
    fig, ax = newax(7.2, 3.0, 120, 50)
    laptop(ax, 4, 22); pi(ax, 98, 24)
    rbox(ax, 8, 28, 10, 7, "#BFDDF5", NAVY, r=0.4, z=4, lw=0.6); ax.text(13, 31.5, "Pi\ndesktop", ha="center", va="center", fontsize=5.8, zorder=5)
    arrow(ax, (96, 36), (36, 36), color=GREEN, lw=2.2); ax.text(66, 39.4, "pictures of the Pi's screen", ha="center", fontsize=8.4, color=GREEN)
    arrow(ax, (36, 28), (96, 28), color=RASP, lw=2.2); ax.text(66, 24.4, "your mouse clicks and key presses", ha="center", fontsize=8.4, color=RASP)
    ax.text(66, 46, "VNC = Virtual Network Computing: remote control of a graphical desktop", ha="center", fontsize=9, fontweight="bold", color=INK)
    ax.text(60, 8, "SSH carries text only (a command line).  VNC carries the whole desktop picture, so it needs more bandwidth and more Pi resources.", ha="center", fontsize=8, color=GREY, style="italic", wrap=True)
    fig.savefig(f"{OUT}/d2_vnc.png", pad_inches=0); plt.close(fig)

def fig_twonets():
    fig, ax = newax(7.2, 3.6, 120, 60)
    rbox(ax, 1, 4, 36, 52, "#F3F8F2", GREEN, r=1.5, lw=1.3, ls=(0, (5, 3))); ax.text(4, 52.5, "Network A (e.g. lab)", fontsize=8.8, color=GREEN, fontweight="bold")
    rbox(ax, 83, 4, 36, 52, "#FFF5F5", RASP, r=1.5, lw=1.3, ls=(0, (5, 3))); ax.text(86, 52.5, "Network B (e.g. home)", fontsize=8.8, color=RASP, fontweight="bold")
    pi(ax, 12, 22, "Pi in the lab"); laptop(ax, 92, 22, "Laptop at home")
    for dx, dy, w, h in ((60, 40, 22, 11), (70, 44, 18, 10), (50, 44, 16, 9)): ax.add_patch(Ellipse((dx, dy), w, h, fc="#D8EBFB", ec="#2B6CB0", lw=1.2, zorder=2))
    ax.text(60, 43, "Internet", ha="center", fontsize=9, zorder=4)
    arrow(ax, (30, 33), (48, 40), color=GREY, lw=1.6); arrow(ax, (70, 38), (92, 33), color=GREY, lw=1.6)
    ax.plot([34, 91], [20, 20], color=RASP, lw=1.6, ls=(0, (3, 3))); ax.text(60, 22.6, "raspi-lab.local does NOT work here", ha="center", fontsize=7.8, color=RASP)
    rbox(ax, 40, 6, 40, 10, "#FFF4DB", AMBER, r=1, lw=1.2); ax.text(60, 12.5, "remote-access service", ha="center", fontsize=8.6, fontweight="bold"); ax.text(60, 8.5, "(a virtual network or a relay)", ha="center", fontsize=7.4)
    arrow(ax, (30, 20), (41, 12), color=AMBER, lw=1.6); arrow(ax, (79, 12), (92, 20), color=AMBER, lw=1.6)
    fig.savefig(f"{OUT}/d2_twonets.png", pad_inches=0); plt.close(fig)

def fig_decision():
    fig, ax = newax(7.2, 3.3, 120, 55)
    def box(x, y, w, h, t, fc, ec, fs=8.2): rbox(ax, x, y, w, h, fc, ec, r=1.2); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, linespacing=1.2)
    box(38, 44, 44, 9, "Are the laptop and the Pi on the same network?", NAVY_L, NAVY)
    box(2, 24, 44, 11, "YES: use the nickname or the IP address.\nssh, scp, SFTP and VNC all work.", GREEN_L, GREEN)
    box(70, 24, 48, 11, "NO: can you carry the Pi (or the laptop)\nto the other network?", NAVY_L, NAVY)
    box(52, 4, 30, 14, "YES: add the other\nWi-Fi to the Pi (Part E)", GREEN_L, GREEN)
    box(86, 4, 32, 14, "NO: use a remote-access\nservice (Part F)", AMBER_L, AMBER)
    arrow(ax, (48, 44), (30, 36), color=GREEN); ax.text(34, 40.5, "yes", fontsize=8, color=GREEN)
    arrow(ax, (72, 44), (90, 36), color=RASP); ax.text(84, 40.5, "no", fontsize=8, color=RASP)
    arrow(ax, (84, 24), (68, 19), color=GREEN); ax.text(72, 22.5, "yes", fontsize=8, color=GREEN)
    arrow(ax, (104, 24), (102, 19), color=RASP); ax.text(104.5, 21.5, "no", fontsize=8, color=RASP)
    fig.savefig(f"{OUT}/d2_decision.png", pad_inches=0); plt.close(fig)

def fig_sync():
    fig, ax = newax(7.2, 3.2, 120, 53)
    rbox(ax, 40, 22, 40, 18, "#F0EAF6", "#7A4FA0", r=1.4, lw=1.6); ax.text(60, 34.5, "Online repository", ha="center", fontsize=10, fontweight="bold"); ax.text(60, 28.5, "(for example on GitHub)\nthe single source of truth", ha="center", fontsize=8, linespacing=1.25)
    laptop(ax, 2, 28, "Laptop"); pi(ax, 6, 4, "Pi in the lab", w=14); pi(ax, 100, 4, "Pi at home", w=14); laptop(ax, 98, 28, "Laptop 2")
    for a, b in (((22, 36), (39, 33)), ((20, 11), (44, 22)), ((108, 12), (78, 22)), ((97, 36), (81, 33))):
        arrow(ax, a, b, color=GREY, lw=1.5, style="<|-|>")
    ax.text(60, 8, "git pull (get the latest)   /   git push (share my changes)", ha="center", fontsize=8.6, color=INK, family=MONO)
    ax.text(60, 3, "Every computer works on its own copy and syncs through the repository.", ha="center", fontsize=8.2, color=GREY, style="italic")
    fig.savefig(f"{OUT}/d2_sync.png", pad_inches=0); plt.close(fig)

def fig_tmux():
    fig, ax = newax(7.2, 2.5, 120, 42)
    for x0, title, col, lines in ((2, "Without tmux", RASP, ["training...  epoch 12/50", "<connection drops>", "-> the job is killed"]), (62, "With tmux", GREEN, ["tmux new -s train", "training...  epoch 12/50", "<connection drops>", "-> the job keeps running", "tmux attach -t train   (back again)"])):
        rbox(ax, x0, 3, 56, 36, "#0F1C2B", col, r=1.2, lw=1.8); ax.text(x0 + 2, 35.6, title, color="white", fontsize=9, fontweight="bold", va="center")
        for i, l in enumerate(lines): ax.text(x0 + 2.5, 29.5 - i * 5.2, l, color=(G_ if "keeps" in l or "attach" in l or "new" in l else (D_ if "drops" in l else W_)), fontsize=7.6, family=MONO, va="center")
    fig.savefig(f"{OUT}/d2_tmux.png", pad_inches=0); plt.close(fig)

def placeholder(name, title, how, size):
    fig, ax = newax(size[0], size[1], 100, 100 * size[1] / size[0]); H = 100 * size[1] / size[0]
    rbox(ax, 1, 1, 98, H - 2, "#FAFAFA", "#9AA5B1", r=2.5, lw=1.6, ls=(0, (5, 3)))
    ax.text(50, H * 0.64, "YOUR SCREENSHOT GOES HERE", ha="center", va="center", fontsize=13, fontweight="bold", color="#9AA5B1")
    ax.text(50, H * 0.46, title, ha="center", va="center", fontsize=10.5, color=NAVY, fontweight="bold"); ax.text(50, H * 0.27, how, ha="center", va="center", fontsize=8.8, color=GREY, linespacing=1.4)
    fig.savefig(f"{OUT}/{name}.png", pad_inches=0); plt.close(fig)

if __name__ == "__main__":
    fig_roadmap(); fig_sshconfig(); fig_keys(); fig_scp(); fig_sftp(); fig_vnc(); fig_twonets(); fig_decision(); fig_sync(); fig_tmux()
    placeholder("ph_S1_ssh_alias", "S1 - PowerShell: connecting with a nickname", "Capture the window after  ssh lab  shows the Pi prompt.\nSave as  S1_ssh_alias.png  in the folder  my_screenshots/day02/", (7.2, 2.6))
    placeholder("ph_S2_sftp", "S2 - your SFTP program connected to your Pi", "Capture FileZilla or WinSCP with both panes visible (hide the password).\nSave as  S2_sftp.png", (7.2, 3.6))
    placeholder("ph_S3_vnc", "S3 - the Pi desktop in the VNC viewer", "Capture the VNC viewer window showing the Pi desktop.\nSave as  S3_vnc.png", (7.2, 3.6))
    placeholder("ph_S4_nmcli", "S4 - the list of Wi-Fi networks on your Pi", "Capture  nmcli connection show  or  nmcli device wifi list  (hide private names).\nSave as  S4_wifi_list.png", (7.2, 2.6))
    print("day02 figures done")
