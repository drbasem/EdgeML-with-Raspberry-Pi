// Clean line-art diagrams for the notebook-style notes.
const NS = "http://www.w3.org/2000/svg";
window.DRAW = {};
const INK = "#222";
function S(w, h) { const s = document.createElementNS(NS, "svg"); s.setAttribute("width", w); s.setAttribute("height", h); s.setAttribute("viewBox", `0 0 ${w} ${h}`); return s; }
function E(s, tag, a) { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); s.appendChild(e); return e; }
function R(s, x, y, w, h, o = {}) { return E(s, "rect", { x, y, width: w, height: h, rx: o.r ?? 3, fill: o.fill || "none", stroke: o.stroke || INK, "stroke-width": o.sw || 1.6, "stroke-dasharray": o.dash || "" }); }
function L(s, x1, y1, x2, y2, o = {}) { return E(s, "line", { x1, y1, x2, y2, stroke: o.stroke || INK, "stroke-width": o.sw || 1.6, "stroke-dasharray": o.dash || "", "stroke-linecap": "round" }); }
function C(s, cx, cy, r, o = {}) { return E(s, "circle", { cx, cy, r, fill: o.fill || "none", stroke: o.stroke || INK, "stroke-width": o.sw || 1.6 }); }
function T(s, x, y, txt, o = {}) {
  const t = E(s, "text", { x, y, "font-size": o.size || 16, fill: o.fill || INK, "text-anchor": o.anchor || "start", "font-weight": o.weight || "normal" });
  String(txt).split("\n").forEach((ln, i) => { const ts = document.createElementNS(NS, "tspan"); ts.setAttribute("x", x); ts.setAttribute("dy", i ? (o.lh || (o.size || 16) * 1.05) : 0); ts.textContent = ln; t.appendChild(ts); });
  return t;
}
function A(s, x1, y1, x2, y2, col = "#c0194a", w = 1.8) {
  L(s, x1, y1, x2, y2, { stroke: col, sw: w }); const a = Math.atan2(y2 - y1, x2 - x1), l = 8;
  E(s, "polygon", { points: `${x2},${y2} ${x2 - l * Math.cos(a - .4)},${y2 - l * Math.sin(a - .4)} ${x2 - l * Math.cos(a + .4)},${y2 - l * Math.sin(a + .4)}`, fill: col });
}
function cam(s, x, y) { R(s, x, y, 34, 24, { fill: "#eee" }); C(s, x + 17, y + 12, 7); }

