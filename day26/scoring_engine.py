# scoring_engine.py - Day 26 Screening Scoring Engine
import re
import json
from datetime import datetime

class ScoringEngine:
    def __init__(self):
        # Scoring weights
        self.weights = {
            'clarity': 0.3,
            'relevance': 0.3,
            'completeness': 0.2,
            'consistency': 0.2
        }
        
        # Keyword patterns for relevance scoring
        self.keywords = {
            'skills': ['python', 'java', 'react', 'javascript', 'sql', 'aws', 'docker'],
            'experience': ['years', 'experience', 'worked', 'company', 'role'],
            'salary': ['lakh', 'lpa', 'thousand', 'salary', 'ctc'],
            'availability': ['immediate', 'days', 'notice', 'join', 'start']
        }
        
        # Vague phrases (for clarity score)
        self.vague_phrases = ['not sure', 'maybe', 'probably', 'i think', 'around', 'approximately', 'like']
        
        # Filler words (for clarity score)
        self.filler_words = ['um', 'uh', 'ah', 'er', 'like', 'you know', 'actually']
    
    # ========== SCORING FUNCTIONS ==========
    
    def score_clarity(self, text):
        """Score how clear the answer is (0-100)"""
        original_len = len(text)
        words = text.split()
        word_count = len(words)
        
        # Start with base score
        score = 80
        
        # Penalty for filler words
        filler_count = 0
        text_lower = text.lower()
        for filler in self.filler_words:
            if filler in text_lower:
                filler_count += 1
                score -= 5
        
        # Penalty for vague phrases
        for phrase in self.vague_phrases:
            if phrase in text_lower:
                score -= 10
        
        # Penalty for very short answers
        if word_count < 5:
            score -= 20
        elif word_count < 10:
            score -= 10
        
        # Bonus for longer answers (but not too long)
        if 10 <= word_count <= 30:
            score += 5
        
        # Cap between 0 and 100
        score = max(0, min(100, score))
        
        return {
            'score': score,
            'word_count': word_count,
            'filler_count': filler_count,
            'details': f"{word_count} words, {filler_count} filler words"
        }
    
    def score_relevance(self, text, question_intent):
        """Score how relevant the answer is to the question (0-100)"""
        text_lower = text.lower()
        score = 0
        matched_keywords = []
        
        # Get keywords for this intent
        keywords = self.keywords.get(question_intent, [])
        
        # If no specific keywords, use generic
        if not keywords:
            keywords = ['experience', 'skill', 'work', 'job']
        
        # Count matching keywords
        for keyword in keywords:
            if keyword in text_lower:
                score += 20
                matched_keywords.append(keyword)
        
        # Cap at 100
        score = min(100, score)
        
        return {
            'score': score,
            'matched_keywords': matched_keywords,
            'details': f"Matched {len(matched_keywords)} keywords: {matched_keywords}"
        }
    
    def score_completeness(self, text, question_intent):
        """Score how complete the answer is (0-100)"""
        text_lower = text.lower()
        score = 0
        checks_passed = []
        
        # Check 1: Has at least 5 words
        if len(text.split()) >= 5:
            score += 25
            checks_passed.append("Sufficient length (≥5 words)")
        
        # Check 2: Has proper ending (., !, ?)
        if text.strip()[-1] in '.!?':
            score += 25
            checks_passed.append("Proper ending punctuation")
        
        # Check 3: Contains key information based on intent
        if question_intent == 'skills' and any(s in text_lower for s in ['python', 'java', 'react', 'javascript']):
            score += 25
            checks_passed.append("Skills mentioned")
        elif question_intent == 'experience' and any(s in text_lower for s in ['years', 'experience']):
            score += 25
            checks_passed.append("Experience mentioned")
        elif question_intent == 'salary' and any(s in text_lower for s in ['lakh', 'lpa', 'salary']):
            score += 25
            checks_passed.append("Salary mentioned")
        elif question_intent == 'availability' and any(s in text_lower for s in ['immediate', 'days', 'notice']):
            score += 25
            checks_passed.append("Availability mentioned")
        else:
            # Generic check - if answer is longer than 10 words
            if len(text.split()) > 10:
                score += 25
                checks_passed.append("Detailed answer")
        
        # Check 4: No vague phrases
        vague_found = False
        for phrase in self.vague_phrases:
            if phrase in text_lower:
                vague_found = True
                break
        if not vague_found:
            score += 25
            checks_passed.append("Clear, no vague phrases")
        
        # Cap at 100
        score = min(100, score)
        
        return {
            'score': score,
            'checks_passed': checks_passed,
            'details': f"{len(checks_passed)}/4 checks passed"
        }
    
    def score_consistency(self, text, previous_answers=None):
        """Score consistency with previous answers (simplified)"""
        # For now, return base score (can be enhanced later)
        if not previous_answers:
            return {
                'score': 80,
                'details': 'No previous answers to compare'
            }
        
        # Simple check: look for contradictions
        text_lower = text.lower()
        contradictions = 0
        
        for prev in previous_answers:
            prev_lower = prev.lower()
            # Check for contradictory phrases
            if 'not' in text_lower and 'not' not in prev_lower:
                if any(word in text_lower for word in ['available', 'ready']):
                    contradictions += 1
        
        score = 80 - (contradictions * 20)
        score = max(0, min(100, score))
        
        return {
            'score': score,
            'contradictions': contradictions,
            'details': f"{contradictions} contradictions found"
        }
    
    # ========== SCORE AGGREGATION ==========
    
    def calculate_total_score(self, scores):
        """Calculate weighted total score"""
        total = (scores['clarity']['score'] * self.weights['clarity'] +
                 scores['relevance']['score'] * self.weights['relevance'] +
                 scores['completeness']['score'] * self.weights['completeness'] +
                 scores['consistency']['score'] * self.weights['consistency'])
        
        return round(total, 2)
    
    def score_answer(self, text, question_intent, previous_answers=None):
        """Score a single answer with all parameters"""
        
        clarity = self.score_clarity(text)
        relevance = self.score_relevance(text, question_intent)
        completeness = self.score_completeness(text, question_intent)
        consistency = self.score_consistency(text, previous_answers)
        
        scores = {
            'clarity': clarity,
            'relevance': relevance,
            'completeness': completeness,
            'consistency': consistency
        }
        
        total = self.calculate_total_score(scores)
        
        return {
            'answer': text,
            'intent': question_intent,
            'scores': scores,
            'total_score': total,
            'weights_used': self.weights,
            'evaluated_at': datetime.now().isoformat()
        }
    
    def normalize_scores(self, scores_list):
        """Normalize a list of scores to 0-100 range"""
        if not scores_list:
            return []
        
        min_score = min(scores_list)
        max_score = max(scores_list)
        
        if max_score == min_score:
            return [50] * len(scores_list)
        
        normalized = []
        for score in scores_list:
            norm = ((score - min_score) / (max_score - min_score)) * 100
            normalized.append(round(norm, 2))
        
        return normalized
    
    def aggregate_screening_score(self, answers):
        """Aggregate all answers into final screening score"""
        total = 0
        scores_by_question = []
        
        for ans in answers:
            total += ans['total_score']
            scores_by_question.append({
                'question_intent': ans['intent'],
                'score': ans['total_score'],
                'breakdown': ans['scores']
            })
        
        avg = total / len(answers) if answers else 0
        
        return {
            'total_answers': len(answers),
            'average_score': round(avg, 2),
            'scores_by_question': scores_by_question,
            'normalized_scores': self.normalize_scores([a['total_score'] for a in answers]),
            'weights_used': self.weights
        }
    
    def generate_explainable_output(self, score_result):
        """Generate human-readable explanation"""
        total = score_result['total_score']
        
        if total >= 80:
            rating = "Excellent"
            recommendation = "Strongly recommend for next round"
        elif total >= 60:
            rating = "Good"
            recommendation = "Recommend for next round"
        elif total >= 40:
            rating = "Average"
            recommendation = "Consider for review"
        else:
            rating = "Poor"
            recommendation = "Not recommended for next round"
        
        breakdown = score_result['scores']
        
        return f"""
        Score: {total}% ({rating})
        
        Breakdown:
        • Clarity: {breakdown['clarity']['score']}% - {breakdown['clarity']['details']}
        • Relevance: {breakdown['relevance']['score']}% - {breakdown['relevance']['details']}
        • Completeness: {breakdown['completeness']['score']}% - {breakdown['completeness']['details']}
        • Consistency: {breakdown['consistency']['score']}% - {breakdown['consistency']['details']}
        
        Recommendation: {recommendation}
        """
    
    def save_report(self, report, filename='output/screening_report.json'):
        """Save report"""
        import os
        os.makedirs('output', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✅ Report saved: {filename}")

def main():
    print("="*70)
    print("DAY 26 - SCREENING SCORING ENGINE")
    print("="*70)
    
    engine = ScoringEngine()
    
    # Sample answers from a candidate
    answers = [
        engine.score_answer("I know Python, Java, and React. I have 3 years of experience.", "skills"),
        engine.score_answer("I have 5 years of experience in software development.", "experience"),
        engine.score_answer("My expected salary is around 12 lakhs.", "salary"),
        engine.score_answer("I can join in 30 days.", "availability"),
        engine.score_answer("I like watching movies.", "skills"),  # Off-topic
        engine.score_answer("I'm not sure about salary.", "salary")  # Vague
    ]
    
    print("\n📋 SCORING RESULTS")
    print("="*60)
    
    for i, ans in enumerate(answers, 1):
        print(f"\nQ{i}: {ans['intent']}")
        print(f"   Answer: {ans['answer'][:50]}...")
        print(f"   Score: {ans['total_score']}%")
        print(f"   Breakdown:")
        print(f"      Clarity: {ans['scores']['clarity']['score']}%")
        print(f"      Relevance: {ans['scores']['relevance']['score']}%")
        print(f"      Completeness: {ans['scores']['completeness']['score']}%")
        print(f"      Consistency: {ans['scores']['consistency']['score']}%")
    
    # Aggregate all scores
    print("\n" + "="*60)
    print("📊 AGGREGATED SCREENING SCORE")
    print("="*60)
    
    aggregated = engine.aggregate_screening_score(answers)
    print(f"\nTotal Answers: {aggregated['total_answers']}")
    print(f"Average Score: {aggregated['average_score']}%")
    print(f"Normalized Scores: {aggregated['normalized_scores']}")
    
    print("\n📋 SCORES BY QUESTION:")
    for q in aggregated['scores_by_question']:
        print(f"   {q['question_intent']}: {q['score']}%")
    
    # Generate explainable output for first answer
    print("\n" + "="*60)
    print("📝 EXPLAINABLE OUTPUT (Sample)")
    print("="*60)
    print(engine.generate_explainable_output(answers[0]))
    
    # Save report
    report = {
        'generated_at': datetime.now().isoformat(),
        'candidate_scores': [a['total_score'] for a in answers],
        'aggregated': aggregated,
        'weights': engine.weights
    }
    engine.save_report(report)
    
    print("\n" + "="*70)
    print("✅ DAY 26 COMPLETED - SCREENING SCORING ENGINE")
    print("="*70)

if __name__ == "__main__":
    main()