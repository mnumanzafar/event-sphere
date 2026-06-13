"""
Chapter 5 - IMPLEMENTATION
ADD: Environment config, Gamification, Chatbot fix, Social sharing, State management
TRIM: Verbose algorithm descriptions, verbose UI screen descriptions
"""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document(r"E:\FYP-main\report_extracted\report\ch5.docx")

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

# Map all sections
sections = {}
for i, p in enumerate(paragraphs):
    txt = p.text.strip()
    if txt.startswith('5.1.1'):
        sections['5.1.1_start'] = i
    elif txt.startswith('5.1.2'):
        sections['5.1.2_start'] = i
    elif txt.startswith('5.1.3'):
        sections['5.1.3_start'] = i
    elif txt.startswith('5.1.4'):
        sections['5.1.4_start'] = i
    elif txt.startswith('5.1.5'):
        sections['5.1.5_start'] = i
    elif txt.startswith('5.1.6'):
        sections['5.1.6_start'] = i
    elif txt.startswith('5.1.7'):
        sections['5.1.7_start'] = i
    elif txt.startswith('5.1.8'):
        sections['5.1.8_start'] = i
    elif txt.startswith('5.1.9'):
        sections['5.1.9_start'] = i
    elif txt.startswith('5.1.10'):
        sections['5.1.10_start'] = i
    elif txt.startswith('5.2 External'):
        sections['5.2_start'] = i
    elif txt.startswith('5.3 User Interface'):
        sections['5.3_start'] = i
    elif txt.startswith('5.3.1'):
        sections['5.3.1_start'] = i
    elif txt.startswith('5.3.2'):
        sections['5.3.2_start'] = i
    elif txt.startswith('5.3.3'):
        sections['5.3.3_start'] = i
    elif txt.startswith('5.3.4'):
        sections['5.3.4_start'] = i
    elif txt.startswith('5.3.5'):
        sections['5.3.5_start'] = i
    elif txt.startswith('5.3.6'):
        sections['5.3.6_start'] = i
    elif txt.startswith('5.3.7'):
        sections['5.3.7_start'] = i
    elif txt.startswith('5.3.8'):
        sections['5.3.8_start'] = i
    elif txt.startswith('5.3.9'):
        sections['5.3.9_start'] = i
    elif txt.startswith('5.3.10'):
        sections['5.3.10_start'] = i
    elif txt.startswith('5.3.11'):
        sections['5.3.11_start'] = i
    elif txt.startswith('5.3.12'):
        sections['5.3.12_start'] = i
    elif txt.startswith('5.3.13'):
        sections['5.3.13_start'] = i
    elif txt.startswith('5.3.14'):
        sections['5.3.14_start'] = i
    # Find the last paragraph of ch5
    if 'Function: sendAIQuery' in txt:
        sections['ai_func'] = i

print(f"Found {len(sections)} sections")

# ============================================================================
# STEP 1: TRIM - Condense each algorithm's Description paragraphs
# For each 5.1.x, the Input/Output lines contain \x07 (bell char) for bullet
# We'll trim the Description paragraphs to be shorter
# ============================================================================

# For algorithms 5.1.7-5.1.9, the format changed to single paragraphs
# Let's trim the Description text in those combined paragraphs
trimmed_count = 0
for p in paragraphs:
    txt = p.text
    # Trim very long description paragraphs that start with bell char + Description
    if '\x07Description:' in txt and len(txt) > 400:
        for run in p.runs:
            if '\x07Description:' in run.text and len(run.text) > 400:
                # Find Description section and truncate it
                desc_start = run.text.find('\x07Description:')
                before = run.text[:desc_start]
                desc_text = run.text[desc_start:]
                # Truncate description to ~200 chars
                sentences = desc_text.split('. ')
                if len(sentences) > 3:
                    shortened = '. '.join(sentences[:3]) + '.'
                    run.text = before + shortened
                    trimmed_count += 1

print(f"Trimmed {trimmed_count} long algorithm descriptions")

# ============================================================================
# STEP 2: TRIM - Shorten UI screen descriptions (5.3.1-5.3.14)
# Each screen description is a full paragraph - trim to 2-3 sentences
# ============================================================================
ui_sections = [
    ('5.3.1_start', '5.3.2_start'),
    ('5.3.2_start', '5.3.3_start'),
    ('5.3.3_start', '5.3.4_start'),
    ('5.3.4_start', '5.3.5_start'),
    ('5.3.5_start', '5.3.6_start'),
    ('5.3.6_start', '5.3.7_start'),
    ('5.3.7_start', '5.3.8_start'),
    ('5.3.8_start', '5.3.9_start'),
    ('5.3.9_start', '5.3.10_start'),
    ('5.3.10_start', '5.3.11_start'),
    ('5.3.11_start', '5.3.12_start'),
    ('5.3.12_start', '5.3.13_start'),
    ('5.3.13_start', '5.3.14_start'),
]

