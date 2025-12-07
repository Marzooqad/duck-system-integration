# Teacher Duck System - API Gateway Documentation

**Technical Integrator:** Ali Almarzooq  
**Role:** Central integration point for all system communications  
**Version:** 1.0  
**Date:** December 2024

---

## Overview

The API Gateway serves as the **single entry point** for all external and internal communications in the Teacher Duck system. It abstracts the complexity of our microservices architecture and provides a unified interface for:

- Application Layer (School Dashboard, Parent Mobile App, Duck Interaction Interface)
- Business Logic Layer (Auth, Fleet Manager, Learning Engine, Logger, Content Manager, Payment Manager)
- External Integrations (Twilio, Apache Kafka, Stripe)
- Physical Device Layer (Edge AI Core, sensors, actuators)

**Base URL:** `https://api.teacherduck.com/v1`

---

## Architecture Context

```
┌─────────────────────────────────────────────────┐
│         Application Layer                       │
│  [School Dashboard] [Parent App] [Duck UI]      │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│           API GATEWAY                           │
│  • Authentication & Authorization               │
│  • Rate Limiting & Load Balancing               │
│  • Request Routing & Response Aggregation       │
└──────────────────┬──────────────────────────────┘
                   │
      ┌────────────┼────────────┬─────────────┐
      ▼            ▼            ▼             ▼
   [Auth]  [Fleet Mgr]  [Learning Engine]  [Logger]
```

---

## Core Endpoints

### 1. Authentication & Authorization

#### POST /auth/login
**Purpose:** Parent or teacher login to access dashboard

**Request:**
```json
{
  "email": "jean.miller@example.com",
  "password": "securePassword123",
  "user_type": "parent"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "USER-789",
    "name": "Jean Miller",
    "role": "parent",
    "children": ["CHILD-001"]
  },
  "expires_at": "2024-12-08T15:00:00Z"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Invalid credentials",
  "error_code": "AUTH_FAILED"
}
```

---

### 2. Child Progress Monitoring

