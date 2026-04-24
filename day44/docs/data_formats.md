# Data Formats

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
