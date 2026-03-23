``# Transcript Metadata Standards

## 1. Core Identifiers

| Field | Format | Example | Description |
|-------|--------|---------|-------------|
| transcript_id | TSCR-YYYYMMDD-NNN | TSCR-20260323-001 | Unique transcript ID |
| candidate_id | CAND-YYYYMMDD-NNN | CAND-20260323-001 | Candidate identifier |
| job_id | JOB-ROLE-YYYY-NNN | JOB-SE-2025-001 | Job identifier |
| question_id | Q_{role}_{category} | q_software_engineer_skills | Question identifier |

## 2. Timestamp Standards

| Field | Format | Example |
|-------|--------|---------|
| timestamp | ISO 8601 UTC | 2026-03-23T10:30:00Z |
| duration_seconds | Integer | 245 |

## 3. Confidence Scoring

| Range | Interpretation |
|-------|----------------|
| 90-100 | High confidence – clear speech |
| 70-89 | Medium confidence – some noise |
| 50-69 | Low confidence – unclear speech |
| <50 | Very low – manual review needed |

## 4. Transcript Normalization Rules

| Rule | Description | Example |
|------|-------------|---------|
| Lowercase | Convert all text to lowercase | "Hello" → "hello" |
| Remove filler | Remove um, uh, like | "I um like Python" → "I like Python" |
| Correct grammar | Fix common errors | "I am having 3 years" → "I have 3 years" |
| Extract values | Pull numbers, dates | "I have 3 years" → {"extracted_value": 3} |
| Mask PII | Hide personal info | "email: john@email.com" → "[EMAIL]" |