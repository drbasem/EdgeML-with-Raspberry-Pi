import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon
OUT = os.path.join(ROOT, "day01", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": SANS, "font.size": 11, "savefig.dpi": 300})

def newax(w, h, xl, yl):
    fig = plt.figure(figsize=(w, h)); ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, xl); ax.set_ylim(0, yl); ax.axis("off"); return fig, ax

def rbox(ax, x, y, w, h, fc, ec=None, r=0.012, lw=1.4, z=2, **kw):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc,
                       ec=ec or fc, lw=lw, zorder=z, **kw)
    ax.add_patch(p); return p

def arrow(ax, a, b, color=GREY, lw=2, ms=16, rad=0.0, z=3):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=color,
                                 connectionstyle=f"arc3,rad={rad}", zorder=z))

# ---------------------------------------------------------------- F1 roadmap
def fig_roadmap():
    fig, ax = newax(7.2, 2.4, 126, 40)
    ax.set_xlim(-3, 123)
    segs = [("A", "Big picture", 20, NAVY), ("B", "Meet the board", 20, "#7A4FA0"),
            ("C", "Prepare the microSD", 45, RASP), ("D", "First boot", 15, AMBER),
            ("E", "First SSH login", 20, GREEN)]
    t = 0
    for k, name, m, c in segs:
        w = m  # 1 minute = 1 unit; 120 total
        rbox(ax, t + 0.6, 14, w - 1.2, 14, c, r=1.5)
        ax.text(t + w / 2, 23.5, k, ha="center", va="center", color="white", fontsize=17, fontweight="bold")
        ax.text(t + w / 2, 17.8, f"{m} min", ha="center", va="center", color="white", fontsize=9.5)
        ax.text(t + w / 2, 10.3, name, ha="center", va="top", color=INK, fontsize=9.3, wrap=True)
        t += w
    ax.plot([0, 120], [33, 33], color=GREY, lw=1.2)
    for x in (0, 20, 40, 85, 100, 120):
        ax.plot([x, x], [32, 34], color=GREY, lw=1.2)
        ax.text(x, 36.5, f"{x//60}:{x%60:02d}", ha="center", fontsize=9, color=GREY)
    fig.savefig(f"{OUT}/d1_roadmap.png", pad_inches=0); plt.close(fig)

