# EVENT SPHERE - INTERVIEW PREP & PRACTICE QUESTIONS
## Get Ready to Ace Your Evaluation

---

## 🎯 LIKELY EVALUATION QUESTIONS

### **SECTION 1: PROJECT OVERVIEW**

**Q1: "Tell me about your project in 30 seconds."**

**Model Answer:**
> "Event Sphere is a Flutter-based event management application for university communities. 
> It connects students, faculty, and administrators in a unified platform. 
> Students can discover and register for events using their mobile device. 
> Faculty can create events and track attendance using QR codes. 
> Admins can approve events and view analytics. 
> The backend is Supabase (PostgreSQL) with Firebase for notifications and image storage. 
> The app works offline and syncs when internet returns."

**Why this works:**
- ✅ Clear purpose
- ✅ All three user types mentioned
- ✅ Key features highlighted
- ✅ Technology mentioned
- ✅ Unique feature (offline) mentioned

---

**Q2: "Why did you choose Flutter and Dart?"**

**Model Answer:**
> "I chose Flutter for three reasons:
> 1. **Cross-platform**: Code once, run on Android and iOS with 99% code reuse
> 2. **Hot reload**: Change code and see results instantly - speeds up development
> 3. **Performance**: Dart compiles to native code, similar speed to native Android/iOS
> 4. **Rich widgets**: Material Design comes built-in
> 
> Dart is Flutter's language - statically typed for safety, but with flexibility.
> This was my first Flutter project and I learned a lot!"

---

**Q3: "Why Supabase instead of Firebase?"**

**Model Answer:**
> "Great question. I used both:
> 
> **Supabase for:**
> - PostgreSQL database (relational)
> - Complex queries and joins (events, registrations, societies)
> - Authentication (email + password)
> - Row-Level Security (database-level access control)
> 
> **Firebase for:**
> - Cloud Messaging (push notifications)
> - Storage (event images, receipts)
> 
> Supabase is PostgreSQL-based with better relational data support, 
> while Firebase is more document-based. 
> For event management with complex relationships, 
> PostgreSQL's relational model was better suited."

---

### **SECTION 2: ARCHITECTURE & DESIGN**

**Q4: "Explain your 3-layer architecture."**

**Model Answer & Diagram:**
```
┌─────────────────────────────────┐
│  PRESENTATION LAYER             │
│  (Flutter UI - What users see)  │
│  - Pages/Screens                │
│  - Widgets/Components           │
│  - Form validation              │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│  APPLICATION LAYER              │
│  (Business logic)               │
│  - Services (Auth, Event, etc)  │
│  - State Management (Riverpod)  │
│  - Repositories                 │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│  DATA LAYER                     │
│  (Storage & Backend)            │
│  - Supabase Database            │
│  - Supabase Storage             │
│  - Firebase Messaging           │
│  - Local Cache (Hive)           │
└─────────────────────────────────┘
```

**Why 3 layers?**
- **Separation of Concerns**: Each layer has one responsibility
- **Testability**: Can test each layer independently
- **Maintainability**: Easy to change one layer without affecting others
- **Scalability**: Can optimize each layer separately

---

**Q5: "How does data flow from database to UI?"**

**Model Answer with Diagram:**
```
Database (PostgreSQL)
    ↓ (Supabase SDK)
Service Layer (Dart)
    ├─ Fetch data
    ├─ Apply business rules
    └─ Return to provider
    ↓ (Riverpod)
State Management
    ├─ Cache in memory
    └─ Notify listeners
    ↓ (Widget rebuild)
UI Layer (Flutter)
    └─ Display to user

Example:
1. User opens Events Page
2. Widget calls: ref.watch(allEventsProvider)
3. Provider calls: EventService.getAllEvents()
4. Service queries Supabase: SELECT * FROM events...
5. Database returns JSON
6. Service maps to Event objects
7. Provider caches and notifies
8. Widget rebuilds with events
9. ListView displays events
```

**Time**: ~100-200ms total

---

### **SECTION 3: DATABASE & DATA MODEL**

**Q6: "Show me your database schema."**

