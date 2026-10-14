"""Generate the sketch-note roadmap HTML from roadmap_data.py, then render with Playwright."""
import os, sys, html, json
sys.path.insert(0, os.path.dirname(__file__))
from roadmap_data import *
here = os.path.join(os.path.dirname(__file__), "notes")

def col_html(keys):
    out = []
    for k in keys:
        key, title, (a, b), col, _, _ = next(p for p in PHASES if p[0] == k)
        out.append(f'<div class="ph" style="color:{col}">P{key[1]} &middot; {html.escape(title)} <span class="dd2">days {a}-{b}</span></div>')
        for (day, topic, src, pp, res) in ROWS[k]:
            parts = ([] if src == "-" else [html.escape(src)]) + ([] if pp == "-" else [f"pp. {html.escape(pp)}"])
            meta = " &middot; ".join(parts)
            sr = f'<span class="sr">{meta}</span>' if meta else ""
            out.append(f'<div class="r"><span class="dn" style="background:{col}">{day}</span><span class="tp">{html.escape(topic)}</span>{sr}</div>')
    return "\n".join(out)

left = col_html(["P0", "P1", "P2"])
right = col_html(["P3", "P4", "P5", "P6"])
page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Roadmap - sketch notes</title>
<link rel="stylesheet" href="notes_common.css">
<style>
.ph {{ font-family: "Marker"; font-size: 16.5px; margin: 8px 0 3px 0; line-height: 1.1; }}
.ph .dd2 {{ font-family: "Caveat"; font-size: 17px; color: #555; }}
.r {{ position: relative; min-height: 21px; padding-left: 30px; margin: 0 0 2px 0; font-size: 13.9px; line-height: 1.1; }}
.dn {{ position: absolute; left: 0; top: 1px; width: 23px; height: 19px; border-radius: 9px; color: #fff; font-family: "Marker"; font-size: 11.5px; text-align: center; line-height: 19px; }}
.sr {{ display: block; font-family: "Caveat"; font-size: 14.8px; color: #c51a4a; line-height: 1; }}
.cols {{ display: flex; gap: 18px; }} .cols > div {{ flex: 1; }}
</style>
<script src="../../_assets/js/rough.js"></script><script src="notes_common.js"></script></head><body>

<div class="pg"><div class="main">
  <div class="h-title" data-ul="#c51a4a" style="position:relative;display:inline-block">My 46-day roadmap</div>
  <div class="h-sub">Pi 4 (4 GB) &nbsp;|&nbsp; 2 Pis + 2 laptops &nbsp;|&nbsp; 2 hours a day &nbsp;|&nbsp; ~9 weeks</div>
  <svg width="506" height="418" data-draw="stairs"></svg>

  <h2>Two Pis, two laptops: do every day twice</h2>
  <div class="row">
    <div class="col box" data-r data-fill="#d6ecff" data-stroke="#2b6cb0"><h3 style="margin-top:0;color:#2b6cb0">Pass 1 - learn</h3>on Pi A, ~2 hours: tutorial + animation + lab + notes</div>
    <div class="col box" data-r data-fill="#dff5e1" data-stroke="#1f7a4d"><h3 style="margin-top:0;color:#1f7a4d">Pass 2 - consolidate</h3>on Pi B, from my notes only. Faster. Finds the hidden mistakes</div>
  </div>
  <ul class="dd" style="font-size:16px">
    <li>different host names: <code>raspi-office</code> / <code>raspi-home</code>, same user</li>
    <li>code + notes in GitHub, then <code>git pull</code> everywhere</li>
    <li>Phase 1 needs no Pi (Colab) - good for travelling</li>
  </ul>
  <h2>Get ready (by day)</h2>
  <ul class="cb" style="font-size:16px">
    <li><b>1</b> Pi 4, microSD 32 GB+, 5 V / 3 A supply, card reader</li>
    <li><b>4</b> Pi camera (CSI) or USB webcam</li>
    <li><b>6</b> Google account (Colab) &nbsp; <b>13</b> Edge Impulse account</li>
    <li><b>35</b> USB mic + speaker</li>
    <li><b>36</b> breadboard, wires, LEDs + resistors, button, DHT + BMP280 sensors</li>
  </ul>
  <div class="box" data-r data-fill="#ffe0e8" data-stroke="#c51a4a" style="margin-top:4px"><b class="red">Honest limits:</b> 4 GB = small language models only, slower than the book's Pi 5. Check Python vs TFLite on day 4-5. Day splits are estimates.</div>
</div>
<div class="side" data-prompts="my start date|which Pi first"></div>
<div class="folio">Roadmap &middot; sketch notes &middot; page 1</div></div>

<div class="pg"><div class="main" style="width:186mm;left:12mm">
  <div class="h-title" style="font-size:27px">Day by day</div>
  <div class="h-sub" style="font-size:17px">C = class number in the course repos (IESTI05 Edge AI, IESTI01 TinyML) &middot; pp. = PDF pages of the book (printed + 1)</div>
  <div class="cols"><div>{left}</div><div>{right}</div></div>
</div><div class="folio">Roadmap &middot; sketch notes &middot; page 2</div></div>

<script>
DRAW.stairs = (rc, s) => {{
  const st = [["0","Pi\\nbring-up","days 1-5","#1F3A5F","#bcd4ff"],["1","ML basics\\n(Colab)","days 6-13","#7A4FA0","#e3d1ff"],["2","Vision AI\\non the Pi","days 14-26","#C51A4A","#ffc4d3"],
              ["3","GenAI\\non the Pi","days 27-38","#2E8B57","#c8efd3"],["4","TinyML\\napps","days 39-42","#c77a00","#ffe3a3"],["5","Capstone\\n+ teaching","days 43-46","#0F8B8D","#bdeaea"]];
  st.forEach(([n, t, d, col, fill], i) => {{
    const x = 4 + i * 84, y = 276 - i * 46;
    R(rc, s, x, y, 80, 92, {{ fill: fill, fillStyle: "solid", stroke: col, strokeWidth: 2.4 }});
    T(s, x + 10, y + 28, n, {{ font: "Marker", size: 26, fill: col }});
    T(s, x + 8, y + 50, t, {{ size: 16, fill: "#1d2f6f", lh: 15 }});
    T(s, x + 40, y + 86, d, {{ size: 16, fill: col, weight: 700, anchor: "middle" }});
    if ([0, 1, 2, 3, 5].includes(i)) {{ s.appendChild(rc.line(x + 60, y, x + 60, y - 12, {{ stroke: "#c51a4a", strokeWidth: 2, roughness: 1, seed: sd() }})); star(rc, s, x + 60, y - 20, 8); }}
  }});
  R(rc, s, 330, 2, 86, 40, {{ stroke: "#6B7785", strokeLineDash: [7, 6], strokeWidth: 2 }});
  T(s, 373, 19, "optional", {{ size: 14, anchor: "middle", fill: "#6B7785" }}); T(s, 373, 36, "UNO Q 47+", {{ size: 15, anchor: "middle", fill: "#6B7785", weight: 700 }});
  T(s, 4, 22, "climb one step at a time", {{ size: 22, fill: "#1d2f6f" }});
  s.appendChild(rc.curve([[4, 30], [60, 40], [130, 36], [180, 20]], {{ stroke: "#c51a4a", strokeWidth: 2, roughness: 1, seed: sd() }}));
  T(s, 4, 392, "stars = what I can show: Pi ready (5) - first CNN (13) - own classifier on the Pi (18)\\nYOLO counting (26) - RAG (32) - SLM drives GPIO (38) - capstone (46)", {{ size: 16, fill: "#c51a4a", lh: 17 }});
}};
</script></body></html>'''
open(os.path.join(here, "roadmap_notes.html"), "w").write(page)
print("html written")
