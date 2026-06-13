# EVENT SPHERE - PROJECT STRUCTURE GUIDE
## Navigate Your Codebase Confidently

---

## 📂 FOLDER STRUCTURE EXPLAINED

```
FYP-main/
├── lib/                          👈 ALL YOUR FLUTTER CODE HERE
│   ├── main.dart                 ← App entry point
│   ├── constants/                ← Fixed values
│   │   ├── app_theme.dart       (Colors, fonts, styling)
│   │   ├── role_constants.dart  (Student, Faculty, Admin definitions)
│   │   └── enums.dart           (Enums like UserRole, etc)
│   │
│   ├── models/                   ← Data structures
│   │   ├── user.dart            (User class with roles)
│   │   ├── event.dart           (Event class)
│   │   ├── registration.dart    (Registration class)
│   │   ├── announcement.dart
│   │   ├── expense.dart
│   │   ├── comment.dart
│   │   ├── feedback.dart
│   │   ├── poll.dart
│   │   └── notification.dart
│   │
│   ├── services/                 👈 BUSINESS LOGIC - Most Important!
│   │   ├── supabase_service.dart    (Supabase client setup)
│   │   ├── auth_service.dart        (Login/Register/RBAC) ⭐
│   │   ├── event_service.dart       (CRUD for events) ⭐
│   │   ├── registration_service.dart (Registrations) ⭐
│   │   ├── qr_service.dart          (QR code logic)
│   │   ├── notification_service.dart (Push notifications)
│   │   ├── expense_service.dart
│   │   ├── bookmark_service.dart
│   │   ├── user_service.dart
│   │   ├── society_service.dart
│   │   ├── announcement_service.dart
│   │   ├── cache_service.dart       (Hive caching)
│   │   ├── offline_service.dart     (Connectivity)
│   │   ├── settings_service.dart    (App preferences)
│   │   ├── logging_service.dart     (Debug logs)
│   │   ├── email_service.dart       (Sending emails)
│   │   ├── avatar_service.dart
│   │   ├── storage_service.dart     (File uploads)
│   │   ├── gamification_service.dart
│   │   ├── feedback_service.dart
│   │   ├── poll_service.dart
│   │   ├── comment_service.dart
│   │   ├── reminder_service.dart
│   │   ├── error_service.dart
│   │   ├── report_service.dart
│   │   ├── role_service.dart
│   │   ├── photo_service.dart
│   │   ├── share_service.dart
│   │   ├── event_timer_service.dart
│   │   ├── user_stats_service.dart
│   │   ├── waitlist_service.dart
│   │   ├── resource_service.dart
│   │   ├── reaction_service.dart
│   │   ├── committee_service.dart
│   │   └── chatbot/
│   │       └── chatbot_service.dart (AI assistance)
│   │
│   ├── providers/                 ← RIVERPOD STATE MANAGEMENT
│   │   ├── auth_provider.dart      (User auth state)
│   │   ├── event_provider.dart     (Event data state)
│   │   ├── registration_provider.dart
│   │   ├── bookmark_provider.dart
│   │   └── society_provider.dart
│   │
│   ├── pages/                     ← UI SCREENS (40+ screens)
│   │   ├── splash_screen.dart          (Loading screen)
│   │   ├── landing_page.dart
│   │   ├── welcome_screen.dart
│   │   ├── login_page.dart
│   │   ├── registration_page.dart
│   │   ├── home_page.dart              (Student dashboard)
│   │   ├── events_page.dart            (Browse events)
│   │   ├── event_detail_page.dart      (Event info)
│   │   ├── add_event_page.dart         (Faculty: create)
│   │   ├── edit_event_page.dart        (Faculty: edit)
│   │   ├── event_approval_page.dart    (Admin: approve) ⭐
│   │   ├── event_approval_detail_page.dart
│   │   ├── registered_events_page.dart (My registrations)
│   │   ├── attended_events_page.dart
│   │   ├── event_attendance_list_page.dart
│   │   ├── bookmarks_page.dart         (Saved events)
│   │   ├── calendar_page.dart          (Calendar view)
│   │   ├── poll_page.dart
│   │   ├── qr_generate_page.dart       (Faculty: create QR) ⭐
│   │   ├── qr_scan_page.dart           (Student: scan QR) ⭐
│   │   ├── profile_page.dart
│   │   ├── edit_profile_page.dart
│   │   ├── admin_dashboard_page.dart   (Admin: analytics) ⭐
│   │   ├── admin_tools_page.dart
│   │   ├── announcements_page.dart
│   │   ├── expenses_page.dart
│   │   ├── reports_page.dart
│   │   ├── societies_page.dart
│   │   ├── society_detail_page.dart
│   │   ├── society_management_page.dart
│   │   ├── chatbot_page.dart
│   │   ├── global_search_page.dart
│   │   ├── notification_settings_page.dart
│   │   ├── privacy_settings_page.dart
│   │   ├── account_settings_page.dart
│   │   ├── change_password_page.dart
│   │   ├── faq_page.dart
│   │   ├── photo_gallery_page.dart
│   │   ├── public_events_page.dart
│   │   ├── resources_page.dart
│   │   ├── onboarding_screen.dart
│   │   ├── committee_page.dart
│   │   ├── user_management_page.dart
│   │   ├── attendance_page.dart
│   │   ├── my_events_page.dart
│   │   ├── event_detail/            (Subfolder)
│   │   │   └── [event detail widgets]
│   │   └── profile/                 (Subfolder)
│   │       └── [profile widgets]
│   │
│   ├── widgets/                   ← REUSABLE COMPONENTS
│   │   └── [Custom Flutter widgets for repeated UI]
│   │
│   ├── repositories/              ← DATA ACCESS LAYER
│   │   ├── base_repository.dart    (Abstract class)
│   │   ├── event_repository.dart   (Event data access)
│   │   └── user_repository.dart    (User data access)
│   │
│   └── utils/                     ← HELPER FUNCTIONS
│       ├── validators.dart        (Form validation)
│       ├── formatters.dart        (Date/time/currency)
│       ├── user_mapper.dart       (Map JSON to objects)
│       ├── pagination.dart        (Pagination logic)
│       └── [other utilities]
│
├── pubspec.yaml                  ← Dependencies list ⭐
├── analysis_options.yaml         ← Dart analysis rules
├── firebase.json                 ← Firebase config
│
├── supabase/                     ← DATABASE MIGRATION FILES
│   ├── schema_fixes.sql          (Table definitions)
│   ├── row_level_security.sql    (Access control policies)
│   ├── create_storage_bucket.sql (File storage setup)
│   ├── rbac_migration.sql        (Role definitions)
│   ├── soft_delete_events.sql
│   ├── email_notifications.sql
│   ├── capacity_and_features.sql
│   ├── create_event_reminders_table.sql
│   ├── create_profile_images_bucket.sql
│   ├── create_user_tokens_table.sql
│   ├── delete_user_function.sql
│   ├── fix_attendee_counts.sql
│   ├── fix_events_rls.sql
│   ├── fix_reminders_rls.sql
│   ├── new_features_schema.sql
│   ├── welcome_email_trigger.sql
│   ├── setup_reminder_cron.sql
│   ├── add_society_category.sql
│   ├── add_privacy_consent.sql
│   ├── supabase_migration.sql
│   ├── supabase_schema.sql
│   ├── functions/                (Supabase Functions)
│   └── migrations/               (Database migrations)
│
├── assets/                       ← App resources
│   ├── images/                   (Event images, logos)
│   └── icon/                     (App icon)
│
├── docs/                         ← Documentation
│   └── PUSH_NOTIFICATIONS_SETUP.md
│
├── android/                      ← Android-specific code
│   └── app/src/
│       └── google-services.json  (Firebase Android config)
│
├── ios/                          ← iOS-specific code
│   └── Runner/
│       └── GoogleService-Info.plist (Firebase iOS config)
│
├── web/                          ← Web version (optional)
│
├── test/                         ← Test files
│   └── widget_test.dart
│
├── report_extracted/             ← Your FYP Report
│   ├── full_report.txt           (All chapters combined)
│   ├── analyze_styles.py         (Report generation scripts)
│   ├── extract.ps1
│   ├── verify_changes.py
│   ├── modify_ch*.py              (Chapter modification scripts)
│   ├── report/                   (Generated report)
│   └── report_backup/            (Backup)
│
├── README.md                     ← Project overview
├── EVALUATION_GUIDE.md           ← 👈 START HERE! (Complete briefing)
├── TECHNICAL_REFERENCE.md        ← API calls and database queries
├── INTERVIEW_PREP.md             ← Interview questions and answers
├── QUICK_REFERENCE.md            ← 5-minute summary
└── .gitignore                    ← Don't commit secrets
```

