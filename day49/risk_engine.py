# risk_engine.py - Risk scoring and flagging

def calculate_integrity_score(events):
    score = 100
    score -= events.get("tab_switch", 0) * 5
    score -= events.get("focus_loss", 0) * 3
    score -= events.get("voice_detect", 0) * 10
    score -= events.get("gaze_off", 0) * 4
    return max(score, 0)

def risk_flagging(score):
    if score < 50:
        return "High Risk"
    elif score < 75:
        return "Moderate Risk"
    return "Low Risk"

def combined_risk(behavior_score, integrity_score):
    return round(behavior_score * 0.4 + integrity_score * 0.6, 2)