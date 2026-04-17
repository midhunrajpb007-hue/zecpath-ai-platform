# summary_generator.py - Day 39 Interview Summary Generator (Fixed Encoding)
import json
from datetime import datetime

class SummaryGenerator:
    def __init__(self):
        # Sample data from previous days (would come from actual evaluation)
        self.candidate_data = {
            'candidate_id': 'C001',
            'name': 'Midhun Raj',
            'role': 'Software Engineer',
            'hr_scores': {
                'relevance': 33.33,
                'communication': 84.83,
                'confidence': 82.33,
                'consistency': 94.67,
                'overall': 67.16
            },
            'aptitude_score': 70.46,
            'aptitude_clarity': 85.0,
            'comm_components': {
                'fluency': 80,
                'grammar': 100,
                'vocabulary': 95,
                'clarity': 80,
                'filler_words': 90
            },
            'confidence_components': {
                'hesitation': 100,
                'sentiment': 100,
                'contradiction': 85,
                'stress': 97
            },
            'answers': [
                {'question': 'How many years of experience?', 'answer': 'I have 4 years of experience in Python and React.'},
                {'question': 'What are your strengths?', 'answer': 'Problem-solving and teamwork.'},
                {'question': 'When can you join?', 'answer': 'I can join in 30 days.'},
                {'question': 'Tell me about a challenging project', 'answer': 'I optimized database queries for a large e-commerce platform.'}
            ]
        }
    
    def identify_strengths(self):
        strengths = []
        if self.candidate_data['hr_scores']['communication'] >= 80:
            strengths.append("Strong communication skills (fluent, clear vocabulary)")
        if self.candidate_data['hr_scores']['confidence'] >= 80:
            strengths.append("High confidence in responses (no hesitation, positive tone)")
        if self.candidate_data['aptitude_clarity'] >= 80:
            strengths.append("Good problem-solving clarity (structured answers)")
        if self.candidate_data['comm_components']['grammar'] == 100:
            strengths.append("Excellent grammar usage")
        if any('experience' in ans['answer'].lower() for ans in self.candidate_data['answers']):
            strengths.append("Relevant experience mentioned")
        return strengths if strengths else ["No major strengths identified"]
    
    def identify_weaknesses(self):
        weaknesses = []
        if self.candidate_data['hr_scores']['relevance'] < 50:
            weaknesses.append("Answers sometimes missed key expected information")
        if self.candidate_data['aptitude_score'] < 60:
            weaknesses.append("Logical reasoning could be improved")
        if self.candidate_data['comm_components']['filler_words'] < 90:
            weaknesses.append("Filler words (um, like, you know) used occasionally")
        if self.candidate_data['confidence_components']['contradiction'] < 90:
            weaknesses.append("Some contradictory statements detected")
        return weaknesses if weaknesses else ["No major weaknesses identified"]
    
    def cultural_fit_indicators(self):
        indicators = []
        answers_text = ' '.join([a['answer'].lower() for a in self.candidate_data['answers']])
        if 'team' in answers_text or 'collaborat' in answers_text:
            indicators.append("Team-oriented – mentions collaboration")
        if 'learn' in answers_text or 'improve' in answers_text:
            indicators.append("Growth mindset – open to learning")
        if 'lead' in answers_text or 'mentor' in answers_text:
            indicators.append("Leadership potential")
        if 'deadline' in answers_text or 'pressure' in answers_text:
            indicators.append("Works well under pressure")
        return indicators if indicators else ["Neutral – no clear cultural indicators"]
    
    def risk_flags(self):
        risks = []
        if self.candidate_data['hr_scores']['consistency'] < 80:
            risks.append("Inconsistent answer lengths (may indicate uncertainty)")
        if self.candidate_data['confidence_components']['stress'] < 70:
            risks.append("Possible stress indicators (nervous language)")
        if self.candidate_data['aptitude_score'] < 50:
            risks.append("Low aptitude score – may struggle with complex problems")
        if self.candidate_data['comm_components']['clarity'] < 60:
            risks.append("Unclear explanations – may need follow-up")
        return risks if risks else ["No significant risks identified"]
    
    def highlight_inconsistencies(self):
        inconsistencies = []
        answers_text = ' '.join([a['answer'].lower() for a in self.candidate_data['answers']])
        if 'yes' in answers_text and 'no' in answers_text:
            inconsistencies.append("Potential contradiction: candidate answered both 'yes' and 'no' on similar topics")
        exp_mentions = [a for a in self.candidate_data['answers'] if 'experience' in a['answer'].lower()]
        if len(exp_mentions) > 1:
            inconsistencies.append("Multiple experience statements – verify consistency")
        return inconsistencies if inconsistencies else ["No clear inconsistencies detected"]
    
    def overall_hr_performance(self):
        overall = self.candidate_data['hr_scores']['overall']
        aptitude = self.candidate_data['aptitude_score']
        combined = (overall * 0.7) + (aptitude * 0.3)
        if combined >= 80:
            rating = "Excellent"
        elif combined >= 60:
            rating = "Good"
        elif combined >= 40:
            rating = "Average"
        else:
            rating = "Needs Improvement"
        return {
            'combined_score': round(combined, 2),
            'rating': rating,
            'summary': f"Candidate performed {rating.lower()} in HR interview. "
                       f"Communication and confidence are strong, but relevance and aptitude have room for improvement."
        }
    
    def generate_natural_language_report(self):
        strengths = self.identify_strengths()
        weaknesses = self.identify_weaknesses()
        cultural = self.cultural_fit_indicators()
        risks = self.risk_flags()
        inconsistencies = self.highlight_inconsistencies()
        perf = self.overall_hr_performance()
        
        report_text = f"""
CANDIDATE: {self.candidate_data['name']} (ID: {self.candidate_data['candidate_id']})
ROLE: {self.candidate_data['role']}
OVERALL SCORE: {perf['combined_score']}% ({perf['rating']})

STRENGTHS:
{chr(10).join('• ' + s for s in strengths)}

WEAKNESSES:
{chr(10).join('• ' + w for w in weaknesses)}

CULTURAL FIT:
{chr(10).join('• ' + c for c in cultural)}

RISK FLAGS:
{chr(10).join('• ' + r for r in risks)}

INCONSISTENCIES:
{chr(10).join('• ' + i for i in inconsistencies)}

SUMMARY:
{perf['summary']}

RECOMMENDATION:
"""
        if perf['combined_score'] >= 70:
            report_text += "Proceed to next round (technical interview)."
        elif perf['combined_score'] >= 50:
            report_text += "Keep in review queue for another round."
        else:
            report_text += "Not recommended for next round."
        
        return report_text
    
    def generate_structured_summary(self):
        return {
            'candidate_id': self.candidate_data['candidate_id'],
            'name': self.candidate_data['name'],
            'role': self.candidate_data['role'],
            'generated_at': datetime.now().isoformat(),
            'overall_performance': self.overall_hr_performance(),
            'strengths': self.identify_strengths(),
            'weaknesses': self.identify_weaknesses(),
            'cultural_fit': self.cultural_fit_indicators(),
            'risk_flags': self.risk_flags(),
            'inconsistencies': self.highlight_inconsistencies(),
            'recommendation': self._recommendation()
        }
    
    def _recommendation(self):
        perf = self.overall_hr_performance()
        if perf['combined_score'] >= 70:
            return "Proceed to technical interview"
        elif perf['combined_score'] >= 50:
            return "Keep for review"
        else:
            return "Not recommended"

def main():
    print("="*70)
    print("DAY 39 - INTERVIEW SUMMARY GENERATOR")
    print("="*70)
    
    generator = SummaryGenerator()
    
    # Generate structured summary
    structured = generator.generate_structured_summary()
    print("\n📋 STRUCTURED SUMMARY (JSON)")
    print("-"*50)
    print(json.dumps(structured, indent=2))
    
    # Generate natural language report
    nl_report = generator.generate_natural_language_report()
    print("\n📝 NATURAL LANGUAGE REPORT")
    print("-"*50)
    print(nl_report)
    
    # Save outputs with UTF-8 encoding
    import os
    os.makedirs('output', exist_ok=True)
    with open('output/structured_summary.json', 'w', encoding='utf-8') as f:
        json.dump(structured, f, indent=2, ensure_ascii=False)
    print("\n✅ Structured summary saved: output/structured_summary.json")
    
    with open('output/natural_language_report.txt', 'w', encoding='utf-8') as f:
        f.write(nl_report)
    print("✅ Natural language report saved: output/natural_language_report.txt")
    
    print("\n" + "="*70)
    print("✅ DAY 39 COMPLETED - INTERVIEW SUMMARY GENERATOR")
    print("="*70)

if __name__ == "__main__":
    main()