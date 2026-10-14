import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from docx_lib import *
from roadmap_data import *
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = f"{ROOT}/00_roadmap"; FIG = f"{OUT}/figures"

def build():
    d = Doc("Edge AI with the Raspberry Pi  |  Course material  |  Roadmap",
            "Edge AI with the Raspberry Pi  -  Course roadmap  -  Prof. Basem M. ElHalawany")
    d.title_block("Edge AI with the Raspberry Pi", "Course Roadmap:\nFrom Absolute Beginner to Edge AI Engineer",
                  "46 core days of about 2 hours each (roughly nine weeks at five days a week), on a Raspberry Pi 4 or Raspberry Pi 5, plus an optional Arduino UNO Q track.")
    d.h2("The course in one picture")
    d.figure(f"{FIG}/rm_timeline.png", 16.8, "Six phases, 46 core days, and an optional extension. The red flags are milestones you will be able to demonstrate.")
    d.table(["Phase", "Days", "What you learn", "What you need"],
            [[f"**{k[1]}**  {t}", f"{a}-{b}", w, hw] for (k, t, (a, b), _, w, hw) in PHASES],
            [3.8, 1.5, 7.1, 4.8], size=9)
    d.h2("How the course works")
    d.bullets([
        "**One day is about two hours.** Each day has a full tutorial (complete in itself: no book or website is needed), a narrated animation where it helps, hands-on steps, a quiz and a set of notebook-style notes with space for your own comments.",
        "**Pi 4 and Pi 5.** Every day works on both boards. Where the boards differ (speed, memory, power, camera cable, model sizes) the lesson says so.",
        "**Learn it twice.** If you have two Pis, do each day once on one Pi (the learning pass), then repeat it on the other from your notes only (the consolidation pass). Give the Pis different host names, keep the same user name, and keep your code and notes in a shared online repository.",
        "**Phase 1 needs no Pi:** only Google Colab, so it can be done anywhere.",
        "**Lesson sizes** are estimates. A day that needs longer is simply continued the next day.",
    ], size=10)
    d.callout("warn", "Notes on hardware and software", [
        "- **Pi 4 and Pi 5 speed and memory:** the vision phase runs well on both. In the language-model phase a Pi 5 (8 GB is best) runs larger models; a Pi 4 uses smaller models and longer waits. Each lesson recommends a model size per board.",
        "- **Software versions:** a newer Raspberry Pi OS may ship a newer Python than some machine-learning packages support. Days 4 and 5 include the check and the remedy (virtual environments, or an older OS image).",
        "- **Online services** (Colab, Edge Impulse, model downloads) need Internet access; if your network restricts them, use a phone hotspot on those days.",
        "- **Arduino UNO Q** is an optional extension; the core course does not need it.",
    ], size=9.5)
    d.h2("What to prepare, and when")
    d.table(["By day", "Item", "Why"], [[a, b, c] for a, b, c in PREP], [1.6, 9.4, 6.2], size=9)
    d.page_break()
    d.h1("Day-by-day syllabus")
    widths = [1.0, 4.7, 6.7, 4.8]
    t = d.d.add_table(rows=1, cols=4); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Day", "Topic", "What you do", "You will have"]):
        c = t.rows[0].cells[j]; shade(c, NAVY); cell_margins(c, 50, 50, 90, 90); borders(c)
        add_runs(c.paragraphs[0], h, size=8.8, color="FFFFFF", bold=True); para_fmt(c.paragraphs[0], after=0)
    repeat_header(t.rows[0])
    for (key, title, (a, b), col, _, _) in PHASES:
        r = t.add_row(); no_split(r)
        m = r.cells[0].merge(r.cells[3]); shade(m, col.lstrip("#")); cell_margins(m, 45, 45, 90, 90); borders(m)
        add_runs(m.paragraphs[0], f"Phase {key[1]}  -  {title}   (days {a}-{b})", size=9.2, color="FFFFFF", bold=True); para_fmt(m.paragraphs[0], after=0)
        for i, (day, topic, do, res) in enumerate(ROWS[key]):
            r = t.add_row(); no_split(r)
            for j, v in enumerate([str(day), topic, do, res]):
                c = r.cells[j]; shade(c, "F5F7FA" if i % 2 else "FFFFFF"); cell_margins(c, 35, 35, 90, 90); borders(c, bottom=(4, "D9DEE4"))
                add_runs(c.paragraphs[0], v, size=8.6, bold=(j == 0), color=(col.lstrip("#") if j == 0 else None)); para_fmt(c.paragraphs[0], after=0, line=1.05)
    set_col_widths(t, widths); d.spacer(6)
    d.callout("note", "Checkpoints: what you can demonstrate", [
        "- **Day 5:** a Pi you can log into from your laptop, with Python and Jupyter ready.",
        "- **Day 13:** a convolutional network you trained yourself.   **Day 18:** your own image classifier running live on the Pi.",
        "- **Day 26:** objects counted by a vision system.   **Day 32:** a question-answering system over your own documents (RAG).",
        "- **Day 38:** a small language model switching real hardware.   **Day 46:** your capstone project and the plan to teach it.",
    ], size=9.5)
    d.page_break()
    d.h1("Acknowledgments and references")
    d.p("This course is a compilation: it combines material from the sources below with new explanations, examples, diagrams, exercises and comments written for this course. The original authors are gratefully acknowledged.", size=10)
    d.reflist(REFERENCES)
    d.save(f"{OUT}/Roadmap_Edge_AI_with_Raspberry_Pi.docx")

if __name__ == "__main__":
    build(); print("roadmap docx built")
