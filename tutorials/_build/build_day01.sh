#!/usr/bin/env bash
# Rebuild everything for Day 01.  Needs: python venv with matplotlib/python-docx/pymupdf/fonttools, node + playwright, ffmpeg, libreoffice.
set -e
cd "$(dirname "$0")"; PY=${PY:-python3}
$PY -I figs_day01.py
$PY -I anim_day01.py   # needs animations/narration/s1..s5.mp3 (kept in the repo)
$PY -I day01_tutorial.py
( cd ../day01 && soffice --headless --convert-to pdf Day01_Meet_Your_Raspberry_Pi.docx >/dev/null 2>&1 )
TMP=$(mktemp -d)
node notes/render_notes.js notes/day01_notes.html "$TMP/n"
cp "$TMP/n.pdf" ../day01/Day01_Meet_Your_Raspberry_Pi_SKETCH-NOTES.pdf
$PY -I make_notes_docx.py ../day01/Day01_Meet_Your_Raspberry_Pi_SKETCH-NOTES.docx "$TMP"/n_p*.png
# notebook-style edition (style B)
TMPB=$(mktemp -d)
node notes/render_notes.js notes/day01_notes_b.html "$TMPB/b"
cp "$TMPB/b.pdf" ../day01/Day01_Meet_Your_Raspberry_Pi_NOTEBOOK-NOTES.pdf
$PY -I make_notes_docx.py ../day01/Day01_Meet_Your_Raspberry_Pi_NOTEBOOK-NOTES.docx "$TMPB"/b_p*.png
echo "Day 01 built."
