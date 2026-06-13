"""
Chapter 4 - DESIGN AND ARCHITECTURE
ADD: Missing database entities to data dictionary, expanded role system
TRIM: Verbose sequence/class diagram descriptions
"""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document(r"E:\FYP-main\report_extracted\report\ch4.docx")

def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)

def make_paragraph(text, style='Normal'):
    new_p = OxmlElement('w:p')
    new_ppr = OxmlElement('w:pPr')
    new_style = OxmlElement('w:pStyle')
    new_style.set(qn('w:val'), style)
    new_ppr.append(new_style)
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
    if 'These nine entities' in txt:
        sections['after_data_dict'] = i
    elif txt.startswith('4.2.2'):
        sections['4.2.2_start'] = i
    elif txt.startswith('4.1.1'):
        sections['4.1.1_start'] = i
    elif txt.startswith('4.4.1 Sequence'):
        sections['4.4.1_start'] = i
    elif txt.startswith('4.4.2 Class'):
        sections['4.4.2_start'] = i
    elif txt.startswith('4.4.3'):
        sections['4.4.3_start'] = i
    # Find the paragraph about "three different role-based interfaces"
    if 'three different role-based interfaces' in txt:
        sections['role_para'] = i

print(f"Found sections: {sections}")

# ============================================================================
# STEP 1: Add missing database entities after the data dictionary reference
# ============================================================================
if 'after_data_dict' in sections:
    ref_para = paragraphs[sections['after_data_dict']]
    parent = ref_para._element.getparent()
    insert_pos = list(parent).index(ref_para._element) + 1
    
    # Replace the "nine entities" text to reflect the actual count
    for run in ref_para.runs:
        if 'nine entities' in run.text:
            run.text = run.text.replace('nine entities', 'entities')
    
    # Add missing entities section
    additions = [
        ("In addition to the nine primary entities listed in Table 4.1, the Event Sphere system "
         "includes several supplementary entities that support extended functionality:", "Normal"),
        
        ("Table 4.1b: Supplementary Data Entities - Event Sphere", "Normal"),
        
        ("EventFeedback: feedbackId (PK), eventId (FK→Event), userId (FK→User), rating (Integer 1-5), "
         "comment (Text), createdAt. Stores star ratings and written reviews submitted by students "
         "after attending events.", "Normal"),
        
        ("EventWaitlist: waitlistId (PK), eventId (FK→Event), userId (FK→User), position (Integer), "
         "joinedAt, promotedAt. Manages a queue of students waiting for spots when events reach "
         "full capacity.", "Normal"),
        
        ("EventReactions: reactionId (PK), eventId (FK→Event), userId (FK→User), reactionType "
         "(like/dislike), createdAt. Enables students to express interest in events through "
         "like/dislike interactions.", "Normal"),
        
        ("EventComments: commentId (PK), eventId (FK→Event), userId (FK→User), content (Text), "
         "parentId (FK→EventComments, nullable), createdAt. Provides threaded discussion "
         "capabilities on event pages.", "Normal"),
        
        ("EventPhotos: photoId (PK), eventId (FK→Event), userId (FK→User), photoUrl (Text), "
         "caption (Text), isApproved (Boolean), uploadedAt. Supports a photo gallery feature "
         "for capturing event memories.", "Normal"),
        
        ("EventResources: resourceId (PK), eventId (FK→Event), title (Text), fileUrl (Text), "
         "fileType (document/pdf/image/video/link), uploadedBy (FK→User), uploadedAt. Allows "
         "organizers to attach downloadable files and links to events.", "Normal"),
        
        ("EventCommittees: committeeId (PK), eventId (FK→Event), userId (FK→User), role "
         "(head/coordinator/volunteer), responsibilities (Text), joinedAt. Manages the organizing "
         "team assigned to each event.", "Normal"),
        
        ("UserPoints: pointsId (PK), userId (FK→User, unique), totalPoints (Integer), "
         "eventsAttended (Integer), badges (Text Array), createdAt, updatedAt. Supports the "
         "gamification system with points, badges, and a leaderboard.", "Normal"),
        
        ("RoleRequests: requestId (PK), userId (FK→User), requestedRole (Text), reason (Text), "
         "status (pending/approved/rejected), reviewedBy (FK→User), reviewedAt, createdAt. "
         "Manages role upgrade requests submitted by users.", "Normal"),
        
        ("RoleChanges: changeId (PK), targetUser (FK→User), oldRole (Text), newRole (Text), "
         "changedBy (FK→User), changedAt. Provides an audit log for all role changes in the system.", "Normal"),
    ]
    
    for text, style in reversed(additions):
        new_p = make_paragraph(text, style)
        parent.insert(insert_pos, new_p)
    
    print("Added supplementary data entities")

# ============================================================================
# STEP 2: Fix role system - update "three" to "five" roles
# ============================================================================
if 'role_para' in sections:
    p = paragraphs[sections['role_para']]
    for run in p.runs:
        if 'three different role-based' in run.text:
            run.text = run.text.replace(
                'three different role-based interfaces',
                'five different role-based interfaces'
            )

