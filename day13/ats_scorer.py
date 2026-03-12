# ats_scorer.py
import json
import numpy as np
from datetime import datetime

class ATSScorer:
    def __init__(self, weights_config=None):
        """
        Initialize ATS Scorer with configurable weights
        weights_config: dict with keys skill_weight, exp_weight, edu_weight, semantic_weight
        """
        if weights_config is None:
            # Default weights (balanced)
            self.weights = {
                'skill_weight': 0.40,
                'exp_weight': 0.30,
                'edu_weight': 0.20,
                'semantic_weight': 0.10
            }
        else:
            self.weights = weights_config
        
        self.validate_weights()
    
    def validate_weights(self):
        """Ensure weights sum to 1.0"""
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            print(f"⚠️ Warning: Weights sum to {total}, normalizing...")
            for k in self.weights:
                self.weights[k] /= total
    
    def score_skill_match(self, required_skills, candidate_skills):
        """
        Calculate skill match percentage
        required_skills: list of required skills
        candidate_skills: list of candidate's skills
        """
        if not required_skills:
            return 0
        
        # Convert to sets for comparison
        required_set = set(s.lower() for s in required_skills)
        candidate_set = set(s.lower() for s in candidate_skills)
        
        # Find matches
        matched = required_set.intersection(candidate_set)
        match_count = len(matched)
        
        # Calculate score
        score = (match_count / len(required_set)) * 100
        
        return {
            'score': round(score, 2),
            'matched_skills': list(matched),
            'missing_skills': list(required_set - candidate_set),
            'details': f"Matched {match_count}/{len(required_set)} required skills"
        }
    
    def score_experience_relevance(self, required_years, candidate_years, role_level=None):
        """
        Calculate experience relevance
        required_years: minimum years required
        candidate_years: candidate's total experience
        role_level: 'fresher', 'junior', 'mid', 'senior', 'lead'
        """
        if required_years is None or candidate_years is None:
            return {'score': 0, 'details': 'Experience data missing'}
        
        # If candidate has more than required, cap at 100%
        if candidate_years >= required_years:
            score = 100
        else:
            # Partial score based on ratio
            score = (candidate_years / required_years) * 100
        
        # Bonus for senior roles with extra experience
        if role_level in ['senior', 'lead'] and candidate_years > required_years * 1.5:
            score = min(score + 10, 100)
        
        return {
            'score': round(score, 2),
            'details': f"{candidate_years} years / {required_years} years required"
        }
    
    def score_education_alignment(self, required_edu, candidate_edu):
        """
        Score education alignment
        required_edu: dict with degree, field, min_year
        candidate_edu: list of candidate's education entries
        """
        if not required_edu or not candidate_edu:
            return {'score': 0, 'details': 'Education data missing'}
        
        degree_weights = {
            'phd': 1.0,
            'master': 0.9,
            'bachelor': 0.8,
            'diploma': 0.6,
            'higher_secondary': 0.4,
            'secondary': 0.2
        }
        
        best_score = 0
        best_match = None
        
        for edu in candidate_edu:
            score = 0
            
            # Degree level match
            req_level = required_edu.get('degree_level', '').lower()
            cand_level = edu.get('level', '').lower()
            
            if req_level and cand_level:
                if cand_level in degree_weights:
                    level_score = degree_weights[cand_level]
                    # If candidate has higher degree, still good
                    if cand_level == 'master' and req_level == 'bachelor':
                        level_score = 0.95
                    elif cand_level == 'phd' and req_level == 'master':
                        level_score = 0.95
                    score += level_score * 50  # 50% weight for degree level
            
            # Field match
            req_field = required_edu.get('field', '').lower()
            cand_field = edu.get('field', '').lower()
            
            if req_field and cand_field:
                if req_field in cand_field or cand_field in req_field:
                    score += 40  # 40% weight for field
                elif any(word in cand_field for word in req_field.split()):
                    score += 30  # Partial match
            
            # Year check (if applicable)
            if required_edu.get('min_year') and edu.get('year'):
                if edu['year'] >= required_edu['min_year']:
                    score += 10  # 10% weight for recency
            
            if score > best_score:
                best_score = score
                best_match = edu
        
        return {
            'score': round(best_score, 2),
            'matched_education': best_match,
            'details': f"Best match: {best_match.get('degree', 'N/A')} in {best_match.get('field', 'N/A')}" if best_match else 'No match'
        }
    
    def score_semantic_similarity(self, semantic_score):
        """
        Use semantic similarity from Day 12
        semantic_score: 0-100 score from semantic matcher
        """
        if semantic_score is None:
            return {'score': 0, 'details': 'Semantic data missing'}
        
        return {
            'score': round(semantic_score, 2),
            'details': f"Semantic similarity: {semantic_score:.2f}%"
        }
    
    def calculate_final_score(self, scores):
        """
        Calculate weighted final score
        scores: dict with skill, experience, education, semantic scores
        """
        final = (
            scores['skill']['score'] * self.weights['skill_weight'] +
            scores['experience']['score'] * self.weights['exp_weight'] +
            scores['education']['score'] * self.weights['edu_weight'] +
            scores['semantic']['score'] * self.weights['semantic_weight']
        )
        
        return round(final, 2)
    
    def generate_explainable_output(self, candidate_id, job_id, scores, final_score):
        """
        Generate human-readable score explanation
        """
        explanation = {
            'candidate_id': candidate_id,
            'job_id': job_id,
            'timestamp': datetime.now().isoformat(),
            'final_score': final_score,
            'weights_used': self.weights,
            'component_scores': {
                'skill': {
                    'score': scores['skill']['score'],
                    'details': scores['skill']['details'],
                    'matched': scores['skill'].get('matched_skills', []),
                    'missing': scores['skill'].get('missing_skills', [])
                },
                'experience': {
                    'score': scores['experience']['score'],
                    'details': scores['experience']['details']
                },
                'education': {
                    'score': scores['education']['score'],
                    'details': scores['education']['details']
                },
                'semantic': {
                    'score': scores['semantic']['score'],
                    'details': scores['semantic']['details']
                }
            },
            'contribution': {
                'skill_contribution': round(scores['skill']['score'] * self.weights['skill_weight'], 2),
                'experience_contribution': round(scores['experience']['score'] * self.weights['exp_weight'], 2),
                'education_contribution': round(scores['education']['score'] * self.weights['edu_weight'], 2),
                'semantic_contribution': round(scores['semantic']['score'] * self.weights['semantic_weight'], 2)
            },
            'summary': self._generate_summary(scores, final_score)
        }
        
        return explanation
    
    def _generate_summary(self, scores, final_score):
        """Generate short summary text"""
        parts = []
        
        if scores['skill']['score'] > 80:
            parts.append("strong skill match")
        elif scores['skill']['score'] > 50:
            parts.append("moderate skill match")
        else:
            parts.append("weak skill match")
        
        if scores['experience']['score'] > 80:
            parts.append("highly relevant experience")
        elif scores['experience']['score'] > 50:
            parts.append("relevant experience")
        
        if scores['education']['score'] > 70:
            parts.append("good education fit")
        
        if not parts:
            return "Candidate does not meet minimum requirements"
        
        return f"Candidate shows {' and '.join(parts)}. Final score: {final_score}%"
    
    def get_role_weights(self, role):
        """
        Get dynamic weights based on role
        """
        role_weights = {
            'software_engineer': {
                'skill_weight': 0.50,
                'exp_weight': 0.30,
                'edu_weight': 0.10,
                'semantic_weight': 0.10
            },
            'data_scientist': {
                'skill_weight': 0.40,
                'exp_weight': 0.30,
                'edu_weight': 0.20,
                'semantic_weight': 0.10
            },
            'marketing_manager': {
                'skill_weight': 0.30,
                'exp_weight': 0.40,
                'edu_weight': 0.20,
                'semantic_weight': 0.10
            },
            'fresher': {
                'skill_weight': 0.40,
                'exp_weight': 0.10,
                'edu_weight': 0.40,
                'semantic_weight': 0.10
            },
            'intern': {
                'skill_weight': 0.30,
                'exp_weight': 0.10,
                'edu_weight': 0.50,
                'semantic_weight': 0.10
            }
        }
        
        return role_weights.get(role, self.weights)
    
    def save_config(self, filename='ats_weights_config.json'):
        """Save current weights to JSON"""
        with open(filename, 'w') as f:
            json.dump(self.weights, f, indent=2)
        print(f"✅ Config saved to {filename}")
    
    def load_config(self, filename='ats_weights_config.json'):
        """Load weights from JSON"""
        try:
            with open(filename, 'r') as f:
                self.weights = json.load(f)
            self.validate_weights()
            print(f"✅ Config loaded from {filename}")
        except FileNotFoundError:
            print(f"⚠️ Config file {filename} not found, using defaults")

