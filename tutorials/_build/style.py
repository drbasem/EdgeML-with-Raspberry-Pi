"""Shared look for the Edge-AI study tutorials."""
import matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager as fm
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONTS = os.path.join(ROOT, "_assets", "fonts")
for f in os.listdir(FONTS):
    if f.endswith(".ttf"):
        fm.fontManager.addfont(os.path.join(FONTS, f))

# palette (also used in the DOCX styles)
RASP = "#C51A4A"      # raspberry
RASP_L = "#FBE3EA"
GREEN = "#2E8B57"
GREEN_L = "#DDF1E4"
NAVY = "#1F3A5F"
NAVY_L = "#E3EAF4"
INK = "#1F2933"
GREY = "#6B7785"
GREY_L = "#EEF1F4"
AMBER = "#D98E04"
AMBER_L = "#FFF2D1"
PCB = "#1E7B4A"

SANS = "Inter"
HAND = "Caveat"
