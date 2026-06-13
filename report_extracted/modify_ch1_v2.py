"""
Chapter 1 - Fix by working at full paragraph text level
"""
from docx import Document
from lxml import etree

doc = Document(r"E:\FYP-main\report_extracted\report\EventSphere_Ch1.docx")

# Check full paragraph text for what needs fixing
fixes_needed = []
for i, p in enumerate(doc.paragraphs):
    txt = p.text
    if 'three' in txt.lower() and 'role' in txt.lower() and 'three-layer' not in txt:
        fixes_needed.append((i, 'role', txt[:80]))
    if 'Gemini' in txt:
        fixes_needed.append((i, 'gemini', txt[:80]))
    if 'Firestore' in txt and 'primary' in txt.lower():
        fixes_needed.append((i, 'firestore', txt[:80]))
    if 'Admin, Faculty' in txt or 'Faculty, Admin' in txt:
        fixes_needed.append((i, 'role_names', txt[:80]))

print("Fixes needed:")
for idx, ftype, txt in fixes_needed:
    print(f"  P{idx} ({ftype}): {txt}")

# Now do XML-level text replacement for reliability
from docx.oxml.ns import qn

body = doc.element.body
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

fixes = 0
for t_elem in body.iter(qn('w:t')):
    original = t_elem.text or ''
    
    if 'three role' in original and 'three-layer' not in original:
        t_elem.text = original.replace('three role', 'five role')
        fixes += 1
    if 'three different role' in original and 'three-layer' not in original:
        t_elem.text = t_elem.text.replace('three different role', 'five different role')
        fixes += 1
    if 'three user role' in original:
        t_elem.text = t_elem.text.replace('three user role', 'five user role')
        fixes += 1
    if '(Admin, Faculty, Student)' in (t_elem.text or ''):
        t_elem.text = t_elem.text.replace(
            '(Admin, Faculty, Student)',
            '(Student, Vice President, President, Admin, Super Admin)'
        )
        fixes += 1
    if 'Admin, Faculty, and Student' in (t_elem.text or ''):
        t_elem.text = t_elem.text.replace(
            'Admin, Faculty, and Student',
            'Student, Vice President, President, Admin, and Super Admin'
        )
        fixes += 1
    if '(Students, Faculty, Administrators)' in (t_elem.text or ''):
        t_elem.text = t_elem.text.replace(
            '(Students, Faculty, Administrators)',
            '(Students, Vice Presidents, Presidents, Admins, Super Admins)'
        )
        fixes += 1

print(f"\nChapter 1: Applied {fixes} XML-level fixes")

doc.save(r"E:\FYP-main\report_extracted\report\EventSphere_Ch1.docx")
print("Chapter 1 saved successfully!")
