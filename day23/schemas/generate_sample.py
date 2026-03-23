import json
from datetime import datetime

# Sample transcript
transcript = {
    "transcript_id": "TSCR-20260323-001",
    "candidate_id": "CAND-20260323-001",
    "job_id": "JOB-SE-2025-001",
    "timestamp": datetime.now().isoformat() + "Z",
    "duration_seconds": 245,
    "interactions": [
        {
            "question_id": "q_software_engineer_intro",
            "question_text": "Tell me about yourself and your career background.",
            "answer_text": "I am a software developer with 3 years of experience in Python and React.",
            "answer_normalized": "software developer with 3 years experience in python and react",
            "confidence_score": 92,
            "processing_time_ms": 45
        },
        {
            "question_id": "q_software_engineer_skills",
            "question_text": "What programming languages and frameworks are you proficient in?",
            "answer_text": "I know Python, JavaScript, React, and Node.js.",
            "answer_normalized": "python javascript react node.js",
            "confidence_score": 88,
            "processing_time_ms": 38
        }
    ],
    "metadata": {
        "model_version": "stt-v2.1",
        "language": "en",
        "voice_gender": "female",
        "call_status": "completed"
    }
}

with open('data/sample_transcript.json', 'w') as f:
    json.dump(transcript, f, indent=2)

print("✅ Sample transcript created")