---

## 🎯 WHERE TO FIND THINGS

### "How do I understand the login flow?"
```
1. Read: lib/services/auth_service.dart (implements login)
2. See: lib/pages/login_page.dart (UI that calls it)
3. Know: lib/models/user.dart (what gets returned)
4. Understand: lib/constants/role_constants.dart (role definitions)
```

### "How does event registration work?"
```
1. lib/services/registration_service.dart     (Business logic)
2. lib/pages/events_page.dart                 (Shows events)
3. lib/pages/event_detail_page.dart           (Register button)
4. supabase/schema_fixes.sql                  (Database structure)
```

### "Where is the admin dashboard?"
```
lib/pages/admin_dashboard_page.dart           (Main file)
lib/providers/event_provider.dart             (Gets data)
lib/services/event_service.dart               (Fetches from database)
```

### "How does QR code scanning work?"
```
1. lib/services/qr_service.dart               (QR logic)
2. lib/pages/qr_generate_page.dart            (Faculty: generates)
3. lib/pages/qr_scan_page.dart                (Student: scans)
4. lib/services/registration_service.dart     (Marks attendance)
```

### "What's the database structure?"
```
supabase/schema_fixes.sql                    (Main tables)
OR
Open Supabase Dashboard online               (See live data)
```

---

## 🚀 KEY FILES TO SHOW IN DEMO