# ---------------------------------------------------------------- F2 Pi 4 anatomy (schematic)
def fig_anatomy():
    fig, ax = newax(7.2, 5.2, 120, 87)
    bx, by, sc = 26, 22, 0.72          # board origin + mm->unit scale (board 85 x 56 mm)
    X = lambda mm: bx + mm * sc
    Y = lambda mm: by + mm * sc
    S = lambda mm: mm * sc
    rbox(ax, X(0), Y(0), S(85), S(56), PCB, "#14532F", r=2.5, lw=2, z=1)
    for hx, hy in [(3.5, 3.5), (61.5, 3.5), (3.5, 52.5), (61.5, 52.5)]:
        ax.add_patch(Circle((X(hx), Y(hy)), S(1.6), fc="#0E3D22", ec="#C9D6CE", lw=1.2, zorder=3))
    # GPIO (top edge)
    rbox(ax, X(7), Y(49), S(51), S(5.2), "#2B2B2B", r=0.4, z=3)
    for i in range(20):
        for j in range(2):
            ax.add_patch(Rectangle((X(8.3 + i * 2.5), Y(49.9 + j * 2.0)), S(1.0), S(1.0), fc="#E7C65B", ec="none", zorder=4))
    # chips
    rbox(ax, X(28), Y(18), S(15), S(15), "#B8BEC4", "#7C858D", r=0.8, z=3)
    ax.text(X(35.5), Y(25.5), "CPU\nA72 x4\n1.5 GHz", ha="center", va="center", fontsize=7.2, color="#2B3138", zorder=5, fontweight="bold", linespacing=1.2)
    rbox(ax, X(12), Y(19), S(12), S(11), "#2B2B2B", r=0.6, z=3)
    ax.text(X(18), Y(24.5), "RAM", ha="center", va="center", fontsize=8, color="white", zorder=5, fontweight="bold")
    rbox(ax, X(10), Y(36), S(12), S(8), "#B8BEC4", "#7C858D", r=0.6, z=3)
    ax.text(X(16), Y(40), "Wi-Fi/BT", ha="center", va="center", fontsize=6.8, color="#2B3138", zorder=5)
    # right edge: two USB stacks (top) + Ethernet (bottom)
    rbox(ax, X(66), Y(34), S(21), S(17), "#C9CED3", "#8B949C", r=0.8, z=3)      # USB 2.0 stack
    rbox(ax, X(66), Y(34), S(4), S(17), "#2B2B2B", r=0.2, z=4)
    rbox(ax, X(66), Y(15), S(21), S(17), "#C9CED3", "#8B949C", r=0.8, z=3)      # USB 3.0 stack
    rbox(ax, X(66), Y(15), S(4), S(17), "#3C6FD1", r=0.2, z=4)
    rbox(ax, X(66), Y(-1), S(20), S(14), "#AEB5BC", "#8B949C", r=0.8, z=3)       # Ethernet
    ax.text(X(78), Y(6), "RJ45", ha="center", va="center", fontsize=8, color="#2B3138", zorder=5)
    # bottom edge: USB-C, 2 micro-HDMI, audio jack (+ camera ribbon inset)
    rbox(ax, X(6.5), Y(-1.4), S(9), S(4.2), "#C9CED3", "#8B949C", r=0.5, z=3)
    rbox(ax, X(22.5), Y(-1.4), S(7), S(3.8), "#C9CED3", "#8B949C", r=0.5, z=3)
    rbox(ax, X(34.5), Y(-1.4), S(7), S(3.8), "#C9CED3", "#8B949C", r=0.5, z=3)
    rbox(ax, X(50.5), Y(-1.4), S(7), S(6.5), "#2B2B2B", "#000", r=0.8, z=3)
    rbox(ax, X(44), Y(5), S(16), S(2.6), "#F2F2F2", "#9aa", r=0.3, z=3)
    # microSD slot (underside) dashed, left edge
    rbox(ax, X(-3.5), Y(21), S(14), S(15), "none", "#2B2B2B", r=0.8, lw=1.6, z=4, ls=(0, (3, 2)))
    # LEDs
    ax.add_patch(Circle((X(21), Y(7.5)), S(1.0), fc="#FF3B3B", ec="none", zorder=5))
    ax.add_patch(Circle((X(21), Y(4.6)), S(1.0), fc="#3BFF6B", ec="none", zorder=5))
    def call(txt, xy, xyt, ha="left", col=INK):
        ax.annotate(txt, xy=xy, xytext=xyt, fontsize=8.6, color=col, ha=ha, va="center", linespacing=1.2,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=1.0, shrinkA=3, shrinkB=0))
    call("40-pin GPIO header\n(sensors, LEDs, buttons)", (X(32), Y(54.2)), (X(32), 83.5), ha="center")
    call("Wi-Fi + Bluetooth", (X(10), Y(40)), (1, 66))
    call("4 GB RAM", (X(12), Y(25)), (1, 50))
    call("microSD slot (underside)\n= the Pi's 'hard disk'", (X(-3.5), Y(28)), (1, 34))
    call("2 USB 2.0 + 2 USB 3.0\n(blue = USB 3.0)", (X(87), Y(40)), (X(88) + 4, 66))
    call("Gigabit Ethernet\n(wired network)", (X(86), Y(6)), (X(88) + 4, 33))
    call("USB-C power\n5 V / 3 A", (X(11), Y(-1.4)), (4, 9), ha="left")
    call("2 x micro-HDMI", (X(32), Y(-1.4)), (X(25), 3.6), ha="center")
    call("3.5 mm\naudio jack", (X(54), Y(-1.4)), (X(53), 5.5), ha="center")
    call("Camera (CSI) ribbon\nconnector (approx.)", (X(60), Y(6.3)), (X(72), 9), ha="left")
    ax.text(119, 84, "red LED = power\ngreen LED = activity", ha="right", va="center", fontsize=8, color=GREY)
    ax.text(1, 83.5, "Raspberry Pi 4 B\n(schematic, not to scale)", fontsize=9, color=NAVY, fontweight="bold", va="center", linespacing=1.2)
    fig.savefig(f"{OUT}/d1_pi4_anatomy.png", pad_inches=0); plt.close(fig)

