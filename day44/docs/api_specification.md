# API Specification

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
