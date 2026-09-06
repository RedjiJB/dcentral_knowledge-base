---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 684e1139-6712-4d86-a1af-0892f6f7f211
original_filename: OS-CONCIERGE_Logical_Topology.md
created_at: 2026-03-04T20:34:59.927158+00:00
content_hash: c4db718d53f7
topic: opensecure-os-concierge-topology
consolidated_into: docs/DC-OPENSECURE-OS-CONCIERGE-TOPOLOGY-RECONCILED-001.md
---

# OS-CONCIERGE Logical Topology
## Intelligent Concierge System Architecture & Data Flow Patterns

**Document Type**: Logical Architecture Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Solution Architects, Product Managers, Developers

---

## Executive Summary

### Architectural Philosophy

OS-CONCIERGE implements an **AI-first, multi-tenant architecture** designed to deliver personalized concierge services across multiple properties. Key principles:

- **AI-Powered Interactions**: Natural language chatbot handles 80% of inquiries
- **Context-Aware Responses**: System knows property details, amenities, user history
- **Multi-Tenant Isolation**: Each property has isolated data while sharing infrastructure
- **Event-Driven Architecture**: Real-time notifications and integrations
- **API-First Design**: Every feature accessible via REST/GraphQL APIs

---

## Logical Architecture Overview

### Six-Layer Architecture

```
┌────────────────────────────────────────────────────────────────┐
│            LAYER 6: USER EXPERIENCE                            │
├────────────────────────────────────────────────────────────────┤
│ • Kiosk UI (React)                                             │
│ • Mobile App (Flutter)                                         │
│ • Web Portal (React)                                           │
│ • Voice Interface (Alexa/Google Home)                          │
└────────────────────────┬───────────────────────────────────────┘
                         │ HTTPS / WebSocket / GraphQL
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 5: API GATEWAY                                │
├────────────────────────────────────────────────────────────────┤
│ Kong API Gateway                                               │
│ • Authentication (JWT)                                         │
│ • Rate Limiting                                                │
│ • Request Routing                                              │
│ • Load Balancing                                               │
└────────────────────────┬───────────────────────────────────────┘
                         │ Internal Services
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 4: APPLICATION SERVICES                       │
├────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐  ┌──────────────────┐                    │
│ │ AI Chatbot       │  │ Visitor Mgmt     │                    │
│ │ (Rasa + GPT-4)   │  │ Service          │                    │
│ └──────────────────┘  └──────────────────┘                    │
│                                                                 │
│ ┌──────────────────┐  ┌──────────────────┐                    │
│ │ Smart Lock       │  │ Service Request  │                    │
│ │ Controller       │  │ Management       │                    │
│ └──────────────────┘  └──────────────────┘                    │
│                                                                 │
│ ┌──────────────────┐  ┌──────────────────┐                    │
│ │ Notification     │  │ Analytics        │                    │
│ │ Service          │  │ Engine           │                    │
│ └──────────────────┘  └──────────────────┘                    │
└────────────────────────┬───────────────────────────────────────┘
                         │ Message Bus (NATS)
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 3: INTEGRATION LAYER                          │
├────────────────────────────────────────────────────────────────┤
│ • Property Management Systems (PMS)                            │
│ • CRM Integration (HubSpot, Salesforce)                        │
│ • Smart Building APIs (BACnet, Modbus)                         │
│ • Payment Gateways (Stripe, Square)                            │
│ • External APIs (Google Maps, Weather, OpenAI)                 │
└────────────────────────┬───────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 2: DATA SERVICES                              │
├────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│ │ PostgreSQL   │  │ MongoDB      │  │ Redis        │         │
│ │ (Relational) │  │ (Chat Logs)  │  │ (Cache)      │         │
│ └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│ ┌──────────────┐  ┌──────────────┐                            │
│ │Elasticsearch │  │ MinIO        │                            │
│ │ (Search)     │  │ (Files)      │                            │
│ └──────────────┘  └──────────────┘                            │
└────────────────────────┬───────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 1: PROPERTY EDGE                              │
├────────────────────────────────────────────────────────────────┤
│ • Kiosks (local processing)                                    │
│ • Smart Locks                                                  │
│ • Access Control Systems                                       │
│ • Building Management Systems                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Relationships

### Core Entity Model

```
┌─────────────┐
│  PROPERTY   │
├─────────────┤
│ id          │ PK
│ name        │
│ address     │
│ timezone    │
└──────┬──────┘
       │ 1:N
       │
