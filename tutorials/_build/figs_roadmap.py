import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from roadmap_data import *
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
OUT = os.path.join(ROOT, "00_roadmap", "figures"); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": SANS, "savefig.dpi": 300})
fig = plt.figure(figsize=(7.2, 3.1)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-1.5, 58.5); ax.set_ylim(-1.5, 31); ax.axis("off")
for k, (key, title, (a, b), col, _, _) in enumerate(PHASES):
    opt = key == "P6"
    ax.add_patch(FancyBboxPatch((a - 0.5 + 0.12, 12), (b - a + 1) - 0.24, 7.5, boxstyle="round,pad=0,rounding_size=0.6", fc=("white" if opt else col), ec=col, lw=1.6, ls=((0, (4, 3)) if opt else "-")))
    ax.text((a + b) / 2, 15.75, key[1], ha="center", va="center", color=(col if opt else "white"), fontsize=15, fontweight="bold")
    yy = 6.4 - (k % 2) * 4.6
    ax.plot([(a + b) / 2, (a + b) / 2], [11, yy + 1.9], color=col, lw=0.8)
    ax.text((a + b) / 2, yy, f"{title}\nDays {a}-{b}", ha="center", va="center", fontsize=7.0, color=INK, linespacing=1.15)
ax.plot([0.5, 56.5], [11, 11], color=GREY, lw=1)
for d, lab in MILESTONES:
    ax.plot([d, d], [11, 25.5], color="#9AA5B1", lw=0.9, ls=(0, (2, 2)))
    ax.plot([d], [25.5], marker="v", color=RASP, ms=6)
    ax.text(d, 27.6 + (0.0 if MILESTONES.index((d, lab)) % 2 == 0 else 2.2), lab, ha="center", va="bottom", fontsize=6.9, color=RASP)
fig.savefig(f"{OUT}/rm_timeline.png"); print("ok")