**Model Answer:**
```sql
KEY TABLES:

users (each person in system)
├─ id (UUID)
├─ email (unique)
├─ name
├─ role (student/faculty/admin)
└─ profile_image_url

events (what faculty create)
├─ id
├─ title, description
├─ date, venue
├─ created_by → references users
├─ approval_status (pending/approved/rejected)
├─ max_attendees
├─ current_attendees
└─ deleted_at (soft delete)

registrations (student signups)
├─ id
├─ user_id → references users
├─ event_id → references events
├─ registered_at
├─ checked_in (boolean)
└─ checked_in_at

societies (clubs/groups)
├─ id
├─ name
├─ president_id → references users
└─ society_members (join table)
    ├─ user_id
    └─ society_id

RELATIONSHIPS:
- Users create many events (1 to N)
- Events have many registrations (1 to N)
- Registrations belong to users (N to 1)
```

**Q7: "How do you prevent double registrations?"**

**Model Answer:**
```sql
-- Constraint in database:
UNIQUE(user_id, event_id)

-- This means:
-- Cannot have two registrations with same user AND same event
-- Database rejects duplicates automatically

-- In code, we also check:
SELECT * FROM registrations 
WHERE user_id = 'user-uuid' 
  AND event_id = 'event-uuid'

-- If found, show error: "Already registered"
```

---

**Q8: "What are soft deletes and why use them?"**

**Model Answer:**
```sql
-- Hard delete (permanent):
DELETE FROM events WHERE id = 'event-123'
-- Data is GONE forever

-- Soft delete (safer):
UPDATE events 
SET deleted_at = NOW() 
WHERE id = 'event-123'
-- Data still exists but marked deleted_at

ADVANTAGES:
✓ Can recover accidentally deleted data
✓ Maintains referential integrity
✓ Keeps analytics history
✓ Safer for regulatory/audit requirements

IN YOUR APP:
-- When fetching events, exclude soft-deleted:
SELECT * FROM events WHERE deleted_at IS NULL

-- When showing event count, exclude:
SELECT COUNT(*) FROM events WHERE deleted_at IS NULL
```

---

### **SECTION 4: AUTHENTICATION & SECURITY**

**Q9: "How do you handle user authentication?"**

**Model Answer:**
```
FLOW:
1. User enters email + password
2. App sends to Supabase Auth (not to your database)
3. Supabase verifies password (encrypted, salted)
4. If valid, returns JWT token
5. App stores token locally (secure)
6. All future API calls include token
7. Supabase verifies token before allowing access

SECURITY FEATURES:
✓ Password never stored in plain text
✓ Password salted + hashed with bcrypt
✓ JWT expires after 1 hour
✓ Refresh tokens for long sessions
✓ Email confirmation required for signup
✓ Password reset via email
```

---

**Q10: "What is Row-Level Security (RLS)?"**

**Model Answer:**
```sql
-- RLS = Database-level access control
-- Rules written in SQL that database enforces

EXAMPLE POLICY (Students only see approved events):
CREATE POLICY "Students see approved events"
  ON public.events
  FOR SELECT
  USING (approval_status = 'approved');

HOW IT WORKS:
1. Student runs: SELECT * FROM events
2. Database adds WHERE clause automatically:
   SELECT * FROM events WHERE approval_status = 'approved'
3. Only approved events returned

ANOTHER EXAMPLE (Users see only their own data):
CREATE POLICY "Users see own registrations"
  ON public.registrations
  FOR SELECT
  USING (user_id = auth.uid());

-- auth.uid() = ID of logged-in user
-- So you can NEVER see someone else's registrations

BENEFITS:
✓ Cannot access data even with bug in app
✓ Cannot access data even if JWT is stolen
✓ Authorization enforced at database layer
✓ Prevents massive data breaches
```

---

**Q11: "How do you handle sensitive data (passwords, tokens)?"**

