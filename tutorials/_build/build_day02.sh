#!/usr/bin/env bash
# Rebuild everything for Day 02: figures, narrated animation, tutorial (DOCX + PDF), notebook-style notes (PDF + DOCX).
set -e
cd "$(dirname "$0")"; PY=${PY:-python3}
$PY -I figs_day02.py
$PY -I anim_day02.py     # needs day02/animations/narration/s1..s5.mp3 (kept in the repo)
$PY -I day02_tutorial.py
( cd ../day02 && soffice --headless --convert-to pdf Day02_Remote_Access_Files_and_Networks.docx >/dev/null 2>&1 )
( cd notes && python3 day02_notes_b_build.py )
TMP=$(mktemp -d)
node notes/render_notes.js notes/day02_notes_b.html "$TMP/b"
cp "$TMP/b.pdf" ../day02/Day02_Remote_Access_Files_and_Networks_NOTEBOOK-NOTES.pdf
$PY -I make_notes_docx.py ../day02/Day02_Remote_Access_Files_and_Networks_NOTEBOOK-NOTES.docx $(ls "$TMP"/b_p*.png | sort -V)
echo "Day 02 built."
