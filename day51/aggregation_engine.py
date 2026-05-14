"""
Cross-Round Aggregation Engine for Zecpath AI Platform
Day 51 Task Deliverable – Pure Python, No External Dependencies

Improvements:
- Single-candidate groups now keep original raw score (instead of 50% default)
- Better explanation output
- Fully tested
"""

from typing import Dict, List, Optional, Any
from collections import defaultdict

class HiringFitAggregator:
    """
    Aggregates scores from multiple evaluation rounds into Hiring Fit Score.
    Supports single candidate and batch with cross-candidate normalization.
    """
    
    # Default weightage per role (modify as needed)
    DEFAULT_WEIGHTS = {
        "software_engineer": {
            "ats": 0.10,
            "screening": 0.10,
            "hr_interview": 0.10,
            "technical_interview": 0.40,
            "machine_test": 0.30
        },
        "data_scientist": {
            "ats": 0.10,
            "screening": 0.10,
            "hr_interview": 0.10,
            "technical_interview": 0.35,
            "machine_test": 0.35
        },
        "product_manager": {
            "ats": 0.15,
            "screening": 0.20,
            "hr_interview": 0.25,
            "technical_interview": 0.20,
            "machine_test": 0.20
        },
        "frontend_engineer": {
            "ats": 0.10,
            "screening": 0.10,
            "hr_interview": 0.15,
            "technical_interview": 0.35,
            "machine_test": 0.30
        },
        "devops_engineer": {
            "ats": 0.10,
            "screening": 0.10,
            "hr_interview": 0.10,
            "technical_interview": 0.40,
            "machine_test": 0.30
        }
    }
    
    def __init__(self, custom_weights: Optional[Dict] = None):
        self.weights = custom_weights or self.DEFAULT_WEIGHTS
    
    def set_weights(self, role: str, weights: Dict[str, float]):
        self.weights[role] = weights
    
    def _normalize_scores(self, scores_list: List[float]) -> List[float]:
        """
        Min-max normalization to 0-100 scale.
        If only one score, keep original (no change).
        """
        if not scores_list:
            return []
        min_s = min(scores_list)
        max_s = max(scores_list)
        if max_s == min_s:
            # Single candidate or all same: return original scores unchanged
            return scores_list[:]
        return [(s - min_s) / (max_s - min_s) * 100 for s in scores_list]
    
    def aggregate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute Hiring Fit Score for a single candidate.
        
        Input:
        {
            "candidate_id": str,
            "role": str,
            "scores": {"ats": float, "screening": float, ...}
        }
        
        Output:
        {
            "candidate_id": str,
            "role": str,
            "hiring_fit_score": float,
            "breakdown": dict,
            "weights_used": dict,
            "explanation": str
        }
        """
        cand_id = candidate_data["candidate_id"]
        role = candidate_data["role"]
        scores = candidate_data["scores"]
        
        weights = self.weights.get(role, self.weights["software_engineer"])
        
        total_weighted = 0.0
        total_weight = 0.0
        breakdown = {}
        
        for round_name, weight in weights.items():
            if round_name in scores:
                score = scores[round_name]
                contribution = score * weight
                total_weighted += contribution
                total_weight += weight
                breakdown[round_name] = round(contribution, 2)
        
        if total_weight == 0:
            hiring_score = 0.0
        else:
            hiring_score = total_weighted / total_weight
        
        # Find top contributor for explanation
        if breakdown:
            top_round = max(breakdown, key=breakdown.get)
            top_value = breakdown[top_round]
        else:
            top_round = "none"
            top_value = 0
        
        explanation = (
            f"Candidate {cand_id} for role '{role}' achieved {hiring_score:.1f}% Hiring Fit. "
            f"Top contributor: {top_round} ({top_value:.1f} points)."
        )
        
        return {
            "candidate_id": cand_id,
            "role": role,
            "hiring_fit_score": round(hiring_score, 2),
            "breakdown": breakdown,
            "weights_used": weights,
            "explanation": explanation
        }
    
    def aggregate_batch(self, candidates: List[Dict[str, Any]], 
                        normalize: bool = True) -> List[Dict[str, Any]]:
        """
        Batch aggregation with optional cross-candidate normalization.
        
        Args:
            candidates: List of candidate dicts (same format as aggregate)
            normalize: If True, normalize each round's scores across candidates
        
        Returns:
            List of result dicts
        """
        if not normalize:
            return [self.aggregate(c) for c in candidates]
        
        # Group by role (normalize within each role)
        role_groups: Dict[str, List[Dict]] = defaultdict(list)
        for cand in candidates:
            role_groups[cand["role"]].append(cand)
        
        all_results = []
        
        for role, group in role_groups.items():
            # Collect all scores per round for this role
            round_scores: Dict[str, List[float]] = defaultdict(list)
            for cand in group:
                for round_name, score in cand["scores"].items():
                    round_scores[round_name].append(score)
            
            # Normalize each round's scores
            normalized_rounds: Dict[str, List[float]] = {}
            for round_name, scores in round_scores.items():
                normalized_rounds[round_name] = self._normalize_scores(scores)
            
            # Assign normalized scores back to each candidate
            for idx, cand in enumerate(group):
                normalized_cand_scores = {}
                for round_name in cand["scores"].keys():
                    if round_name in normalized_rounds and idx < len(normalized_rounds[round_name]):
                        normalized_cand_scores[round_name] = normalized_rounds[round_name][idx]
                    else:
                        normalized_cand_scores[round_name] = cand["scores"][round_name]
                
                cand_copy = cand.copy()
                cand_copy["scores"] = normalized_cand_scores
                result = self.aggregate(cand_copy)
                if len(group) == 1:
                    result["explanation"] += " (Single candidate in group: original score retained)"
                else:
                    result["explanation"] += f" (Normalized across {len(group)} candidates for role '{role}')"
                all_results.append(result)
        
        return all_results


# -------------------------
# Self-test when run directly
# -------------------------
if __name__ == "__main__":
    print("=== Cross-Round Aggregation Engine Test ===\n")
    
    agg = HiringFitAggregator()
    
    # Test single candidate
    cand1 = {
        "candidate_id": "C001",
        "role": "software_engineer",
        "scores": {
            "ats": 85,
            "screening": 90,
            "hr_interview": 80,
            "technical_interview": 70,
            "machine_test": 75
        }
    }
    res1 = agg.aggregate(cand1)
    print(f"Single candidate {res1['candidate_id']}: {res1['hiring_fit_score']}%")
    print(f"  Explanation: {res1['explanation']}\n")
    
    # Test batch with normalization
    cand2 = {
        "candidate_id": "C002",
        "role": "software_engineer",
        "scores": {
            "ats": 60,
            "screening": 70,
            "hr_interview": 65,
            "technical_interview": 50,
            "machine_test": 55
        }
    }
    cand3 = {
        "candidate_id": "C003",
        "role": "data_scientist",
        "scores": {
            "ats": 95,
            "screening": 85,
            "hr_interview": 90,
            "technical_interview": 80,
            "machine_test": 88
        }
    }
    
    # First compute raw weighted scores for cand3 to show original
    raw_res3 = agg.aggregate(cand3)
    print(f"Raw score for C003 (no batch normalization): {raw_res3['hiring_fit_score']}%")
    
    batch_results = agg.aggregate_batch([cand1, cand2, cand3], normalize=True)
    print("\nBatch results (with cross-candidate normalization):")
    for r in batch_results:
        print(f"  {r['candidate_id']} ({r['role']}): {r['hiring_fit_score']}%")
        print(f"    {r['explanation']}")