**Model Answer:**
```
PASSWORDS:
- Never store in app
- Never send in plaintext
- Only Supabase Auth handles (encrypted)
- Can reset via email

FCM TOKENS:
- Stored in database (not sensitive)
- Used to send notifications
- Regenerated if user logs out

JWT TOKENS:
- Returned by Supabase Auth
- Stored locally with FlutterSecure
- Sent in HTTP Authorization header
- Expires automatically
- Refresh token used to get new one

ENVIRONMENT VARIABLES:
- API keys in .env file
- NOT committed to git
- Loaded at runtime
- Different keys for dev/prod
```

---

### **SECTION 5: OFFLINE SUPPORT**

**Q12: "How does your app work offline?"**

**Model Answer:**
```
ARCHITECTURE:
Internet Available
    ↓
Fetch from Supabase
    ↓
Cache locally (Hive)
    ↓
Return to UI
    
Internet Unavailable
    ↓
No fresh data available
    ↓
Return cached data
    ↓
Show to user (might be stale)

IMPLEMENTATION:
1. Check internet: OfflineService.isConnected
2. If online: Fetch from Supabase + cache
3. If offline: Serve from Hive cache
4. When online returns: Sync queued actions

CACHED DATA:
- Events (list)
- User profile
- My registrations
- Bookmarks
- Announcements

QUEUED ACTIONS (if offline):
- Register for event
- Create bookmark
- Update profile
- These sync when online

HIVE (Local storage):
- Key-value database
- 1000x faster than JSON parsing
- Data persists after app close
- Encrypted option available
- Used for offline cache
```

---

**Q13: "What if user edits data offline then goes online?"**

**Model Answer:**
```
SCENARIO:
- User offline, edits profile (name, bio)
- Changes saved locally only
- User comes online
- Changes should sync to server

SOLUTION:
1. Actions queued in OfflineService
2. When internet returns, detect in app
3. Trigger: OfflineService.syncPendingActions()
4. For each action: POST to Supabase
5. If successful: Remove from queue
6. If fails: Retry later
7. UI shows "Syncing..." indicator

WHAT IF SERVER HAS NEWER DATA?
- Use timestamp comparison
- Server data is source of truth
- Local cache is only for offline
- Rare conflicts handled by refresh

CODE EXAMPLE:
await OfflineService.initialize();

OfflineService.onConnectivityChanged().listen((isOnline) {
  if (isOnline) {
    // Sync pending actions
    await OfflineService.syncPendingActions();
  }
});
```

---

### **SECTION 6: STATE MANAGEMENT (RIVERPOD)**

**Q14: "Why did you choose Riverpod over Provider or GetX?"**

**Model Answer:**
```
RIVERPOD ADVANTAGES:
1. Compile-time safe (Provider is not)
2. Better TypeScript-like experience in Dart
3. Automatic dependency injection
4. Easier to test (no context needed)
5. FutureProvider for async data
6. StateNotifier for mutable state
7. Less boilerplate

COMPARISON:
Provider:
  - Okay, but runtime checks only
  - Need BuildContext everywhere
  - Hard to test

GetX:
  - Reactive, but magic behind scenes
  - Easy for beginners, complex later
  - Learning curve steep for advanced

Riverpod:
  - Functional approach
  - Clean separation
  - Better for larger apps
```

**Q15: "Show me how you use Riverpod."**

**Model Answer:**
```dart
// 1. SIMPLE PROVIDER (read-only value)
final helloProvider = Provider((ref) {
  return "Hello World";
});

// 2. FUTURE PROVIDER (async data)
final eventsProvider = FutureProvider<List<Event>>((ref) async {
  return EventService.getAllEvents();
});

// 3. STATE NOTIFIER PROVIDER (mutable state)
final userNotifierProvider = StateNotifierProvider<
    UserNotifier,
    User?
>((ref) {
  return UserNotifier(null);
});

class UserNotifier extends StateNotifier<User?> {
  UserNotifier(User? initial) : super(initial);
  
  void setUser(User user) {
    state = user;
  }
}

// 4. IN WIDGET
class EventsWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch provider
    final eventsAsync = ref.watch(eventsProvider);
    
    // Update notifier
    ref.read(userNotifierProvider.notifier).setUser(newUser);
    
    return eventsAsync.when(
      loading: () => Loading(),
      error: (err, st) => Error(err),
      data: (events) => EventList(events),
    );
  }
}
```

