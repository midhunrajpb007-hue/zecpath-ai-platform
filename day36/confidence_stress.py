# confidence_stress.py - Day 36 Confidence & Stress Indicators
import re
import json
from datetime import datetime

class ConfidenceStressAnalyzer:
    def __init__(self):
        # Hesitation indicators
        self.uncertainty_phrases = [
            'i think', 'i guess', 'i believe', 'maybe', 'perhaps',
            'not sure', 'i don\'t know', 'probably', 'possibly', 'could be'
        ]
        # Repeated word patterns (simple simulation)
        self.repeat_pattern = r'\b(\w+)\s+\1\b'
        # Long pause simulation (in text, represented by ellipsis or multiple dots)
        self.pause_pattern = r'\.{3,}|\.\s+\.'
        
        # Sentiment word lists
        self.positive_words = ['good', 'great', 'excellent', 'happy', 'confident', 'sure', 'definitely', 'absolutely']
        self.negative_words = ['bad', 'poor', 'terrible', 'unhappy', 'worried', 'nervous', 'stress', 'difficult']
        
        # Stress indicators
        self.stress_indicators = ['nervous', 'stress', 'anxious', 'worried', 'difficult', 'hard', 'problem', 'issue']
        
        # Filler words
        self.filler_words = ['um', 'uh', 'ah', 'er', 'hmm', 'like', 'you know', 'actually', 'basically']
    
    # ========== HESITATION DETECTION ==========
    def detect_hesitation(self, text):
        """Detect hesitation patterns: pauses, repeated words, uncertainty phrases"""
        text_lower = text.lower()
        # Uncertainty phrases
        uncertainty_count = sum(1 for phrase in self.uncertainty_phrases if phrase in text_lower)
        # Repeated words
        repeats = len(re.findall(self.repeat_pattern, text_lower))
        # Long pauses (ellipsis or multiple dots)
        pauses = len(re.findall(self.pause_pattern, text))
        
        # Hesitation score (higher = more hesitant)
        hesitation_score = min(100, (uncertainty_count * 10) + (repeats * 5) + (pauses * 10))
        # Invert so higher confidence = lower hesitation
        confidence_from_hesitation = 100 - hesitation_score
        
        return {
            'confidence_score': confidence_from_hesitation,
            'uncertainty_count': uncertainty_count,
            'repeated_words': repeats,
            'pause_count': pauses,
            'details': f"{uncertainty_count} uncertain, {repeats} repeats, {pauses} pauses"
        }
    
    # ========== SENTIMENT ANALYSIS ==========
    def analyze_sentiment(self, text):
        """Basic sentiment analysis using word lists"""
        text_lower = text.lower()
        pos_count = sum(1 for w in self.positive_words if w in text_lower)
        neg_count = sum(1 for w in self.negative_words if w in text_lower)
        total = pos_count + neg_count
        if total == 0:
            sentiment_score = 50  # neutral
            sentiment = 'neutral'
        else:
            ratio = (pos_count - neg_count) / total
            # Convert -1..1 to 0..100
            sentiment_score = 50 + (ratio * 50)
            if sentiment_score > 70:
                sentiment = 'positive'
            elif sentiment_score < 30:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
        return {
            'score': round(sentiment_score, 2),
            'sentiment': sentiment,
            'positive_words': pos_count,
            'negative_words': neg_count
        }
    
    # ========== CONTRADICTION DETECTION ==========
    def detect_contradictions(self, text):
        """Detect contradictory patterns (simplified)"""
        text_lower = text.lower()
        contradictions = 0
        # Look for "yes but no" patterns
        if 'yes' in text_lower and 'but' in text_lower and 'no' in text_lower:
            contradictions += 1
        # Look for "I have experience but not"
        if 'experience' in text_lower and 'not' in text_lower and ('no' in text_lower or 'never' in text_lower):
            contradictions += 1
        # Look for contradictory phrases
        if 'always' in text_lower and 'never' in text_lower:
            contradictions += 1
        if 'definitely' in text_lower and 'maybe' in text_lower:
            contradictions += 1
        
        # Contradiction score (higher contradictions = lower confidence)
        contradiction_penalty = min(30, contradictions * 15)
        confidence_after_contradiction = 100 - contradiction_penalty
        
        return {
            'confidence_score': confidence_after_contradiction,
            'contradiction_count': contradictions,
            'details': f"{contradictions} contradiction(s)"
        }
    
    # ========== STRESS INDICATORS ==========
    def measure_stress(self, text):
        """Measure stress indicators: filler words, short answers, negative words, etc."""
        text_lower = text.lower()
        # Filler word count
        filler_count = sum(1 for f in self.filler_words if f in text_lower)
        # Short answer stress (very short answers indicate stress)
        word_count = len(text.split())
        if word_count < 5:
            short_answer_penalty = 20
        elif word_count < 10:
            short_answer_penalty = 10
        else:
            short_answer_penalty = 0
        # Negative word count (from sentiment list)
        neg_count = sum(1 for w in self.negative_words if w in text_lower)
        # Stress indicator words
        stress_word_count = sum(1 for w in self.stress_indicators if w in text_lower)
        
        # Total penalty (max 50)
        total_penalty = min(50, (filler_count * 3) + short_answer_penalty + (neg_count * 5) + (stress_word_count * 10))
        stress_score = 100 - total_penalty
        
        return {
            'confidence_score': stress_score,
            'filler_count': filler_count,
            'short_answer_penalty': short_answer_penalty,
            'negative_words': neg_count,
            'stress_words': stress_word_count,
            'details': f"{filler_count} fillers, {short_answer_penalty} short penalty, {neg_count} negatives"
        }
    
    # ========== OVERALL BEHAVIORAL CONFIDENCE SCORE ==========
    def behavioral_confidence(self, text):
        """Combine all components into final confidence score (0-100)"""
        hesitation = self.detect_hesitation(text)
        sentiment = self.analyze_sentiment(text)
        contradiction = self.detect_contradictions(text)
        stress = self.measure_stress(text)
        
        # Weights
        weights = {
            'hesitation': 0.3,
            'sentiment': 0.2,
            'contradiction': 0.25,
            'stress': 0.25
        }
        
        final_score = (hesitation['confidence_score'] * weights['hesitation'] +
                       sentiment['score'] * weights['sentiment'] +
                       contradiction['confidence_score'] * weights['contradiction'] +
                       stress['confidence_score'] * weights['stress'])
        
        final_score = round(final_score, 2)
        
        # Determine confidence level
        if final_score >= 80:
            level = "High"
        elif final_score >= 60:
            level = "Medium"
        else:
            level = "Low"
        
        return {
            'overall_confidence_score': final_score,
            'confidence_level': level,
            'components': {
                'hesitation': hesitation,
                'sentiment': sentiment,
                'contradiction': contradiction,
                'stress': stress
            },
            'evaluated_at': datetime.now().isoformat()
        }