### **Top 5 Files Your Evaluator Will Want to See:**

1. **lib/services/auth_service.dart**
   - Shows: Authentication logic
   - Highlight: `signIn()` method, role-based access

2. **lib/services/event_service.dart**
   - Shows: Event CRUD operations
   - Highlight: `getAllEvents()`, caching, real-time stream

3. **lib/models/user.dart** + **lib/models/event.dart**
   - Shows: Data structures
   - Highlight: Role enum, event status

4. **supabase/schema_fixes.sql**
   - Shows: Database design
   - Highlight: Tables, relationships, constraints

5. **lib/pages/admin_dashboard_page.dart**
   - Shows: Complex UI
   - Highlight: Real-time updates, charts, analytics

---

## 🔍 CODE NAVIGATION TIPS

### **In VS Code:**
- Press `Ctrl+P` to open file quickly
- Type filename: `auth_service.dart`
- Press `Ctrl+G` to go to line number
- Press `Ctrl+F` to find text in file

### **Find Related Code:**
- `Ctrl+Shift+F` = Search in all files
- Search: "EventService" to find all uses
- Search: "registrations" to find all mentions

### **Understand a Function:**
1. Find the function name
2. Look at return type
3. Read the parameters
4. Follow the logic line by line
5. See what database operations it does

---

## 📊 CODE STATISTICS

| Category | Count |
|----------|-------|
| Service Files | 35+ |
| UI Pages | 40+ |
| Models/Data Classes | 9 |
| Database Tables | 7 |
| Riverpod Providers | 5+ |
| Features/Functionalities | 50+ |

---

## 🎬 WHICH FILE TO OPEN FIRST

### **To understand architecture:**
→ `lib/main.dart` (shows initialization order)

### **To understand data flow:**
→ `lib/providers/` (Riverpod providers show how data flows)

### **To understand features:**
→ `lib/services/` (Pick any service to understand that feature)

### **To understand UI:**
→ `lib/pages/` (Pick any page to see UI for that feature)

### **To understand database:**
→ `supabase/schema_fixes.sql` (See all tables)

---

## 🛠️ QUICK DEVELOPMENT COMMANDS

```bash
# Get dependencies
flutter pub get

# Run app
flutter run

# Run on specific device
flutter run -d emulator-5554

# Run release build
flutter run --release

# Build APK
flutter build apk

# Hot reload (in running app)
Press 'r' in terminal

# Full restart
Press 'R' in terminal
```

---

## 💾 IMPORTANT FILES TO NEVER DELETE

- ✅ `pubspec.yaml` - Dependency list
- ✅ `lib/main.dart` - Entry point
- ✅ `.env` - Environment variables (don't commit!)
- ✅ `supabase/schema_fixes.sql` - Database setup
- ✅ `android/app/google-services.json` - Firebase config
- ✅ `ios/Runner/GoogleService-Info.plist` - Firebase iOS config

---

## 📝 WHAT TO TELL EVALUATOR ABOUT EACH LAYER

### **If asked about Presentation Layer:**
> "It's 40+ Flutter screens using Material Design. Each screen is a widget that calls services through Riverpod providers. Everything is role-based - students see different UI than faculty."

### **If asked about Application Layer:**
> "I have 35+ services handling different features. Each service has methods like getAll(), create(), update(), delete(). Services call Supabase API using the SDK. State management uses Riverpod - providers watch services and update UI automatically."

### **If asked about Data Layer:**
> "7 PostgreSQL tables with relationships. Supabase provides real-time sync - when data changes, all connected clients update instantly. Row-Level Security policies prevent unauthorized access at database level."

---

## 🚀 CONFIDENCE TIPS

**Know This By Heart:**
- Main.dart → initializes Supabase, Auth, Cache, Notifications
- Services → have CRUD methods (Create, Read, Update, Delete)
- Providers → watch services and notify UI when data changes
- Pages → widgets that build UI and call providers
- Database → 7 tables with relationships

**Show This First:**
1. Open main.dart (shows it's organized)
2. Navigate to a service (shows business logic)
3. Navigate to a page (shows UI that uses service)
4. Show Supabase dashboard (shows real data)
5. Perform a feature (shows it works)

**Remember:**
- Every feature has a service
- Every service calls the database
- Every database change triggers UI update
- Every page uses multiple services

---

## 🎯 FINAL CHECKLIST

- [ ] Can navigate to any file in 5 seconds
- [ ] Can explain any service in 1 minute
- [ ] Can show code for any feature
- [ ] Know which file handles which feature
- [ ] Can open Supabase dashboard and show data
- [ ] Can run app and perform all features

---

**You're ready to confidently navigate your codebase! 💪**