# ---------------------------------------------------------------- F3 kit
def fig_kit():
    fig, ax = newax(7.2, 3.9, 120, 65)
    items_req = [("Raspberry Pi 4\n(4 GB)", "board"), ("microSD card\n32 GB+ (A1/A2)", "sd"),
                 ("USB-C power\n5 V / 3 A", "psu"), ("SD card reader\n(or laptop slot)", "reader"),
                 ("Windows laptop\n+ Wi-Fi", "laptop")]
    items_opt = [("micro-HDMI cable\n+ monitor", "hdmi"), ("USB keyboard\n+ mouse", "kb"), ("Ethernet cable\n(fallback)", "eth")]
    def icon(kind, cx, cy):
        k = 0.8
        if kind == "board":
            rbox(ax, cx - 8*k, cy - 5*k, 16*k, 10*k, PCB, r=1)
            for dx in (-6, 6):
                for dy in (-3.5, 3.5): ax.add_patch(Circle((cx + dx*k, cy + dy*k), 0.5, fc="#cfe", ec="none", zorder=4))
            rbox(ax, cx - 2*k, cy - 2*k, 5*k, 4.5*k, "#B8BEC4", r=0.5, z=4)
        elif kind == "sd":
            ax.add_patch(Polygon([(cx - 3.6, cy - 5), (cx + 3.6, cy - 5), (cx + 3.6, cy + 3.2), (cx + 2.0, cy + 5), (cx - 3.6, cy + 5)], fc=NAVY, ec="none", zorder=3))
            for i in range(4): ax.add_patch(Rectangle((cx - 2.8 + i * 1.6, cy - 4.5), 0.9, 2.4, fc="#E7C65B", ec="none", zorder=4))
        elif kind == "psu":
            rbox(ax, cx - 7, cy - 2.6, 7, 5.2, "#2B2B2B", r=1); ax.plot([cx, cx + 5], [cy, cy], color="#2B2B2B", lw=2.5, zorder=3)
            rbox(ax, cx + 5, cy - 1.2, 3, 2.4, "#C9CED3", r=0.4, z=4)
        elif kind == "reader":
            rbox(ax, cx - 5, cy - 2.2, 10, 4.4, "#5C6B7A", r=0.8); rbox(ax, cx - 5, cy - 2.2, 4, 4.4, "#C9CED3", r=0.6, z=4)
        elif kind == "laptop":
            rbox(ax, cx - 5.5, cy - 0.5, 11, 6.2, "#344", r=0.6); rbox(ax, cx - 4.7, cy + 0.3, 9.4, 4.7, "#8FD0FF", r=0.3, z=4)
            ax.add_patch(Polygon([(cx - 7.5, cy - 0.5), (cx + 7.5, cy - 0.5), (cx + 6.6, cy - 2.6), (cx - 6.6, cy - 2.6)], fc="#556", ec="none", zorder=3))
        elif kind == "hdmi":
            rbox(ax, cx - 5.5, cy - 0.8, 11, 6.2, "#344", r=0.6); rbox(ax, cx - 4.7, cy, 9.4, 4.7, "#8FD0FF", r=0.3, z=4)
            ax.plot([cx, cx], [cy - 2.2, cy - 0.8], color="#344", lw=2.5); rbox(ax, cx - 2.6, cy - 3, 5.2, 0.9, "#344", r=0.3, z=4)
        elif kind == "kb":
            rbox(ax, cx - 7, cy - 2.4, 14, 4.8, "#C9CED3", "#8B949C", r=0.6)
            for i in range(6):
                for j in range(2): ax.add_patch(Rectangle((cx - 6 + i * 2.05, cy - 1.5 + j * 1.9), 1.5, 1.2, fc="white", ec="none", zorder=4))
        elif kind == "eth":
            ax.plot([cx - 7, cx - 2.5, cx + 2.5, cx + 6], [cy - 2, cy + 2, cy - 2, cy + 2], color="#2B6CB0", lw=2.8, solid_capstyle="round", zorder=3)
            rbox(ax, cx + 5, cy + 0.6, 3.6, 3, "#2B6CB0", r=0.4, z=4)
    def row(items, y0, title, tcol, border, fill):
        ax.text(1, y0 + 24.6, title, fontsize=10.5, fontweight="bold", color=tcol, va="center")
        w = 118 / 5
        for i, (lab, kind) in enumerate(items):
            x = 1 + i * w
            rbox(ax, x, y0, w - 2, 21, fill, border, r=1.4, lw=1.2)
            icon(kind, x + (w - 2) / 2, y0 + 14.2)
            ax.text(x + (w - 2) / 2, y0 + 4.6, lab, ha="center", va="center", fontsize=8.2, color=INK, linespacing=1.2)
    row(items_req, 38, "REQUIRED today", RASP, RASP, RASP_L)
    row(items_opt, 6.5, "OPTIONAL (nice to have)", GREEN, GREEN, GREEN_L)
    fig.savefig(f"{OUT}/d1_kit.png", pad_inches=0); plt.close(fig)

