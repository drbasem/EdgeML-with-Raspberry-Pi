"""Generate the notebook-style roadmap HTML from roadmap_data.py (run from this folder)."""
import os, sys, html, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roadmap_data import *
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes")
def mn(h=60): return f'<div class="mn" style="height:{h}px"></div>'
def page(n, title, body, topic="Course roadmap"):
    return f'''<div class="pg"><div class="content">
<div class="top"><div class="t">{topic}</div><div class="p">PAGE {n}</div></div>
<div class="title">{title}</div>
{body}
</div><div class="folio">Edge AI with the Raspberry Pi &middot; Course roadmap &middot; notebook notes</div></div>
'''
COL = {"P0": ("b", "#cfe8fb"), "P1": ("v", "#e5dcf8"), "P2": ("p", "#fbd3e2"), "P3": ("g", "#d6efc9"), "P4": ("y", "#fff3b8"), "P5": ("b", "#cfe8fb"), "P6": ("v", "#e5dcf8")}
def phase_table(keys):
    out = []
    for k in keys:
        key, title, (a, b), col, _, _ = next(p for p in PHASES if p[0] == k)
        cls = COL[k][0]
        out.append(f'<div class="sh {cls}">Phase {k[1]}: {html.escape(title)} <span class="small">(days {a}-{b})</span></div>')
        rows = "".join(f'<tr><td style="width:6%"><b>{day}</b></td><td style="width:28%">{html.escape(t)}</td><td>{html.escape(do)}</td><td style="width:22%">{html.escape(res)}</td></tr>' for (day, t, do, res) in ROWS[k])
        out.append(f'<table class="t" style="font-size:13.5px"><tr><th>Day</th><th>Topic</th><th>What you do</th><th>You will have</th></tr>{rows}</table>{mn(52)}')
    return "\n".join(out)
