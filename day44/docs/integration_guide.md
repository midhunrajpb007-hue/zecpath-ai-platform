# Integration Guide

1. Get API key.
2. Use Python requests:

import requests
headers = {"Authorization": "Bearer YOUR_KEY"}
session = requests.post("https://api.zecpath.com/v1/hr/sessions", headers=headers, json={...})
session_id = session.json()["session_id"]

# Submit answers
requests.post(f"https://api.zecpath.com/v1/hr/sessions/{session_id}/answer", headers=headers, json={"answer": "..."})

# Get final score
score = requests.get(f"https://api.zecpath.com/v1/hr/sessions/{session_id}/score", headers=headers).json()
print(score["final_score"])