# ---------------------------------------------------------------- F4 flash flow
def fig_flow():
    fig, ax = newax(7.2, 2.4, 120, 40)
    steps = [("1", "Laptop +\nPi Imager", NAVY), ("2", "Write OS image\nonto microSD", RASP),
             ("3", "microSD into Pi,\nplug in power", AMBER), ("4", "Pi boots and joins\nyour Wi-Fi", "#7A4FA0"),
             ("5", "Laptop connects\nover SSH", GREEN)]
    w = 20.6; gap = 3.6
    for i, (n, lab, c) in enumerate(steps):
        x = 0.8 + i * (w + gap)
        rbox(ax, x, 10, w, 26, c, r=2)
        ax.add_patch(Circle((x + 3.2, 33), 2.6, fc="white", ec="none", zorder=4))
        ax.text(x + 3.2, 33, n, ha="center", va="center", color=c, fontsize=11, fontweight="bold", zorder=5)
        ax.text(x + w / 2, 21, lab, ha="center", va="center", color="white", fontsize=8.6, linespacing=1.25)
        if i < 4: arrow(ax, (x + w + 0.4, 23), (x + w + gap - 0.4, 23), color=GREY, lw=2.2)
    ax.text(60, 3.2, "everything you set in step 1 (name, user, password, Wi-Fi, SSH) is baked into the card",
            ha="center", va="center", fontsize=9, color=GREY, style="italic")
    fig.savefig(f"{OUT}/d1_flash_flow.png", pad_inches=0); plt.close(fig)

# ---------------------------------------------------------------- F5 network / two laptops
def fig_network():
    fig, ax = newax(7.2, 3.1, 120, 52)
    # same-LAN case
    rbox(ax, 1, 3, 58, 46, GREY_L, GREY, r=2, lw=1)
    ax.text(30, 45.5, "Works on Day 1: same Wi-Fi network", ha="center", fontsize=9.5, fontweight="bold", color=GREEN)
    rbox(ax, 5, 18, 14, 10, NAVY, r=1.2); ax.text(12, 23, "Laptop", color="white", ha="center", va="center", fontsize=9)
    rbox(ax, 24, 8, 12, 8, "#666", r=1.2);  ax.text(30, 12, "Router", color="white", ha="center", va="center", fontsize=9)
    rbox(ax, 41, 18, 14, 10, PCB, r=1.2); ax.text(48, 23, "Pi 4", color="white", ha="center", va="center", fontsize=9)
    arrow(ax, (19, 22), (26, 16.5), lw=1.8); arrow(ax, (36, 16), (42, 21), lw=1.8)
    ax.text(30, 33, "ssh user@raspi4.local", ha="center", fontsize=9, family="DejaVu Sans Mono", color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GREY, lw=0.8))
    # different-LAN case
    rbox(ax, 61, 3, 58, 46, "#FFF5F5", RASP, r=2, lw=1)
    ax.text(90, 45.5, "Day 2 topic: laptop on a different network", ha="center", fontsize=9.5, fontweight="bold", color=RASP)
    rbox(ax, 64, 30, 14, 9, NAVY, r=1.2); ax.text(71, 34.5, "Office\nlaptop", color="white", ha="center", va="center", fontsize=8.5)
    rbox(ax, 64, 9, 14, 9, NAVY, r=1.2); ax.text(71, 13.5, "Home\nlaptop", color="white", ha="center", va="center", fontsize=8.5)
    rbox(ax, 98, 19, 14, 10, PCB, r=1.2); ax.text(105, 24, "Pi 4", color="white", ha="center", va="center", fontsize=9)
    ax.text(88, 24, "?", fontsize=26, color=RASP, ha="center", va="center", fontweight="bold")
    arrow(ax, (78, 34), (86, 27), lw=1.6, color=RASP); arrow(ax, (78, 14), (86, 21), lw=1.6, color=RASP)
    ax.text(90, 5.3, "'.local' names only work inside one network", ha="center", fontsize=8.3, color=GREY, style="italic")
    fig.savefig(f"{OUT}/d1_network.png", pad_inches=0); plt.close(fig)