def main():
    print("="*70)
    print("DAY 36 - CONFIDENCE & STRESS INDICATORS")
    print("="*70)
    
    analyzer = ConfidenceStressAnalyzer()
    
    # Sample answers with different confidence/stress levels
    test_answers = [
        "I am definitely confident in my Python skills. I have worked on several projects.",
        "Um, I think maybe I have some experience, like 2 years? I'm not sure.",
        "I have 5 years of experience. I am sure I can handle the role. Absolutely confident.",
        "I don't know... maybe? It's difficult. I feel nervous about this question.",
        "Yes, I have experience. But no, I haven't worked on that. Actually, I have no experience in that area."
    ]
    
    print("\n📋 CONFIDENCE & STRESS ANALYSIS")
    print("-"*50)
    
    for i, ans in enumerate(test_answers, 1):
        print(f"\nAnswer {i}: {ans[:80]}...")
        result = analyzer.behavioral_confidence(ans)
        print(f"Overall Confidence Score: {result['overall_confidence_score']}% ({result['confidence_level']})")
        comp = result['components']
        print(f"  Hesitation: {comp['hesitation']['confidence_score']}% - {comp['hesitation']['details']}")
        print(f"  Sentiment: {comp['sentiment']['score']}% ({comp['sentiment']['sentiment']})")
        print(f"  Contradiction: {comp['contradiction']['confidence_score']}% - {comp['contradiction']['details']}")
        print(f"  Stress: {comp['stress']['confidence_score']}% - {comp['stress']['details']}")
    
    # Save sample output
    sample_output = {
        'model': 'ConfidenceStressAnalyzer',
        'formula': 'overall = hesitation*0.3 + sentiment*0.2 + contradiction*0.25 + stress*0.25',
        'sample_results': [analyzer.behavioral_confidence(ans) for ans in test_answers]
    }
    import os
    os.makedirs('output', exist_ok=True)
    with open('output/confidence_stress_report.json', 'w') as f:
        json.dump(sample_output, f, indent=2)
    print("\n✅ Report saved: output/confidence_stress_report.json")
    
    print("\n" + "="*70)
    print("✅ DAY 36 COMPLETED - CONFIDENCE & STRESS INDICATORS")
    print("="*70)

if __name__ == "__main__":
    main()