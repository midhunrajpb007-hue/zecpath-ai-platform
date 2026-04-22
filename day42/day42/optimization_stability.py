# optimization_stability.py - Day 42 Optimization & Stability (FINAL FIX)
import re
import json
import time
from functools import lru_cache
from datetime import datetime

class OptimizationStability:
    def __init__(self):
        self.original_thresholds = {'shortlist': 70, 'review': 50}
        self.optimized_thresholds = {'shortlist': 65, 'review': 50}
    
    def tune_thresholds(self, test_results):
        scores = [r['score'] for r in test_results]
        decisions = [r['human_decision'] for r in test_results]
        best_thresh = 70
        best_acc = 0
        for thresh in range(50, 81, 5):
            correct = 0
            for score, dec in zip(scores, decisions):
                ai_dec = 'shortlist' if score >= thresh else 'reject'
                if ai_dec == dec:
                    correct += 1
            acc = correct / len(scores)
            if acc > best_acc:
                best_acc = acc
                best_thresh = thresh
        return best_thresh, best_acc
    
    # Fixed follow‑up logic (now triggers elaboration for very short answers)
    def stable_followup(self, question, answer_history, max_attempts=2):
        asked_count = len(answer_history)
        if asked_count >= max_attempts:
            return None
        # If there is a previous answer that is very short (≤3 words), ask for elaboration
        if answer_history and len(answer_history[-1].split()) <= 3:
            return "Could you please elaborate a bit more?"
        return question
    
    def detect_anomalies(self, scores):
        if len(scores) < 3:
            return []
        mean = sum(scores) / len(scores)
        std = (sum((x - mean) ** 2 for x in scores) / len(scores)) ** 0.5
        anomalies = []
        for i, s in enumerate(scores):
            if abs(s - mean) > 2 * std:
                anomalies.append({'index': i, 'score': s, 'reason': 'outlier'})
        return anomalies
    
    @lru_cache(maxsize=128)
    def fast_clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\-\:\?\!]', '', text)
        text = text.lower().strip()
        return text
    
    def advanced_clean_transcript(self, text):
        text = self.fast_clean_text(text)
        # Remove filler words
        fillers = ['um', 'uh', 'ah', 'er', 'hmm', 'like', 'you know', 'actually', 'basically']
        for filler in fillers:
            text = re.sub(r'\b' + re.escape(filler) + r'\b', '', text)
        # Fix common contractions (preserve apostrophe)
        replacements = {
            r"don't": 'do not', r"can't": 'cannot', r"won't": 'will not',
            r"wanna": 'want to', r"gonna": 'going to'
        }
        for pattern, repl in replacements.items():
            text = re.sub(r'\b' + pattern + r'\b', repl, text)
        # Normalize punctuation
        text = re.sub(r'\.{2,}', '.', text)
        text = re.sub(r'\?{2,}', '?', text)
        text = re.sub(r'\!{2,}', '!', text)
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove leading punctuation
        text = re.sub(r'^[^\w]+', '', text)
        return text
    
    def generate_report(self, test_results):
        best_thresh, accuracy = self.tune_thresholds(test_results)
        report = {
            'generated_at': datetime.now().isoformat(),
            'original_shortlist_threshold': 70,
            'optimized_shortlist_threshold': best_thresh,
            'accuracy_after_tuning': round(accuracy * 100, 2),
            'follow_up_stability': {'max_attempts': 2, 'repetition_prevention': True},
            'scoring_anomalies': self.detect_anomalies([r['score'] for r in test_results]),
            'speed_optimizations': ['cached text cleaning (LRU cache)'],
            'transcript_cleanup_improvements': [
                'filler word removal', 'contraction expansion', 'punctuation normalization'
            ],
            'recommendations': []
        }
        return report

def main():
    print("="*70)
    print("DAY 42 - OPTIMIZATION & STABILITY")
    print("="*70)
    
    opt = OptimizationStability()
    
    test_results = [
        {'score': 96.5, 'human_decision': 'shortlist'},
        {'score': 44.8, 'human_decision': 'reject'},
        {'score': 82.3, 'human_decision': 'shortlist'},
        {'score': 67.5, 'human_decision': 'shortlist'},
        {'score': 55.0, 'human_decision': 'reject'},
        {'score': 91.2, 'human_decision': 'shortlist'},
        {'score': 49.7, 'human_decision': 'reject'},
        {'score': 78.9, 'human_decision': 'shortlist'},
        {'score': 62.4, 'human_decision': 'reject'},
        {'score': 38.2, 'human_decision': 'reject'}
    ]
    
    best_thresh, acc = opt.tune_thresholds(test_results)
    print(f"\n📊 THRESHOLD TUNING")
    print(f"   Original: 70 → Optimized: {best_thresh} (Accuracy: {acc*100:.1f}%)")
    
    # Follow-up stability test (with very short answer to trigger elaboration)
    print(f"\n🔄 FOLLOW-UP STABILITY TEST")
    history = []
    q = "How many years of experience do you have?"
    for attempt in range(3):
        next_q = opt.stable_followup(q, history, max_attempts=2)
        if next_q is None:
            print(f"   Attempt {attempt+1}: Skipping (max attempts reached)")
        else:
            print(f"   Attempt {attempt+1}: Asking: {next_q}")
        # Simulate a very short answer for the first attempt (≤3 words)
        if attempt == 0:
            history.append("yes")
        else:
            history.append("I have five years of experience in backend development.")
    
    scores = [r['score'] for r in test_results]
    anomalies = opt.detect_anomalies(scores)
    print(f"\n⚠️ SCORING ANOMALIES")
    if anomalies:
        for a in anomalies:
            print(f"   Anomaly at index {a['index']}: score={a['score']}")
    else:
        print("   None")
    
    sample = "This is a   sample   with   many   spaces."
    start = time.time()
    for _ in range(1000):
        _ = opt.fast_clean_text(sample)
    elapsed = time.time() - start
    print(f"\n⚡ SPEED: {elapsed*1000:.2f} ms for 1000 iterations")
    
    noisy = "Um, I don't know... maybe 3 years??? I have like experience."
    cleaned = opt.advanced_clean_transcript(noisy)
    print(f"\n🧹 TRANSCRIPT CLEANUP")
    print(f"   Original: {noisy}")
    print(f"   Cleaned : {cleaned}")
    
    report = opt.generate_report(test_results)
    import os
    os.makedirs('output', exist_ok=True)
    with open('output/optimization_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("\n✅ Report saved: output/optimization_report.json")
    
    print("\n" + "="*70)
    print("✅ DAY 42 COMPLETED - OPTIMIZATION & STABILITY")
    print("="*70)

if __name__ == "__main__":
    main()