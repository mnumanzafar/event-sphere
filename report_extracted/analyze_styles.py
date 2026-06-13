"""Analyze paragraph styles in each chapter to preserve formatting."""
from docx import Document
import os

report_dir = r"E:\FYP-main\report_extracted\report"

for fname in sorted(os.listdir(report_dir)):
    if not fname.endswith('.docx'):
        continue
    doc = Document(os.path.join(report_dir, fname))
    print(f"\n{'='*60}")
    print(f"FILE: {fname}")
    print(f"{'='*60}")
    
    styles_used = set()
    for i, p in enumerate(doc.paragraphs[:30]):
        text = p.text.strip()
        if text:
            style_name = p.style.name if p.style else "None"
            styles_used.add(style_name)
            # Show font details of first run
            font_info = ""
            if p.runs:
                r = p.runs[0]
                font_info = f"  [font={r.font.name}, size={r.font.size}, bold={r.font.bold}]"
            print(f"  P{i:03d} Style='{style_name}'{font_info}: {text[:80]}")
    
    print(f"\n  Unique styles: {styles_used}")
