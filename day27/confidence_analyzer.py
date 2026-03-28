# confidence_analyzer.py - Day 27 Confidence & Sentiment Signal Analysis
import re
import json
from datetime import datetime

class ConfidenceAnalyzer:
    def __init__(self):
        # Filler words (hesitation indicators)
        self.filler_words = [
            'um', 'uh', 'ah', 'er', 'hmm', 'like', 'you know', 
            'actually', 'basically', 'sort of', 'kind of', 'well'
        ]
        
        # Positive sentiment words
        self.positive_words = [
            'good', 'great', 'excellent', 'awesome', 'amazing', 'happy',
            'confident', 'sure', 'yes', 'absolutely', 'definitely',
            'love', 'enjoy', 'passionate', 'excited', 'proud'
        ]
        
        # Negative sentiment words
        self.negative_words = [
            'bad', 'poor', 'terrible', 'awful', 'difficult', 'hard',
            'struggle', 'problem', 'issue', 'no', 'not', 'never',
            'dislike', 'hate', 'unhappy', 'frustrated', 'worried'
        ]
        
        # Uncertainty indicators
        self.uncertainty_words = [
            'maybe', 'perhaps', 'probably', 'possibly', 'i think',
            'i guess', 'not sure', 'i don\'t know', 'approximately',
            'around', 'about', 'roughly', 'could be', 'might be'
        ]
        
        # Contradiction patterns
        self.contradiction_patterns = [
            (r'\b(no|not|never)\b', r'\b(yes|always|definitely)\b'),
            (r'\b(i don\'t know)\b', r'\b(i know)\b'),
            (r'\b(maybe|perhaps)\b', r'\b(definitely|absolutely)\b')
        ]
    
    # ========== HESITATION DETECTION ==========
    
    def detect_hesitation(self, text):
        """Detect hesitation patterns in speech"""
        text_lower = text.lower()
        filler_count = 0
        filler_found = []
        
        for filler in self.filler_words:
            if filler in text_lower:
                filler_count += 1
                filler_found.append(filler)
        
        # Calculate hesitation score (0-100)
        # More filler words = lower score
        words = text.split()
        word_count = len(words)
        
        if word_count == 0:
            hesitation_score = 0
        else:
            filler_ratio = filler_count / word_count
            hesitation_score = max(0, 100 - (filler_ratio * 200))
        
        return {
            'hesitation_score': round(hesitation_score, 2),
            'filler_count': filler_count,
            'filler_words': filler_found[:5],  # Top 5 filler words
            'word_count': word_count,
            'details': f"{filler_count} filler words in {word_count} words"
        }
    
    # ========== RESPONSE LENGTH & PACE ==========
    
    def measure_response(self, text):
        """Measure response length and estimate pace"""
        words = text.split()
        word_count = len(words)
        
        # Estimate speaking pace (assume 2-3 seconds per word? simplified)
        # In real system, you'd have actual timestamps
        if word_count < 5:
            pace_rating = "very short"
            pace_score = 30
        elif word_count < 10:
            pace_rating = "short"
            pace_score = 50
        elif word_count < 20:
            pace_rating = "medium"
            pace_score = 70
        elif word_count < 40:
            pace_rating = "long"
            pace_score = 85
        else:
            pace_rating = "very long"
            pace_score = 60
        
        return {
            'word_count': word_count,
            'pace_score': pace_score,
            'pace_rating': pace_rating,
            'details': f"{word_count} words - {pace_rating} response"
        }
    
    # ========== SENTIMENT ANALYSIS ==========
    
    def analyze_sentiment(self, text):
        """Analyze positive/negative sentiment"""
        text_lower = text.lower()
        positive_count = 0
        negative_count = 0
        
        for word in self.positive_words:
            if word in text_lower:
                positive_count += 1
        
        for word in self.negative_words:
            if word in text_lower:
                negative_count += 1
        
        # Calculate sentiment score (-100 to 100, convert to 0-100)
        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 50  # neutral
            sentiment = "neutral"
        else:
            raw_score = ((positive_count - negative_count) / total) * 100
            sentiment_score = 50 + (raw_score / 2)
            sentiment_score = max(0, min(100, sentiment_score))
            
            if sentiment_score > 70:
                sentiment = "positive"
            elif sentiment_score < 30:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            'sentiment_score': round(sentiment_score, 2),
            'sentiment': sentiment,
            'positive_words': positive_count,
            'negative_words': negative_count,
            'details': f"{positive_count} positive, {negative_count} negative words"
        }
    
    # ========== UNCERTAINTY DETECTION ==========
    
    def detect_uncertainty(self, text):
        """Detect uncertainty in responses"""
        text_lower = text.lower()
        uncertainty_count = 0
        uncertainty_terms = []
        
        for term in self.uncertainty_words:
            if term in text_lower:
                uncertainty_count += 1
                uncertainty_terms.append(term)
        
        # Calculate uncertainty score (0-100)
        # More uncertainty = lower confidence
        words = text.split()
        word_count = len(words)
        
        if word_count == 0:
            uncertainty_score = 0
        else:
            uncertainty_ratio = uncertainty_count / word_count
            uncertainty_score = max(0, 100 - (uncertainty_ratio * 100))
        
        return {
            'uncertainty_score': round(uncertainty_score, 2),
            'uncertainty_count': uncertainty_count,
            'uncertainty_terms': uncertainty_terms[:5],
            'details': f"{uncertainty_count} uncertainty indicators"
        }
    
    # ========== CONTRADICTION DETECTION ==========
    
    def detect_contradictions(self, text, previous_texts=None):
        """Detect contradictions within answer or with previous answers"""
        text_lower = text.lower()
        contradictions = []
        
        # Check internal contradictions
        for pattern1, pattern2 in self.contradiction_patterns:
            if re.search(pattern1, text_lower) and re.search(pattern2, text_lower):
                contradictions.append(f"Internal: {pattern1} and {pattern2}")
        
        # Check with previous answers
        if previous_texts:
            for prev in previous_texts:
                prev_lower = prev.lower()
                for pattern1, pattern2 in self.contradiction_patterns:
                    if re.search(pattern1, text_lower) and re.search(pattern2, prev_lower):
                        contradictions.append(f"With previous: {pattern1} and {pattern2}")
                    elif re.search(pattern2, text_lower) and re.search(pattern1, prev_lower):
                        contradictions.append(f"With previous: {pattern2} and {pattern1}")
        
        # Calculate contradiction score (0-100)
        contradiction_score = max(0, 100 - (len(contradictions) * 20))
        
        return {
            'contradiction_score': contradiction_score,
            'contradiction_count': len(contradictions),
            'contradictions': contradictions[:3],
            'details': f"{len(contradictions)} contradictions found"
        }
    
    # ========== COMMUNICATION STRENGTH ==========
    
    def analyze_communication_strength(self, text, previous_texts=None):
        """Overall communication strength analysis"""
        hesitation = self.detect_hesitation(text)
        response = self.measure_response(text)
        sentiment = self.analyze_sentiment(text)
        uncertainty = self.detect_uncertainty(text)
        contradictions = self.detect_contradictions(text, previous_texts)
        
        # Calculate overall score
        scores = [
            hesitation['hesitation_score'],
            response['pace_score'],
            sentiment['sentiment_score'],
            uncertainty['uncertainty_score'],
            contradictions['contradiction_score']
        ]
        overall = sum(scores) / len(scores)
        
        # Determine rating
        if overall >= 80:
            rating = "Excellent communication"
        elif overall >= 60:
            rating = "Good communication"
        elif overall >= 40:
            rating = "Average communication"
        else:
            rating = "Needs improvement"
        
        return {
            'overall_score': round(overall, 2),
            'rating': rating,
            'components': {
                'hesitation': hesitation,
                'response_length': response,
                'sentiment': sentiment,
                'uncertainty': uncertainty,
                'contradictions': contradictions
            },
            'evaluated_at': datetime.now().isoformat()
        }
    
    def generate_behavioral_report(self, analysis):
        """Generate behavioral indicators report"""
        comp = analysis['components']
        
        report = {
            'overall_score': analysis['overall_score'],
            'rating': analysis['rating'],
            'behavioral_indicators': {
                'confidence_level': {
                    'score': comp['hesitation']['hesitation_score'],
                    'details': comp['hesitation']['details']
                },
                'communication_pace': {
                    'score': comp['response_length']['pace_score'],
                    'details': comp['response_length']['details']
                },
                'sentiment_tone': {
                    'score': comp['sentiment']['sentiment_score'],
                    'details': comp['sentiment']['details']
                },
                'certainty_level': {
                    'score': comp['uncertainty']['uncertainty_score'],
                    'details': comp['uncertainty']['details']
                },
                'consistency': {
                    'score': comp['contradictions']['contradiction_score'],
                    'details': comp['contradictions']['details']
                }
            }
        }
        
        return report
    
    def save_report(self, report, filename='output/behavioral_report.json'):
        """Save report"""
        import os
        os.makedirs('output', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✅ Report saved: {filename}")

def main():
    print("="*70)
    print("DAY 27 - CONFIDENCE & SENTIMENT SIGNAL ANALYSIS")
    print("="*70)
    
    analyzer = ConfidenceAnalyzer()
    
    # Sample answers from candidates
    answers = [
        "I am a software developer with 3 years of experience in Python and React.",
        "Um, I think I have like maybe 2 or 3 years of experience... I'm not sure exactly.",
        "Yes! I'm absolutely confident in my Python skills. I love coding and I'm very passionate about it.",
        "I don't know... maybe 5 years? I'm not sure. Probably around that.",
        "I have experience with Java and Spring. No, wait, actually I have more experience with Python.",
        "I can join immediately. I'm very excited about this opportunity!"
    ]
    
    print("\n📋 CONFIDENCE & SENTIMENT ANALYSIS")
    print("="*70)
    
    previous_texts = []
    for i, ans in enumerate(answers, 1):
        print(f"\n--- Answer {i} ---")
        print(f"Text: {ans[:80]}...")
        
        analysis = analyzer.analyze_communication_strength(ans, previous_texts)
        
        print(f"Overall Score: {analysis['overall_score']}% ({analysis['rating']})")
        print(f"   Hesitation: {analysis['components']['hesitation']['hesitation_score']}% - {analysis['components']['hesitation']['details']}")
        print(f"   Pace: {analysis['components']['response_length']['pace_score']}% - {analysis['components']['response_length']['details']}")
        print(f"   Sentiment: {analysis['components']['sentiment']['sentiment_score']}% - {analysis['components']['sentiment']['sentiment']}")
        print(f"   Uncertainty: {analysis['components']['uncertainty']['uncertainty_score']}% - {analysis['components']['uncertainty']['details']}")
        print(f"   Contradictions: {analysis['components']['contradictions']['contradiction_score']}% - {analysis['components']['contradictions']['details']}")
        
        previous_texts.append(ans)
    
    # Generate behavioral report for first answer
    print("\n" + "="*70)
    print("📊 BEHAVIORAL INDICATORS REPORT (Sample)")
    print("="*70)
    
    sample_analysis = analyzer.analyze_communication_strength(answers[0])
    report = analyzer.generate_behavioral_report(sample_analysis)
    
    print(json.dumps(report, indent=2))
    
    # Save report
    analyzer.save_report(report)
    
    print("\n" + "="*70)
    print("✅ DAY 27 COMPLETED - CONFIDENCE & SENTIMENT ANALYSIS")
    print("="*70)

if __name__ == "__main__":
    main()