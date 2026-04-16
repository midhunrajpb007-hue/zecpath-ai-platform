# hr_scoring_engine.py - Day 37 HR Interview Scoring Engine
import json
from datetime import datetime

class HRScoringEngine:
    def __init__(self, weights_config=None):
        # Default weights
        if weights_config is None:
            self.weights = {
                'relevance': 0.35,
                'communication': 0.30,
                'confidence': 0.25,
                'consistency': 0.10
            }
        else:
            self.weights = weights_config
        self._validate_weights()
    
    def _validate_weights(self):
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            # Normalize
            for k in self.weights:
                self.weights[k] /= total
    
    # ========== SCORING PARAMETERS ==========
    def score_relevance(self, answers, expected_keywords):
        """Score relevance based on keyword matching"""
        if not answers:
            return 0, "No answers"
        total_score = 0
        for ans in answers:
            ans_lower = ans.lower()
            matched = sum(1 for kw in expected_keywords if kw in ans_lower)
            if expected_keywords:
                score = (matched / len(expected_keywords)) * 100
            else:
                score = 50
            total_score += score
        avg = total_score / len(answers)
        return round(avg, 2), f"{len(answers)} answers, matched keywords"
    
    def score_communication(self, comm_scores):
        """Communication score from Day 35 (already 0-100)"""
        if not comm_scores:
            return 0, "No communication scores"
        avg = sum(comm_scores) / len(comm_scores)
        return round(avg, 2), f"average of {len(comm_scores)} answers"
    
    def score_confidence(self, conf_scores):
        """Confidence score from Day 36 (already 0-100)"""
        if not conf_scores:
            return 0, "No confidence scores"
        avg = sum(conf_scores) / len(conf_scores)
        return round(avg, 2), f"average of {len(conf_scores)} answers"
    
    def score_consistency(self, answers):
        """Simple consistency: variance in answer lengths (lower variance = higher consistency)"""
        if len(answers) < 2:
            return 80, "Only one answer"
        lengths = [len(ans.split()) for ans in answers]
        if max(lengths) == min(lengths):
            variance = 0
        else:
            mean = sum(lengths) / len(lengths)
            variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
        # Convert variance to 0-100 score (higher variance = lower consistency)
        # Cap variance effect
        consistency = max(0, 100 - (variance * 2))
        consistency = min(100, consistency)
        return round(consistency, 2), f"variance={variance:.1f}"
    
    # ========== OVERALL SCORE ==========
    def calculate_hr_score(self, answers, expected_keywords, comm_scores, conf_scores):
        """Combine all components"""
        relevance_score, relevance_detail = self.score_relevance(answers, expected_keywords)
        comm_score, comm_detail = self.score_communication(comm_scores)
        conf_score, conf_detail = self.score_confidence(conf_scores)
        consistency_score, consistency_detail = self.score_consistency(answers)
        
        final = (relevance_score * self.weights['relevance'] +
                 comm_score * self.weights['communication'] +
                 conf_score * self.weights['confidence'] +
                 consistency_score * self.weights['consistency'])
        
        final = round(final, 2)
        
        return {
            'final_hr_score': final,
            'components': {
                'relevance': {'score': relevance_score, 'detail': relevance_detail},
                'communication': {'score': comm_score, 'detail': comm_detail},
                'confidence': {'score': conf_score, 'detail': conf_detail},
                'consistency': {'score': consistency_score, 'detail': consistency_detail}
            },
            'weights_used': self.weights,
            'evaluated_at': datetime.now().isoformat()
        }
    
    # ========== NORMALIZATION (adjust for different interview lengths) ==========
    def normalize_score(self, score, min_possible=0, max_possible=100):
        """Simple min-max normalization (already in range)"""
        return max(0, min(100, score))
    
    def save_config(self, filename='config/weights_config.json'):
        import os
        os.makedirs('config', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.weights, f, indent=2)
        print(f"✅ Config saved: {filename}")
    
    def load_config(self, filename='config/weights_config.json'):
        try:
            with open(filename, 'r') as f:
                self.weights = json.load(f)
            self._validate_weights()
            print(f"✅ Config loaded: {filename}")
        except FileNotFoundError:
            print(f"⚠️ Config file not found, using defaults")

def main():
    print("="*70)
    print("DAY 37 - HR INTERVIEW SCORING ENGINE")
    print("="*70)
    
    # Sample data from previous days
    # Answers to HR questions (from Day 33)
    hr_answers = [
        "I have 4 years of experience in software development, mainly in Python and React.",
        "My greatest strength is problem-solving and teamwork. I'm looking to grow into a tech lead role.",
        "I can join in 30 days. I am excited about this opportunity."
    ]
    # Expected keywords for relevance (for HR questions)
    expected_keywords = ['experience', 'years', 'strength', 'team', 'join', 'days']
    
    # Communication scores from Day 35 (for each answer)
    comm_scores = [89.0, 85.5, 80.0]   # example from Day 35
    # Confidence scores from Day 36 (for each answer)
    conf_scores = [99.25, 85.0, 62.75] # example from Day 36
    
    engine = HRScoringEngine()
    
    # Calculate HR score
    result = engine.calculate_hr_score(hr_answers, expected_keywords, comm_scores, conf_scores)
    
    print("\n📋 HR SCORE REPORT")
    print("-"*50)
    print(f"Final HR Score: {result['final_hr_score']}%")
    print(f"Components:")
    print(f"  Relevance: {result['components']['relevance']['score']}% - {result['components']['relevance']['detail']}")
    print(f"  Communication: {result['components']['communication']['score']}% - {result['components']['communication']['detail']}")
    print(f"  Confidence: {result['components']['confidence']['score']}% - {result['components']['confidence']['detail']}")
    print(f"  Consistency: {result['components']['consistency']['score']}% - {result['components']['consistency']['detail']}")
    print(f"Weights: Relevance={engine.weights['relevance']*100}%, Comm={engine.weights['communication']*100}%, Conf={engine.weights['confidence']*100}%, Cons={engine.weights['consistency']*100}%")
    
    # Normalize (just ensure 0-100)
    normalized = engine.normalize_score(result['final_hr_score'])
    print(f"\nNormalized Score: {normalized}%")
    
    # Save sample report
    sample_report = {
        'candidate_id': 'C001',
        'hr_score': result['final_hr_score'],
        'normalized_score': normalized,
        'breakdown': result['components'],
        'weights': engine.weights,
        'generated_at': datetime.now().isoformat()
    }
    import os
    os.makedirs('output', exist_ok=True)
    with open('output/hr_score_report.json', 'w') as f:
        json.dump(sample_report, f, indent=2)
    print("\n✅ Sample HR score report saved: output/hr_score_report.json")
    
    # Save default weights config
    engine.save_config()
    
    print("\n" + "="*70)
    print("✅ DAY 37 COMPLETED - HR INTERVIEW SCORING ENGINE")
    print("="*70)

if __name__ == "__main__":
    main()