┌──────▼──────┐
│   UNIT      │
├─────────────┤
│ id          │ PK
│ property_id │ FK
│ unit_number │
│ floor       │
│ type        │ (studio, 1br, 2br, penthouse)
└──────┬──────┘
       │ 1:N
       │
┌──────▼──────┐
│  RESIDENT   │
├─────────────┤
│ id          │ PK
│ unit_id     │ FK
│ name        │
│ email       │
│ phone       │
│ move_in_date│
└──────┬──────┘
       │ 1:N
       │
┌──────▼─────────┐
│    VISITOR     │
├────────────────┤
│ id             │ PK
│ property_id    │ FK
│ host_unit_id   │ FK
│ name           │
│ company        │
│ check_in_time  │
│ check_out_time │
│ access_code    │
│ photo_url      │
└──────┬─────────┘
       │
       │ N:M (via ACCESS_EVENTS)
       │
┌──────▼───────────┐
│  ACCESS_POINT    │
├──────────────────┤
│ id               │ PK
│ property_id      │ FK
│ name             │ (main_entrance, gym, roof, etc.)
│ lock_type        │ (smart_lock, keypad, card_reader)
│ integration_id   │ (device-specific ID)
└──────────────────┘

┌────────────────┐
│CHATBOT_SESSION │
├────────────────┤
│ id             │ PK
│ property_id    │ FK
│ user_type      │ (resident, visitor, guest)
│ user_id        │ (nullable FK)
│ start_time     │
│ end_time       │
│ message_count  │
└────────┬───────┘
         │ 1:N
         │
┌────────▼───────┐
│ CHAT_MESSAGE   │
├────────────────┤
│ id             │ PK
│ session_id     │ FK
│ timestamp      │
│ role           │ (user, bot)
│ message_text   │
│ intent         │ (detected by NLU)
│ entities       │ JSON (key-value pairs)
│ confidence     │ 0.0 - 1.0
└────────────────┘

┌──────────────────┐
│ SERVICE_REQUEST  │
├──────────────────┤
│ id               │ PK
│ property_id      │ FK
│ unit_id          │ FK (nullable)
│ requester_id     │ FK → RESIDENT
│ category         │ (maintenance, amenity, concierge)
│ description      │
│ priority         │ (low, medium, high, urgent)
│ status           │ (open, in_progress, resolved)
│ created_at       │
│ resolved_at      │
└──────────────────┘
```

---

## AI Chatbot Architecture

### Conversational Flow

```
┌────────────────────────────────────────────────────────────────┐
│               CHATBOT PROCESSING PIPELINE                       │
└────────────────────────────────────────────────────────────────┘

User Input: "What time does the gym close on Sundays?"
        │
        ▼
┌─────────────────────────┐
│ Natural Language        │
│ Understanding (Rasa)    │
│                         │
│ Intent Detection:       │
│ → "amenity_hours"       │
│                         │
│ Entity Extraction:      │
│ → amenity: "gym"        │
│ → day: "sunday"         │
│                         │
│ Confidence: 0.95        │
└──────────┬──────────────┘
           │
           │ IF confidence < 0.7 → Fallback to GPT-4
           │ ELSE → Continue with Rasa
           ▼