ui_trimmed = 0
for start_key, end_key in ui_sections:
    if start_key in sections and end_key in sections:
        for i in range(sections[start_key] + 1, sections[end_key]):
            p = paragraphs[i]
            txt = p.text.strip()
            if txt and len(txt) > 350:
                # Trim to first 3 sentences
                sentences = txt.split('. ')
                if len(sentences) > 3:
                    new_txt = '. '.join(sentences[:3]) + '.'
                    # Clear all runs and set first run
                    if p.runs:
                        p.runs[0].text = new_txt
                        for r in p.runs[1:]:
                            r.text = ''
                        ui_trimmed += 1

# Handle last UI section (5.3.14 to end)
if '5.3.14_start' in sections:
    for i in range(sections['5.3.14_start'] + 1, len(paragraphs)):
        p = paragraphs[i]
        txt = p.text.strip()
        if txt and len(txt) > 350:
            sentences = txt.split('. ')
            if len(sentences) > 3:
                new_txt = '. '.join(sentences[:3]) + '.'
                if p.runs:
                    p.runs[0].text = new_txt
                    for r in p.runs[1:]:
                        r.text = ''
                    ui_trimmed += 1

print(f"Trimmed {ui_trimmed} verbose UI screen descriptions")

# ============================================================================
# STEP 3: ADD - New sections at the end of chapter 5
# Add after the last content: Environment Config, Gamification, Chatbot, etc.
# ============================================================================
body = doc.element.body
# Find last paragraph element
last_p = None
for elem in reversed(list(body)):
    if elem.tag == qn('w:p'):
        last_p = elem
        break

