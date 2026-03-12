# ats_tester.py - Day 17 ATS System Testing
import json
import pandas as pd
from datetime import datetime
import os

class ATSTester:
    def __init__(self):
        self.results = []
        self.metrics = {
            'true_positives': 0,
            'false_positives': 0,
            'true_negatives': 0,
            'false_negatives': 0
        }
    
    def add_test_case(self, role_type, experience_level, candidate_id, 
                      ai_decision, manual_decision, ai_score, manual_score):
        """
        Add a single test case
        role_type: tech / non-tech
        experience_level: fresher / senior
        ai_decision: shortlisted / review / rejected
        manual_decision: shortlisted / review / rejected
        """
        test_case = {
            'role_type': role_type,
            'experience_level': experience_level,
            'candidate_id': candidate_id,
            'ai_decision': ai_decision,
            'manual_decision': manual_decision,
            'ai_score': ai_score,
            'manual_score': manual_score,
            'match': ai_decision == manual_decision
        }
        
        # Update confusion matrix
        if ai_decision == 'shortlisted' and manual_decision == 'shortlisted':
            self.metrics['true_positives'] += 1
        elif ai_decision == 'shortlisted' and manual_decision != 'shortlisted':
            self.metrics['false_positives'] += 1
        elif ai_decision != 'shortlisted' and manual_decision == 'shortlisted':
            self.metrics['false_negatives'] += 1
        else:
            self.metrics['true_negatives'] += 1
        
        self.results.append(test_case)
        return test_case
    
    def calculate_metrics(self):
        """Calculate precision, recall, F1, accuracy"""
        tp = self.metrics['true_positives']
        fp = self.metrics['false_positives']
        fn = self.metrics['false_negatives']
        tn = self.metrics['true_negatives']
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        
        return {
            'precision': round(precision * 100, 2),
            'recall': round(recall * 100, 2),
            'f1_score': round(f1 * 100, 2),
            'accuracy': round(accuracy * 100, 2),
            'true_positives': tp,
            'false_positives': fp,
            'false_negatives': fn,
            'true_negatives': tn,
            'total_cases': tp + tn + fp + fn
        }
    
    def get_mismatch_cases(self):
        """Return all cases where AI != manual"""
        return [case for case in self.results if not case['match']]
    
    def analyze_by_category(self):
        """Analyze performance by role type and experience level"""
        categories = {}
        
        for case in self.results:
            key = f"{case['role_type']}_{case['experience_level']}"
            if key not in categories:
                categories[key] = {'total': 0, 'correct': 0, 'mismatch': 0}
            
            categories[key]['total'] += 1
            if case['match']:
                categories[key]['correct'] += 1
            else:
                categories[key]['mismatch'] += 1
        
        for key in categories:
            cat = categories[key]
            cat['accuracy'] = round((cat['correct'] / cat['total']) * 100, 2) if cat['total'] > 0 else 0
        
        return categories
    
    def generate_report(self):
        """Generate complete ATS testing report"""
        metrics = self.calculate_metrics()
        mismatches = self.get_mismatch_cases()
        category_analysis = self.analyze_by_category()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_tests': len(self.results),
                'correct_matches': sum(1 for r in self.results if r['match']),
                'mismatches': len(mismatches),
                'accuracy': metrics['accuracy']
            },
            'metrics': metrics,
            'category_analysis': category_analysis,
            'mismatch_cases': mismatches[:10],  # Top 10 mismatches
            'improvement_backlog': self.generate_backlog(mismatches, category_analysis)
        }
        
        return report
    
    def generate_backlog(self, mismatches, category_analysis):
        """Generate improvement backlog based on findings"""
        backlog = []
        
        # Check if tech roles have more issues
        tech_total = 0
        tech_mismatch = 0
        nontech_total = 0
        nontech_mismatch = 0
        
        for case in self.results:
            if case['role_type'] == 'tech':
                tech_total += 1
                if not case['match']:
                    tech_mismatch += 1
            else:
                nontech_total += 1
                if not case['match']:
                    nontech_mismatch += 1
        
        if tech_total > 0 and (tech_mismatch / tech_total) > 0.2:
            backlog.append("Improve matching for tech roles – check skill extraction accuracy")
        
        if nontech_total > 0 and (nontech_mismatch / nontech_total) > 0.2:
            backlog.append("Improve matching for non-tech roles – add more soft skills to dictionary")
        
        # Fresher vs Senior analysis
        fresher_mismatch = sum(1 for c in self.results if c['experience_level'] == 'fresher' and not c['match'])
        senior_mismatch = sum(1 for c in self.results if c['experience_level'] == 'senior' and not c['match'])
        
        if fresher_mismatch > 2:
            backlog.append("Adjust weights for fresher profiles – education should have higher weight")
        
        if senior_mismatch > 2:
            backlog.append("Improve experience parsing for senior profiles – detect leadership roles")
        
        # Score threshold tuning
        score_mismatches = [c for c in mismatches if abs(c['ai_score'] - c['manual_score']) > 15]
        if len(score_mismatches) > 3:
            backlog.append("Re-tune scoring thresholds – current threshold may be too strict")
        
        return backlog
    
    def save_report(self, report, filename='ats_test_report.json'):
        """Save report to JSON"""
        os.makedirs('reports', exist_ok=True)
        path = f'reports/{filename}'
        with open(path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report saved: {path}")
        return path
    
    def save_csv(self, filename='ats_test_results.csv'):
        """Save test results to CSV"""
        df = pd.DataFrame(self.results)
        os.makedirs('output', exist_ok=True)
        path = f'output/{filename}'
        df.to_csv(path, index=False)
        print(f"✅ CSV saved: {path}")
        return path

def create_sample_test_data():
    """Create sample test cases"""
    tester = ATSTester()
    
    # Tech roles - Software Engineer
    tester.add_test_case('tech', 'senior', 'C001', 'shortlisted', 'shortlisted', 96, 95)
    tester.add_test_case('tech', 'senior', 'C002', 'rejected', 'rejected', 44, 40)
    tester.add_test_case('tech', 'senior', 'C003', 'shortlisted', 'shortlisted', 82, 85)
    tester.add_test_case('tech', 'fresher', 'C004', 'review', 'shortlisted', 67, 72)  # Mismatch
    tester.add_test_case('tech', 'fresher', 'C005', 'shortlisted', 'shortlisted', 91, 90)
    
    # Non-tech roles - Marketing Manager
    tester.add_test_case('non-tech', 'senior', 'N001', 'shortlisted', 'shortlisted', 88, 85)
    tester.add_test_case('non-tech', 'senior', 'N002', 'rejected', 'review', 55, 68)   # Mismatch
    tester.add_test_case('non-tech', 'fresher', 'N003', 'review', 'review', 62, 60)
    tester.add_test_case('non-tech', 'fresher', 'N004', 'rejected', 'rejected', 48, 45)
    tester.add_test_case('non-tech', 'senior', 'N005', 'shortlisted', 'shortlisted', 78, 80)
    
    # More tech roles
    tester.add_test_case('tech', 'senior', 'C006', 'shortlisted', 'shortlisted', 94, 92)
    tester.add_test_case('tech', 'fresher', 'C007', 'review', 'rejected', 52, 48)      # Mismatch
    tester.add_test_case('tech', 'senior', 'C008', 'rejected', 'rejected', 38, 35)
    tester.add_test_case('tech', 'fresher', 'C009', 'shortlisted', 'shortlisted', 79, 82)
    
    return tester

def main():
    print("="*80)
    print("DAY 17 - ATS SYSTEM TESTING")
    print("="*80)
    
    # Create test data
    tester = create_sample_test_data()
    
    # Display results
    print(f"\n📊 Total Test Cases: {len(tester.results)}")
    
    # Category-wise summary
    print("\n" + "="*80)
    print("📋 CATEGORY-WISE ANALYSIS")
    print("="*80)
    
    categories = tester.analyze_by_category()
    for category, stats in categories.items():
        print(f"\n📌 {category.replace('_', ' ').title()}:")
        print(f"   Total  : {stats['total']}")
        print(f"   Correct: {stats['correct']} ({stats['accuracy']}%)")
        print(f"   Mismatch: {stats['mismatch']}")
    
    # Mismatch cases
    mismatches = tester.get_mismatch_cases()
    print("\n" + "="*80)
    print("⚠️ MISMATCH CASES (AI vs Manual)")
    print("="*80)
    
    for case in mismatches:
        print(f"\n📋 Candidate {case['candidate_id']} ({case['role_type']}, {case['experience_level']})")
        print(f"   AI Score   : {case['ai_score']} → {case['ai_decision']}")
        print(f"   Manual Score: {case['manual_score']} → {case['manual_decision']}")
    
    # Metrics
    metrics = tester.calculate_metrics()
    print("\n" + "="*80)
    print("📊 ACCURACY METRICS")
    print("="*80)
    print(f"✅ Precision : {metrics['precision']}%")
    print(f"✅ Recall    : {metrics['recall']}%")
    print(f"✅ F1 Score  : {metrics['f1_score']}%")
    print(f"✅ Accuracy  : {metrics['accuracy']}%")
    print(f"\n   True Positives : {metrics['true_positives']}")
    print(f"   False Positives: {metrics['false_positives']}")
    print(f"   False Negatives: {metrics['false_negatives']}")
    print(f"   True Negatives : {metrics['true_negatives']}")
    
    # Generate report
    report = tester.generate_report()
    
    print("\n" + "="*80)
    print("📋 IMPROVEMENT BACKLOG")
    print("="*80)
    for i, item in enumerate(report['improvement_backlog'], 1):
        print(f"{i}. {item}")
    
    # Save outputs
    tester.save_report(report)
    tester.save_csv()
    
    print("\n" + "="*80)
    print("✅ DAY 17 COMPLETED - ATS SYSTEM TESTING")
    print("="*80)

if __name__ == "__main__":
    main()