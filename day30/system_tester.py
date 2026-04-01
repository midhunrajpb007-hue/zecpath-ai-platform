# system_tester.py - Day 30 Screening System Testing & Optimization
import json
import random
from datetime import datetime

class SystemTester:
    def __init__(self):
        self.test_results = []
        self.metrics = {
            'total_tests': 0,
            'correct_intents': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'score_errors': []
        }
        
        # Sample test cases (simulated candidates)
        self.test_cases = [
            {
                'id': 'T001',
                'answers': {
                    'skills': 'I know Python, Java, and React',
                    'experience': 'I have 5 years of experience',
                    'salary': 'I expect around 15 lakhs',
                    'availability': 'I can join in 30 days'
                },
                'expected_intents': ['skills', 'experience', 'salary', 'availability'],
                'expected_scores': [90, 95, 85, 80],
                'human_decision': 'shortlist'
            },
            {
                'id': 'T002',
                'answers': {
                    'skills': 'I know some Python',
                    'experience': 'Maybe 2 years? I am not sure',
                    'salary': 'I don\'t know',
                    'availability': 'Not sure'
                },
                'expected_intents': ['skills', 'experience', 'salary', 'availability'],
                'expected_scores': [50, 40, 30, 35],
                'human_decision': 'reject'
            },
            {
                'id': 'T003',
                'answers': {
                    'skills': 'I am proficient in Python, Django, and PostgreSQL',
                    'experience': 'I have 3 years of professional experience',
                    'salary': 'My expected salary is 10 lakhs',
                    'availability': 'I have a 15 days notice period'
                },
                'expected_intents': ['skills', 'experience', 'salary', 'availability'],
                'expected_scores': [85, 80, 90, 85],
                'human_decision': 'shortlist'
            },
            {
                'id': 'T004',
                'answers': {
                    'skills': 'I like watching movies',
                    'experience': 'I have no experience',
                    'salary': 'I want high salary',
                    'availability': 'I can join anytime'
                },
                'expected_intents': ['skills', 'experience', 'salary', 'availability'],
                'expected_scores': [20, 10, 15, 70],
                'human_decision': 'reject'
            },
            {
                'id': 'T005',
                'answers': {
                    'skills': 'I have experience with Java, Spring Boot, and MySQL',
                    'experience': '4 years in backend development',
                    'salary': 'Expecting around 12-14 lakhs',
                    'availability': '30 days notice period'
                },
                'expected_intents': ['skills', 'experience', 'salary', 'availability'],
                'expected_scores': [88, 85, 82, 80],
                'human_decision': 'shortlist'
            }
        ]
    
    # ========== SIMULATED INTENT DETECTION ==========
    
    def detect_intent(self, answer, expected_intent):
        """Simulate intent detection (improved version)"""
        answer_lower = answer.lower()
        
        # Improved skill detection
        skill_keywords = ['python', 'java', 'react', 'javascript', 'sql', 'aws', 'django', 'spring', 'mysql']
        if expected_intent == 'skills':
            for kw in skill_keywords:
                if kw in answer_lower:
                    return True
            if len(answer.split()) < 3:
                return False
            return any(word in answer_lower for word in ['know', 'proficient', 'experience'])
        
        # Experience detection
        if expected_intent == 'experience':
            if 'year' in answer_lower or 'yr' in answer_lower:
                import re
                if re.search(r'\d+', answer):
                    return True
            return 'experience' in answer_lower
        
        # Salary detection
        if expected_intent == 'salary':
            salary_indicators = ['lakh', 'lpa', 'salary', 'ctc', 'thousand', 'k']
            return any(ind in answer_lower for ind in salary_indicators)
        
        # Availability detection
        if expected_intent == 'availability':
            avail_indicators = ['join', 'notice', 'days', 'immediate', 'available', 'start']
            return any(ind in answer_lower for ind in avail_indicators)
        
        return True
    
    # ========== SIMULATED SCORING ==========
    
    def calculate_score(self, answer, expected_score):
        """Calculate score with improved logic"""
        answer_lower = answer.lower()
        score = 50  # base score
        
        # Boost based on answer quality
        word_count = len(answer.split())
        if word_count >= 5:
            score += 20
        elif word_count >= 3:
            score += 10
        
        # Boost for specific keywords
        if 'year' in answer_lower or 'years' in answer_lower:
            score += 10
        if 'lakh' in answer_lower or 'lpa' in answer_lower:
            score += 10
        if 'immediate' in answer_lower:
            score += 15
        
        # Penalize vague answers
        vague_phrases = ['not sure', 'i don\'t know', 'maybe', 'probably', 'around']
        for phrase in vague_phrases:
            if phrase in answer_lower:
                score -= 20
        
        # Cap and return
        score = max(0, min(100, score))
        
        # Compare with expected (for tuning)
        diff = abs(score - expected_score)
        if diff > 20:
            self.metrics['score_errors'].append({
                'answer': answer[:50],
                'expected': expected_score,
                'got': score,
                'diff': diff
            })
        
        return score
    
    # ========== THRESHOLD TUNING ==========
    
    def tune_thresholds(self, scores, human_decisions):
        """Find optimal thresholds to reduce false rejections"""
        thresholds = [50, 55, 60, 65, 70, 75]
        best_threshold = 70
        best_accuracy = 0
        
        print("\n📊 THRESHOLD TUNING")
        print("-" * 40)
        
        for threshold in thresholds:
            correct = 0
            for i, score in enumerate(scores):
                ai_decision = 'shortlist' if score >= threshold else 'reject'
                if ai_decision == human_decisions[i]:
                    correct += 1
            
            accuracy = (correct / len(scores)) * 100
            print(f"Threshold {threshold}: {accuracy:.1f}% accuracy")
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_threshold = threshold
        
        print(f"\n✅ Best threshold: {best_threshold} ({best_accuracy:.1f}% accuracy)")
        return best_threshold
    
    # ========== SIMULATE AI CALLS ==========
    
    def run_simulation(self):
        """Run simulated AI screening calls"""
        print("\n" + "="*70)
        print("🎙️ AI SCREENING CALL SIMULATION")
        print("="*70)
        
        all_scores = []
        all_human_decisions = []
        intent_correct = 0
        intent_total = 0
        
        for test in self.test_cases:
            print(f"\n📋 Test Case: {test['id']}")
            print("-" * 40)
            
            scores = []
            intent_results = []
            
            for i, (intent, answer) in enumerate(test['answers'].items()):
                expected_intent = test['expected_intents'][i]
                expected_score = test['expected_scores'][i]
                
                # Detect intent
                intent_correct_flag = self.detect_intent(answer, expected_intent)
                intent_correct += 1 if intent_correct_flag else 0
                intent_total += 1
                
                # Calculate score
                score = self.calculate_score(answer, expected_score)
                scores.append(score)
                
                # Display
                status = "✅" if intent_correct_flag else "❌"
                print(f"   {intent.upper()}: '{answer[:40]}...'")
                print(f"      Intent: {status} | Score: {score}% (Expected: {expected_score}%)")
                
                intent_results.append({
                    'intent': intent,
                    'answer': answer,
                    'detected': intent_correct_flag,
                    'score': score,
                    'expected_score': expected_score
                })
            
            avg_score = sum(scores) / len(scores)
            all_scores.append(avg_score)
            all_human_decisions.append(test['human_decision'])
            
            ai_decision = 'shortlist' if avg_score >= 70 else 'reject'
            match = "✅ MATCH" if ai_decision == test['human_decision'] else "❌ MISMATCH"
            
            print(f"\n   Average Score: {avg_score:.1f}%")
            print(f"   AI Decision: {ai_decision.upper()}")
            print(f"   Human Decision: {test['human_decision'].upper()}")
            print(f"   Result: {match}")
            
            self.test_results.append({
                'test_id': test['id'],
                'scores': scores,
                'avg_score': avg_score,
                'ai_decision': ai_decision,
                'human_decision': test['human_decision'],
                'match': ai_decision == test['human_decision'],
                'intent_results': intent_results
            })
        
        # Calculate metrics
        matches = sum(1 for r in self.test_results if r['match'])
        self.metrics['total_tests'] = len(self.test_results)
        self.metrics['correct_decisions'] = matches
        self.metrics['intent_accuracy'] = (intent_correct / intent_total) * 100 if intent_total > 0 else 0
        
        return all_scores, all_human_decisions
    
    # ========== GENERATE REPORT ==========
    
    def generate_report(self, best_threshold):
        """Generate comprehensive test report"""
        matches = self.metrics['correct_decisions']
        total = self.metrics['total_tests']
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_tests': total,
                'correct_decisions': matches,
                'accuracy': (matches / total) * 100 if total > 0 else 0,
                'intent_accuracy': self.metrics['intent_accuracy'],
                'best_threshold': best_threshold
            },
            'metrics': {
                'false_positives': self.metrics['false_positives'],
                'false_negatives': self.metrics['false_negatives']
            },
            'score_errors': self.metrics['score_errors'][:5],
            'detailed_results': self.test_results
        }
        
        return report
    
    def save_report(self, report, filename='output/test_report.json'):
        """Save report"""
        import os
        os.makedirs('output', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✅ Report saved: {filename}")
    
    def print_summary(self, report):
        """Print summary statistics"""
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"Total Test Cases: {report['summary']['total_tests']}")
        print(f"Correct Decisions: {report['summary']['correct_decisions']}")
        print(f"Decision Accuracy: {report['summary']['accuracy']:.1f}%")
        print(f"Intent Detection Accuracy: {report['summary']['intent_accuracy']:.1f}%")
        print(f"Best Threshold: {report['summary']['best_threshold']}")
        
        # Show mismatches
        mismatches = [r for r in self.test_results if not r['match']]
        if mismatches:
            print("\n⚠️ MISMATCH CASES:")
            for m in mismatches:
                print(f"   {m['test_id']}: AI={m['ai_decision'].upper()} | Human={m['human_decision'].upper()} | Score={m['avg_score']:.1f}%")
        else:
            print("\n✅ No mismatches found!")

def main():
    print("="*70)
    print("DAY 30 - SCREENING SYSTEM TESTING & OPTIMIZATION")
    print("="*70)
    
    tester = SystemTester()
    
    # Run simulations
    all_scores, human_decisions = tester.run_simulation()
    
    # Tune thresholds
    best_threshold = tester.tune_thresholds(all_scores, human_decisions)
    
    # Generate report
    report = tester.generate_report(best_threshold)
    tester.print_summary(report)
    tester.save_report(report)
    
    print("\n" + "="*70)
    print("✅ DAY 30 COMPLETED - SCREENING SYSTEM TESTING & OPTIMIZATION")
    print("="*70)

if __name__ == "__main__":
    main()