def create_sample_data():
    """Create sample candidate and job data"""
    
    # Job 1: Software Engineer
    job1 = {
        'job_id': 'SE001',
        'title': 'Software Engineer',
        'required_skills': ['Python', 'Django', 'SQL', 'REST APIs'],
        'required_experience': 3,
        'required_education': {
            'degree_level': 'bachelor',
            'field': 'Computer Science',
            'min_year': 2020
        },
        'role_level': 'mid'
    }
    
    # Candidate 1: Good match
    candidate1 = {
        'candidate_id': 'C001',
        'skills': ['Python', 'Django', 'SQL', 'REST APIs', 'Git'],
        'experience_years': 4,
        'education': [
            {
                'degree': 'B.Tech Computer Science',
                'field': 'Computer Science',
                'level': 'bachelor',
                'year': 2019,
                'institution': 'ABC University'
            }
        ],
        'semantic_score': 85  # From Day 12
    }
    
    # Candidate 2: Partial match
    candidate2 = {
        'candidate_id': 'C002',
        'skills': ['Python', 'Flask', 'MongoDB'],
        'experience_years': 2,
        'education': [
            {
                'degree': 'M.Sc Physics',
                'field': 'Physics',
                'level': 'master',
                'year': 2021,
                'institution': 'XYZ College'
            }
        ],
        'semantic_score': 65
    }
    
    return {
        'jobs': [job1],
        'candidates': [candidate1, candidate2]
    }

