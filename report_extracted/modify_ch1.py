"""
Chapter 1 - INTRODUCTION
FIX: Update role references from 3 to 5
FIX: Update database references (Supabase is primary, not just Firebase)
FIX: Update Gemini AI chatbot reference
"""
from docx import Document

doc = Document(r"E:\FYP-main\report_extracted\report\EventSphere_Ch1.docx")

fixes = 0
for p in doc.paragraphs:
    for run in p.runs:
        original = run.text
        
        # Fix role references
        if 'three user roles' in run.text:
            run.text = run.text.replace('three user roles', 'five user roles')
        if 'three types of users' in run.text:
            run.text = run.text.replace('three types of users', 'five types of users')
        if 'three role-based' in run.text and 'three-layer' not in run.text:
            run.text = run.text.replace('three role-based', 'five role-based')
        if '(Admin, Faculty, Student)' in run.text:
            run.text = run.text.replace(
                '(Admin, Faculty, Student)',
                '(Student, Vice President, President, Admin, Super Admin)'
            )
        if 'Admin, Faculty, and Student' in run.text:
            run.text = run.text.replace(
                'Admin, Faculty, and Student',
                'Student, Vice President, President, Admin, and Super Admin'
            )
        if '(Students, Faculty, Administrators)' in run.text:
            run.text = run.text.replace(
                '(Students, Faculty, Administrators)',
                '(Students, Vice Presidents, Presidents, Admins, Super Admins)'
            )
        
        # Fix Gemini AI reference - make accurate
        if 'Google Gemini AI' in run.text and 'chatbot' in run.text.lower():
            run.text = run.text.replace('Google Gemini AI', 'AI-powered')
        elif 'Gemini AI' in run.text and 'chatbot' in run.text.lower():
            run.text = run.text.replace('Gemini AI', 'AI-powered')
        
        # Fix database - clarify Supabase is primary
        if 'Firebase Firestore as the primary database' in run.text:
            run.text = run.text.replace(
                'Firebase Firestore as the primary database',
                'Supabase (PostgreSQL) as the primary database with Firebase for authentication and push notifications'
            )
        
        if run.text != original:
            fixes += 1

print(f"Chapter 1: Applied {fixes} fixes")

doc.save(r"E:\FYP-main\report_extracted\report\EventSphere_Ch1.docx")
print("Chapter 1 saved successfully!")
