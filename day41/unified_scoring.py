# unified_scoring.py - Day 41 Unified Scoring Engine (Fixed)
import json
import os
from datetime import datetime

class UnifiedScoringEngine:
    def __init__(self, role='software_engineer', custom_weights=None):
        # Default weights for different roles
        self.default_weights = {
            'software_engineer': {
                'ats_weight': 0.40,
                'screening_weight': 0.30,
                'hr_weight': 0.30
            },
            'data_scientist': {
                'ats_weight': 0.35,
                'screening_weight': 0.35,
                'hr_weight': 0.30
            },
            'marketing_manager': {
                'ats_weight': 0.20,
                'screening_weight': 0.30,
                'hr_weight': 0.50
            },
            'fresher': {
                'ats_weight': 0.30,
                'screening_weight': 0.20,
                'hr_weight': 0.50
            }
        }
        self.role = role
        if custom_weights:
            self.weights = custom_weights
        else:
            self.weights = self.default_weights.get(role, self.default_weights['software_engineer'])
        self._validate_weights()
    
    def _validate_weights(self):
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            for k in self.weights:
                self.weights[k] /= total
    
    def set_role(self, role):
        if role in self.default_weights:
            self.weights = self.default_weights[role]
            self.role = role
            self._validate_weights()
            return True
        return False
    
    def calculate_hiring_fit(self, ats_score, screening_score, hr_score):
        final = (ats_score * self.weights['ats_weight'] +
                 screening_score * self.weights['screening_weight'] +
                 hr_score * self.weights['hr_weight'])
        return round(final, 2)
    
    def get_recommendation(self, final_score):
        if final_score >= 80:
            return "Strong Hire"
        elif final_score >= 65:
            return "Hire"
        elif final_score >= 50:
            return "Consider"
        else:
            return "Reject"
    
    def generate_unified_score(self, candidate_id, candidate_name, ats_score, screening_score, hr_score):
        final_score = self.calculate_hiring_fit(ats_score, screening_score, hr_score)
        recommendation = self.get_recommendation(final_score)
        return {
            'candidate_id': candidate_id,
            'candidate_name': candidate_name,
            'role': self.role,
            'weights_used': self.weights,
            'component_scores': {
                'ats_score': ats_score,
                'screening_score': screening_score,
                'hr_score': hr_score
            },
            'final_hiring_score': final_score,
            'recommendation': recommendation,
            'generated_at': datetime.now().isoformat()
        }
    
    def save_weights(self, filename='config/role_weights.json'):
        os.makedirs('config', exist_ok=True)   # <-- FIX: create config folder
        with open(filename, 'w') as f:
            json.dump(self.default_weights, f, indent=2)
        print(f"✅ Weights config saved: {filename}")

def main():
    print("="*70)
    print("DAY 41 - UNIFIED SCORING ENGINE")
    print("="*70)
    
    # Sample scores from previous days
    sample_candidates = [
        {
            'id': 'C001',
            'name': 'Midhun Raj',
            'ats_score': 96.5,
            'screening_score': 78.0,
            'hr_score': 67.16
        },
        {
            'id': 'C002',
            'name': 'Jane Smith',
            'ats_score': 44.8,
            'screening_score': 55.0,
            'hr_score': 50.0
        }
    ]
    
    roles = ['software_engineer', 'data_scientist', 'marketing_manager', 'fresher']
    
    for role in roles:
        print(f"\n{'='*50}")
        print(f"Role: {role.replace('_', ' ').title()}")
        print(f"{'='*50}")
        engine = UnifiedScoringEngine(role=role)
        print(f"Weights: ATS={engine.weights['ats_weight']*100:.0f}%, "
              f"Screening={engine.weights['screening_weight']*100:.0f}%, "
              f"HR={engine.weights['hr_weight']*100:.0f}%")
        for cand in sample_candidates:
            result = engine.generate_unified_score(
                cand['id'], cand['name'],
                cand['ats_score'], cand['screening_score'], cand['hr_score']
            )
            print(f"\nCandidate: {cand['name']} (ID: {cand['id']})")
            print(f"  ATS: {cand['ats_score']}% | Screening: {cand['screening_score']}% | HR: {cand['hr_score']}%")
            print(f"  Final Score: {result['final_hiring_score']}%")
            print(f"  Recommendation: {result['recommendation']}")
    
    # Save default weights config
    engine = UnifiedScoringEngine()
    engine.save_weights()
    
    # Save a sample unified score object
    sample_result = engine.generate_unified_score(
        'C001', 'Midhun Raj', 96.5, 78.0, 67.16
    )
    os.makedirs('output', exist_ok=True)
    with open('output/unified_score_sample.json', 'w') as f:
        json.dump(sample_result, f, indent=2)
    print("\n✅ Sample unified score saved: output/unified_score_sample.json")
    
    print("\n" + "="*70)
    print("✅ DAY 41 COMPLETED - UNIFIED SCORING ENGINE")
    print("="*70)

if __name__ == "__main__":
    main()