P = []
over = "".join(f'<tr><td><b>{k[1]}</b> {html.escape(t)}</td><td>{a}-{b}</td><td>{html.escape(w)}</td><td>{html.escape(hw)}</td></tr>' for (k, t, (a, b), _, w, hw) in PHASES)
P.append(("46 days, six phases", f'''
<div class="small" style="margin-top:-2px">From absolute beginner to Edge AI engineer: about 2 hours a day, roughly nine weeks at five days a week, on a Raspberry Pi 4 or 5. Optional extension: Arduino UNO Q.</div>
<div class="sh b">1. The course in one picture</div>
<div data-draw="phases"></div>
<div class="small"><b class="red">Stars = what I can demonstrate:</b> day 5 Pi ready &middot; day 13 first CNN &middot; day 18 own classifier on the Pi &middot; day 26 object counting &middot; day 32 RAG &middot; day 38 a language model drives GPIO &middot; day 46 capstone.</div>
{mn(48)}
<div class="sh g">2. The phases</div>
<table class="t small"><tr><th style="width:22%">Phase</th><th style="width:8%">Days</th><th>What I learn</th><th style="width:24%">What I need</th></tr>{over}</table>
{mn(60)}
'''))
prep = "".join(f'<li><b>day {a}</b> &nbsp;{html.escape(b)}</li>' for a, b, c in PREP)
P.append(("How the course works", f'''
<div class="sh y">3. The rules of the game</div>
<ul class="bl small">
<li><b>One day = about 2 hours.</b> Every day has a full tutorial (complete in itself: no book or website needed), a narrated animation where it helps, hands-on steps, a quiz, and notebook notes with space for my own comments.</li>
<li><b>Pi 4 and Pi 5:</b> every day works on both boards. Where they differ (speed, memory, power, camera cable, model sizes) the lesson says so.</li>
<li><b>Learn it twice:</b> with two Pis, learn on one, then repeat on the other from my notes only. Different host names (<code>raspi-lab</code>, <code>raspi-home</code>), same user, code and notes in a shared online repository.</li>
<li><b>Phase 1 needs no Pi</b>, only Google Colab: do it anywhere.</li>
<li>Day sizes are estimates; a long day simply continues the next day.</li></ul>
{mn(52)}
<div class="sh p">4. Notes on hardware and software</div>
<div class="pbox small"><b>Speed and memory:</b> vision runs well on both boards. In the language-model phase a Pi 5 (8 GB best) runs larger models; a Pi 4 uses smaller models and longer waits.<br><b>Python:</b> a newer Raspberry Pi OS may ship a newer Python than some ML packages support; days 4-5 include the check and the remedy.<br><b>Online services</b> (Colab, Edge Impulse, model downloads) need Internet; use a phone hotspot if the network restricts them.<br><b>UNO Q</b> is an optional extension.</div>
{mn(52)}
<div class="sh g">5. Get ready (by day)</div>
<ul class="ck small">{prep}</ul>
{mn(60)}
'''))
P.append(("Day by day (1)", phase_table(["P0", "P1"])))
P.append(("Day by day (2)", phase_table(["P2"])))
P.append(("Day by day (3)", phase_table(["P3"])))
P.append(("Day by day (4)", phase_table(["P4", "P5", "P6"])))
chk = ''.join(f'<li>day {d}: {html.escape(t)}</li>' for d, t in MILESTONES)
P.append(("Checkpoints &amp; references", f'''
<div class="sh y">What I can demonstrate</div>
<ul class="ck small">{chk}</ul>
{mn(150)}
<div class="sh b">Acknowledgments and references</div>
<div class="small">This course is a compilation: it combines material from the sources below with new explanations, examples, diagrams, exercises and comments written for this course. The original authors are gratefully acknowledged.</div>
<ol class="refs">''' + "".join(f'<li>{html.escape(r).replace("__", "")}</li>' for r in REFERENCES) + f'''</ol>
{mn(120)}
'''))
bars = json.dumps([[k[1], t, a, b, col] for (k, t, (a, b), col, _, _) in PHASES])
ms = json.dumps(MILESTONES)
body = "".join(page(i + 1, t, b) for i, (t, b) in enumerate(P))
doc = f'''<!doctype html><html><head><meta charset="utf-8"><title>Course roadmap - notebook notes</title>
<link rel="stylesheet" href="notes_b.css"><script src="notes_b.js"></script></head><body>
{body}
<script>
DRAW.phases = (host) => {{
  const s = S(694, 240), ph = {bars}, ms = {ms}; const X = d => 6 + (d - 1) * 12.2;
  ph.forEach(([n, t, a, b, col], i) => {{
    const x = X(a), w = (b - a + 1) * 12.2 - 3, opt = n === "6";
    R(s, x, 74, w, 46, {{ fill: opt ? "#fff" : col, stroke: col, sw: 2, dash: opt ? "6 4" : "" }});
    T(s, x + w / 2, 105, n, {{ size: 24, anchor: "middle", fill: opt ? col : "#fff", weight: "bold" }});
    const yy = 146 + (i % 3) * 30; L(s, x + w / 2, 120, x + w / 2, yy - 14, {{ stroke: col, sw: 1.2 }});
    T(s, x + w / 2, yy, t + "\\ndays " + a + "-" + b, {{ size: 13.5, anchor: "middle", lh: 13 }});
  }});
  ms.forEach(([d, lab], i) => {{
    const x = X(d) + 6; L(s, x, 74, x, 38 - (i % 2) * 0, {{ stroke: "#c0194a", sw: 1.2, dash: "3 3" }});
    E(s, "polygon", {{ points: (() => {{ let p = []; for (let k = 0; k < 10; k++) {{ const r = k % 2 ? 4.5 : 10, a = -Math.PI / 2 + k * Math.PI / 5; p.push((x + r * Math.cos(a)) + "," + (28 + r * Math.sin(a))); }} return p.join(" "); }})(), fill: "#f5b700", stroke: "#b07d00", "stroke-width": 1.3 }});
    T(s, x, 12, "day " + d, {{ size: 13, anchor: "middle", fill: "#c0194a" }});
  }});
  host.appendChild(s);
}};
</script></body></html>'''
open(os.path.join(here, "roadmap_notes.html"), "w").write(doc)
print("html written, pages:", len(P))
