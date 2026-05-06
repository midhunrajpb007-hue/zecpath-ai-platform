def calculate_behavior_score(signals):
    """
    signals = {
        "eye_focus": 0-1,
        "head_stability": 0-1,
        "engagement": 0-1,
        "distraction": 0-1
    }
    """
    focus = signals.get("eye_focus", 0.5)
    head = signals.get("head_stability", 0.5)
    engagement = signals.get("engagement", 0.5)
    distraction = signals.get("distraction", 0.5)
    
    # weights: focus 30%, head 20%, engagement 30%, inverse distraction 20%
    score = (focus * 0.30 + head * 0.20 + engagement * 0.30 + (1 - distraction) * 0.20) * 100
    return round(score, 2)