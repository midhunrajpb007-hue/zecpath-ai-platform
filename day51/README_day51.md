# Day 51 – Cross-Round Aggregation Engine

## Overview
Combines ATS, Screening, HR Interview, Technical Interview, Machine Test scores into a unified Hiring Fit Score with role‑based weights and optional cross‑candidate normalization.

## Files
- `aggregation_engine.py` – main engine (pure Python)

## Usage Example
```python
from aggregation_engine import HiringFitAggregator

agg = HiringFitAggregator()
result = agg.aggregate({
    "candidate_id": "C001",
    "role": "software_engineer",
    "scores": {"ats": 85, "technical_interview": 70, ...}
})
print(result["hiring_fit_score"])