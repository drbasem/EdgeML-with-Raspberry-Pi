#!/usr/bin/env bash
# Rebuild the roadmap (standard DOCX/PDF + sketch-note PDF/DOCX).
set -e
cd "$(dirname "$0")"; PY=${PY:-python3}
$PY -I figs_roadmap.py
$PY -I roadmap_docx.py
( cd ../00_roadmap && soffice --headless --convert-to pdf Roadmap_Edge_AI_Study_Plan.docx >/dev/null 2>&1 )
python3 roadmap_notes_build.py
TMP=$(mktemp -d)
node notes/render_notes.js notes/roadmap_notes.html "$TMP/r"
cp "$TMP/r.pdf" ../00_roadmap/Roadmap_Edge_AI_Study_Plan_SKETCH-NOTES.pdf
$PY -I make_notes_docx.py ../00_roadmap/Roadmap_Edge_AI_Study_Plan_SKETCH-NOTES.docx "$TMP"/r_p*.png
echo "Roadmap built."