def main():
    print("=" * 70)
    print("DAY 13 - ATS SCORING FORMULA DESIGN")
    print("=" * 70)
    
    # Create sample data
    data = create_sample_data()
    job = data['jobs'][0]
    
    print(f"\n📌 Job: {job['title']} (ID: {job['job_id']})")
    print(f"   Required Skills: {', '.join(job['required_skills'])}")
    print(f"   Required Experience: {job['required_experience']} years")
    
    # Test different roles with dynamic weights
    roles_to_test = ['software_engineer', 'data_scientist', 'fresher']
    
    for role in roles_to_test:
        print(f"\n{'='*50}")
        print(f"🔧 Testing Role: {role.replace('_', ' ').title()}")
        print(f"{'='*50}")
        
        # Get role-specific weights
        scorer = ATSScorer()
        scorer.weights = scorer.get_role_weights(role)
        print(f"Weights: Skill={scorer.weights['skill_weight']*100:.0f}%, "
              f"Exp={scorer.weights['exp_weight']*100:.0f}%, "
              f"Edu={scorer.weights['edu_weight']*100:.0f}%, "
              f"Sem={scorer.weights['semantic_weight']*100:.0f}%")
        
        # Score each candidate
        for candidate in data['candidates']:
            print(f"\n📋 Candidate: {candidate['candidate_id']}")
            
            # Calculate component scores
            skill_score = scorer.score_skill_match(
                job['required_skills'], 
                candidate['skills']
            )
            
            exp_score = scorer.score_experience_relevance(
                job['required_experience'],
                candidate['experience_years'],
                job.get('role_level')
            )
            
            edu_score = scorer.score_education_alignment(
                job['required_education'],
                candidate['education']
            )
            
            semantic_score = scorer.score_semantic_similarity(
                candidate['semantic_score']
            )
            
            scores = {
                'skill': skill_score,
                'experience': exp_score,
                'education': edu_score,
                'semantic': semantic_score
            }
            
            # Calculate final score
            final_score = scorer.calculate_final_score(scores)
            
            # Generate explanation
            explanation = scorer.generate_explainable_output(
                candidate['candidate_id'],
                job['job_id'],
                scores,
                final_score
            )
            
            # Print summary
            print(f"   Skill Score   : {skill_score['score']:.1f}% ({skill_score['details']})")
            print(f"   Exp Score     : {exp_score['score']:.1f}% ({exp_score['details']})")
            print(f"   Edu Score     : {edu_score['score']:.1f}% ({edu_score['details']})")
            print(f"   Semantic Score: {semantic_score['score']:.1f}%")
            print(f"   → FINAL SCORE : {final_score}%")
            print(f"   📝 Summary    : {explanation['summary']}")
    
    # Save config
    scorer = ATSScorer()
    scorer.save_config()
    
    print("\n" + "=" * 70)
    print("✅ DAY 13 COMPLETED - ATS SCORING FORMULA DESIGN")
    print("=" * 70)

if __name__ == "__main__":
    main()