"""
Test script for VIOLET Kick Bot webhook endpoint
Run this to test if your webhook is working correctly
"""

import requests
import json
import hmac
import hashlib
from datetime import datetime

# Configuration
WEBHOOK_URL = "http://localhost:5000/webhook"
WEBHOOK_SECRET = "your_webhook_secret_here"  # Must match .env

def create_signature(payload: dict, secret: str) -> str:
    """Create HMAC signature for webhook"""
    body = json.dumps(payload).encode()
    signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={signature}"

def test_webhook(event_type: str, payload: dict):
    """Send test webhook"""
    print(f"\n{'='*60}")
    print(f"Testing webhook: {event_type}")
    print(f"{'='*60}")
    
    # Create signature
    signature = create_signature(payload, WEBHOOK_SECRET)
    
    # Send request
    headers = {
        "Content-Type": "application/json",
        "X-Kick-Signature": signature
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print("❌ Webhook test failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🧪 VIOLET Webhook Test Suite")
    print("="*60)
    
    # Test 1: New Follower
    test_webhook("channel.follow", {
        "type": "channel.follow",
        "data": {
            "follower": {
                "id": "12345",
                "username": "TestFollower",
                "avatar": "https://example.com/avatar.jpg"
            },
            "followed_at": datetime.now().isoformat()
        }
    })
    
    # Test 2: New Subscription
    test_webhook("channel.subscription", {
        "type": "channel.subscription",
        "data": {
            "subscriber": {
                "id": "67890",
                "username": "TestSubscriber",
                "avatar": "https://example.com/avatar.jpg"
            },
            "tier": 1,
            "months": 1,
            "subscribed_at": datetime.now().isoformat()
        }
    })
    
    # Test 3: Stream Online
    test_webhook("stream.online", {
        "type": "stream.online",
        "data": {
            "stream": {
                "id": "stream123",
                "title": "Test Stream",
                "category": "Gaming",
                "started_at": datetime.now().isoformat()
            }
        }
    })
    
    # Test 4: Chat Message
    test_webhook("chat.message", {
        "type": "chat.message",
        "data": {
            "message": {
                "id": "msg123",
                "content": "Hello VIOLET!",
                "sender": {
                    "id": "user123",
                    "username": "TestUser"
                },
                "sent_at": datetime.now().isoformat()
            }
        }
    })
    
    print(f"\n{'='*60}")
    print("🎉 All webhook tests completed!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()