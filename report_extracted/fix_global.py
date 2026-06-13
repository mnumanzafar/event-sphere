"""
Global fixes across ALL chapters - fix role refs, Firestore refs, Gemini refs
Works at XML text element level for reliability
"""
from docx import Document
from docx.oxml.ns import qn
import os

report_dir = r"E:\FYP-main\report_extracted\report"

for fname in sorted(os.listdir(report_dir)):
    if not fname.endswith('.docx'):
        continue
    
    fpath = os.path.join(report_dir, fname)
    doc = Document(fpath)
    body = doc.element.body
    
    fixes = 0
    for t_elem in body.iter(qn('w:t')):
        text = t_elem.text or ''
        if not text.strip():
            continue
        
        original = text
        
        # Fix role count references (preserve "three-layer architecture")
        if 'three role' in text and 'three-layer' not in text:
            text = text.replace('three role', 'five role')
        if 'three different role' in text:
            text = text.replace('three different role', 'five different role')
        if 'three user role' in text:
            text = text.replace('three user role', 'five user role')
        if 'three types of user' in text:
            text = text.replace('three types of user', 'five types of user')
        if 'three stakeholder' in text:
            # Don't change this - stakeholders ARE 3 (student, faculty, admin)
            pass
        
        # Fix role name listings
        if '(Admin, Faculty, Student)' in text:
            text = text.replace(
                '(Admin, Faculty, Student)',
                '(Student, Vice President, President, Admin, Super Admin)'
            )
        if 'Admin, Faculty, and Student' in text:
            text = text.replace(
                'Admin, Faculty, and Student',
                'Student, Vice President, President, Admin, and Super Admin'
            )
        if '(Students, Faculty, Administrators)' in text:
            text = text.replace(
                '(Students, Faculty, Administrators)',
                '(Students, Vice Presidents, Presidents, Admins, Super Admins)'
            )
        
        # Fix Firebase/Firestore as primary DB (Supabase is actual primary)
        if 'Firebase Firestore as the primary database' in text:
            text = text.replace(
                'Firebase Firestore as the primary database',
                'Supabase (PostgreSQL) as the primary database, with Firebase for authentication and push notifications'
            )
        if 'Firestore database' in text and 'primary' in text.lower():
            text = text.replace('Firestore database', 'Supabase database')
        
        # Fix Gemini AI chatbot references (actual impl is rules-based)
        if 'Google Gemini AI' in text:
            # Keep in future improvements context
            if 'future' not in text.lower() and 'will' not in text.lower() and 'planned' not in text.lower():
                text = text.replace('Google Gemini AI', 'AI-powered rules-based')
        
        if text != original:
            t_elem.text = text
            fixes += 1
    
    if fixes > 0:
        doc.save(fpath)
        print(f"{fname}: Applied {fixes} global fixes")
    else:
        print(f"{fname}: No fixes needed")

print("\nAll global fixes applied!")
