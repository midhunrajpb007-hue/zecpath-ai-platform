# task_evaluator.py - Task Evaluation Logic (Pseudo‑code for Day 50 design)

def evaluate_task(submission, test_cases, time_used, estimated_time):
    """
    Evaluate a machine test task.
    submission: dict with keys 'code', 'comments', etc.
    test_cases: list of {'input': ..., 'expected': ...}
    time_used: minutes taken by candidate
    estimated_time: expected minutes for the task
    """
    # 1. Correctness (simulate test case execution)
    passed = 0
    for case in test_cases:
        # In real implementation, execute submission['code'] with case['input']
        # Here we use a placeholder: assume correctness is predetermined (e.g., from test runner)
        # For design, we'll set a sample value.
        pass
    # For demonstration, we'll assume 80% correctness; in real system this comes from test runner.
    correctness = 80.0   # placeholder
    
    # 2. Efficiency (simplified – based on Big‑O analysis of the code)
    efficiency = 70.0    # placeholder
    
    # 3. Code quality (linting, naming, comments)
    quality = 80.0       # placeholder
    
    # 4. Problem‑solving approach (extracted from comments or human rating)
    approach = 90.0      # placeholder
    
    # Weighted raw score
    raw_score = (correctness * 0.40) + (efficiency * 0.25) + (quality * 0.20) + (approach * 0.15)
    
    # Time factor
    time_factor = min(1.0, (time_used / estimated_time) * 1.2)
    final_score = raw_score * time_factor
    
    return round(final_score, 2)

# Example usage (commented)
# result = evaluate_task({}, [], 20, 15)
# print(result)