import requests
import json

test_message = "server status"

test_data = {
    "destination": "1",
    "events": [
        {
            "type": "message",
            "message": {
                "type": "text",
                "id": "1",
                "text": f"{test_message}",
            },
            "timestamp": 1,
            "source": {"type": "user", "userId": "U12345678123456781234567812345678"},
            "replyToken": "1",
            "mode": "active",
        }
    ],
}
test_data = json.dumps(test_data)
r = requests.post("http://127.0.0.1:8000/debug_page", data=test_data, timeout=10)
print(r.status_code)
