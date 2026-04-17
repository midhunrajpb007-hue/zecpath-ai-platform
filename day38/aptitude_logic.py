# aptitude_logic.py - Day 38 Aptitude Logic Design (Fixed)
import re
import json
import os
from datetime import datetime

class AptitudeLogic:
    def __init__(self):
        # Question bank for reasoning and situational judgment
        self.question_bank = {
            'reasoning': [
                {
                    'id': 'R1',
                    'question': 'If all Bloops are Razzies and all Razzies are Lazzies, then all Bloops are definitely Lazzies. True or False?',
                    'ideal_keywords': ['true', 'definitely', 'all', 'bloops', 'lazzies'],
                    'expected_logic': 'transitive property',
                    'score_weight': 1.0
                },
                {
                    'id': 'R2',
                    'question': 'A train travels 60 km in 1 hour. How long will it take to travel 150 km at the same speed?',
                    'ideal_keywords': ['2.5', 'hours', '150/60', 'speed', 'constant'],
                    'expected_logic': 'ratio and proportion',
                    'score_weight': 1.0
                },
                {
                    'id': 'R3',
                    'question': 'Complete the series: 2, 6, 12, 20, ?',
                    'ideal_keywords': ['30', 'pattern', 'difference', 'increasing'],
                    'expected_logic': 'difference increases by 2 each time',
                    'score_weight': 1.0
                }
            ],
            'situational': [
                {
                    'id': 'S1',
                    'question': 'You have two important deadlines tomorrow, but you can only complete one today. What do you do?',
                    'ideal_keywords': ['prioritize', 'deadline', 'communicate', 'manager', 'team', 'delegate'],
                    'expected_logic': 'prioritization + communication',
                    'score_weight': 1.0
                },
                {
                    'id': 'S2',
                    'question': 'A team member is consistently late with their work, affecting the whole team. How do you handle it?',
                    'ideal_keywords': ['talk', 'private', 'understand', 'reason', 'support', 'deadline', 'escalate'],
                    'expected_logic': 'one-on-one discussion + offer help + escalate if needed',
                    'score_weight': 1.0
                },
                {
                    'id': 'S3',
                    'question': 'You discover a critical bug in a product that is about to be released. What steps do you take?',
                    'ideal_keywords': ['assess', 'severity', 'report', 'manager', 'team', 'fix', 'delay', 'communication'],
                    'expected_logic': 'assess impact → report to manager → discuss with team → propose fix → communicate to stakeholders',
                    'score_weight': 1.0
                }
            ]
        }
    
    # ========== SCORING FUNCTIONS ==========
    def score_reasoning(self, answer, ideal_keywords):
        """Score reasoning answer based on keyword presence and logic"""
        answer_lower = answer.lower()
        matched = sum(1 for kw in ideal_keywords if kw in answer_lower)
        keyword_score = (matched / len(ideal_keywords)) * 70
        
        # Bonus for structured reasoning (length, connectors)
        word_count = len(answer.split())
        if word_count > 15:
            keyword_score += 15
        elif word_count > 8:
            keyword_score += 8
        
        # Penalize very short answers
        if word_count < 5:
            keyword_score -= 20
        
        final = max(0, min(100, keyword_score))
        return round(final, 2)
    
    def score_situational(self, answer, ideal_keywords):
        """Score situational judgment answer"""
        answer_lower = answer.lower()
        matched = sum(1 for kw in ideal_keywords if kw in answer_lower)
        keyword_score = (matched / len(ideal_keywords)) * 100
        # Bonus for logical sequence (presence of step indicators)
        step_indicators = ['first', 'then', 'next', 'after', 'finally', 'step']
        steps = sum(1 for ind in step_indicators if ind in answer_lower)
        keyword_score += min(10, steps * 3)
        final = max(0, min(100, keyword_score))
        return round(final, 2)
    
    def detect_problem_solving_clarity(self, answer):
        """Check for clear problem-solving steps"""
        answer_lower = answer.lower()
        clarity_score = 50
        # Look for structured words
        if any(w in answer_lower for w in ['first', 'second', 'then', 'next']):
            clarity_score += 20
        if any(w in answer_lower for w in ['because', 'therefore', 'so', 'hence']):
            clarity_score += 15
        if len(answer.split()) > 20:
            clarity_score += 10
        # Penalize vagueness
        vague_phrases = ['i don\'t know', 'not sure', 'maybe', 'probably']
        if any(p in answer_lower for p in vague_phrases):
            clarity_score -= 30
        return max(0, min(100, clarity_score))
    
    def evaluate_aptitude(self, answers):
        """
        answers: list of dicts with keys 'type' ('reasoning' or 'situational'), 'question_id', 'answer'
        """
        results = []
        total_score = 0
        for ans in answers:
            q_type = ans['type']
            q_id = ans['question_id']
            user_answer = ans['answer']
            # Find the question in bank
            question_data = None
            for q in self.question_bank[q_type]:
                if q['id'] == q_id:
                    question_data = q
                    break
            if not question_data:
                continue
            if q_type == 'reasoning':
                score = self.score_reasoning(user_answer, question_data['ideal_keywords'])
            else:
                score = self.score_situational(user_answer, question_data['ideal_keywords'])
            clarity = self.detect_problem_solving_clarity(user_answer)
            results.append({
                'question_id': q_id,
                'type': q_type,
                'question': question_data['question'],
                'answer': user_answer,
                'score': score,
                'clarity_score': clarity,
                'expected_logic': question_data.get('expected_logic', '')
            })
            total_score += score
        avg_score = total_score / len(answers) if answers else 0
        overall_clarity = sum(r['clarity_score'] for r in results) / len(results) if results else 0
        return {
            'individual_results': results,
            'average_score': round(avg_score, 2),
            'average_clarity': round(overall_clarity, 2),
            'total_questions': len(answers)
        }
    
    def generate_report(self, evaluation):
        """Generate final aptitude report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'aptitude_score': evaluation['average_score'],
            'problem_solving_clarity': evaluation['average_clarity'],
            'questions_answered': evaluation['total_questions'],
            'breakdown': evaluation['individual_results'],
            'interpretation': self._interpret_score(evaluation['average_score'])
        }
        return report
    
    def _interpret_score(self, score):
        if score >= 80:
            return "Excellent logical reasoning and problem-solving ability"
        elif score >= 60:
            return "Good logical reasoning, some room for improvement"
        elif score >= 40:
            return "Average logical reasoning, needs practice"
        else:
            return "Weak logical reasoning, requires significant improvement"

def main():
    print("="*70)
    print("DAY 38 - APTITUDE LOGIC DESIGN")
    print("="*70)
    
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    aptitude = AptitudeLogic()
    
    # Sample candidate answers (simulate interview)
    sample_answers = [
        {'type': 'reasoning', 'question_id': 'R1', 'answer': 'True, because if all Bloops are Razzies and all Razzies are Lazzies, then Bloops are Lazzies.'},
        {'type': 'reasoning', 'question_id': 'R2', 'answer': 'First, find speed = 60 km/h. Then time = distance/speed = 150/60 = 2.5 hours.'},
        {'type': 'reasoning', 'question_id': 'R3', 'answer': 'The differences are 4,6,8 so next difference is 10, so next number is 30.'},
        {'type': 'situational', 'question_id': 'S1', 'answer': 'First, I would assess which deadline is more critical. Then I would communicate with my manager to reprioritize. I would also see if I can delegate some tasks.'},
        {'type': 'situational', 'question_id': 'S2', 'answer': 'I would have a private conversation to understand the reason. Then offer support and set clear expectations. If it continues, escalate to manager.'},
        {'type': 'situational', 'question_id': 'S3', 'answer': 'First, assess severity. Then immediately inform the team and manager. Discuss a fix plan. If needed, delay release. Communicate with stakeholders.'}
    ]
    
    print("\n📋 APTITUDE EVALUATION")
    print("-"*50)
    evaluation = aptitude.evaluate_aptitude(sample_answers)
    
    for res in evaluation['individual_results']:
        print(f"\nQ{res['question_id']} ({res['type']}): {res['question'][:60]}...")
        print(f"  Answer: {res['answer'][:80]}...")
        print(f"  Score: {res['score']}% | Clarity: {res['clarity_score']}%")
    
    print(f"\n📊 OVERALL APTITUDE SCORE: {evaluation['average_score']}%")
    print(f"📊 PROBLEM-SOLVING CLARITY: {evaluation['average_clarity']}%")
    
    # Generate report
    report = aptitude.generate_report(evaluation)
    with open('output/aptitude_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("\n✅ Report saved: output/aptitude_report.json")
    
    # Save question bank as reference
    with open('data/aptitude_questions.json', 'w') as f:
        json.dump(aptitude.question_bank, f, indent=2)
    print("✅ Question bank saved: data/aptitude_questions.json")
    
    print("\n" + "="*70)
    print("✅ DAY 38 COMPLETED - APTITUDE LOGIC DESIGN")
    print("="*70)

if __name__ == "__main__":
    main()