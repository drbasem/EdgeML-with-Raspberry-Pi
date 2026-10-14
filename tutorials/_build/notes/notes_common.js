// Sketch-note helpers (rough.js). All doodles are seeded so rebuilds are identical.
const NS = "http://www.w3.org/2000/svg";
window.DRAW = {};
let _seed = 7; const sd = () => (_seed = (_seed * 16807) % 2147483647);
const INK = "#1d2f6f", RED = "#c51a4a", GREEN = "#1f7a4d", AMBER = "#c77a00";
function mk(w, h, cls) { const s = document.createElementNS(NS, "svg"); s.setAttribute("width", w); s.setAttribute("height", h); s.setAttribute("viewBox", `0 0 ${w} ${h}`); if (cls) s.setAttribute("class", cls); s.style.overflow = "visible"; return s; }
function T(svg, x, y, txt, o = {}) {
  const t = document.createElementNS(NS, "text"); t.setAttribute("x", x); t.setAttribute("y", y);
  t.setAttribute("font-family", o.font || "Caveat"); t.setAttribute("font-size", o.size || 19); t.setAttribute("fill", o.fill || INK);
  t.setAttribute("text-anchor", o.anchor || "start"); if (o.weight) t.setAttribute("font-weight", o.weight);
  if (o.rot) t.setAttribute("transform", `rotate(${o.rot} ${x} ${y})`);
  const lines = String(txt).split("\n");
  lines.forEach((ln, i) => { const ts = document.createElementNS(NS, "tspan"); ts.setAttribute("x", x); ts.setAttribute("dy", i ? (o.lh || (o.size || 19) * 0.95) : 0); ts.textContent = ln; t.appendChild(ts); });
  svg.appendChild(t); return t;
}
function A(rc, svg, x1, y1, x2, y2, col = RED, w = 2) {
  svg.appendChild(rc.line(x1, y1, x2, y2, { stroke: col, strokeWidth: w, roughness: 1.1, seed: sd() }));
  const a = Math.atan2(y2 - y1, x2 - x1), L = 9;
  [-0.45, 0.45].forEach(d => svg.appendChild(rc.line(x2, y2, x2 - L * Math.cos(a + d), y2 - L * Math.sin(a + d), { stroke: col, strokeWidth: w, roughness: 0.8, seed: sd() })));
}
function R(rc, svg, x, y, w, h, o = {}) {
  svg.appendChild(rc.rectangle(x, y, w, h, Object.assign({ stroke: INK, strokeWidth: 2, roughness: 1.4, bowing: 1.2, seed: sd() }, o)));
}
function star(rc, svg, cx, cy, r, col = "#f5b700") {
  const pts = []; for (let i = 0; i < 10; i++) { const rr = i % 2 ? r * 0.45 : r, a = -Math.PI / 2 + i * Math.PI / 5; pts.push([cx + rr * Math.cos(a), cy + rr * Math.sin(a)]); }
  svg.appendChild(rc.polygon(pts, { stroke: "#b07d00", fill: col, fillStyle: "solid", strokeWidth: 1.5, roughness: 1, seed: sd() }));
}
function squiggle(rc, svg, x, y, w, col = RED) {
  const pts = []; for (let i = 0; i <= w; i += 8) pts.push([x + i, y + (i / 8 % 2 ? 3 : -3)]);
  svg.appendChild(rc.curve(pts, { stroke: col, strokeWidth: 2.4, roughness: 0.6, seed: sd() }));
}

function boxes() {
  document.querySelectorAll(".box[data-r]").forEach(el => {
    const r = el.getBoundingClientRect(), w = el.offsetWidth, h = el.offsetHeight;
    const s = mk(w, h, "rough"); const rc = rough.svg(s);
    const o = { stroke: el.dataset.stroke || INK, strokeWidth: +(el.dataset.w || 2), roughness: 1.5, bowing: 1.4, seed: sd() };
    if (el.dataset.fill) { o.fill = el.dataset.fill; o.fillStyle = el.dataset.style || "solid"; o.fillWeight = 2; o.hachureGap = 7; }
    if (el.dataset.dash) o.strokeLineDash = [8, 6];
    s.appendChild(rc.rectangle(3, 3, w - 6, h - 6, o));
    el.insertBefore(s, el.firstChild);
  });
  document.querySelectorAll("ul.cb li").forEach(li => {
    const s = mk(18, 18); const rc = rough.svg(s);
    s.appendChild(rc.rectangle(2, 2, 14, 14, { stroke: INK, strokeWidth: 1.8, roughness: 1.6, seed: sd() }));
    li.insertBefore(s, li.firstChild);
  });
  document.querySelectorAll("[data-ul]").forEach(el => {
    const w = el.offsetWidth, s = mk(w, 10); s.style.cssText = "position:absolute;left:0;bottom:-6px;overflow:visible"; const rc = rough.svg(s);
    squiggle(rc, s, 2, 5, w - 4, el.dataset.ul || RED); el.appendChild(s);
  });
  document.querySelectorAll(".side").forEach(side => {
    const w = side.offsetWidth, h = side.offsetHeight; const s = mk(w, h, "rough"); const rc = rough.svg(s);
    s.appendChild(rc.rectangle(2, 2, w - 4, h - 4, { stroke: "#9fb2da", strokeWidth: 2, roughness: 1.6, strokeLineDash: [9, 7], seed: sd() }));
    const box = document.createElement("div"); box.className = "sidebox"; box.appendChild(s);
    const lines = document.createElement("div"); lines.className = "lines"; box.appendChild(lines);
    const head = document.createElement("div"); head.className = "sidehead"; head.textContent = "my notes"; box.appendChild(head);
    (side.dataset.prompts || "").split("|").filter(Boolean).forEach((p, i, arr) => {
      const d = document.createElement("div"); d.className = "prompt"; d.textContent = p; d.style.top = (36 + i * (h - 60) / arr.length) + "px"; box.appendChild(d);
    });
    side.appendChild(box);
  });
  document.querySelectorAll("svg[data-draw]").forEach(s => { const rc = rough.svg(s); window.DRAW[s.dataset.draw](rc, s); });
}
window.addEventListener("load", async () => { await document.fonts.ready; await Promise.all([...document.fonts].map(f => f.load().catch(() => {}))); boxes(); document.body.dataset.ready = "1"; });