---

### **SECTION 7: QR CODE SYSTEM**

**Q16: "Explain your QR code attendance system."**

**Model Answer:**
```
HOW IT WORKS:

EVENT DAY:
1. Faculty opens "Generate QR"
2. App creates unique code: EVENT_ID | TIMESTAMP | SIGNATURE
3. QR displayed on faculty device
4. Students scan with phone camera
5. App decodes QR
6. Validates: signature correct?
7. Validates: same event?
8. Checks: user registered?
9. Checks: not already checked in?
10. If all valid: mark attendance in database
11. Show success message

SECURITY:
- QR includes HMAC signature
- Prevents tampering
- QR expires after event
- Unique per event
- Can't be reused

DATABASE UPDATE:
UPDATE registrations
SET checked_in = TRUE,
    checked_in_at = NOW()
WHERE user_id = 'xxx'
  AND event_id = 'yyy'
  AND checked_in = FALSE

PREVENTS:
✓ Duplicate check-ins
✓ Unauthorized check-ins
✓ Scanning same QR twice
```

---

### **SECTION 8: NOTIFICATION SYSTEM**

**Q17: "How do push notifications work?"**

**Model Answer:**
```
ARCHITECTURE:

Event happens in database
    ↓
App detects (Supabase listener)
    ↓
NotificationService.sendNotification()
    ↓
Firebase Cloud Messaging
    ↓
Mobile device receives
    ↓
Shows in notification tray
    ↓
User taps
    ↓
App opens, shows relevant screen

FLOW EXAMPLE (Event Approved):
1. Admin approves event in dashboard
2. EventService.approveEvent() called
3. Database updated: approval_status = 'approved'
4. Supabase triggers event
5. NotificationService sends FCM message
6. FCM sends to faculty's phone
7. Phone shows: "Event Approved!"
8. User taps, goes to event details

WHAT'S STORED:
- Notification saved in database
- So user can see history even if missed push
- FCM token stored in user profile
- Token refreshes when user logs in/out

PERMISSIONS:
- App asks for notification permission
- iOS: More restrictive
- Android: Less restrictive
- User can deny
```

---

### **SECTION 9: CHALLENGES & SOLUTIONS**

**Q18: "What was the hardest challenge you faced?"**

**Strong Answer:**
> "The hardest challenge was implementing atomic transactions for event registration 
> to prevent overbooking when multiple students register simultaneously.
> 
> **The Problem:**
> Imagine event capacity is 100. Two students hit register at exact same time.
> 1. Server checks capacity: 99/100 (okay, register both)
> 2. Student A registered successfully
> 3. Student B registered successfully
> 4. Now 101 registered (OVERFULL!)
> 
> **My Solution:**
> I used Supabase transactions with serializable isolation:
> ```sql
> BEGIN TRANSACTION;
>   SELECT current_attendees FROM events WHERE id = 'xxx' FOR UPDATE;
>   IF current_attendees < max_attendees THEN
>     INSERT INTO registrations...
>     UPDATE events SET current_attendees = current_attendees + 1
>   ELSE
>     ROLLBACK;
>   END IF;
> COMMIT;
> ```
> 
> This ensures:
> - Only one registration processes at a time
> - Capacity check and registration are atomic (all or nothing)
> - If full, registration rejected immediately
> 
> **Result:** Never overfull, even with thousands of concurrent registrations."

---

**Q19: "What would you improve if you had more time?"**

**Great Answer:**
> "Several things:
> 
> 1. **Testing**
>    - Add unit tests for all services
>    - Integration tests for database operations
>    - UI tests for critical flows
>    - Currently: 0% test coverage → Goal: 80%
> 
> 2. **Performance**
>    - Add database indexing on frequently-queried columns
>    - Implement Redis caching for expensive queries
>    - Optimize image loading (lazy load)
>    - Currently decent but could be faster
> 
> 3. **Advanced Features**
>    - Event recommendations (ML)
>    - Video streaming for events
>    - Payment integration for paid events
>    - Event cancellation refund logic
> 
> 4. **DevOps**
>    - CI/CD pipeline (automated testing on push)
>    - Automated deployment
>    - Error tracking (Sentry)
>    - Analytics (Mixpanel)
> 
> 5. **Documentation**
>    - API docs (Swagger/OpenAPI)
>    - Architecture diagrams
>    - Setup guide for developers
>    - Video tutorial"