if last_p is not None:
    insert_pos = list(body).index(last_p) + 1
    
    new_sections = [
        # --- 5.4 Environment Configuration ---
        ("5.4 Environment Configuration and API Key Management", "Heading3"),
        (
            "Event Sphere uses a secure environment variable approach to manage sensitive API keys "
            "and service credentials. During development, the flutter_dotenv package loads configuration "
            "from a .env file containing SUPABASE_URL and SUPABASE_ANON_KEY values. This file is excluded "
            "from version control via .gitignore to prevent credential exposure. For production builds, "
            "API keys are injected at compile time using Flutter's --dart-define mechanism "
            "(e.g., flutter build apk --dart-define=SUPABASE_URL=... --dart-define=SUPABASE_ANON_KEY=...), "
            "ensuring no credentials are stored in the application source code. The main.dart entry point "
            "checks for --dart-define values first and falls back to the .env file only in development mode, "
            "providing a dual-layer configuration system.",
            "Normal"
        ),
        
        # --- 5.5 State Management ---
        ("5.5 State Management and Architecture Patterns", "Heading3"),
        (
            "Event Sphere implements the Flutter Riverpod state management framework (flutter_riverpod 2.4.9) "
            "to provide reactive, testable, and scalable state management across the application. The app is "
            "wrapped in a ProviderScope at the root level in main.dart, enabling dependency injection and "
            "state sharing across all screens. The application follows a Repository Pattern with three "
            "architectural layers: Providers (auth_provider, event_provider, registration_provider, "
            "bookmark_provider, society_provider) that manage UI state and expose data streams; Repositories "
            "(base_repository, event_repository, user_repository) that abstract data access logic; and "
            "Services (35 specialized service classes) that handle business logic and external API "
            "communication with Supabase and Firebase.",
            "Normal"
        ),
        
        # --- 5.6 Expanded Role-Based Access Control ---
        ("5.6 Expanded Role-Based Access Control System", "Heading3"),
        (
            "Event Sphere implements a five-tier role hierarchy rather than the basic three-role system. "
            "The roles, ordered by increasing privilege, are: Student (rank 1) with access to event browsing, "
            "registration, and QR attendance; Vice President (rank 2) with society-level event management "
            "capabilities; President (rank 3) with full society management including member management and "
            "announcements; Admin (rank 4) with system-wide event approval, user management, and analytics; "
            "and Super Admin (rank 5) with unrestricted access including admin account management. The "
            "role_constants.dart module defines the hierarchy with permission checking functions including "
            "canManage() for hierarchy-based access control, canChangeRole() with special rules preventing "
            "privilege escalation, getAssignableRoles() listing roles each level can assign, and "
            "getManageableRoles() for user management visibility. Super Admin cannot be assigned through "
            "the UI, and Admin users cannot modify other Admin accounts.",
            "Normal"
        ),
        
        # --- 5.7 Gamification Module ---
        ("5.7 Gamification Module", "Heading3"),
        (
            "Event Sphere includes a gamification system to encourage student engagement through points, "
            "badges, and a competitive leaderboard. The GamificationService awards points for specific "
            "actions: 10 points for event attendance, 5 points for submitting feedback, 15 points for "
            "being the first to register for an event, and 10 points for joining a society. Points are "
            "stored atomically in the user_points Supabase table using database-level increment operations "
            "to prevent race conditions during concurrent point awards.",
            "Normal"
        ),
        (
            "The system automatically awards eight milestone badges based on cumulative activity: "
            "First Step (1 event attended), Regular (5 events), Enthusiast (10 events), Champion "
            "(20 events), Legend (50 events), Critic (5 feedback submissions), Early Bird (first "
            "registrant for an event), and Social Butterfly (3 societies joined). Badge checks are "
            "triggered after each point-awarding action. A leaderboard displays the top users ranked "
            "by total points, fostering healthy competition among students.",
            "Normal"
        ),
        
        # --- 5.8 AI Chatbot Assistant ---
        ("5.8 AI Chatbot Assistant", "Heading3"),
        (
            "Event Sphere features a built-in chatbot assistant that provides conversational access to "
            "event information and app functionality. The chatbot is implemented as a rules-based intent "
            "recognition system with four core components: IntentRecognizer performs keyword-based pattern "
            "matching to classify user messages into over 20 intent types including event listing, event "
            "search, registration, QR code requests, recommendations, analytics, and FAQ queries. "
            "DatabaseHandler executes live Supabase queries to fetch real-time event data, user "
            "registrations, attendance records, and statistics. ResponseBuilder formats query results "
            "into user-friendly chat messages with structured event listings and statistics. "
            "ChatPdfGenerator creates downloadable PDF reports and ZIP archives from chat commands, "
            "enabling users to export event lists, registration summaries, and weekly digests.",
            "Normal"
        ),
        (
            "The chatbot supports contextual follow-up questions by maintaining the last viewed event "
            "and event list in memory. Users can interact with action buttons embedded in chat responses "
            "for one-tap event registration and PDF export. Quick suggestion chips provide common queries "
            "such as 'Show current events', 'My registered events', 'Recommend events', and 'Events "
            "this week'.",
            "Normal"
        ),
        
        # --- 5.9 Social Sharing ---
        ("5.9 Social Sharing System", "Heading3"),
        (
            "The ShareService module enables event sharing across multiple platforms. It generates "
            "shareable event URLs and formatted share text containing the event title, date, venue, "
            "and description. Sharing options include native OS share sheet via the share_plus package, "
            "direct sharing to WhatsApp, Twitter/X, Facebook, LinkedIn, and email through URL scheme "
            "integration, and clipboard copy for manual sharing. A visually rich share bottom sheet "
            "presents all sharing options with platform-specific icons and colors, adapting to both "
            "light and dark themes.",
            "Normal"
        ),
        
        # --- 5.10 Additional Features ---
        ("5.10 Additional Implemented Features", "Heading3"),
        (
            "Several additional features enhance the overall user experience of Event Sphere: "
            "Offline Service and Cache Service use the Hive local database to cache event data and "
            "queue user actions for execution when connectivity is restored. The Waitlist Service "
            "manages a position-based queue when events reach full capacity, automatically promoting "
            "users when spots become available. The Poll System enables event organizers to create "
            "polls with multiple options and collect votes from attendees. The Photo Gallery allows "
            "users to upload and browse event photos. The Global Search provides unified search across "
            "events, societies, and users. Image Compression optimizes uploaded images to reduce storage "
            "usage and improve load times. Input Sanitization and Form Validators ensure data integrity "
            "across all user inputs. The Dark Theme system provides a premium purple-themed dark mode "
            "with glassmorphism effects, and Shimmer Loading provides skeleton loading animations "
            "during data fetches.",
            "Normal"
        ),
        
        # --- 5.11 Supabase Row Level Security ---
        ("5.11 Database Security - Row Level Security", "Heading3"),
        (
            "Supabase Row Level Security (RLS) policies enforce fine-grained, role-based data access "
            "at the database level. All 19 tables have RLS enabled with specific policies: Users can "
            "read all user profiles but only update their own. Events are readable by all but only "
            "creatable by authenticated users and updatable by creators or admins. Registrations are "
            "viewable by the registering user and the event creator, and only the user can create or "
            "delete their own registrations. Society management operations are restricted to admin users "
            "and society presidents. Role changes and role requests are audited and only accessible by "
            "admin and super_admin roles. All storage buckets (event-images, profile-images) have "
            "corresponding policies allowing public read access but restricting uploads to "
            "authenticated users.",
            "Normal"
        ),
    ]
    
    for text, style in reversed(new_sections):
        new_p = make_paragraph(text, style)
        body.insert(insert_pos, new_p)
    
    print(f"Added {len(new_sections)} new section paragraphs to Chapter 5")

# ============================================================================
# STEP 4: Fix AI section reference - update 5.1.10 to clarify it's rules-based
# ============================================================================
for p in paragraphs:
    txt = p.text
    if 'Google Gemini AI API' in txt:
        for run in p.runs:
            if 'Google Gemini AI API' in run.text:
                run.text = run.text.replace(
                    'Google Gemini AI API',
                    'chatbot intent recognition engine'
                )
            if 'Gemini API' in run.text:
                run.text = run.text.replace('Gemini API', 'chatbot engine')
    if 'Google Gemini AI' in txt and 'Table' not in txt:
        for run in p.runs:
            if run.text == 'Google Gemini AI':
                run.text = 'Rules-Based Chatbot Engine'
            elif 'Google Gemini AI' in run.text:
                run.text = run.text.replace(
                    'Google Gemini AI',
                    'Rules-Based Chatbot Engine'
                )

doc.save(r"E:\FYP-main\report_extracted\report\ch5.docx")
print("Chapter 5 saved successfully!")