┌─────────────────────────┐
│ Context Management      │
│                         │
│ Retrieve:               │
│ • Property ID (from     │
│   kiosk/session)        │
│ • Previous messages     │
│ • User preferences      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Action Execution        │
│                         │
│ Query Knowledge Base:   │
│ SELECT hours            │
│ FROM amenities          │
│ WHERE property_id = X   │
│   AND name = 'gym'      │
│   AND day = 'sunday'    │
│                         │
│ Result: "6am - 10pm"    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Response Generation     │
│                         │
│ Template:               │
│ "The {amenity} is open  │
│  {hours} on {day}."     │
│                         │
│ Generated Response:     │
│ "The gym is open 6am -  │
│  10pm on Sundays."      │
└──────────┬──────────────┘
           │
           │ Log to MongoDB (chat history)
           │ Update analytics (intent frequency)
           ▼
Display to User

Latency Breakdown:
├── NLU Processing: 200ms
├── Context Retrieval: 50ms
├── Database Query: 100ms
├── Response Generation: 50ms
└── Total: 400ms (under 0.5s target)
```

### Multi-Turn Conversation State

```python
class ConversationState:
    """
    Maintains conversation context across multiple turns
    """
    def __init__(self, session_id):
        self.session_id = session_id
        self.property_id = None
        self.user_id = None
        self.context = {
            'last_intent': None,
            'entities': {},
            'awaiting_input': None,  # For slot-filling
            'conversation_history': []
        }
    
    def update(self, intent, entities, response):
        """Update state after each turn"""
        self.context['last_intent'] = intent
        self.context['entities'].update(entities)
        self.context['conversation_history'].append({
            'role': 'user',
            'intent': intent,
            'timestamp': datetime.now()
        })
        self.context['conversation_history'].append({
            'role': 'bot',
            'response': response,
            'timestamp': datetime.now()
        })
        
        # Save to Redis (TTL: 24 hours)
        redis.setex(
            f"conversation:{self.session_id}",
            86400,
            json.dumps(self.context)
        )

# Example multi-turn conversation:

Turn 1:
User: "I need to schedule a service request"
Bot: "I can help with that! What kind of service do you need?"
State: {awaiting_input: 'service_type'}

Turn 2:
User: "Air conditioning not working"
Bot: "Got it - AC repair. What's your unit number?"
State: {
  service_type: 'ac_repair',
  awaiting_input: 'unit_number'
}

Turn 3:
User: "Unit 12A"
Bot: "Perfect. I'll create a maintenance request for AC repair 
     in Unit 12A. Is this urgent?"
State: {
  service_type: 'ac_repair',
  unit_number: '12A',
  awaiting_input: 'priority'
}

Turn 4:
User: "Yes, it's very hot"
Bot: "Request submitted as URGENT. Maintenance will contact 
     you within 2 hours. Request ID: #5678"
State: {
  service_type: 'ac_repair',
  unit_number: '12A',
  priority: 'urgent',
  request_id: 5678
}
```

### Intent Classification

```python
# Rasa NLU Training Data Example

intents = {
    'amenity_hours': {
        'examples': [
            "What time does the [gym](amenity) open?",
            "When is the [pool](amenity) closed?",
            "Is the [lounge](amenity) open on [Sunday](day)?",
            "What are the [gym](amenity) hours?"
        ],
        'action': 'action_query_amenity_hours'
    },
    
    'directions': {
        'examples': [
            "How do I get to the [gym](amenity)?",
            "Where is the [mailroom](amenity)?",
            "Directions to [rooftop](amenity)",
            "Take me to the [parking garage](amenity)"
        ],
        'action': 'action_provide_directions'
    },
    
    'service_request': {
        'examples': [
            "I need maintenance",
            "My [AC](issue) is broken",
            "Report a problem with [plumbing](issue)",
            "Submit a service request"
        ],
        'action': 'action_create_service_request'
    },
    
    'visitor_checkin': {
        'examples': [
            "I'm here to visit [John Smith](resident)",
            "Check in a visitor",
            "Guest arrival",
            "I'm visiting unit [12A](unit)"
        ],
        'action': 'action_visitor_checkin'
    },
    
    'local_search': {
        'examples': [
            "Where's a good [restaurant](business_type) nearby?",
            "Coffee shops near here",
            "Find a [pharmacy](business_type)",
            "What [bars](business_type) are close?"
        ],
        'action': 'action_local_search'
    },
    
    'package_notification': {
        'examples': [
            "I have a package",
            "Delivery arrived",
            "Package for unit [12A](unit)",
            "Log a delivery"
        ],
        'action': 'action_log_package'
    }
}

