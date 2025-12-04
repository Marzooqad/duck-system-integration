"""
Example API Usage for Duck System Parent App
Demonstrates how to interact with the Duck System API
"""

import requests

# Configuration
BASE_URL = "https://api.ducksystem.com/v1"
PARENT_EMAIL = "jean@example.com"
PARENT_PASSWORD = "password123"

def example_login():
    """Example: Parent login"""
    print("=== Example 1: Parent Login ===")
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": PARENT_EMAIL,
            "password": PARENT_PASSWORD
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"   Token: {data['token'][:20]}...")
        print(f"   Duck ID: {data['duck_id']}")
        print(f"   Parent: {data['parent_name']}")
        return data['token']
    else:
        print(f"❌ Login failed: {response.status_code}")
        return None

def example_get_progress(token, child_id):
    """Example: Get child progress"""
    print(f"\n=== Example 2: Get Child Progress ===")
    
    response = requests.get(
        f"{BASE_URL}/progress/{child_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Progress retrieved for {data['name']}")
        print(f"   Quizzes completed: {data['daily_activity']['quizzes_completed']}")
        print(f"   Time spent: {data['daily_activity']['time_spent_minutes']} minutes")
        print(f"   Subjects: {', '.join(data['daily_activity']['subjects'])}")
        print(f"   Quiz scores:")
        for score in data['quiz_scores']:
            print(f"     - {score['subject']}: {score['score']}/{score['total']}")
    else:
        print(f"❌ Failed to get progress: {response.status_code}")

def example_update_privacy(token, duck_id):
    """Example: Update privacy settings"""
    print(f"\n=== Example 3: Update Privacy Settings ===")
    
    response = requests.put(
        f"{BASE_URL}/privacy/{duck_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "voice_recording": False,
            "data_sharing": False,
            "camera_enabled": True
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Privacy settings updated")
        print(f"   Message: {data['message']}")
    else:
        print(f"❌ Failed to update privacy: {response.status_code}")

def example_schedule_homework(token, child_id, duck_id):
    """Example: Schedule homework reminder"""
    print(f"\n=== Example 4: Schedule Homework Reminder ===")
    
    response = requests.post(
        f"{BASE_URL}/homework/schedule",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "child_id": child_id,
            "task": "Math homework",
            "scheduled_time": "17:00",
            "duck_id": duck_id
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Homework reminder scheduled")
        print(f"   Reminder ID: {data['reminder_id']}")
        print(f"   Message: {data['message']}")
    else:
        print(f"❌ Failed to schedule homework: {response.status_code}")

if __name__ == "__main__":
    print("=" * 60)
    print("DUCK SYSTEM API - USAGE EXAMPLES")
    print("=" * 60)
    print("\nNote: These examples show the API structure.")
    print("In a real implementation, replace BASE_URL with your actual API endpoint.")
    print("\n" + "=" * 60 + "\n")
    
    # Note: These will fail without a real API server
    # They're provided as reference examples
    token = example_login()
    
    if token:
        example_get_progress(token, "CHILD-789")
        example_update_privacy(token, "DUCK-12345")
        example_schedule_homework(token, "CHILD-789", "DUCK-12345")

