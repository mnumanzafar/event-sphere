"""
Chapter 6 - TESTING AND EVALUATION
TRIM: Remove verbose test strategy sections 6.1.1-6.1.5 (already covered by test cases)
      Keep only test plan table, test cases, and results
"""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document(r"E:\FYP-main\report_extracted\report\EventSphere_Ch6_v1.docx")

def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)

def make_paragraph(text, style='Normal'):
    new_p = OxmlElement('w:p')
    new_ppr = OxmlElement('w:pPr')
    new_style_el = OxmlElement('w:pStyle')
    new_style_el.set(qn('w:val'), style)
    new_ppr.append(new_style_el)
    new_p.append(new_ppr)
    new_run = OxmlElement('w:r')
    new_text = OxmlElement('w:t')
    new_text.set(qn('xml:space'), 'preserve')
    new_text.text = text
    new_run.append(new_text)
    new_p.append(new_run)
    return new_p

paragraphs = doc.paragraphs

# Map sections
sections = {}
for i, p in enumerate(paragraphs):
    txt = p.text.strip()
    if txt.startswith('6.1 Testing Strategy'):
        sections['6.1_start'] = i
    elif txt.startswith('6.1.1 Unit Testing'):
        sections['6.1.1_start'] = i
    elif txt.startswith('6.1.1.1'):
        sections['6.1.1.1_start'] = i
    elif txt.startswith('6.1.2 Integration'):
        sections['6.1.2_start'] = i
    elif txt.startswith('6.1.3 System'):
        sections['6.1.3_start'] = i
    elif txt.startswith('6.1.4 Performance'):
        sections['6.1.4_start'] = i
    elif txt.startswith('6.1.5 Usability'):
        sections['6.1.5_start'] = i
    elif txt.startswith('6.2 Test Plan'):
        sections['6.2_start'] = i

print(f"Found sections: {sections}")

# ============================================================================
# STEP 1: Replace verbose test strategy (6.1.1 to 6.1.5) with a condensed summary
# Delete everything from 6.1.1 to just before 6.2
# ============================================================================
to_delete = []
if '6.1.1_start' in sections and '6.2_start' in sections:
    for i in range(sections['6.1.1_start'], sections['6.2_start']):
        to_delete.append(i)

# Insert condensed summary before deleting
if to_delete and '6.1.1_start' in sections:
    ref_para = paragraphs[sections['6.1.1_start']]
    parent = ref_para._element.getparent()
    insert_pos = list(parent).index(ref_para._element)
    
    condensed_parts = [
        ("6.1.1 Testing Approach Summary", "Heading3"),
        (
            "Unit Testing: Individual functions, services, and UI elements were tested in isolation "
            "across all modules including Authentication (login validation, role routing, password reset "
            "expiry), Event Management (form validation, Firestore writes, poster uploads), Registration "
            "and Attendance (atomic seat checks, duplicate prevention, QR validation), Notifications "
            "(FCM delivery, document creation, reminder scheduling), Expense Management (form validation, "
            "receipt uploads, approval workflows), and Admin operations (CRUD operations, activity logging, "
            "analytics accuracy).",
            "Normal"
        ),
        (
            "Integration Testing: Cross-module workflows were validated including the complete event "
            "lifecycle (Faculty creation → Admin approval → Student visibility), student participation "
            "flow (registration → capacity update → QR scan → attendance record), Firebase backend "
            "integration (authentication tokens → Firestore queries → real-time UI updates → Storage "
            "uploads), and notification pipeline (status change → FCM delivery → in-app display).",
            "Normal"
        ),
        (
            "System Testing: Full end-to-end flows were tested for each role: Students (login → browse → "
            "register → scan QR → receive notifications), Faculty (login → create event → submit → "
            "receive approval → manage participants → submit expenses), and Admin (login → review events → "
            "approve/reject → manage users → review expenses → view analytics → download reports).",
            "Normal"
        ),
        (
            "Performance Testing: Response times were measured for event listing loads, registration "
            "processing, and QR attendance verification on mid-tier Android devices. Concurrent user "
            "load testing was conducted with 500 simultaneous users. Backend performance metrics were "
            "recorded for Firestore read/write operations, Storage uploads, and FCM delivery times.",
            "Normal"
        ),
        (
            "Usability Testing: Representative users from each stakeholder group assessed ease of use. "
            "Students completed event registration in three taps and found QR scanning intuitive. "
            "Faculty found the event form thorough yet simple, with clear error messages. Administrators "
            "confirmed the dashboard was well-organized with efficient approval and user management workflows.",
            "Normal"
        ),
    ]
    
    for text, style in reversed(condensed_parts):
        new_p = make_paragraph(text, style)
        parent.insert(insert_pos, new_p)
    
    print(f"Inserted condensed test strategy ({len(condensed_parts)} paragraphs)")

# Delete old verbose paragraphs
deleted = 0
for i in sorted(to_delete, reverse=True):
    try:
        delete_paragraph(paragraphs[i])
        deleted += 1
    except:
        pass

print(f"Chapter 6: Deleted {deleted} verbose test strategy paragraphs")

doc.save(r"E:\FYP-main\report_extracted\report\EventSphere_Ch6_v1.docx")
print("Chapter 6 saved successfully!")
