"""
Chapter 2 - PROBLEM DEFINITION
TRIM: Merge repeated challenge sections into consolidated text, remove redundant current system section
"""
from docx import Document
from docx.shared import Pt
import copy

doc = Document(r"E:\FYP-main\report_extracted\report\EventSphere_Ch2.docx")

def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)

def get_para_text(p):
    return p.text.strip()

# Find all paragraphs and their indices
paragraphs = doc.paragraphs

# STEP 1: Find sections to trim
# We want to consolidate 2.1.2, 2.1.3, 2.1.4 (separate stakeholder challenges) 
# into a single shorter combined paragraph
# And remove 2.3.1 and 2.3.2 (repeats of challenges)

# Map paragraph indices
sections = {}
for i, p in enumerate(paragraphs):
    txt = get_para_text(p)
    if txt.startswith('2.1.2'):
        sections['2.1.2_start'] = i
    elif txt.startswith('2.1.3'):
        sections['2.1.3_start'] = i
    elif txt.startswith('2.1.4'):
        sections['2.1.4_start'] = i
    elif txt.startswith('2.2'):
        sections['2.2_start'] = i
    elif txt.startswith('2.3.1'):
        sections['2.3.1_start'] = i
    elif txt.startswith('2.3.2'):
        sections['2.3.2_start'] = i
    elif txt.startswith('2.3.3'):
        sections['2.3.3_start'] = i

print(f"Found sections: {sections}")

# STEP 2: Replace 2.1.2, 2.1.3, 2.1.4 with a consolidated version
# We'll replace all content from 2.1.2 to just before 2.2 with consolidated text

# First, collect paragraphs to delete (from 2.1.2 heading through end of 2.1.4, before 2.2)
to_delete_challenges = []
if '2.1.2_start' in sections and '2.2_start' in sections:
    # Delete everything from after the 2.1.2 heading's content up to 2.2
    # But keep the 2.1.2 heading and replace its content
    for i in range(sections['2.1.2_start'], sections['2.2_start']):
        to_delete_challenges.append(i)

# STEP 3: Remove 2.3.1 and 2.3.2 (redundant with challenges already stated)
to_delete_current = []
if '2.3.1_start' in sections and '2.3.3_start' in sections:
    for i in range(sections['2.3.1_start'], sections['2.3.3_start']):
        to_delete_current.append(i)

# Now collect all paragraphs to delete
all_to_delete = set(to_delete_challenges + to_delete_current)

# Before deleting, insert consolidated content at position of 2.1.2
# We need to add new paragraphs before deleting
if '2.1.2_start' in sections:
    insert_ref = paragraphs[sections['2.1.2_start']]
    parent = insert_ref._element.getparent()
    insert_pos = list(parent).index(insert_ref._element)
    
    # Create consolidated section
    consolidated_heading = "2.1.2 Stakeholder-Specific Challenges"
    consolidated_text = (
        "The challenges created by the absence of a centralized event management system "
        "impact all three stakeholder groups in distinct but interrelated ways. "
        "Students face fragmented event communication through informal channels (WhatsApp, notice boards), "
        "lack of a searchable event repository, unreliable registration through Google Forms or paper sheets "
        "that cannot prevent duplicates, time-consuming manual attendance via printed lists, and no automated "
        "event reminders. Faculty experience disjointed event announcements across multiple channels, "
        "the absence of a formal online event submission and approval process, no real-time access to "
        "participant lists, unstandardized expense management, and no systematic event feedback mechanism. "
        "Administrators lack a centralized event approval system risking inappropriate event listings, "
        "have no aggregated event analytics or participation data, manage user accounts manually "
        "increasing the risk of errors, and have no moderation tools for outdated or cancelled events."
    )
    
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    
    # Create heading paragraph
    new_heading = OxmlElement('w:p')
    new_heading_ppr = OxmlElement('w:pPr')
    new_heading_style = OxmlElement('w:pStyle')
    new_heading_style.set(qn('w:val'), 'Heading3')
    new_heading_ppr.append(new_heading_style)
    new_heading.append(new_heading_ppr)
    new_heading_run = OxmlElement('w:r')
    new_heading_text = OxmlElement('w:t')
    new_heading_text.text = consolidated_heading
    new_heading_run.append(new_heading_text)
    new_heading.append(new_heading_run)
    
    # Create body paragraph
    new_body = OxmlElement('w:p')
    new_body_run = OxmlElement('w:r')
    new_body_text = OxmlElement('w:t')
    new_body_text.text = consolidated_text
    new_body_run.append(new_body_text)
    new_body.append(new_body_run)
    
    # Insert at position
    parent.insert(insert_pos, new_body)
    parent.insert(insert_pos, new_heading)

# Delete old paragraphs (in reverse order to maintain indices)
deleted = 0
for i in sorted(all_to_delete, reverse=True):
    try:
        delete_paragraph(paragraphs[i])
        deleted += 1
    except Exception as e:
        print(f"Warning: Could not delete paragraph {i}: {e}")

print(f"Chapter 2: Deleted {deleted} paragraphs, added consolidated stakeholder section")

doc.save(r"E:\FYP-main\report_extracted\report\EventSphere_Ch2.docx")
print("Chapter 2 saved successfully!")