# Custom Actions (Python)

class ActionQueryAmenityHours(Action):
    def name(self):
        return "action_query_amenity_hours"
    
    def run(self, dispatcher, tracker, domain):
        # Extract entities
        amenity = tracker.get_slot('amenity')
        day = tracker.get_slot('day') or 'today'
        property_id = tracker.sender_id.split('_')[0]  # From session
        
        # Query database
        hours = db.query(
            "SELECT hours FROM amenities "
            "WHERE property_id = %s AND name = %s AND day = %s",
            (property_id, amenity, day)
        )
        
        if hours:
            response = f"The {amenity} is open {hours[0]} on {day}."
        else:
            response = f"I don't have hours for the {amenity}. " \
                      f"Let me connect you with the front desk."
        
        dispatcher.utter_message(text=response)
        return []
```

---

## Visitor Management Flow

### Check-In Process

```
┌────────────────────────────────────────────────────────────────┐
│           VISITOR CHECK-IN STATE MACHINE                        │
└────────────────────────────────────────────────────────────────┘

Initial State: VISITOR_ARRIVING
        │
        │ Visitor approaches kiosk
        ▼
State: COLLECTING_INFO
        │
        │ System collects:
        │ • Name
        │ • Company
        │ • Host (unit number or name)
        │ • Photo (optional)
        │ • Purpose of visit
        │
        ▼
State: VALIDATING_HOST
        │
        │ Query database:
        │ • Lookup unit by number or resident name
        │ • Verify unit is occupied
        │ • Get host contact info
        │
    ┌───┴───┐
    │       │
  VALID   INVALID
    │       │
    │       └──► State: ERROR
    │           Display: "Unit not found. Please verify."
    │           Retry or call front desk
    ▼
State: NOTIFYING_HOST
        │
        │ PARALLEL notifications:
        │ ├── SMS: "Visitor John Doe is here"
        │ ├── Email: [Details + approve/deny links]
        │ ├── Push: Mobile app notification
        │ └── Phone Call: If no response in 2 min
        │
        │ Wait for response (timeout: 5 minutes)
        ▼
State: AWAITING_APPROVAL
        │
    ┌───┴───┐
    │       │
APPROVED  DENIED / TIMEOUT
    │       │
    │       └──► State: REJECTED
    │           Display: "Host declined or unavailable"
    │           Options: Call host, call front desk
    ▼
State: GENERATING_ACCESS
        │
        │ Generate:
        │ • Temporary access code (4 digits)
        │ • QR code (for mobile access)
        │ • Valid duration (default: 4 hours)
        │ • Scope (main entrance + host floor/unit)
        │
        │ Store in database:
        │ INSERT INTO visitor_access ...
        │
        ▼
State: ACCESS_GRANTED
        │
        │ Display/Print badge:
        │ • Visitor name
        │ • Host name & unit
        │ • QR code + access code
        │ • Valid until [time]
        │
        │ Enable access:
        │ • Program smart locks
        │ • Update access control system
        │ • Remove elevator floor restrictions
        │
        ▼
State: CHECKED_IN
        │
        │ Log event:
        │ {
        │   visitor_id, host_unit, check_in_time,
        │   access_code, photo, notification_log
        │ }
        │
        │ Send confirmation:
        │ • SMS to visitor (if provided phone)
        │ • Email to host
        │
        ▼
