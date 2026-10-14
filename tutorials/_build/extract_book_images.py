"""Crop embedded figures out of the book PDF at 300 dpi (render, not re-encode).
usage: extract_book_images.py BOOK.pdf OUTDIR page:name [page:name ...]
page is the 1-based PDF page; the first image on the page is used (or page:name:idx)."""
import sys, fitz
pdf, outdir, *specs = sys.argv[1:]
doc = fitz.open(pdf)
for s in specs:
    parts = s.split(":")
    pno, name = int(parts[0]), parts[1]
    idx = int(parts[2]) if len(parts) > 2 else 0
    page = doc[pno - 1]
    imgs = page.get_images(full=True)
    # keep only images that are actually drawn (skip pure masks)
    rects = []
    for im in imgs:
        for r in page.get_image_rects(im[0]):
            if r.width > 40 and r.height > 40:
                rects.append(r)
    r = rects[idx]
    pix = page.get_pixmap(dpi=300, clip=r, alpha=False)
    out = f"{outdir}/{name}.png"
    pix.save(out)
    print(out, pix.width, pix.height)