# ---------------------------------------------------------------- F6 SSH idea
def fig_ssh():
    fig, ax = newax(7.2, 2.6, 120, 43)
    rbox(ax, 2, 6, 44, 30, "#0B1620", NAVY, r=2)
    ax.text(5, 31.5, "PowerShell (your laptop)", color="#9BB4CC", fontsize=8.3, va="center")
    ax.text(5, 23.5, "PS C:\\> ssh user@raspi4.local", color="#E7EEF5", fontsize=8.8, family="DejaVu Sans Mono", va="center")
    ax.text(5, 16, "password: ••••••••", color="#E7EEF5", fontsize=8.8, family="DejaVu Sans Mono", va="center")
    ax.text(5, 9.5, "(you type; nothing is drawn)", color="#7C8B99", fontsize=7.6, va="center", style="italic")
    rbox(ax, 74, 6, 44, 30, "#0B1620", GREEN, r=2)
    ax.text(77, 31.5, "Terminal running ON the Pi", color="#9BD6B2", fontsize=8.3, va="center")
    ax.text(77, 23.5, "user@raspi4:~ $ hostname -I", color="#E7EEF5", fontsize=8.8, family="DejaVu Sans Mono", va="center")
    ax.text(77, 16, "192.168.1.57", color="#9BD6B2", fontsize=8.8, family="DejaVu Sans Mono", va="center")
    arrow(ax, (47, 24), (73, 24), color=GREEN, lw=2.4); arrow(ax, (73, 15), (47, 15), color=NAVY, lw=2.4)
    ax.text(60, 28.2, "keystrokes (encrypted)", ha="center", fontsize=8, color=GREEN)
    ax.text(60, 10.8, "text output (encrypted)", ha="center", fontsize=8, color=NAVY)
    ax.text(60, 38.2, "SSH = Secure SHell: a private tunnel to the Pi's command line", ha="center", fontsize=9, color=INK, fontweight="bold")
    fig.savefig(f"{OUT}/d1_ssh_idea.png", pad_inches=0); plt.close(fig)

# ---------------------------------------------------------------- placeholder
def placeholder(name, title, how, size=(7.2, 3.6)):
    fig, ax = newax(size[0], size[1], 100, 100 * size[1] / size[0])
    H = 100 * size[1] / size[0]
    rbox(ax, 1, 1, 98, H - 2, "#FAFAFA", "#9AA5B1", r=2.5, lw=1.6, ls=(0, (5, 3)))
    ax.text(50, H * 0.64, "YOUR SCREENSHOT GOES HERE", ha="center", va="center", fontsize=13, fontweight="bold", color="#9AA5B1")
    ax.text(50, H * 0.46, title, ha="center", va="center", fontsize=10.5, color=NAVY, fontweight="bold")
    ax.text(50, H * 0.27, how, ha="center", va="center", fontsize=8.8, color=GREY, linespacing=1.4)
    fig.savefig(f"{OUT}/{name}.png", pad_inches=0); plt.close(fig)

if __name__ == "__main__":
    fig_roadmap(); fig_anatomy(); fig_kit(); fig_flow(); fig_network(); fig_ssh()
    placeholder("ph_S1_imager_windows", "S1 - Raspberry Pi Imager main window on YOUR Windows laptop",
                "Win + Shift + S, drag over the Imager window,\npaste into Paint, save as  S1_imager_windows.png\nin  tutorials/my_screenshots/day01/", size=(7.2, 5.37))
    placeholder("ph_S2_customisation", "S2 - The customisation screen with YOUR hostname/user (blur the password!)",
                "Capture the General and Services tabs.  Save as  S2_customisation.png\n(hide the Wi-Fi password before saving)", size=(7.2, 2.3))
    placeholder("ph_S3_powershell_login", "S3 - PowerShell after a successful  ssh  login to your Pi",
                "Capture the window showing the\nuser@raspi4:~ $  prompt.   Save as  S3_powershell_login.png\n(hide anything private)", size=(7.2, 3.77))
    placeholder("ph_S4_my_board", "S4 - A photo of YOUR Pi 4 with the ports labelled", 
                "Take a top-down photo; write labels on it with any editor.\nSave as  S4_my_board.jpg  (or .png)", size=(7.2, 2.6))
    print("figures done")
