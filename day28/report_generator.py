# report_generator.py - Day 28 AI Screening Report Generator
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.report = {}
    
    def generate_report(self, candidate_data, screening_results, extracted_data):
        """
        Generate complete screening report
        candidate_data: {'name': str, 'email': str, 'phone': str, 'job_id': str}
        screening_results: list of dicts with question, answer, score
        extracted_data: dict with skills, experience, salary, availability
        """
        report = {
            'report_id': f"SCR-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'candidate_info': {
                'name': candidate_data.get('name', 'Not provided'),
                'email': candidate_data.get('email', 'Not provided'),
                'phone': candidate_data.get('phone', 'Not provided'),
                'job_id': candidate_data.get('job_id', 'Not provided')
            },
            'screening_summary': self._generate_summary(screening_results),
            'key_answers': self._extract_key_answers(screening_results),
            'strengths': self._identify_strengths(screening_results, extracted_data),
            'risks': self._identify_risks(screening_results, extracted_data),
            'missing_data': self._identify_missing(extracted_data),
            'highlights': self._create_highlights(extracted_data),
            'overall_assessment': self._assess_overall(screening_results),
            'recommendation': self._make_recommendation(screening_results)
        }
        
        return report
    
    def _generate_summary(self, results):
        """Generate screening summary"""
        if not results:
            return {'total_questions': 0, 'average_score': 0}
        
        scores = [r.get('score', 0) for r in results]
        avg_score = sum(scores) / len(scores)
        
        # Determine overall rating
        if avg_score >= 80:
            rating = "Excellent"
        elif avg_score >= 60:
            rating = "Good"
        elif avg_score >= 40:
            rating = "Average"
        else:
            rating = "Needs Improvement"
        
        return {
            'total_questions': len(results),
            'average_score': round(avg_score, 2),
            'rating': rating
        }
    
    def _extract_key_answers(self, results):
        """Extract important answers from screening"""
        key_answers = []
        
        # Priority questions to highlight
        priority_intents = ['skills', 'experience', 'salary', 'availability']
        
        for r in results:
            if r.get('intent') in priority_intents:
                key_answers.append({
                    'question': r.get('question', ''),
                    'answer': r.get('answer', ''),
                    'score': r.get('score', 0),
                    'intent': r.get('intent')
                })
        
        return key_answers
    
    def _identify_strengths(self, results, extracted):
        """Identify candidate strengths"""
        strengths = []
        
        # Check scores
        high_scores = [r for r in results if r.get('score', 0) >= 80]
        if high_scores:
            strengths.append(f"Strong performance on {len(high_scores)} questions (score ≥80%)")
        
        # Check skills
        skills = extracted.get('skills', [])
        if skills:
            strengths.append(f"Technical skills identified: {', '.join(skills[:5])}")
        
        # Check experience
        exp = extracted.get('experience_years')
        if exp and exp >= 3:
            strengths.append(f"Good experience level: {exp} years")
        
        # Check availability
        availability = extracted.get('availability')
        if availability and availability.get('status') == 'immediate':
            strengths.append("Available immediately - can join soon")
        
        if not strengths:
            strengths.append("No major strengths identified")
        
        return strengths
    
    def _identify_risks(self, results, extracted):
        """Identify potential risks"""
        risks = []
        
        # Check low scores
        low_scores = [r for r in results if r.get('score', 0) < 50]
        if low_scores:
            risks.append(f"Weak performance on {len(low_scores)} questions (score <50%)")
        
        # Check missing skills
        if not extracted.get('skills'):
            risks.append("No technical skills identified")
        
        # Check low experience
        exp = extracted.get('experience_years')
        if exp and exp < 2:
            risks.append(f"Limited experience: only {exp} years")
        
        # Check salary not provided
        if not extracted.get('salary'):
            risks.append("Salary expectation not provided")
        
        # Check availability not provided
        if not extracted.get('availability'):
            risks.append("Joining availability not provided")
        
        if not risks:
            risks.append("No major risks identified")
        
        return risks
    
    def _identify_missing(self, extracted):
        """Identify missing data"""
        missing = []
        
        required_fields = ['skills', 'experience_years', 'salary', 'availability']
        for field in required_fields:
            if not extracted.get(field):
                missing.append(field.replace('_', ' ').title())
        
        return missing
    
    def _create_highlights(self, extracted):
        """Create highlights for recruiter"""
        highlights = {}
        
        # Salary expectation
        salary = extracted.get('salary')
        if salary:
            highlights['salary_expectation'] = f"{salary.get('amount', '?')} {salary.get('unit', 'lakhs')}"
        else:
            highlights['salary_expectation'] = 'Not provided'
        
        # Availability
        availability = extracted.get('availability')
        if availability:
            if availability.get('status') == 'immediate':
                highlights['availability'] = 'Immediate'
            elif availability.get('days'):
                highlights['availability'] = f"{availability.get('days')} days notice"
            else:
                highlights['availability'] = 'Available'
        else:
            highlights['availability'] = 'Not provided'
        
        # Skill confirmations
        skills = extracted.get('skills', [])
        if skills:
            highlights['skills_confirmed'] = skills[:5]
        else:
            highlights['skills_confirmed'] = []
        
        # Experience
        exp = extracted.get('experience_years')
        if exp:
            highlights['experience_years'] = exp
        else:
            highlights['experience_years'] = 'Not provided'
        
        return highlights
    
    def _assess_overall(self, results):
        """Overall assessment"""
        if not results:
            return "Insufficient data"
        
        avg_score = sum(r.get('score', 0) for r in results) / len(results)
        
        if avg_score >= 80:
            return "Strong candidate - meets all requirements"
        elif avg_score >= 60:
            return "Good candidate - meets most requirements"
        elif avg_score >= 40:
            return "Average candidate - consider for review"
        else:
            return "Weak candidate - not recommended"
    
    def _make_recommendation(self, results):
        """Make hiring recommendation"""
        if not results:
            return "Review needed - insufficient data"
        
        avg_score = sum(r.get('score', 0) for r in results) / len(results)
        
        if avg_score >= 80:
            return "Proceed to next round"
        elif avg_score >= 60:
            return "Consider for next round"
        elif avg_score >= 40:
            return "Keep in review queue"
        else:
            return "Not recommended for next round"
    
    def export_to_json(self, report, filename='output/screening_report.json'):
        """Export report to JSON"""
        import os
        os.makedirs('output', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ JSON report saved: {filename}")
    
    def export_to_html(self, report, filename='output/screening_report.html'):
        """Export report to HTML (recruiter-friendly)"""
        import os
        os.makedirs('output', exist_ok=True)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AI Screening Report - {report['report_id']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #2563eb; color: white; padding: 20px; border-radius: 10px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }}
        .section h2 {{ color: #2563eb; margin-top: 0; }}
        .score-high {{ color: green; font-weight: bold; }}
        .score-low {{ color: red; font-weight: bold; }}
        .highlight {{ background: #f0f9ff; padding: 10px; border-left: 4px solid #2563eb; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f5f5f5; }}
        .strength {{ color: green; }}
        .risk {{ color: red; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Screening Report</h1>
        <p>Report ID: {report['report_id']}</p>
        <p>Generated: {report['generated_at']}</p>
    </div>
    
    <div class="section">
        <h2>📋 Candidate Information</h2>
        <p><strong>Name:</strong> {report['candidate_info']['name']}</p>
        <p><strong>Email:</strong> {report['candidate_info']['email']}</p>
        <p><strong>Phone:</strong> {report['candidate_info']['phone']}</p>
        <p><strong>Job ID:</strong> {report['candidate_info']['job_id']}</p>
    </div>
    
    <div class="section">
        <h2>📊 Screening Summary</h2>
        <p><strong>Total Questions:</strong> {report['screening_summary']['total_questions']}</p>
        <p><strong>Average Score:</strong> {report['screening_summary']['average_score']}%</p>
        <p><strong>Rating:</strong> {report['screening_summary']['rating']}</p>
    </div>
    
    <div class="section">
        <h2>⭐ Strengths</h2>
        <ul>
            {''.join(f'<li class="strength">{s}</li>' for s in report['strengths'])}
        </ul>
    </div>
    
    <div class="section">
        <h2>⚠️ Risks</h2>
        <ul>
            {''.join(f'<li class="risk">{r}</li>' for r in report['risks'])}
        </ul>
    </div>
    
    <div class="section">
        <h2>📌 Key Highlights</h2>
        <div class="highlight">
            <p><strong>💰 Salary Expectation:</strong> {report['highlights']['salary_expectation']}</p>
            <p><strong>📅 Availability:</strong> {report['highlights']['availability']}</p>
            <p><strong>🛠️ Skills Confirmed:</strong> {', '.join(report['highlights']['skills_confirmed']) if report['highlights']['skills_confirmed'] else 'None'}</p>
            <p><strong>📈 Experience:</strong> {report['highlights']['experience_years']} years</p>
        </div>
    </div>
    
    <div class="section">
        <h2>📝 Missing Data</h2>
        <p>{', '.join(report['missing_data']) if report['missing_data'] else 'All required data provided'}</p>
    </div>
    
    <div class="section">
        <h2>🎯 Recommendation</h2>
        <p><strong>{report['recommendation']}</strong></p>
        <p>{report['overall_assessment']}</p>
    </div>
</body>
</html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ HTML report saved: {filename}")

def main():
    print("="*70)
    print("DAY 28 - AI SCREENING REPORT GENERATOR")
    print("="*70)
    
    # Sample candidate data
    candidate = {
        'name': 'Midhun Raj',
        'email': 'midhun@email.com',
        'phone': '9037095458',
        'job_id': 'SE-2025-001'
    }
    
    # Sample screening results
    screening_results = [
        {'intent': 'skills', 'question': 'What are your technical skills?', 'answer': 'Python, Java, React, SQL', 'score': 85},
        {'intent': 'experience', 'question': 'How many years of experience?', 'answer': 'I have 4 years of experience', 'score': 90},
        {'intent': 'salary', 'question': 'What is your salary expectation?', 'answer': 'Around 12 lakhs', 'score': 70},
        {'intent': 'availability', 'question': 'When can you join?', 'answer': 'I can join in 30 days', 'score': 75},
        {'intent': 'location', 'question': 'Are you willing to relocate?', 'answer': 'Yes, I can relocate', 'score': 80}
    ]
    
    # Sample extracted data
    extracted_data = {
        'skills': ['Python', 'Java', 'React', 'SQL'],
        'experience_years': 4,
        'salary': {'amount': 12, 'unit': 'lakhs'},
        'availability': {'status': 'notice_period', 'days': 30}
    }
    
    # Generate report
    generator = ReportGenerator()
    report = generator.generate_report(candidate, screening_results, extracted_data)
    
    # Display report summary
    print("\n📋 REPORT SUMMARY")
    print("="*60)
    print(f"Candidate: {report['candidate_info']['name']}")
    print(f"Job ID: {report['candidate_info']['job_id']}")
    print(f"Average Score: {report['screening_summary']['average_score']}% ({report['screening_summary']['rating']})")
    
    print("\n⭐ Strengths:")
    for s in report['strengths']:
        print(f"   • {s}")
    
    print("\n⚠️ Risks:")
    for r in report['risks']:
        print(f"   • {r}")
    
    print("\n📌 Highlights:")
    print(f"   • Salary: {report['highlights']['salary_expectation']}")
    print(f"   • Availability: {report['highlights']['availability']}")
    print(f"   • Skills: {', '.join(report['highlights']['skills_confirmed'])}")
    
    print(f"\n🎯 Recommendation: {report['recommendation']}")
    
    # Export reports
    generator.export_to_json(report)
    generator.export_to_html(report)
    
    print("\n" + "="*70)
    print("✅ DAY 28 COMPLETED - AI SCREENING REPORT GENERATOR")
    print("="*70)

if __name__ == "__main__":
    main()