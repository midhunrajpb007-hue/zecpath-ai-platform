# semantic_matcher.py
import os
import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticMatcher:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"✅ Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = 0.6
    
    def get_embedding(self, text):
        if not text or len(text.strip()) == 0:
            return np.zeros(384)
        return self.model.encode(text)
    
    def compare_sections(self, text1, text2):
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        sim = cosine_similarity([emb1], [emb2])[0][0]
        return round(float(sim), 4)
    
    def match(self, resume, jd, weights=None):
        if weights is None:
            weights = {'skills': 0.5, 'experience': 0.3, 'projects': 0.2}
        
        scores = {}
        for section in weights.keys():
            scores[section] = self.compare_sections(
                resume.get(section, ''),
                jd.get(section, '')
            )
        
        total_score = sum(scores[s] * weights[s] for s in weights)
        
        return {
            'total_score': round(total_score, 4),
            'section_scores': scores,
            'match': total_score >= self.similarity_threshold
        }
    
    def tune_threshold(self, test_pairs, labels, thresholds=None):
        if thresholds is None:
            thresholds = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]
        
        best_thresh = self.similarity_threshold
        best_acc = 0
        
        print("\n📊 Threshold Tuning:")
        print("-" * 40)
        
        for thresh in thresholds:
            self.similarity_threshold = thresh
            correct = 0
            for (resume, jd), expected in zip(test_pairs, labels):
                if self.match(resume, jd)['match'] == expected:
                    correct += 1
            acc = correct / len(test_pairs)
            print(f"Threshold {thresh:.2f} → Accuracy: {acc:.2%}")
            if acc > best_acc:
                best_acc = acc
                best_thresh = thresh
        
        self.similarity_threshold = best_thresh
        print("-" * 40)
        print(f"✅ Best threshold: {best_thresh:.2f}")
        return best_thresh

def create_sample_data():
    resumes = [
        {
            'skills': 'Python, Django, SQL, REST APIs',
            'experience': '3 years web development with Django',
            'projects': 'Built e-commerce platform'
        },
        {
            'skills': 'Python, TensorFlow, Pandas, SQL',
            'experience': '2 years machine learning experience',
            'projects': 'Customer churn prediction'
        },
        {
            'skills': 'JavaScript, React, HTML, CSS',
            'experience': '2 years frontend development',
            'projects': 'Dashboard for analytics'
        }
    ]
    
    jds = [
        {
            'skills': 'Python, Django, SQL',
            'experience': 'Web development experience',
            'projects': 'Web applications'
        },
        {
            'skills': 'Python, Machine Learning, TensorFlow',
            'experience': 'ML model development',
            'projects': 'Predictive modeling'
        },
        {
            'skills': 'React, JavaScript, CSS',
            'experience': 'Frontend experience',
            'projects': 'UI development'
        }
    ]
    
    return resumes, jds

def main():
    print("=" * 60)
    print("DAY 12 - SEMANTIC MATCHING ENGINE")
    print("=" * 60)
    
    matcher = SemanticMatcher()
    resumes, jds = create_sample_data()
    
    print("\n📌 Sample Matches:")
    print("-" * 40)
    
    for i in range(3):
        result = matcher.match(resumes[i], jds[i])
        print(f"\nPair {i+1}:")
        print(f"  Skills Match: {result['section_scores']['skills']:.3f}")
        print(f"  Total Score : {result['total_score']:.3f}")
        print(f"  Match       : {'✅' if result['match'] else '❌'}")
    
    # Threshold tuning
    test_pairs = [(resumes[0], jds[0]), (resumes[1], jds[1]), (resumes[2], jds[2])]
    labels = [1, 1, 1]
    matcher.tune_threshold(test_pairs, labels)
    
    print("\n" + "=" * 60)
    print("✅ DAY 12 COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()