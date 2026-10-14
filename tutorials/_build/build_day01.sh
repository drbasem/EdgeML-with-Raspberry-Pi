#!/usr/bin/env bash
# Rebuild everything for Day 01: figures, narrated animation, tutorial (DOCX + PDF) and notebook-style notes (PDF + DOCX).
# Needs: python venv with matplotlib, python-docx, pillow, fonttools; node + playwright (Chromium); ffmpeg; LibreOffice.
set -e
cd "$(dirname "$0")"; PY=${PY:-python3}
$PY -I figs_day01.py
$PY -I anim_day01.py     # needs animations/narration/s1..s5.mp3 (kept in the repo)
$PY -I day01_tutorial.py
( cd ../day01 && soffice --headless --convert-to pdf Day01_Meet_Your_Raspberry_Pi.docx >/dev/null 2>&1 )
( cd notes && python3 day01_notes_b_build.py )
TMP=$(mktemp -d)
node notes/render_notes.js notes/day01_notes_b.html "$TMP/b"
cp "$TMP/b.pdf" ../day01/Day01_Meet_Your_Raspberry_Pi_NOTEBOOK-NOTES.pdf
$PY -I make_notes_docx.py ../day01/Day01_Meet_Your_Raspberry_Pi_NOTEBOOK-NOTES.docx $(ls "$TMP"/b_p*.png | sort -V)
echo "Day 01 built."