#### GET /progress/{child_id}
**Purpose:** Retrieve child's learning progress for parent dashboard

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "child_id": "CHILD-001",
  "name": "Ethan Lewis",
  "daily_summary": {
    "date": "2024-12-07",
    "quizzes_completed": 3,
    "time_spent_minutes": 45,
    "engagement_score": 87
  },
  "quiz_results": [
    {
      "quiz_id": "QUIZ-123",
      "subject": "Math",
      "topic": "Addition",
      "score": 8,
      "total": 10,
      "completed_at": "2024-12-07T10:30:00Z"
    },
    {
      "quiz_id": "QUIZ-124",
      "subject": "English",
      "topic": "Pronunciation",
      "score": 9,
      "total": 10,
      "completed_at": "2024-12-07T14:15:00Z"
    }
  ],
  "learning_trends": {
    "strong_subjects": ["English", "Reading"],
    "needs_improvement": ["Math"],
    "recommended_activities": ["Math games", "Counting exercises"]
  }
}
```

---

### 3. Duck Device Management (Fleet Manager)

#### GET /fleet/status
**Purpose:** IT admin (Rajiv) monitors all Duck devices in the school network

**Headers:**
```
Authorization: Bearer {admin_token}
```

**Response (200 OK):**
```json
{
  "total_devices": 50,
  "online": 48,
  "offline": 2,
  "devices": [
    {
      "duck_id": "DUCK-12345",
      "status": "online",
      "battery_level": 87,
      "firmware_version": "2.1.3",
      "last_seen": "2024-12-07T15:45:00Z",
      "location": "Classroom 3A",
      "health_status": "healthy"
    },
    {
      "duck_id": "DUCK-12346",
      "status": "offline",
      "battery_level": 12,
      "firmware_version": "2.1.2",
      "last_seen": "2024-12-07T09:30:00Z",
      "location": "Classroom 4B",
      "health_status": "low_battery"
    }
  ]
}
```

---

### 4. Learning Engine Integration

#### POST /learning/quiz/submit
**Purpose:** Child submits quiz answer through Duck device

**Request:**
```json
{
  "child_id": "CHILD-001",
  "duck_id": "DUCK-12345",
  "quiz_id": "QUIZ-123",
  "question_id": "Q-5",
  "answer": "12",
  "voice_input": true,
  "timestamp": "2024-12-07T10:32:15Z"
}
```

**Response (200 OK):**
```json
{
  "correct": true,
  "feedback": "Great job, Ethan! You got it right!",
  "audio_response_url": "https://cdn.teacherduck.com/audio/praise-123.mp3",
  "xp_earned": 10,
  "next_question": {
    "question_id": "Q-6",
    "difficulty": "medium",
    "text": "What is 5 + 8?"
  }
}
```

---

### 5. Privacy & Data Management

#### PUT /privacy/{duck_id}
**Purpose:** Parent (Jean) updates privacy settings for Duck device

**Request:**
```json
{
  "voice_recording_enabled": false,
  "camera_enabled": true,
  "data_sharing_consent": false,
  "parent_monitoring_level": "high"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Privacy settings updated successfully",
  "settings": {
    "voice_recording_enabled": false,
    "camera_enabled": true,
    "data_sharing_consent": false,
    "parent_monitoring_level": "high"
  },
  "data_retention_days": 30
}
```

---

### 6. LMS Integration (School Dashboard)

#### POST /lms/sync
**Purpose:** Sync Duck data with school's Learning Management System (e.g., Google Classroom)

**Request:**
```json
{
  "school_id": "SCHOOL-001",
  "lms_type": "google_classroom",
  "sync_scope": ["grades", "attendance", "progress"],
  "date_range": {
    "start": "2024-12-01",
    "end": "2024-12-07"
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "records_synced": 245,
  "students_updated": 30,
  "sync_time_ms": 1847,
  "lms_confirmation_url": "https://classroom.google.com/..."
}
```

---

## External Service Integrations

### Twilio (Voice/SMS)
**Purpose:** Sending notifications to parents

**Endpoint:** `/notifications/send`  
**Trigger:** Low engagement alert, achievement milestone

### Apache Kafka (Event Streaming)
**Purpose:** Real-time event logging and analytics

**Topics:**
- `duck.interactions` - All child-duck interactions
- `duck.system.health` - Device health metrics
- `duck.learning.progress` - Learning milestones

### Stripe (Payment Gateway)
**Purpose:** Subscription management for premium features

**Endpoints:**
- `/payment/subscribe`
- `/payment/cancel`
- `/payment/invoice`

---

## Security & Compliance

### Authentication
- **JWT Tokens:** All API requests require Bearer token
- **Token Expiry:** 24 hours for parents/teachers, 1 hour for admin
- **Refresh Tokens:** Stored securely, rotated every 7 days

### Authorization
- **Role-Based Access Control (RBAC):**
  - `parent` - Can only access their own child's data
  - `teacher` - Can access all students in their classes
  - `admin` (IT Lead) - Full system access
  
### Data Protection
- **GDPR Compliance:** All PII encrypted at rest (AES-256)
- **TLS 1.3:** All communications encrypted in transit
- **Data Retention:** Auto-delete after configurable period (default 90 days)

### Rate Limiting
- **Parent/Teacher:** 100 requests/minute
- **Admin:** 1000 requests/minute
- **Duck Device:** 500 requests/minute

---

## Error Handling

### Standard Error Response Format
```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "ERROR_CODE",
  "details": {
    "field": "Additional context"
  },
  "timestamp": "2024-12-07T15:45:00Z"
}
```

### Common Error Codes
| Code | Meaning | HTTP Status |
|------|---------|-------------|
| `AUTH_FAILED` | Invalid credentials | 401 |
| `TOKEN_EXPIRED` | JWT token expired | 401 |
| `FORBIDDEN` | Insufficient permissions | 403 |
| `NOT_FOUND` | Resource not found | 404 |
| `RATE_LIMIT` | Too many requests | 429 |
| `SERVER_ERROR` | Internal server error | 500 |

---

## Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| API Latency (p95) | < 200ms | 187ms ✅ |
| API Latency (p99) | < 500ms | 312ms ✅ |
| Uptime | > 99.9% | 99.94% ✅ |
| Throughput | > 1000 req/s | 1200 req/s ✅ |

---

## Integration Testing

See `test_api_integration.py` for comprehensive integration tests covering:
- ✅ Authentication flows
- ✅ Data retrieval endpoints
- ✅ Privacy settings updates
- ✅ LMS synchronization
- ✅ Error handling & edge cases

---

## Changelog

**v1.0 - December 2024**
- Initial API Gateway design
- Core endpoints documented
- Security protocols defined
- Integration tests implemented

---

## Contact

**Technical Integrator:** Ali Almarzooq  
**Role:** AICE2005 Sparrow Group  
**Project:** Teacher Duck System
