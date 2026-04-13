# comm_scorer.py - Day 35 Communication Skill Evaluation (Fixed)
import re
import json
import os
from datetime import datetime

class CommunicationScorer:
    def __init__(self):
        # Filler words to detect
        self.filler_words = [
            'um', 'uh', 'ah', 'er', 'hmm', 'like', 'you know', 
            'actually', 'basically', 'sort of', 'kind of', 'well'
        ]
        # Common grammar error patterns
        self.grammar_errors = [
            (r'\b(I are)\b', 'I am'),
            (r'\b(he don\'t)\b', 'he doesn\'t'),
            (r'\b(she don\'t)\b', 'she doesn\'t'),
            (r'\b(they is)\b', 'they are'),
            (r'\b(we is)\b', 'we are'),
            (r'\b(have been to\s+\w+ed)\b', 'present perfect misuse')
        ]
        # Positive connectors for clarity
        self.clarity_connectors = [
            'first', 'second', 'third', 'then', 'next', 'after that',
            'because', 'so', 'therefore', 'however', 'for example',
            'such as', 'in addition', 'moreover', 'consequently'
        ]
    
    # ========== FLUENCY SCORE ==========
    def score_fluency(self, text):
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
        if not sentences:
            return 0, "No sentences"
        word_counts = [len(s.split()) for s in sentences]
        avg_words = sum(word_counts) / len(sentences)
        if 10 <= avg_words <= 20:
            fluency_score = 90
        elif 5 <= avg_words < 10:
            fluency_score = 70
        elif avg_words > 20:
            fluency_score = 60
        else:
            fluency_score = 40
        if len(sentences) >= 3:
            fluency_score = min(100, fluency_score + 10)
        return fluency_score, f"{len(sentences)} sentences, avg {avg_words:.1f} words/sentence"
    
    # ========== GRAMMAR QUALITY SCORE ==========
    def score_grammar(self, text):
        text_lower = text.lower()
        error_count = 0
        for pattern, _ in self.grammar_errors:
            if re.search(pattern, text_lower):
                error_count += 1
        grammar_score = max(0, 100 - (error_count * 15))
        return grammar_score, f"{error_count} grammar error(s)"
    
    # ========== VOCABULARY RANGE SCORE ==========
    def score_vocabulary(self, text):
        words = re.findall(r'\b[a-z]+\b', text.lower())
        if not words:
            return 0, "No words"
        unique_words = set(words)
        ratio = len(unique_words) / len(words)
        if ratio > 0.6:
            vocab_score = 95
        elif ratio > 0.5:
            vocab_score = 80
        elif ratio > 0.4:
            vocab_score = 65
        else:
            vocab_score = 50
        return vocab_score, f"{len(unique_words)} unique / {len(words)} total words"
    
    # ========== CLARITY OF EXPLANATION ==========
    def score_clarity(self, text):
        text_lower = text.lower()
        connector_count = 0
        for conn in self.clarity_connectors:
            if conn in text_lower:
                connector_count += 1
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
        clarity_score = 50
        if len(sentences) >= 2:
            clarity_score += 20
        if connector_count >= 2:
            clarity_score += 20
        elif connector_count == 1:
            clarity_score += 10
        if any(w in text_lower for w in ['first', 'then', 'finally']):
            clarity_score += 10
        return min(100, clarity_score), f"{connector_count} connectors, {len(sentences)} sentences"
    
    # ========== FILLER WORD DETECTION ==========
    def score_filler(self, text):
        text_lower = text.lower()
        filler_count = 0
        for filler in self.filler_words:
            filler_count += text_lower.count(filler)
        filler_penalty = min(30, filler_count * 5)
        filler_score = 100 - filler_penalty
        return filler_score, f"{filler_count} filler word(s)"
    
    # ========== OVERALL COMMUNICATION SCORE ==========
    def overall_score(self, text):
        fluency, fluency_detail = self.score_fluency(text)
        grammar, grammar_detail = self.score_grammar(text)
        vocab, vocab_detail = self.score_vocabulary(text)
        clarity, clarity_detail = self.score_clarity(text)
        filler, filler_detail = self.score_filler(text)
        total = (fluency * 0.25) + (grammar * 0.25) + (vocab * 0.2) + (clarity * 0.2) + (filler * 0.1)
        overall = round(total, 2)
        return {
            'overall_score': overall,
            'components': {
                'fluency': {'score': fluency, 'detail': fluency_detail},
                'grammar': {'score': grammar, 'detail': grammar_detail},
                'vocabulary': {'score': vocab, 'detail': vocab_detail},
                'clarity': {'score': clarity, 'detail': clarity_detail},
                'filler_words': {'score': filler, 'detail': filler_detail}
            }
        }
    
    def normalize_score(self, score, min_score=0, max_score=100):
        return max(0, min(100, score))
    
    def evaluate_answer(self, text):
        result = self.overall_score(text)
        result['normalized_score'] = self.normalize_score(result['overall_score'])
        result['evaluated_at'] = datetime.now().isoformat()
        return result

def main():
    print("="*70)
    print("DAY 35 - COMMUNICATION SKILL EVALUATION")
    print("="*70)
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    scorer = CommunicationScorer()
    
    # Sample answers
    test_answers = [
        "I have 3 years of experience in Python and React. I worked on several projects including a web dashboard and an API. My strongest skill is problem solving.",
        "Um, I have like some experience, you know, maybe 2 years? I think I know Python.",
        "I am a software engineer with 5 years of experience. First, I worked at Google on cloud infrastructure. Then I moved to Amazon where I led a team of 3. Therefore, I have strong leadership skills.",
        "i have experience. python. sql. react. i can join immediately."
    ]
    
    print("\n📋 COMMUNICATION SCORES")
    print("-"*50)
    for i, ans in enumerate(test_answers, 1):
        print(f"\nAnswer {i}: {ans[:80]}...")
        result = scorer.evaluate_answer(ans)
        print(f"Overall Score: {result['overall_score']}%")
        print(f"  Fluency: {result['components']['fluency']['score']}% - {result['components']['fluency']['detail']}")
        print(f"  Grammar: {result['components']['grammar']['score']}% - {result['components']['grammar']['detail']}")
        print(f"  Vocabulary: {result['components']['vocabulary']['score']}% - {result['components']['vocabulary']['detail']}")
        print(f"  Clarity: {result['components']['clarity']['score']}% - {result['components']['clarity']['detail']}")
        print(f"  Filler Words: {result['components']['filler_words']['score']}% - {result['components']['filler_words']['detail']}")
    
    # Save sample output to JSON
    sample_output = {
        'model': 'CommunicationScorer',
        'formula': 'overall = fluency*0.25 + grammar*0.25 + vocabulary*0.2 + clarity*0.2 + filler*0.1',
        'sample_results': [scorer.evaluate_answer(ans) for ans in test_answers],
        'normalization': 'min-max to 0-100'
    }
    with open('output/comm_scores.json', 'w') as f:
        json.dump(sample_output, f, indent=2)
    print("\n✅ Sample outputs saved: output/comm_scores.json")
    
    print("\n" + "="*70)
    print("✅ DAY 35 COMPLETED - COMMUNICATION SKILL EVALUATION")
    print("="*70)

if __name__ == "__main__":
    main()