---

### **SECTION 10: TECHNICAL DEEP DIVES**

**Q20: "What's the most complex feature you built?"**

**Strong Answer:**
> "The expense approval workflow because it involves multiple systems:
> 
> 1. **File Upload:**
>    - User picks image (receipt)
>    - Compress image to reduce size
>    - Upload to Supabase Storage
>    - Get public URL back
> 
> 2. **Database Record:**
>    - Insert expense with receipt URL
>    - Set approved = false (pending)
>    - Store created_by for audit trail
> 
> 3. **Notifications:**
>    - Send push notification to all admins
>    - Save in notifications table
>    - Email to admin
> 
> 4. **Admin Review:**
>    - Admin opens approval queue
>    - Real-time updates via Supabase streams
>    - Admin taps approve/reject
> 
> 5. **Feedback:**
>    - Notification sent back to faculty
>    - Status updated in database
>    - Email confirmation
> 
> The complexity was coordinating:
>    - File system
>    - Multiple database tables
>    - Multiple notification channels
>    - Real-time updates
>    - Error handling at each step"

---

**Q21: "How do you handle errors?"**

**Model Answer:**
```dart
// LAYERED ERROR HANDLING:

// 1. TRY-CATCH at service level
Future<void> registerForEvent(String userId, String eventId) async {
  try {
    // Business logic
    validateUser(userId);
    validateEvent(eventId);
    await insertRegistration();
  } on ValidationException catch (e) {
    LoggingService.warning('Validation failed: $e');
    rethrow; // Let UI handle
  } on NetworkException catch (e) {
    LoggingService.error('Network error: $e');
    // Fallback to cache
    return cachedRegistrations;
  } on DatabaseException catch (e) {
    LoggingService.error('Database error: $e');
    // Maybe retry logic
    throw AppException('Registration failed. Please try again.');
  } catch (e) {
    LoggingService.error('Unknown error: $e');
    throw AppException('Unexpected error occurred');
  }
}

// 2. IN PROVIDER
final registrationProvider = FutureProvider((ref) async {
  try {
    return await RegistrationService.registerForEvent(userId, eventId);
  } catch (e) {
    return null; // Will show error in widget
  }
});

// 3. IN WIDGET
.when(
  loading: () => CircularProgressIndicator(),
  error: (error, stack) => ErrorWidget(
    message: error.toString(),
    onRetry: () => ref.refresh(registrationProvider),
  ),
  data: (data) => SuccessWidget(data: data),
)
```

---

### **SECTION 11: PERFORMANCE & OPTIMIZATION**

**Q22: "How do you optimize app performance?"**

**Model Answer:**
```
1. PAGINATION
   - Don't fetch all 10,000 events at once
   - Fetch 20 at a time
   - Load more when user scrolls
   - Code: getEventsPaginated(page: 0, pageSize: 20)

2. CACHING
   - Cache API responses locally (Hive)
   - No need to refetch same data
   - 1000x faster than network

3. LAZY LOADING
   - Images not downloaded until visible
   - Using CachedNetworkImage widget

4. IMAGE OPTIMIZATION
   - Compress images before upload
   - Different sizes for different devices
   - Webp format (smaller than jpg)

5. DATABASE INDEXING
   - Index frequently-searched columns
   - Queries run 100x faster
   - Example: INDEX on (approval_status, created_at)

6. ASSET OPTIMIZATION
   - Minimize app size with Tree Shaking
   - Remove unused dependencies
   - ~50MB app download

7. MEMORY MANAGEMENT
   - Dispose of listeners/streams
   - Clear cache on logout
   - Avoid memory leaks

BENCHMARK:
- First load: ~2 seconds
- Cached load: ~200ms
- Database query: ~20ms
- API roundtrip: ~100ms
```

---

### **SECTION 12: DEPLOYMENT & TESTING**

