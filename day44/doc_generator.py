# doc_generator.py - Simple Day 44 script (no errors)
import os

# Create docs folder
os.makedirs('docs', exist_ok=True)

# 1. Architecture document (with simple diagram)
arch = """# Architecture Overview

## Components
- Conversation Flow Engine
- Intent Classifier
- Scoring Engine
- Follow-up Logic
- Ethics & Compliance
- Report Generator

## Data Flow
Candidate -> Voice Call -> STT -> Transcript -> Intent -> Scoring -> Follow-up -> Report

## Tech Stack
Python, FastAPI, PostgreSQL, Redis, Docker
"""
with open('docs/architecture.md', 'w', encoding='utf-8') as f:
    f.write(arch)

# 2. API Specification
api = """# API Specification

Base URL: https://api.zecpath.com/v1/hr
Auth: Bearer token

Endpoints:
- POST /sessions          -> start interview
- POST /sessions/{id}/answer -> submit answer
- GET /sessions/{id}/score   -> get final score

Example response:
{
  "final_score": 82.3,
  "recommendation": "Hire",
  "breakdown": {...}
}
"""
with open('docs/api_specification.md', 'w', encoding='utf-8') as f:
    f.write(api)

# 3. Scoring Logic
scoring = """# Scoring Logic

Each answer scored on:
- Relevance (35%)
- Communication (30%)
- Confidence (25%)
- Consistency (10%)

Final score = average of all questions.

Recommendation:
- >=80: Strong Hire
- 65-79: Hire
- 50-64: Consider
- <50: Reject
"""
with open('docs/scoring_logic.md', 'w', encoding='utf-8') as f:
    f.write(scoring)

# 4. Data Formats
data = """# Data Formats

Input for /sessions:
{
  "candidate_id": "string",
  "job_id": "string",
  "role": "string"
}

Output from /score:
{
  "final_score": 0-100,
  "recommendation": "string",
  "breakdown": {...}
}
"""
with open('docs/data_formats.md', 'w', encoding='utf-8') as f:
    f.write(data)

# 5. Integration Guide
guide = """# Integration Guide

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
"""
with open('docs/integration_guide.md', 'w', encoding='utf-8') as f:
    f.write(guide)

# 6. Troubleshooting
trouble = """# Troubleshooting

| Error | Solution |
|-------|----------|
| 401 Unauthorized | Check API key |
| 404 Not Found | Session expired, create new |
| 429 Too Many Requests | Wait and retry |
"""
with open('docs/troubleshooting.md', 'w', encoding='utf-8') as f:
    f.write(trouble)

# 7. Developer Handbook
handbook = """# Developer Handbook

## Quick Start
1. Get API key.
2. POST /sessions
3. POST /sessions/{id}/answer (repeat for each question)
4. GET /sessions/{id}/score

See integration guide for full details.
"""
with open('docs/developer_handbook.md', 'w', encoding='utf-8') as f:
    f.write(handbook)

# 8. OpenAPI YAML
yaml_content = """openapi: 3.0.0
info:
  title: Zecpath HR Interview API
  version: 1.0.0
servers:
  - url: https://api.zecpath.com/v1/hr
paths:
  /sessions:
    post:
      summary: Start interview
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                candidate_id: {type: string}
                job_id: {type: string}
                role: {type: string}
      responses:
        '200': {description: OK}
  /sessions/{session_id}/answer:
    post:
      summary: Submit answer
      parameters:
        - name: session_id
          in: path
          required: true
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                answer: {type: string}
      responses:
        '200': {description: OK}
  /sessions/{session_id}/score:
    get:
      summary: Get final score
      parameters:
        - name: session_id
          in: path
          required: true
      responses:
        '200': {description: OK}
"""
with open('docs/openapi.yaml', 'w', encoding='utf-8') as f:
    f.write(yaml_content)

print("="*70)
print("DAY 44 - DOCUMENTATION & API SPECIFICATION")
print("="*70)
print("✅ All documentation files created in 'docs/' folder")
print("✅ Files: architecture.md, api_specification.md, scoring_logic.md, data_formats.md, integration_guide.md, troubleshooting.md, developer_handbook.md, openapi.yaml")
print("\n✅ DAY 44 COMPLETED")