[Visitor proceeds to unit]
        │
        │ At check-out (optional):
        │ • Visitor presses "Check Out" at kiosk
        │ • OR System auto-expires access after duration
        ▼
State: CHECKED_OUT
        │
        │ Revoke access:
        │ • Delete access code from locks
        │ • Restore elevator restrictions
        │ • Log check-out time
```

### Access Code Management

```python
class AccessCodeManager:
    def __init__(self):
        self.code_length = 4
        self.valid_duration_hours = 4
    
    def generate_code(self, visitor_id, property_id, host_unit):
        """Generate unique temporary access code"""
        
        # Generate random 4-digit code
        while True:
            code = f"{random.randint(0, 9999):04d}"
            
            # Check uniqueness (no collisions with active codes)
            existing = db.query(
                "SELECT id FROM visitor_access "
                "WHERE property_id = %s AND access_code = %s "
                "AND expires_at > NOW()",
                (property_id, code)
            )
            
            if not existing:
                break  # Code is unique
        
        # Calculate expiration
        expires_at = datetime.now() + timedelta(
            hours=self.valid_duration_hours
        )
        
        # Store in database
        access_id = db.execute(
            "INSERT INTO visitor_access "
            "(visitor_id, property_id, host_unit, access_code, "
            " created_at, expires_at, status) "
            "VALUES (%s, %s, %s, %s, NOW(), %s, 'ACTIVE')",
            (visitor_id, property_id, host_unit, code, expires_at)
        )
        
        # Program smart locks
        self.program_locks(property_id, code, expires_at)
        
        return {
            'access_id': access_id,
            'code': code,
            'expires_at': expires_at
        }
    
    def program_locks(self, property_id, code, expires_at):
        """Send code to all applicable smart locks"""
        
        # Get all locks for this property
        locks = db.query(
            "SELECT id, integration_id, lock_type "
            "FROM access_points "
            "WHERE property_id = %s AND lock_type = 'smart_lock'",
            (property_id,)
        )
        
        for lock in locks:
            if lock['lock_type'] == 'zwave':
                self.program_zwave_lock(
                    lock['integration_id'], code, expires_at
                )
            elif lock['lock_type'] == 'zigbee':
                self.program_zigbee_lock(
                    lock['integration_id'], code, expires_at
                )
            elif lock['lock_type'] == 'wifi':
                self.program_wifi_lock(
                    lock['integration_id'], code, expires_at
                )
    
    def program_zwave_lock(self, lock_id, code, expires_at):
        """Program Z-Wave lock via Home Assistant"""
        
        # Find empty user code slot (1-100)
        slot = self.find_empty_slot(lock_id)
        
        # Home Assistant API call
        requests.post(
            'http://homeassistant.local:8123/api/services/lock/set_usercode',
            json={
                'entity_id': f'lock.{lock_id}',
                'code_slot': slot,
                'usercode': code,
                'expires_at': expires_at.isoformat()
            },
            headers={'Authorization': f'Bearer {HA_TOKEN}'}
        )
        
        # Schedule auto-deletion job
        scheduler.schedule(
            task='delete_access_code',
            args={'lock_id': lock_id, 'slot': slot},
            run_at=expires_at
        )
    
    def revoke_access(self, access_id):
        """Revoke visitor access"""
        
        # Get access record
        access = db.query(
            "SELECT * FROM visitor_access WHERE id = %s",
            (access_id,)
        )
        
        # Delete from all locks
        locks = db.query(
            "SELECT id, integration_id, lock_type "
            "FROM access_points "
            "WHERE property_id = %s",
            (access['property_id'],)
        )
        
        for lock in locks:
            self.delete_code_from_lock(
                lock['integration_id'],
                access['access_code']
            )
        
        # Update database
        db.execute(
            "UPDATE visitor_access "
            "SET status = 'REVOKED', revoked_at = NOW() "
            "WHERE id = %s",
            (access_id,)
        )