DRAW.edge = (host) => {
  const s = S(318, 186);
  R(s, 1, 1, 316, 88, { stroke: "#7aa0d8", dash: "5 4", r: 6 }); T(s, 10, 19, "Cloud AI", { size: 17, fill: "#2b6cb0", weight: "bold" });
  cam(s, 12, 38); T(s, 29, 76, "camera", { size: 13, anchor: "middle" });
  A(s, 50, 44, 168, 40); A(s, 168, 58, 50, 56); T(s, 108, 82, "far away, slow", { size: 15, fill: "#c0194a", anchor: "middle" });
  E(s, "path", { d: "M190 62 q-14 0 -14 -12 q0 -10 12 -11 q2 -14 18 -13 q10 -10 24 -2 q16 -2 18 12 q12 2 10 14 q-2 10 -14 10 z", fill: "#d8ebfb", stroke: "#2b6cb0", "stroke-width": 1.6 });
  T(s, 224, 52, "data centre", { size: 14, anchor: "middle" });
  R(s, 1, 97, 316, 88, { stroke: "#4aa56f", dash: "5 4", r: 6 }); T(s, 10, 115, "Edge AI", { size: 17, fill: "#1f7a4d", weight: "bold" });
  cam(s, 12, 134); T(s, 29, 172, "camera", { size: 13, anchor: "middle" });
  A(s, 52, 146, 98, 146, "#1f7a4d");
  R(s, 100, 126, 108, 44, { fill: "#d6efc9", stroke: "#1f7a4d" }); T(s, 154, 144, "Raspberry Pi", { size: 15, anchor: "middle" }); T(s, 154, 162, "model runs HERE", { size: 14, anchor: "middle", fill: "#1f7a4d", weight: "bold" });
  A(s, 210, 148, 262, 148, "#1f7a4d"); T(s, 290, 153, "result!", { size: 17, anchor: "middle", fill: "#1f7a4d", weight: "bold" });
  host.appendChild(s);
};
DRAW.flow = (host) => {
  const s = S(694, 96); const st = [["laptop +\nPi Imager", "#cfe8fb"], ["write the OS\nimage to microSD", "#fbd3e2"], ["card into Pi,\nplug in power", "#fff3b8"], ["Pi boots and\njoins Wi-Fi", "#e5dcf8"], ["laptop connects\nover SSH", "#d6efc9"]];
  st.forEach(([l, c], i) => { const x = 2 + i * 139; R(s, x, 6, 120, 58, { fill: c }); T(s, x + 60, 30, l, { size: 15, anchor: "middle" }); E(s, "circle", { cx: x + 12, cy: 76, r: 0 }); T(s, x + 60, 86, String(i + 1), { size: 16, anchor: "middle", fill: "#c0194a", weight: "bold" }); if (i < 4) A(s, x + 122, 35, x + 137, 35, "#333"); });
  host.appendChild(s);
};
DRAW.leds = (host) => {
  const s = S(330, 92);
  C(s, 20, 20, 10, { fill: "#ff4d4d", stroke: "#8a0000" }); T(s, 40, 26, "RED steady = power is good", { size: 17, fill: "#c0194a" });
  C(s, 20, 54, 10, { fill: "#4dff7a", stroke: "#0a6b2a" }); T(s, 40, 60, "GREEN flickers = Pi reads the card", { size: 17, fill: "#1f7a4d" });
  T(s, 4, 86, "no red light? check the power supply", { size: 14, fill: "#666" });
  host.appendChild(s);
};
DRAW.net = (host) => {
  const s = S(694, 190);
  R(s, 2, 2, 336, 186, { stroke: "#4aa56f", fill: "#eef8ea", r: 6 }); T(s, 170, 24, "same network = works", { size: 18, anchor: "middle", fill: "#1f7a4d", weight: "bold" });
  R(s, 18, 96, 70, 42, { fill: "#cfe8fb" }); T(s, 53, 123, "laptop", { size: 16, anchor: "middle" });
  R(s, 135, 132, 70, 34, { fill: "#ddd" }); T(s, 170, 155, "router", { size: 16, anchor: "middle" });
  R(s, 250, 96, 70, 42, { fill: "#8fd3a6" }); T(s, 285, 123, "Pi 4", { size: 16, anchor: "middle" });
  A(s, 70, 140, 133, 150, "#333"); A(s, 207, 150, 268, 142, "#333");
  R(s, 70, 42, 200, 28, { fill: "#fff" }); T(s, 170, 62, "ssh piuser@raspi4.local", { size: 15, anchor: "middle" });
  R(s, 356, 2, 336, 186, { stroke: "#e58fb2", fill: "#fdeef3", r: 6 }); T(s, 524, 24, "different networks = ?", { size: 18, anchor: "middle", fill: "#c0194a", weight: "bold" });
  R(s, 376, 50, 78, 42, { fill: "#cfe8fb" }); T(s, 415, 70, "office\nlaptop", { size: 15, anchor: "middle", lh: 15 });
  R(s, 376, 120, 78, 42, { fill: "#cfe8fb" }); T(s, 415, 140, "home\nlaptop", { size: 15, anchor: "middle", lh: 15 });
  R(s, 600, 86, 78, 42, { fill: "#8fd3a6" }); T(s, 639, 112, "Pi 4", { size: 16, anchor: "middle" });
  A(s, 458, 72, 540, 100, "#c0194a"); A(s, 458, 140, 540, 116, "#c0194a"); T(s, 560, 118, "?", { size: 46, anchor: "middle", fill: "#c0194a", weight: "bold" });
  T(s, 524, 182, ".local names stay inside one network", { size: 14, anchor: "middle", fill: "#777" });
  host.appendChild(s);
};
DRAW.pi = (host) => {
  const s = S(694, 352); const g = E(s, "g", { transform: "translate(100,2) scale(1.04)" });
  const bx = 90, by = 56, bw = 288, bh = 190;
  const r = (x, y, w, h, o) => R(g, x, y, w, h, o), t = (x, y, txt, o) => T(g, x, y, txt, o), a = (...p) => A(g, ...p);
  r(bx, by, bw, bh, { fill: "#8fd3a6", stroke: "#14532f", sw: 2.4, r: 8 });
  [[bx + 8, by + 8], [bx + bw - 8, by + 8], [bx + 8, by + bh - 8], [bx + bw - 8, by + bh - 8]].forEach(([x, y]) => C(g, x, y, 4, { fill: "#fff", stroke: "#14532f" }));
  r(bx + 26, by + 12, 190, 18, { fill: "#333", stroke: "#111", r: 2 });
  for (let i = 0; i < 20; i++) { r(bx + 31 + i * 9.2, by + 15, 4, 4, { fill: "#e7c65b", stroke: "#e7c65b", r: 0 }); r(bx + 31 + i * 9.2, by + 23, 4, 4, { fill: "#e7c65b", stroke: "#e7c65b", r: 0 }); }
  r(bx + 105, by + 62, 62, 62, { fill: "#c9ced3", stroke: "#555" }); t(bx + 136, by + 88, "CPU", { anchor: "middle", size: 16, weight: "bold" }); t(bx + 136, by + 106, "4 cores", { anchor: "middle", size: 13 });
  r(bx + 40, by + 70, 48, 44, { fill: "#333", stroke: "#111" }); t(bx + 64, by + 97, "RAM", { anchor: "middle", fill: "#fff", size: 15 });
  r(bx + 36, by + 38, 44, 22, { fill: "#c9ced3", stroke: "#555" }); t(bx + 58, by + 53, "Wi-Fi", { anchor: "middle", size: 13 });
  r(bx + bw - 54, by + 24, 74, 58, { fill: "#e3e6ea", stroke: "#555" }); r(bx + bw - 54, by + 24, 14, 58, { fill: "#333", stroke: "#333", r: 0 });
  r(bx + bw - 54, by + 88, 74, 58, { fill: "#e3e6ea", stroke: "#555" }); r(bx + bw - 54, by + 88, 14, 58, { fill: "#3c6fd1", stroke: "#264d99", r: 0 });
  r(bx + bw - 48, by + 150, 68, 44, { fill: "#aeb5bc", stroke: "#555" }); t(bx + bw - 14, by + 177, "RJ45", { anchor: "middle", size: 13 });
  r(bx + 22, by + bh - 4, 34, 14, { fill: "#c9ced3", stroke: "#555" }); r(bx + 76, by + bh - 4, 26, 12, { fill: "#c9ced3", stroke: "#555" }); r(bx + 112, by + bh - 4, 26, 12, { fill: "#c9ced3", stroke: "#555" });
  r(bx + 158, by + bh - 8, 22, 20, { fill: "#333", stroke: "#111" }); r(bx + 138, by + bh - 36, 56, 11, { fill: "#f4f4f4", stroke: "#888", r: 1 });
  r(bx - 14, by + 62, 40, 52, { stroke: "#1d2f6f", dash: "6 5", sw: 2 });
  C(g, bx + 14, by + bh - 40, 5, { fill: "#ff4d4d", stroke: "#8a0000" }); C(g, bx + 14, by + bh - 24, 5, { fill: "#4dff7a", stroke: "#0a6b2a" });
  t(bx + 110, 22, "40-pin GPIO header", { size: 15, fill: "#c0194a", anchor: "middle" }); a(bx + 110, 27, bx + 110, by + 8);
  t(bx + bw + 38, 40, "2 x USB 2.0", { size: 15, fill: "#c0194a" }); a(bx + bw + 34, 36, bx + bw + 16, by + 40);
  t(bx + bw + 38, 118, "2 x USB 3.0\n(blue inside)", { size: 15, fill: "#2b6cb0", lh: 14 }); a(bx + bw + 34, 114, bx + bw + 16, by + 112, "#2b6cb0");
  t(bx + bw + 38, 226, "Gigabit\nEthernet", { size: 15, fill: "#c0194a", lh: 14 }); a(bx + bw + 34, 222, bx + bw + 16, by + 176);
  t(-88, 112, "microSD slot\n(underside)\n= hard disk", { size: 15, fill: "#1d2f6f", lh: 14 }); a(-10, 118, bx - 16, by + 88, "#1d2f6f");
  t(-88, 48, "Wi-Fi + Bluetooth", { size: 14, fill: "#555" }); a(20, 52, bx + 34, by + 50, "#555", 1.3);
  t(-88, 192, "red = power\ngreen = activity", { size: 13.5, fill: "#555", lh: 13 }); a(-20, 200, bx + 8, by + bh - 28, "#555", 1.3);
  t(bx + 30, 300, "USB-C power\n5 V / 3 A", { size: 15, fill: "#c0194a", anchor: "middle", lh: 14 }); a(bx + 38, 282, bx + 38, by + bh + 10);
  t(bx + 112, 316, "2 x micro-HDMI", { size: 15, fill: "#c0194a", anchor: "middle" }); a(bx + 96, 302, bx + 90, by + bh + 10); a(bx + 124, 302, bx + 125, by + bh + 10);
  t(bx + 200, 286, "audio jack", { size: 14, fill: "#555", anchor: "middle" }); a(bx + 190, 276, bx + 170, by + bh + 12, "#555", 1.3);
  t(bx + 270, 306, "camera (CSI) ribbon", { size: 14, fill: "#555", anchor: "middle" }); a(bx + 250, 292, bx + 190, by + bh - 24, "#555", 1.3);
  t(0, 330, "(schematic - port positions simplified)", { size: 12.5, fill: "#888" });
  host.appendChild(s);
};
window.addEventListener("load", async () => {
  await document.fonts.ready; await Promise.all([...document.fonts].map(f => f.load().catch(() => {})));
  document.querySelectorAll("[data-draw]").forEach(h => DRAW[h.dataset.draw](h));
  document.body.dataset.ready = "1";
});
