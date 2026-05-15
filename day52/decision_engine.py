"""
Day 52 – Final Recommendation AI
Decision engine for automated hiring outcomes.

Usage:
    from decision_engine import HiringDecisionEngine
    
    engine = HiringDecisionEngine()
    decision = engine.decide({
        "candidate_id": "C001",
        "role": "software_engineer",
        "hiring_fit_score": 76.0,   # from Day 51
        "risk_factors": {
            "behavior": 85,      # 0-100, higher is better
            "integrity": 90
        },
        "additional_metrics": {   # optional
            "experience_years": 5,
            "education_level": 4
        }
    })
    print(decision)
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json

@dataclass
class DecisionOutput:
    candidate_id: str
    role: str
    decision: str          # "Selected", "Hold/Review", "Rejected"
    confidence: float      # 0-100
    hiring_fit_score: float
    risk_factors: Dict[str, float]
    risk_score: float      # weighted risk (0-100, lower is better)
    rule_based_hits: List[str]
    explanation: str

class HiringDecisionEngine:
    """
    Hybrid rule + score based decision engine.
    Uses hiring_fit_score and risk factors.
    """
    
    # Default thresholds (can be customized per role)
    DEFAULT_THRESHOLDS = {
        "software_engineer": {
            "selected_min_fit": 75,
            "hold_min_fit": 60,
            "max_risk_score": 30,      # risk score 0-100, lower better
            "behavior_min": 70,
            "integrity_min": 70
        },
        "data_scientist": {
            "selected_min_fit": 80,
            "hold_min_fit": 65,
            "max_risk_score": 25,
            "behavior_min": 75,
            "integrity_min": 75
        },
        "product_manager": {
            "selected_min_fit": 70,
            "hold_min_fit": 55,
            "max_risk_score": 35,
            "behavior_min": 65,
            "integrity_min": 65
        },
        "default": {
            "selected_min_fit": 70,
            "hold_min_fit": 55,
            "max_risk_score": 30,
            "behavior_min": 70,
            "integrity_min": 70
        }
    }
    
    # Risk factor weights
    RISK_WEIGHTS = {
        "behavior": 0.6,
        "integrity": 0.4
    }
    
    def __init__(self, custom_thresholds: Optional[Dict] = None):
        self.thresholds = custom_thresholds or self.DEFAULT_THRESHOLDS
    
    def _compute_risk_score(self, risk_factors: Dict[str, float]) -> float:
        """Compute weighted risk score (0-100, lower = less risk)"""
        total = 0.0
        total_weight = 0.0
        for factor, weight in self.RISK_WEIGHTS.items():
            if factor in risk_factors:
                # Convert to risk (higher raw = lower risk)
                # Risk = 100 - raw_score
                risk_value = 100 - risk_factors[factor]
                total += risk_value * weight
                total_weight += weight
        if total_weight == 0:
            return 50.0  # default medium risk
        return total / total_weight
    
    def _get_thresholds_for_role(self, role: str) -> Dict:
        return self.thresholds.get(role, self.thresholds["default"])
    
    def _apply_rules(self, fit_score: float, risk_factors: Dict[str, float], thresholds: Dict) -> List[str]:
        """Return list of rule violations or flags"""
        hits = []
        if fit_score < thresholds["hold_min_fit"]:
            hits.append(f"fit_score_too_low ({fit_score} < {thresholds['hold_min_fit']})")
        if risk_factors.get("behavior", 100) < thresholds["behavior_min"]:
            hits.append(f"behavior_below_threshold ({risk_factors['behavior']} < {thresholds['behavior_min']})")
        if risk_factors.get("integrity", 100) < thresholds["integrity_min"]:
            hits.append(f"integrity_below_threshold ({risk_factors['integrity']} < {thresholds['integrity_min']})")
        return hits
    
    def _compute_confidence(self, fit_score: float, risk_score: float, thresholds: Dict) -> float:
        """
        Confidence = how strongly the decision is justified.
        Higher fit, lower risk → high confidence.
        Near boundaries → lower confidence.
        """
        # Ideal point: fit = 100, risk = 0
        fit_norm = min(100, max(0, fit_score)) / 100.0
        risk_norm = 1.0 - (min(100, max(0, risk_score)) / 100.0)  # invert so high risk lowers confidence
        
        # Weighted average
        confidence_raw = (fit_norm * 0.7) + (risk_norm * 0.3)
        
        # Scale to 0-100 and apply penalty if near thresholds
        selected_min = thresholds["selected_min_fit"]
        hold_min = thresholds["hold_min_fit"]
        
        # If near boundary, reduce confidence
        if abs(fit_score - selected_min) < 5:
            confidence_raw *= 0.8
        elif abs(fit_score - hold_min) < 5:
            confidence_raw *= 0.7
        
        return round(confidence_raw * 100, 1)
    
    def decide(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input:
        {
            "candidate_id": str,
            "role": str,
            "hiring_fit_score": float (0-100),
            "risk_factors": {"behavior": 0-100, "integrity": 0-100},
            "additional_metrics": {} (optional)
        }
        
        Output: DecisionOutput as dict
        """
        cand_id = candidate_data["candidate_id"]
        role = candidate_data["role"]
        fit_score = candidate_data["hiring_fit_score"]
        risk_factors = candidate_data.get("risk_factors", {"behavior": 80, "integrity": 80})
        
        thresholds = self._get_thresholds_for_role(role)
        risk_score = self._compute_risk_score(risk_factors)
        
        # Rule checks
        rule_hits = self._apply_rules(fit_score, risk_factors, thresholds)
        
        # Determine decision
        if fit_score >= thresholds["selected_min_fit"] and risk_score <= thresholds["max_risk_score"] and len(rule_hits) == 0:
            decision = "Selected"
        elif fit_score >= thresholds["hold_min_fit"] and risk_score <= thresholds["max_risk_score"] + 10:
            decision = "Hold/Review"
        else:
            decision = "Rejected"
        
        # Override if critical rule violation
        if any("behavior" in h or "integrity" in h for h in rule_hits):
            if decision == "Selected":
                decision = "Hold/Review"
            if decision == "Hold/Review" and ("behavior" in str(rule_hits) or "integrity" in str(rule_hits)):
                decision = "Rejected"
        
        confidence = self._compute_confidence(fit_score, risk_score, thresholds)
        
        # Build explanation
        explanation = (
            f"Candidate {cand_id} for role '{role}': Hiring Fit = {fit_score:.1f}%, "
            f"Risk Score = {risk_score:.1f} (lower better). Decision: {decision}. "
            f"Confidence: {confidence:.1f}%. "
        )
        if rule_hits:
            explanation += f"Rule triggers: {', '.join(rule_hits)}. "
        if decision == "Selected":
            explanation += "Meets all criteria for selection."
        elif decision == "Hold/Review":
            explanation += "Requires further review due to borderline scores or risk factors."
        else:
            explanation += "Does not meet minimum requirements."
        
        return asdict(DecisionOutput(
            candidate_id=cand_id,
            role=role,
            decision=decision,
            confidence=confidence,
            hiring_fit_score=fit_score,
            risk_factors=risk_factors,
            risk_score=round(risk_score, 1),
            rule_based_hits=rule_hits,
            explanation=explanation
        ))
    
    def decide_batch(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple candidates"""
        return [self.decide(c) for c in candidates]


# -------------------------
# Self-test
# -------------------------
if __name__ == "__main__":
    print("=== Day 52: Final Recommendation AI Test ===\n")
    
    engine = HiringDecisionEngine()
    
    # Example candidates (using hiring_fit_score from Day 51)
    candidates = [
        {
            "candidate_id": "C001",
            "role": "software_engineer",
            "hiring_fit_score": 100.0,   # top normalized
            "risk_factors": {"behavior": 95, "integrity": 90}
        },
        {
            "candidate_id": "C002",
            "role": "software_engineer",
            "hiring_fit_score": 0.0,      # bottom normalized
            "risk_factors": {"behavior": 60, "integrity": 55}
        },
        {
            "candidate_id": "C003",
            "role": "data_scientist",
            "hiring_fit_score": 85.8,     # raw score
            "risk_factors": {"behavior": 70, "integrity": 75}
        },
        {
            "candidate_id": "C004",
            "role": "product_manager",
            "hiring_fit_score": 72.0,
            "risk_factors": {"behavior": 80, "integrity": 65}  # integrity low
        }
    ]
    
    for cand in candidates:
        result = engine.decide(cand)
        print(f"{result['candidate_id']} ({result['role']}):")
        print(f"  Decision: {result['decision']} | Confidence: {result['confidence']}%")
        print(f"  Risk score: {result['risk_score']} | Rule hits: {result['rule_based_hits']}")
        print(f"  Explanation: {result['explanation']}\n")