```

---

## Service Request Management

### Request Lifecycle

```
┌────────────────────────────────────────────────────────────────┐
│           SERVICE REQUEST WORKFLOW                              │
└────────────────────────────────────────────────────────────────┘

Trigger Points:
├── Chatbot conversation
├── Kiosk manual form
├── Mobile app submission
├── Phone call (transcribed by staff)
└── Email (parsed automatically)

        │
        ▼
State: REQUEST_CREATED
{
  id: 5678,
  property_id: 1,
  unit_id: 45,  // Unit 12A
  requester: "John Smith",
  category: "maintenance",
  subcategory: "hvac",
  description: "AC not cooling, makes loud noise",
  priority: "high",  // Auto-determined or user-selected
  photos: ["s3://bucket/requests/5678/photo1.jpg"],
  created_at: "2024-12-08T14:00:00Z",
  status: "open"
}
        │
        │ Saved to database
        │ Event published to NATS: "service_request.created"
        ▼
PARALLEL Processing:

Branch 1: Assignment
        │
        ▼
Determine Assignment:
├── IF urgent (AC, heat, water, elevator): Immediate dispatch
├── IF high priority: Assign within 2 hours
├── IF normal: Assign within 24 hours
└── IF low: Assign within 72 hours
        │
        │ Query available technicians
        │ SELECT * FROM staff
        │ WHERE role = 'maintenance'
        │   AND property_id = 1
        │   AND status = 'available'
        │   AND skills LIKE '%hvac%'
        ▼
Assign to: "Mike Johnson" (Maintenance Tech)
        │
        │ UPDATE service_requests
        │ SET assigned_to = 'Mike Johnson',
        │     status = 'assigned'
        │
        │ Notification sent (SMS/Email):
        │ "New request #5678: AC repair in Unit 12A (HIGH)"
        ▼

Branch 2: Requester Notification
        │
        ▼
SMS to John Smith:
"Your service request (#5678) has been submitted. 
 A technician will be assigned shortly."
        │
Email confirmation:
Subject: "Service Request Submitted - #5678"
Body: [Details + tracking link]
        │
        ▼

Technician Responds:
        │
        │ Option 1: Accept
        │ POST /api/service-requests/5678/accept
        │ status → "in_progress"
        │
        │ SMS to requester:
        │ "Mike Johnson is on the way. ETA: 30 minutes"
        ▼
Work Performed:
        │
        │ Technician arrives, performs repair
        │ Logs actions in mobile app:
        │ • Work performed: "Replaced compressor relay"
        │ • Parts used: "Relay $15, Labor $50"
        │ • Time spent: 1 hour
        │ • Photos: Before/After
        ▼
State: REQUEST_RESOLVED
        │
        │ UPDATE service_requests
        │ SET status = 'resolved',
        │     resolution = 'Replaced compressor relay',
        │     resolved_at = NOW()
        │
        │ SMS to requester:
        │ "Your AC repair is complete. Please rate your experience"
        ▼
Feedback Request:
        │
        │ Link in SMS → survey form:
        │ • How satisfied are you? (1-5 stars)
        │ • Was the issue resolved? (Yes/No)
        │ • Any additional comments?
        │
        │ Feedback saved for analytics
        ▼
State: CLOSED
```

---

## API Architecture

### REST API Endpoints

```
BASE URL: https://api.concierge.company.com/v1

PROPERTIES
├── GET    /properties              List all properties (admin only)
├── GET    /properties/{id}         Get property details
├── POST   /properties              Create property (admin)
├── PUT    /properties/{id}         Update property
└── DELETE /properties/{id}         Delete property (soft delete)

RESIDENTS
├── GET    /properties/{prop_id}/residents    List residents
├── GET    /residents/{id}                    Get resident details
├── POST   /residents                         Create resident
├── PUT    /residents/{id}                    Update resident
└── DELETE /residents/{id}                    Remove resident

