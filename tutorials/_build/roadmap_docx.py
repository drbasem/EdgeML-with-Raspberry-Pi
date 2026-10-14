import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from docx_lib import *
from roadmap_data import *
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = f"{ROOT}/00_roadmap"; FIG = f"{OUT}/figures"

def build():
    d = Doc("Edge AI with the Raspberry Pi  |  Hands-on study course  |  Roadmap",
            "Prof. Basem M. ElHalawany  -  personal study & teaching reference  -  draft plan, adjusted after each day")
    d.title_block("Roadmap", "Your 46-Day Path from\nAbsolute Beginner to Edge AI Engineer",
                  "Raspberry Pi 4 (4 GB)  +  Windows laptops  +  two Pis  +  2 hours a day  (about 9 weeks at 5 days a week)")
    d.h2("The plan in one picture")
    d.figure(f"{FIG}/rm_timeline.png", 16.8, "Six phases, 46 core days, and an optional Arduino UNO Q track. Red flags are the milestones you will be able to demonstrate.")
    d.table(["Phase", "Days", "What you learn", "What you need"],
            [[f"**{k[1]}**  {t}", f"{a}-{b}", w, hw] for (k, t, (a, b), _, w, hw) in PHASES],
            [3.8, 1.5, 7.1, 4.8], size=9)
    d.h2("How to use the plan")
    d.bullets([
        "**One day = about 2 hours.** Read the tutorial, watch the animation, do the lab, then print the sketch notes and add your own comments.",
        "**Two Pis, two laptops: do every day twice.** Pass 1 is the learning pass on one Pi (about 2 hours). Pass 2 is the consolidation pass on the other Pi, from your notes only, which should take less time. Alternate which Pi you learn on. This catches mistakes that hide behind copy-paste.",
        "**Name your Pis differently** (for example `raspi-office` and `raspi-home`) and keep the same user name on both. Keep code and notes in the GitHub repo and use `git pull`, so both Pis and both laptops stay in sync.",
        "**Phase 1 (ML foundations) needs no Pi**, only Google Colab, so it is a good block to do when you are travelling.",
        "**Book page numbers** below are PDF pages of the book file (printed page + 1). The splits of long chapters across days are estimates; I will adjust them as we go.",
    ], size=10)
    d.callout("warn", "Honest limits of this plan", [
        "- **Pi 4 with 4 GB:** the vision chapters will run fine. The language-model chapters (Phase 3) were written for a Pi 5 and will be slower here, and only small models fit. We will choose model sizes to match your board and I will report slower-than-book results as they are.",
        "- **Software versions:** a newer Raspberry Pi OS may ship a newer Python than the book used, and TensorFlow Lite can be picky about that. Day 4-5 includes the check.",
        "- **Online services** (Colab, Edge Impulse, model downloads) need Internet access, and your office network may restrict some of them. Plan to use a phone hotspot on those days if needed.",
        "- **UNO Q chapters** are from a different online book and course slides that I have not read yet; the RAG classes for it are marked 'to be developed' in the course README.",
    ], size=9.5)
    d.h2("What to prepare, and when")
    d.table(["By day", "Item", "Why"], [
        ["1", "Pi 4, microSD (32 GB+), USB-C power 5 V / 3 A, card reader, Wi-Fi details", "Everything in Phase 0"],
        ["4", "Pi camera module (CSI) **or** a USB webcam", "Camera test and all vision projects"],
        ["6", "Google account (Colab)", "ML foundations"],
        ["13", "Edge Impulse account", "Training in Phase 2 (check the current free tier)"],
        ["27", "Internet on the Pi for model downloads; enough free space on the microSD", "Ollama and models"],
        ["35", "USB microphone and speaker", "Audio pipeline"],
        ["36", "Breadboard, jumper wires, LEDs + resistors, push button, DHT temperature sensor, BMP280 pressure sensor", "GPIO and sensors (the repo scripts use these; confirm the exact parts in the chapter before buying)"],
        ["47+", "Arduino UNO Q (optional)", "Alternative hardware track"],
    ], [1.6, 9.4, 6.2], size=9)

    d.page_break()
    d.h1("Day-by-day plan")
    d.p("**C** = class number in the course repositories (IESTI05 = Edge AI, IESTI01 = TinyML).  **Book pp.** = PDF pages of 'Edge-AI-Engineering book.pdf'.  A dash means the day is based on slides, notebooks and docs rather than the book.", size=9.5, after=4)
    widths = [1.0, 5.6, 3.6, 2.5, 4.5]
    t = d.d.add_table(rows=1, cols=5); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Day", "Topic", "Source", "Book pp.", "You will have"]):
        c = t.rows[0].cells[j]; shade(c, NAVY); cell_margins(c, 50, 50, 90, 90); borders(c)
        add_runs(c.paragraphs[0], h, size=8.8, color="FFFFFF", bold=True); para_fmt(c.paragraphs[0], after=0)
    repeat_header(t.rows[0])
    for (key, title, (a, b), col, _, _) in PHASES:
        r = t.add_row(); no_split(r)
        m = r.cells[0].merge(r.cells[4]); shade(m, col.lstrip("#")); cell_margins(m, 45, 45, 90, 90); borders(m)
        add_runs(m.paragraphs[0], f"Phase {key[1]}  -  {title}   (days {a}-{b})", size=9.2, color="FFFFFF", bold=True); para_fmt(m.paragraphs[0], after=0)
        for i, (day, topic, src, pp, res) in enumerate(ROWS[key]):
            r = t.add_row(); no_split(r)
            vals = [str(day), topic, src, pp, res]
            for j, v in enumerate(vals):
                c = r.cells[j]; shade(c, "F5F7FA" if i % 2 else "FFFFFF"); cell_margins(c, 35, 35, 90, 90); borders(c, bottom=(4, "D9DEE4"))
                add_runs(c.paragraphs[0], v, size=8.6, bold=(j == 0), color=(col.lstrip("#") if j == 0 else None)); para_fmt(c.paragraphs[0], after=0, line=1.05)
    set_col_widths(t, widths); d.spacer(6)
    d.callout("note", "Checkpoints (what you can show a student)", [
        "- **Day 5:** a Pi you can log into from either laptop, with Python and Jupyter ready.",
        "- **Day 13:** a CNN you trained yourself.   **Day 18:** your own image classifier running live on the Pi.",
        "- **Day 26:** YOLO counting objects.   **Day 32:** a question-answering system over your own documents (RAG).",
        "- **Day 38:** a small language model switching real hardware.   **Day 46:** your capstone and the plan to teach it.",
    ], size=9.5)
    d.save(f"{OUT}/Roadmap_Edge_AI_Study_Plan.docx")

if __name__ == "__main__":
    build(); print("roadmap docx built")