# Also fix any "three" role references in presentation layer description
for p in paragraphs:
    txt = p.text
    if 'three-layer' not in txt:  # Don't change architecture layers
        for run in p.runs:
            if 'three different role-based' in run.text:
                run.text = run.text.replace('three different role-based', 'five different role-based')

# ============================================================================
# STEP 3: Add Vice President and President roles after Admin Interface
# ============================================================================
# Find "Admin Interface" heading and the paragraph after it
admin_interface_idx = None
for i, p in enumerate(paragraphs):
    if p.text.strip() == 'Admin Interface':
        admin_interface_idx = i
        break

if admin_interface_idx is not None:
    # Find the paragraph after Admin Interface description (the "All user interface screens..." paragraph)
    # We need to insert VP and President descriptions after Admin Interface description
    for i in range(admin_interface_idx + 1, len(paragraphs)):
        if paragraphs[i].text.strip().startswith('All user interface screens'):
            insert_before = i
            break
    
    ref_para = paragraphs[insert_before]
    parent = ref_para._element.getparent()
    insert_pos = list(parent).index(ref_para._element)
    
    role_additions = [
        ("Vice President Interface", "Heading4"),
        ("The Vice President interface provides event management capabilities within their assigned society, "
         "including event creation and submission for approval, participant list viewing, and society member "
         "coordination. Vice Presidents can manage events associated with their society and view analytics "
         "for events they have organized.", "Normal"),
        ("President Interface", "Heading4"),
        ("The President interface extends the Vice President capabilities with additional society management "
         "features including member management (adding/removing members), society profile editing, and the "
         "ability to create announcements for society members. Presidents serve as the primary point of "
         "contact between the society and the administration.", "Normal"),
    ]
    
    for text, style in reversed(role_additions):
        style_val = 'Heading4' if style == 'Heading4' else 'Normal'
        new_p = make_paragraph(text, style_val)
        parent.insert(insert_pos, new_p)
    
    print("Added Vice President and President role descriptions")

# ============================================================================
# STEP 4: Trim verbose sequence diagram description (4.4.1)
# Keep only the first explanatory paragraph, remove the rest
# ============================================================================
if '4.4.1_start' in sections and '4.4.2_start' in sections:
    # Keep heading + first paragraph, delete the rest until 4.4.2
    kept_first = False
    to_delete = []
    for i in range(sections['4.4.1_start'] + 1, sections['4.4.2_start']):
        txt = paragraphs[i].text.strip()
        if not txt:
            continue
        if not kept_first:
            kept_first = True
            # Keep this paragraph but trim it
            continue
        else:
            to_delete.append(i)
    
    # Add a condensed replacement paragraph at the end
    if to_delete:
        ref_para = paragraphs[to_delete[0]]
        parent = ref_para._element.getparent()
        insert_pos = list(parent).index(ref_para._element)
        
        condensed = make_paragraph(
            "The sequence diagram demonstrates the collaborative interaction across all three architectural "
            "layers of Event Sphere, guaranteeing data integrity through atomic Firestore operations and "
            "real-time notification delivery to stakeholders upon event status changes.",
            "Normal"
        )
        parent.insert(insert_pos, condensed)
    
    for i in sorted(to_delete, reverse=True):
        try:
            delete_paragraph(paragraphs[i])
        except:
            pass
    print(f"Trimmed sequence diagram: removed {len(to_delete)} verbose paragraphs")

# ============================================================================
# STEP 5: Trim class diagram description (4.4.2) - condense class descriptions
# ============================================================================
if '4.4.2_start' in sections and '4.4.3_start' in sections:
    to_delete_class = []
    kept_intro = False
    for i in range(sections['4.4.2_start'] + 1, sections['4.4.3_start']):
        txt = paragraphs[i].text.strip()
        if not txt:
            continue
        if not kept_intro:
            kept_intro = True
            continue
        # Delete all the individual class descriptions (they're in the diagram)
        to_delete_class.append(i)
    
    # Add a condensed summary
    if to_delete_class:
        ref_para = paragraphs[to_delete_class[0]]
        parent = ref_para._element.getparent()
        insert_pos = list(parent).index(ref_para._element)
        
        condensed_class = make_paragraph(
            "The class diagram defines seven core classes (User, Event, Registration, Attendance, "
            "Notification, Expense, Society) with the User class as the parent superclass. The User class "
            "is specialized into five role-specific subclasses: Student, Vice President, President, Admin, "
            "and Super Admin, each inheriting common attributes (uid, email, name, role, department) and "
            "adding role-specific methods. The Event class serves as the central entity linked to "
            "Registration (one-to-many), Attendance (one-to-many), Notification (one-to-many), and "
            "Society (many-to-one). Together, these classes support the complete event management "
            "lifecycle from creation through post-event processing and provide an object-oriented "
            "structural overview that guided the development of Event Sphere.",
            "Normal"
        )
        parent.insert(insert_pos, condensed_class)
    
    for i in sorted(to_delete_class, reverse=True):
        try:
            delete_paragraph(paragraphs[i])
        except:
            pass
    print(f"Trimmed class diagram: removed {len(to_delete_class)} verbose paragraphs")

doc.save(r"E:\FYP-main\report_extracted\report\ch4.docx")
print("Chapter 4 saved successfully!")