**Q23: "How would you deploy this to production?"**

**Model Answer:**
```
STEPS:

1. ENVIRONMENT SETUP
   - Separate dev, staging, prod databases
   - Different API keys for each
   - .env.production with prod credentials

2. BUILD APK/APP BUNDLE
   flutter build apk --release
   flutter build appbundle --release
   
   - Removes debugging info
   - Optimizes code size
   - Shrinks ~50MB to ~15MB

3. CODE SIGNING
   - Sign APK with release key
   - Store key securely (not in git)
   - Key used to update app later

4. TESTING
   - Run full test suite
   - Load testing (many concurrent users)
   - Manual QA checklist
   - Beta testing with real users

5. DEPLOYMENT
   - Google Play Console
   - Upload app bundle
   - Fill metadata (description, screenshots)
   - Set pricing/distribution
   - Submit for review (24-48 hours)
   - Once approved, live in Play Store

6. MONITORING
   - Set up error tracking (Sentry)
   - Monitor crashes
   - Track analytics (user behavior)
   - Prepare update for bugs

CURRENT STATE:
- Not deployed yet (FYP phase)
- Could deploy in 1 day
```

---

**Q24: "Do you have tests?"**

**Honest Answer:**
> "Currently, the app doesn't have automated tests - it was a time constraint during FYP.
> However, I manually tested:
> - All authentication flows
> - Event creation and approval
> - Registration and QR scanning
> - Offline functionality
> - Error scenarios
> 
> If given more time, I would add:
> - Unit tests for all services (90% coverage)
> - Widget tests for critical UI flows
> - Integration tests for API calls
> - Using Dart's test framework
> 
> Example test I would write:
> ```dart
> test('Cannot register when event is full', () async {
>   Event event = Event(..., maxAttendees: 1, currentAttendees: 1);
>   expect(
>     () => RegistrationService.registerForEvent(userId, event.id),
>     throwsException,
>   );
> });
> ```"

---

## 🎬 PRESENTATION TIPS

### **Opening (First 30 seconds):**
1. Stand confidently
2. Smile
3. Make eye contact
4. Speak clearly and slow
5. State project name: "Event Sphere"
6. State what it does in one sentence
7. Take a breath

### **Demo (Most Important):**
1. Have it working before evaluation
2. Have WiFi + mobile hotspot as backup
3. Know what's clickable
4. Walk through student journey first (simplest)
5. Then faculty journey
6. Then admin
7. Show real data, not dummy
8. Keep demo to 5-10 minutes

### **When They Ask Questions:**
1. Listen fully before answering
2. Pause for 2 seconds before answering
3. Answer specifically (not vague)
4. Give examples
5. If you don't know, say "That's a great question, but I haven't explored that yet. However, my approach would be..."
6. Don't make up answers

### **Body Language:**
- ✅ Stand or sit upright
- ✅ Hands visible (not crossed)
- ✅ Make eye contact
- ❌ Don't pace
- ❌ Don't fidget
- ❌ Don't look at feet

### **Handling Tough Questions:**
> "That's a great question..."
> [2 second pause to think]
> [Give thoughtful answer]
> "Does that make sense?"

---

## 💪 CONFIDENCE BOOSTERS

**Remember:**
1. You built this from scratch
2. You understand every line of code
3. You've solved real problems
4. Your app actually works
5. You can explain concepts clearly
6. It's a solid project for FYP level

**You've got this! 🚀**

---

## 📝 FINAL CHECKLIST

Before evaluation:

- [ ] App runs without errors
- [ ] Test all main features
- [ ] Test offline mode
- [ ] Charge phone 100%
- [ ] Have backup power bank
- [ ] Have screenshots as fallback
- [ ] Practice demo 3 times
- [ ] Know answer to: "Why did you choose..."
- [ ] Know answer to: "What would you improve..."
- [ ] Know your database schema
- [ ] Know your architecture layers
- [ ] Be ready to show code
- [ ] Have repository link ready
- [ ] Speak clearly and confidently
- [ ] Show enthusiasm for project

---

**Good luck! You're ready to deliver professionally! 💯**
