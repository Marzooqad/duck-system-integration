# Duck System - Parent App API Documentation

## Overview

This API allows the Parent mobile app to communicate with the Duck System for monitoring child progress, managing privacy settings, and configuring homework schedules.

**Base URL:** `https://api.ducksystem.com/v1`

---

## Authentication

### Login

**Endpoint:** `POST /auth/login`

**Request:**

```json
{
  "email": "parent@example.com",
  "password": "securePassword123"
}
```

**Response:**

```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "duck_id": "DUCK-12345",
  "parent_name": "Jean Miller"
}
```

---

## Child Progress Monitoring

### Get Child Progress

**Endpoint:** `GET /progress/{child_id}`

**Headers:**

```
Authorization: Bearer {token}
```

**Response:**

```json
{
  "child_id": "CHILD-789",
  "name": "Ethan",
  "daily_activity": {
    "quizzes_completed": 3,
    "time_spent_minutes": 45,
    "subjects": ["Math", "English"]
  },
  "quiz_scores": [
    { "subject": "Math", "score": 8, "total": 10 },
    { "subject": "English", "score": 9, "total": 10 }
  ]
}
```

---

## Privacy Settings

### Update Privacy Settings

**Endpoint:** `PUT /privacy/{duck_id}`

**Request:**

```json
{
  "voice_recording": false,
  "data_sharing": false,
  "camera_enabled": true
}
```

**Response:**

```json
{
  "success": true,
  "message": "Privacy settings updated"
}
```

---

## Homework Scheduler

### Set Homework Reminder

**Endpoint:** `POST /homework/schedule`

**Request:**

```json
{
  "child_id": "CHILD-789",
  "task": "Math homework",
  "scheduled_time": "17:00",
  "duck_id": "DUCK-12345"
}
```

**Response:**

```json
{
  "success": true,
  "reminder_id": "REM-456",
  "message": "Duck will alert Ethan at 17:00"
}
```

---

## Example Usage

### Python Example

```python
import requests

# Login
response = requests.post(
    "https://api.ducksystem.com/v1/auth/login",
    json={
        "email": "jean@example.com",
        "password": "password123"
    }
)
token = response.json()["token"]

# Get child progress
progress = requests.get(
    "https://api.ducksystem.com/v1/progress/CHILD-789",
    headers={"Authorization": f"Bearer {token}"}
)
print(progress.json())
```

### JavaScript Example

```javascript
// Login
const login = await fetch('https://api.ducksystem.com/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'jean@example.com',
    password: 'password123'
  })
});
const { token } = await login.json();

// Get progress
const progress = await fetch('https://api.ducksystem.com/v1/progress/CHILD-789', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const data = await progress.json();
console.log(data);
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 401 | Unauthorized (invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Resource not found |
| 500 | Server error |

---

## Notes for Integration Team

- All endpoints require HTTPS
- Token expires after 24 hours
- Rate limit: 100 requests per minute per parent account
- Voice data is encrypted end-to-end

