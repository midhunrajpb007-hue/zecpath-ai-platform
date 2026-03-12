# fairness_engine.py - Fairness, Normalization & Bias Reduction (Day 15)
import re
import json
import pandas as pd
import numpy as np
from datetime import datetime
import os

class FairnessEngine:
    def __init__(self):
        """Initialize fairness engine with bias indicators"""
        self.personal_attributes = [
            'name', 'email', 'phone', 'address', 'gender', 
            'marital', 'religion', 'caste', 'age', 'dob'
        ]
        
        # Bias indicators to track
        self.bias_indicators = {
            'gender_mentioned': 0,
            'age_mentioned': 0,
            'location_mentioned': 0,
            'institution_bias': 0,
            'keyword_overdependence': 0
        }
    
    def mask_personal_attributes(self, text):
        """
        Mask non-essential personal attributes from resume
        """
        masked_text = text
        
        # Email masking
        masked_text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', masked_text)
        
        # Phone masking (10-digit Indian numbers)
        masked_text = re.sub(r'\b\d{10}\b', '[PHONE]', masked_text)
        
        # Age/DOB masking
        masked_text = re.sub(r'\b(age|dob|date of birth)[\s:]*(\d{1,2}[\/-]\d{1,2}[\/-]\d{2,4}|\d{1,2}\s+years?)\b', 
                             '[AGE_MASKED]', masked_text, flags=re.IGNORECASE)
        
        # Address masking
        address_patterns = [
            r'\b(address|addr)[\s:]*[^\n]+',
            r'\b(location|locality)[\s:]*[^\n]+',
            r'\b(city|state|pincode|zip)[\s:]*[^\n]+'
        ]
        for pattern in address_patterns:
            masked_text = re.sub(pattern, '[ADDRESS_MASKED]', masked_text, flags=re.IGNORECASE)
        
        # Gender masking
        gender_pattern = r'\b(gender|sex)[\s:]*[^\n]+'
        masked_text = re.sub(gender_pattern, '[GENDER_MASKED]', masked_text, flags=re.IGNORECASE)
        
        return masked_text
    
    def normalize_resume_format(self, resume_data):
        """
        Convert resume to standard format
        """
        standard_format = {
            'candidate_id': resume_data.get('candidate_id', 'UNKNOWN'),
            'skills': self._normalize_skills(resume_data.get('skills', [])),
            'experience': self._normalize_experience(resume_data.get('experience', [])),
            'education': self._normalize_education(resume_data.get('education', [])),
            'metadata': {
                'normalized_at': datetime.now().isoformat(),
                'original_format': resume_data.get('format', 'unknown')
            }
        }
        return standard_format
    
    def _normalize_skills(self, skills):
        """Normalize skill names (lowercase, trimmed)"""
        if not skills:
            return []
        
        normalized = []
        for skill in skills:
            if isinstance(skill, str):
                # Lowercase and strip
                clean_skill = skill.lower().strip()
                # Remove extra spaces
                clean_skill = ' '.join(clean_skill.split())
                normalized.append(clean_skill)
            else:
                normalized.append(skill)
        
        return normalized
    
    def _normalize_experience(self, experience):
        """Normalize experience entries"""
        if not experience:
            return []
        
        normalized = []
        for exp in experience:
            norm_exp = {}
            if isinstance(exp, dict):
                for key, value in exp.items():
                    if isinstance(value, str):
                        norm_exp[key] = value.lower().strip()
                    else:
                        norm_exp[key] = value
            else:
                norm_exp = exp
            normalized.append(norm_exp)
        
        return normalized
    
    def _normalize_education(self, education):
        """Normalize education entries"""
        if not education:
            return []
        
        normalized = []
        degree_mapping = {
            'b.tech': 'bachelor of technology',
            'b.e': 'bachelor of engineering',
            'm.tech': 'master of technology',
            'm.sc': 'master of science',
            'b.sc': 'bachelor of science',
            'mba': 'master of business administration',
            'ph.d': 'doctor of philosophy'
        }
        
        for edu in education:
            norm_edu = {}
            if isinstance(edu, dict):
                for key, value in edu.items():
                    if isinstance(value, str):
                        lower_val = value.lower().strip()
                        # Map common abbreviations
                        for abbr, full in degree_mapping.items():
                            if abbr in lower_val:
                                lower_val = lower_val.replace(abbr, full)
                        norm_edu[key] = lower_val
                    else:
                        norm_edu[key] = value
            else:
                norm_edu = edu
            normalized.append(norm_edu)
        
        return normalized
    
    def reduce_keyword_dependence(self, skills, required_skills, synonym_dict=None):
        """
        Reduce over-dependence on exact keyword matching
        """
        if synonym_dict is None:
            # Default synonym dictionary
            synonym_dict = {
                'python': ['python', 'py', 'python3'],
                'javascript': ['javascript', 'js', 'ecmascript'],
                'react': ['react', 'reactjs', 'react.js'],
                'node': ['node', 'nodejs', 'node.js'],
                'mongodb': ['mongodb', 'mongo'],
                'sql': ['sql', 'mysql', 'postgresql', 'database'],
                'aws': ['aws', 'amazon web services'],
                'docker': ['docker', 'container'],
                'kubernetes': ['kubernetes', 'k8s'],
                'java': ['java', 'core java'],
                'spring': ['spring', 'spring boot'],
                'django': ['django', 'django framework']
            }
        
        required_lower = [s.lower() for s in required_skills]
        candidate_lower = [s.lower() for s in skills]
        
        # Count matches with synonyms
        match_score = 0
        for req in required_lower:
            # Check exact match
            if req in candidate_lower:
                match_score += 1
                continue
            
            # Check synonyms
            for skill in candidate_lower:
                if req in synonym_dict and skill in synonym_dict[req]:
                    match_score += 1
                    break
                # Also check reverse
                for syn_list in synonym_dict.values():
                    if req in syn_list and skill in syn_list:
                        match_score += 1
                        break
        
        # Calculate percentage
        if required_lower:
            match_percentage = (match_score / len(required_lower)) * 100
        else:
            match_percentage = 0
        
        return {
            'match_percentage': round(match_percentage, 2),
            'exact_matches': sum(1 for r in required_lower if r in candidate_lower),
            'synonym_matches': match_score - sum(1 for r in required_lower if r in candidate_lower),
            'score': match_score
        }
    
    def normalize_scores(self, scores, method='minmax'):
        """
        Normalize scores to 0-100 range
        methods: minmax, zscore, rank
        """
        if not scores:
            return []
        
        scores_array = np.array(scores)
        
        if method == 'minmax':
            # Min-Max normalization
            min_val = scores_array.min()
            max_val = scores_array.max()
            if max_val - min_val == 0:
                normalized = [50] * len(scores_array)
            else:
                normalized = ((scores_array - min_val) / (max_val - min_val)) * 100
        
        elif method == 'zscore':
            # Z-score normalization (standardization)
            mean = scores_array.mean()
            std = scores_array.std()
            if std == 0:
                normalized = [50] * len(scores_array)
            else:
                z_scores = (scores_array - mean) / std
                # Convert to 0-100 scale
                normalized = (z_scores - z_scores.min()) / (z_scores.max() - z_scores.min()) * 100
        
        elif method == 'rank':
            # Rank-based normalization
            sorted_indices = np.argsort(scores_array)
            ranks = np.zeros_like(scores_array)
            ranks[sorted_indices] = np.arange(1, len(scores_array) + 1)
            normalized = (ranks - 1) / (len(scores_array) - 1) * 100
        
        else:
            normalized = scores_array
        
        return [round(float(x), 2) for x in normalized]
    
    def evaluate_bias_indicators(self, resumes):
        """
        Analyze resumes for potential bias indicators
        """
        bias_report = {
            'total_resumes': len(resumes),
            'personal_attributes_found': {},
            'institution_variety': 0,
            'location_variety': 0,
            'gender_indicators': 0,
            'recommendations': []
        }
        
        all_institutions = set()
        all_locations = set()
        
        for resume in resumes:
            text = json.dumps(resume).lower()
            
            # Check for personal attributes
            for attr in self.personal_attributes:
                if attr in text:
                    bias_report['personal_attributes_found'][attr] = \
                        bias_report['personal_attributes_found'].get(attr, 0) + 1
            
            # Track institutions
            if 'education' in resume:
                for edu in resume['education']:
                    if 'institution' in edu:
                        all_institutions.add(edu['institution'].lower())
            
            # Track locations
            if 'location' in resume:
                all_locations.add(resume['location'].lower())
        
        bias_report['institution_variety'] = len(all_institutions)
        bias_report['location_variety'] = len(all_locations)
        
        # Generate recommendations
        if bias_report['personal_attributes_found']:
            bias_report['recommendations'].append(
                "Mask personal attributes like name, email, phone, address"
            )
        
        if bias_report['institution_variety'] < 3:
            bias_report['recommendations'].append(
                "Consider candidates from diverse institutions"
            )
        
        if bias_report['location_variety'] < 3:
            bias_report['recommendations'].append(
                "Consider candidates from diverse locations"
            )
        
        return bias_report
    
    def process_resume(self, resume_data, required_skills=None, normalize_scores_flag=True):
        """
        Complete fairness processing pipeline
        """
        # Step 1: Mask personal attributes
        if 'raw_text' in resume_data:
            masked_text = self.mask_personal_attributes(resume_data['raw_text'])
            resume_data['masked_text'] = masked_text
        
        # Step 2: Normalize format
        normalized = self.normalize_resume_format(resume_data)
        
        # Step 3: Reduce keyword dependence (if required skills provided)
        keyword_analysis = None
        if required_skills and 'skills' in normalized:
            keyword_analysis = self.reduce_keyword_dependence(
                normalized['skills'], 
                required_skills
            )
        
        return {
            'normalized_resume': normalized,
            'keyword_analysis': keyword_analysis,
            'bias_indicators': self.evaluate_bias_indicators([resume_data])
        }
    
    def generate_fairness_report(self, candidates_data):
        """
        Generate comprehensive fairness report
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_candidates': len(candidates_data),
            'bias_analysis': self.evaluate_bias_indicators(candidates_data),
            'normalization_stats': {
                'personal_attributes_masked': sum(
                    1 for c in candidates_data if 'masked_text' in c
                )
            },
            'recommendations': []
        }
        
        # Add score normalization if scores available
        scores = [c.get('score', 0) for c in candidates_data if 'score' in c]
        if scores:
            report['original_scores'] = scores
            report['normalized_scores_minmax'] = self.normalize_scores(scores, 'minmax')
            report['normalized_scores_zscore'] = self.normalize_scores(scores, 'zscore')
            report['normalized_scores_rank'] = self.normalize_scores(scores, 'rank')
        
        return report
    
    def save_report(self, report, filename='fairness_report.json'):
        """Save fairness report to JSON"""
        os.makedirs('output', exist_ok=True)
        path = f'output/{filename}'
        with open(path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report saved: {path}")
        return path

def create_sample_data():
    """Create sample resumes for testing"""
    resumes = [
        {
            'candidate_id': 'C001',
            'raw_text': """
                Name: John Doe
                Email: john.doe@email.com
                Phone: 9876543210
                Address: 123 Main St, Mumbai
                
                SKILLS: Python, Django, React, SQL
                
                EXPERIENCE:
                Software Engineer at Google (2020-2023)
                
                EDUCATION:
                B.Tech Computer Science, IIT Bombay, 2020
            """,
            'skills': ['Python', 'Django', 'React', 'SQL'],
            'experience': [{'company': 'Google', 'role': 'Software Engineer', 'years': 3}],
            'education': [{'degree': 'B.Tech', 'field': 'CS', 'institution': 'IIT Bombay', 'year': 2020}],
            'score': 85,
            'format': 'text'
        },
        {
            'candidate_id': 'C002',
            'raw_text': """
                Name: Jane Smith
                Email: jane.smith@email.com
                Phone: 9876543211
                
                SKILLS: Java, Spring, SQL
                
                EXPERIENCE:
                Developer at Amazon (2019-2022)
                
                EDUCATION:
                B.E. Computer Science, Anna University, 2019
            """,
            'skills': ['Java', 'Spring', 'SQL'],
            'experience': [{'company': 'Amazon', 'role': 'Developer', 'years': 3}],
            'education': [{'degree': 'B.E.', 'field': 'CS', 'institution': 'Anna University', 'year': 2019}],
            'score': 72,
            'format': 'text'
        },
        {
            'candidate_id': 'C003',
            'raw_text': """
                Name: Alex Johnson
                Email: alex.j@email.com
                Phone: 9876543212
                
                SKILLS: Python, TensorFlow, Pandas
                
                EXPERIENCE:
                Data Scientist at Microsoft (2021-2023)
                
                EDUCATION:
                M.Sc Data Science, BITS Pilani, 2021
            """,
            'skills': ['Python', 'TensorFlow', 'Pandas'],
            'experience': [{'company': 'Microsoft', 'role': 'Data Scientist', 'years': 2}],
            'education': [{'degree': 'M.Sc', 'field': 'Data Science', 'institution': 'BITS Pilani', 'year': 2021}],
            'score': 78,
            'format': 'text'
        }
    ]
    return resumes

def main():
    print("="*80)
    print("DAY 15 - FAIRNESS, NORMALIZATION & BIAS REDUCTION")
    print("="*80)
    
    # Initialize engine
    engine = FairnessEngine()
    
    # Create sample data
    resumes = create_sample_data()
    print(f"\n📊 Processing {len(resumes)} sample resumes...")
    
    # Test keyword dependence reduction
    required_skills = ['Python', 'Django', 'SQL', 'Machine Learning']
    
    print("\n" + "="*80)
    print("1️⃣ KEYWORD DEPENDENCE REDUCTION")
    print("="*80)
    
    for resume in resumes:
        print(f"\n📋 Candidate: {resume['candidate_id']}")
        print(f"   Skills: {', '.join(resume['skills'])}")
        
        analysis = engine.reduce_keyword_dependence(
            resume['skills'], 
            required_skills
        )
        print(f"   Match %     : {analysis['match_percentage']}%")
        print(f"   Exact Matches : {analysis['exact_matches']}")
        print(f"   Synonym Matches: {analysis['synonym_matches']}")
    
    # Test personal attribute masking
    print("\n" + "="*80)
    print("2️⃣ PERSONAL ATTRIBUTE MASKING")
    print("="*80)
    
    for resume in resumes:
        print(f"\n📋 Original: {resume['raw_text'][:100]}...")
        masked = engine.mask_personal_attributes(resume['raw_text'])
        print(f"   Masked  : {masked[:100]}...")
    
    # Test score normalization
    print("\n" + "="*80)
    print("3️⃣ SCORE NORMALIZATION")
    print("="*80)
    
    scores = [r['score'] for r in resumes]
    print(f"\n📊 Original Scores: {scores}")
    
    norm_minmax = engine.normalize_scores(scores, 'minmax')
    norm_zscore = engine.normalize_scores(scores, 'zscore')
    norm_rank = engine.normalize_scores(scores, 'rank')
    
    print(f"   Min-Max : {norm_minmax}")
    print(f"   Z-Score : {norm_zscore}")
    print(f"   Rank    : {norm_rank}")
    
    # Generate fairness report
    print("\n" + "="*80)
    print("4️⃣ BIAS EVALUATION REPORT")
    print("="*80)
    
    report = engine.generate_fairness_report(resumes)
    print(json.dumps(report, indent=2))
    
    # Save report
    engine.save_report(report)
    
    print("\n" + "="*80)
    print("✅ DAY 15 COMPLETED - FAIRNESS, NORMALIZATION & BIAS REDUCTION")
    print("="*80)

if __name__ == "__main__":
    main()