VISITORS
├── POST   /visitors/checkin         Check in visitor
├── GET    /visitors                  List visitors (filtered)
├── GET    /visitors/{id}            Get visitor details
├── POST   /visitors/{id}/checkout   Check out visitor
└── GET    /visitors/{id}/access     Get access details

CHATBOT
├── POST   /chat/sessions            Start new chat session
├── POST   /chat/sessions/{id}/messages  Send message
├── GET    /chat/sessions/{id}       Get session history
└── DELETE /chat/sessions/{id}       End session

SERVICE REQUESTS
├── GET    /service-requests         List requests (filtered)
├── GET    /service-requests/{id}    Get request details
├── POST   /service-requests         Create request
├── PUT    /service-requests/{id}    Update request
├── POST   /service-requests/{id}/assign    Assign technician
├── POST   /service-requests/{id}/resolve   Mark resolved
└── POST   /service-requests/{id}/feedback  Submit feedback

AMENITIES
├── GET    /properties/{prop_id}/amenities   List amenities
├── GET    /amenities/{id}                   Get details & hours
├── POST   /amenities/{id}/reserve           Reserve amenity
└── DELETE /amenities/reservations/{id}      Cancel reservation

ACCESS CONTROL
├── POST   /access/grant             Grant temporary access
├── POST   /access/revoke            Revoke access
├── GET    /access/events            Access event log
└── GET    /access/active            List active access grants

NOTIFICATIONS
├── POST   /notifications/send       Send notification
├── GET    /notifications/{id}       Get notification status
└── GET    /notifications/history    Notification history
```

### GraphQL API (Alternative)

```graphql
type Property {
  id: ID!
  name: String!
  address: String!
  units: [Unit!]!
  amenities: [Amenity!]!
  activeVisitors: [Visitor!]!
}

type Unit {
  id: ID!
  property: Property!
  unitNumber: String!
  floor: Int!
  residents: [Resident!]!
}

type Resident {
  id: ID!
  unit: Unit!
  name: String!
  email: String!
  phone: String!
  serviceRequests: [ServiceRequest!]!
}

type Visitor {
  id: ID!
  property: Property!
  name: String!
  company: String
  hostUnit: Unit!
  checkInTime: DateTime!
  checkOutTime: DateTime
  accessCode: String
  photo: String
}

type ServiceRequest {
  id: ID!
  property: Property!
  unit: Unit
  requester: Resident!
  category: String!
  description: String!
  priority: Priority!
  status: RequestStatus!
  assignedTo: Staff
  createdAt: DateTime!
  resolvedAt: DateTime
}

enum Priority {
  LOW
  NORMAL
  HIGH
  URGENT
}

enum RequestStatus {
  OPEN
  ASSIGNED
  IN_PROGRESS
  RESOLVED
  CLOSED
}

# Queries
type Query {
  property(id: ID!): Property
  properties(limit: Int, offset: Int): [Property!]!
  
  visitor(id: ID!): Visitor
  activeVisitors(propertyId: ID!): [Visitor!]!
  
  serviceRequest(id: ID!): ServiceRequest
  serviceRequests(
    propertyId: ID
    status: RequestStatus
    priority: Priority
  ): [ServiceRequest!]!
}

# Mutations
type Mutation {
  checkinVisitor(input: VisitorCheckinInput!): Visitor!
  checkoutVisitor(id: ID!): Visitor!
  
  createServiceRequest(input: ServiceRequestInput!): ServiceRequest!
  assignServiceRequest(id: ID!, staffId: ID!): ServiceRequest!
  resolveServiceRequest(id: ID!, resolution: String!): ServiceRequest!
  
  grantAccess(input: AccessGrantInput!): AccessGrant!
  revokeAccess(id: ID!): Boolean!
}

# Subscriptions (Real-time)
type Subscription {
  visitorCheckedIn(propertyId: ID!): Visitor!
  serviceRequestCreated(propertyId: ID!): ServiceRequest!
  serviceRequestUpdated(id: ID!): ServiceRequest!
}

