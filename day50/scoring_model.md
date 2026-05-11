# Scoring Model for Machine Tests – Zecpath AI

## Overview
This document defines how each machine test (coding, debugging, file‑based, system design) is scored. The final score combines correctness, efficiency, code quality, and problem‑solving approach, with a time factor.

## Scoring Components & Weights

| Component                  | Weigh | Description                                        |
|----------------------------|-------|----------------------------------------------------|
| **Correctness**            | 40%   | Percentage of test cases passed,including edgecases|
| **Efficiency**             | 25%   | Time & space complexity analysis (Big‑O).          |
| **Code Quality**           | 20%   | Readability, naming, comments, structure, linting. |
|**Problem‑Solving Approach**| 15%   | Reasoning clarity, step‑by‑step explanation        |

**Formula:**  
`raw_score = (correctness×0.40) + (efficiency×0.25) + (code_quality×0.20) + (approach×0.15)`

## Difficulty & Time Factors

| Difficulty | Estimated Time (minutes) | Test Cases | Partial Credit Threshold |
|------------|--------------------------|------------|--------------------------|
| Easy       | 15                       | 5          | 40% of correctness       |
| Medium     | 30                       | 7          | 50% of correctness       |
| Hard       | 45                       | 10         | 60% of correctness       |

**Time factor formula:**  
`time_factor = min(1.0, (time_used / estimated_time) × 1.2)`

**Final score:**  
`final_score = raw_score × time_factor`

## Partial Credit Rules
- If candidate exceeds estimated time but has a **reasonable, logical solution** (determined by code structure and comments), they receive up to 50% of the correctness score.  
- Efficiency, quality, and approach are scored normally regardless of time.

## Example
- Task: Easy (est. 15 min). Candidate takes 20 min.  
  correctness = 80%, efficiency = 70%, quality = 80%, approach = 90%  
  raw = 80×0.4 + 70×0.25 + 80×0.2 + 90×0.15 = 32 + 17.5 + 16 + 13.5 = 79%  
  time_factor = min(1.0, (20/15)×1.2) = min(1.0, 1.6) = 1.0  
  final = 79%  

- Edge case: Candidate takes 30 min, correctness still 80% from partial credit (50% of correctness).  
  raw = (80×0.5)×0.4 + 70×0.25 + 80×0.2 + 90×0.15 = 16 + 17.5 + 16 + 13.5 = 63%  
  time_factor = 1.0 (capped)  
  final = 63%

## Integration with Other Modules
- The machine test score contributes to the **Unified Technical Score** (Day 47).  
- Behavioral AI (Day 48) and Integrity Detection (Day 49) can flag distractions/cheating during the test, which may reduce the final score.

---

**✅ Scoring model ready for implementation.**