# Example Usage:
query GetPropertyOverview($propertyId: ID!) {
  property(id: $propertyId) {
    name
    activeVisitors {
      name
      hostUnit {
        unitNumber
      }
      checkInTime
    }
    units {
      unitNumber
      residents {
        name
        serviceRequests(status: OPEN) {
          description
          priority
        }
      }
    }
  }
}
```

---

## Event-Driven Architecture

### Message Bus (NATS)

```
Event Topics:

visitor.*
├── visitor.checkedin        Visitor checked in
├── visitor.checkedout       Visitor checked out
├── visitor.approved         Host approved visitor
├── visitor.denied           Host denied visitor
└── visitor.expired          Access code expired

service_request.*
├── service_request.created  New request submitted
├── service_request.assigned Assigned to technician
├── service_request.updated  Status changed
└── service_request.resolved Request completed

access.*
├── access.granted           Temporary access granted
├── access.revoked           Access revoked
├── access.used              Door unlocked with code
└── access.denied            Invalid code attempted

amenity.*
├── amenity.reserved         Amenity reserved
├── amenity.cancelled        Reservation cancelled
└── amenity.occupied         Amenity in use (sensor)

chatbot.*
├── chatbot.intent_detected  Intent classified
├── chatbot.fallback         Low confidence, GPT-4 used
└── chatbot.session_ended    Conversation ended

# Event Consumers:

Analytics Service
├── Subscribes: visitor.*, service_request.*, chatbot.*
└── Aggregates: Daily/weekly/monthly metrics

Notification Service
├── Subscribes: visitor.approved, service_request.assigned
└── Sends: SMS, Email, Push notifications

Audit Logger
├── Subscribes: access.*, visitor.*
└── Writes: Immutable audit trail

CRM Integration
├── Subscribes: visitor.checkedin, service_request.created
└── Syncs: To HubSpot/Salesforce

# Example Event:

Topic: visitor.checkedin
Payload: {
  "event_id": "evt_12345",
  "timestamp": "2024-12-08T14:23:45Z",
  "property_id": 1,
  "visitor": {
    "id": 678,
    "name": "John Doe",
    "company": "ABC Corp",
    "host_unit": "12A",
    "access_code": "1234#",
    "expires_at": "2024-12-08T18:23:45Z"
  }
}
```

---

## Analytics & Reporting

### Key Metrics

```python
class ConciergeAnalytics:
    def daily_metrics(self, property_id, date):
        """Calculate daily operational metrics"""
        
        return {
            'visitors': {
                'total_checkins': self.count_visitor_checkins(property_id, date),
                'avg_approval_time': self.avg_approval_time(property_id, date),
                'denied_count': self.count_visitor_denials(property_id, date)
            },
            
            'chatbot': {
                'total_sessions': self.count_chat_sessions(property_id, date),
                'total_messages': self.count_chat_messages(property_id, date),
                'avg_session_length': self.avg_session_length(property_id, date),
                'top_intents': self.top_intents(property_id, date, limit=5),
                'fallback_rate': self.fallback_rate(property_id, date),
                'resolution_rate': self.resolution_rate(property_id, date)
            },
            
            'service_requests': {
                'total_created': self.count_requests(property_id, date),
                'avg_resolution_time': self.avg_resolution_time(property_id, date),
                'by_category': self.requests_by_category(property_id, date),
                'by_priority': self.requests_by_priority(property_id, date),
                'satisfaction_score': self.avg_satisfaction(property_id, date)
            },
            
            'kiosks': {
                'uptime_percent': self.kiosk_uptime(property_id, date),
                'avg_session_duration': self.avg_kiosk_session(property_id, date),
                'peak_usage_hour': self.peak_usage_hour(property_id, date)
            }
        }
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Related Documents**:
- [OS-CONCIERGE Network Topology](./OS-CONCIERGE_Network_Topology.md)
- [OS-CONCIERGE Technical Architecture](./OS-CONCIERGE_Technical_Architecture.md)
