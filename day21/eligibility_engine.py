# eligibility_engine.py - Day 21 Eligibility Decision Engine
import json
import pandas as pd
from datetime import datetime

class EligibilityEngine:
    def __init__(self, config_file=None):
        """Initialize with configurable rules"""
        self.rules = self._load_default_rules()
        if config_file:
            self.load_config(config_file)
        self.decisions = []
    
    def _load_default_rules(self):
        """Default eligibility rules"""
        return {
            'default': {
                'min_ats_score': 70,
                'mandatory_skills': [],
                'min_experience_years': 0,
                'max_experience_years': 99,
                'allowed_locations': ['Any'],
                'availability_required': False
            }
        }
    
    def load_config(self, config_file):
        """Load role-specific rules from JSON"""
        try:
            with open(config_file, 'r') as f:
                self.rules = json.load(f)
            print(f"✅ Config loaded: {config_file}")
        except FileNotFoundError:
            print(f"⚠️ Config file not found. Using defaults.")
    
    def save_config(self, config_file='config/eligibility_rules.json'):
        """Save current rules to JSON"""
        import os
        os.makedirs('config', exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(self.rules, f, indent=2)
        print(f"✅ Config saved: {config_file}")
    
    def check_mandatory_skills(self, candidate_skills, required_skills):
        """Check if candidate has all mandatory skills"""
        if not required_skills:
            return True, []
        
        missing = [s for s in required_skills if s.lower() not in [c.lower() for c in candidate_skills]]
        return len(missing) == 0, missing
    
    def check_experience(self, candidate_years, min_exp, max_exp):
        """Check if experience is within range"""
        if candidate_years is None:
            return False, "Experience data missing"
        
        if candidate_years < min_exp:
            return False, f"Experience below minimum ({candidate_years} < {min_exp})"
        if candidate_years > max_exp:
            return False, f"Experience above maximum ({candidate_years} > {max_exp})"
        return True, f"Experience OK ({candidate_years} years)"
    
    def check_location(self, candidate_location, allowed_locations):
        """Check if candidate location is allowed"""
        if 'Any' in allowed_locations:
            return True, "Any location allowed"
        
        if not candidate_location:
            return False, "Location data missing"
        
        if candidate_location not in allowed_locations:
            return False, f"Location {candidate_location} not allowed"
        return True, f"Location {candidate_location} allowed"
    
    def check_availability(self, candidate_available, required):
        """Check availability if required"""
        if not required:
            return True, "Availability not required"
        
        if candidate_available is None:
            return False, "Availability data missing"
        
        if candidate_available:
            return True, "Candidate available"
        return False, "Candidate not available"
    
    def determine_eligibility(self, candidate, job_role='default'):
        """Main eligibility decision logic"""
        # Get rules for this role
        rules = self.rules.get(job_role, self.rules['default'])
        
        # Collect checks
        checks = {}
        reasons = []
        
        # 1. ATS score check
        ats_score = candidate.get('ats_score', 0)
        min_score = rules.get('min_ats_score', 70)
        if ats_score >= min_score:
            checks['score'] = True
            reasons.append(f"ATS score {ats_score} ≥ {min_score}")
        else:
            checks['score'] = False
            reasons.append(f"ATS score {ats_score} < {min_score}")
        
        # 2. Mandatory skills
        mandatory_skills = rules.get('mandatory_skills', [])
        skills_ok, missing = self.check_mandatory_skills(
            candidate.get('skills', []), mandatory_skills
        )
        checks['skills'] = skills_ok
        if skills_ok:
            reasons.append("All mandatory skills present")
        else:
            reasons.append(f"Missing mandatory skills: {missing}")
        
        # 3. Experience range
        min_exp = rules.get('min_experience_years', 0)
        max_exp = rules.get('max_experience_years', 99)
        exp_ok, exp_reason = self.check_experience(
            candidate.get('experience_years'), min_exp, max_exp
        )
        checks['experience'] = exp_ok
        reasons.append(exp_reason)
        
        # 4. Location
        allowed_locations = rules.get('allowed_locations', ['Any'])
        loc_ok, loc_reason = self.check_location(
            candidate.get('location'), allowed_locations
        )
        checks['location'] = loc_ok
        reasons.append(loc_reason)
        
        # 5. Availability
        availability_required = rules.get('availability_required', False)
        avail_ok, avail_reason = self.check_availability(
            candidate.get('available'), availability_required
        )
        checks['availability'] = avail_ok
        reasons.append(avail_reason)
        
        # Final decision
        all_passed = all(checks.values())
        
        if all_passed:
            decision = 'ELIGIBLE'
        elif not checks.get('score', True):
            decision = 'REJECTED'  # Score too low → reject
        else:
            decision = 'REVIEW'     # Other issues → manual review
        
        result = {
            'candidate_id': candidate.get('id'),
            'job_role': job_role,
            'ats_score': ats_score,
            'checks': checks,
            'decision': decision,
            'reasons': reasons,
            'evaluated_at': datetime.now().isoformat()
        }
        
        self.decisions.append(result)
        return result
    
    def get_eligible_candidates(self):
        """Get all eligible candidates"""
        return [d for d in self.decisions if d['decision'] == 'ELIGIBLE']
    
    def get_review_candidates(self):
        """Get candidates needing review"""
        return [d for d in self.decisions if d['decision'] == 'REVIEW']
    
    def get_rejected_candidates(self):
        """Get rejected candidates"""
        return [d for d in self.decisions if d['decision'] == 'REJECTED']
    
    def generate_report(self):
        """Generate eligibility summary report"""
        summary = {
            'generated_at': datetime.now().isoformat(),
            'total_candidates': len(self.decisions),
            'eligible': len(self.get_eligible_candidates()),
            'review': len(self.get_review_candidates()),
            'rejected': len(self.get_rejected_candidates()),
            'by_role': {}
        }
        
        # Group by job role
        for d in self.decisions:
            role = d['job_role']
            if role not in summary['by_role']:
                summary['by_role'][role] = {'eligible': 0, 'review': 0, 'rejected': 0}
            summary['by_role'][role][d['decision'].lower()] += 1
        
        return summary
    
    def export_results(self, filename='output/eligibility_results.json'):
        """Export all decisions to JSON"""
        import os
        os.makedirs('output', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump({
                'summary': self.generate_report(),
                'decisions': self.decisions
            }, f, indent=2)
        print(f"✅ Results exported: {filename}")

def create_sample_data():
    """Create sample candidates with ATS scores"""
    candidates = [
        {
            'id': 'C001',
            'ats_score': 96.5,
            'skills': ['Python', 'React', 'SQL', 'AWS'],
            'experience_years': 4,
            'location': 'Bangalore',
            'available': True
        },
        {
            'id': 'C002',
            'ats_score': 44.8,
            'skills': ['Python', 'Flask'],
            'experience_years': 2,
            'location': 'Mumbai',
            'available': True
        },
        {
            'id': 'C003',
            'ats_score': 82.3,
            'skills': ['Java', 'Spring', 'SQL'],
            'experience_years': 4,
            'location': 'Delhi',
            'available': False
        },
        {
            'id': 'C004',
            'ats_score': 67.5,
            'skills': ['JavaScript', 'React', 'Node'],
            'experience_years': 3,
            'location': 'Bangalore',
            'available': True
        },
        {
            'id': 'C005',
            'ats_score': 91.2,
            'skills': ['Python', 'TensorFlow', 'Pandas'],
            'experience_years': 6,
            'location': 'Pune',
            'available': True
        }
    ]
    return candidates

def create_sample_config():
    """Create sample eligibility rules config"""
    config = {
        'software_engineer': {
            'min_ats_score': 75,
            'mandatory_skills': ['Python', 'SQL'],
            'min_experience_years': 2,
            'max_experience_years': 8,
            'allowed_locations': ['Bangalore', 'Pune', 'Any'],
            'availability_required': True
        },
        'data_scientist': {
            'min_ats_score': 80,
            'mandatory_skills': ['Python', 'Machine Learning'],
            'min_experience_years': 3,
            'max_experience_years': 10,
            'allowed_locations': ['Bangalore', 'Any'],
            'availability_required': True
        },
        'default': {
            'min_ats_score': 70,
            'mandatory_skills': [],
            'min_experience_years': 0,
            'max_experience_years': 99,
            'allowed_locations': ['Any'],
            'availability_required': False
        }
    }
    
    import os
    os.makedirs('config', exist_ok=True)
    with open('config/eligibility_rules.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ Sample config created: config/eligibility_rules.json")

def main():
    print("="*70)
    print("DAY 21 - ELIGIBILITY DECISION ENGINE")
    print("="*70)
    
    # Create config and data
    create_sample_config()
    candidates = create_sample_data()
    
    # Initialize engine with config
    engine = EligibilityEngine('config/eligibility_rules.json')
    
    print("\n📋 EVALUATING CANDIDATES FOR SOFTWARE ENGINEER ROLE")
    print("-"*50)
    
    # Evaluate all candidates
    for candidate in candidates:
        result = engine.determine_eligibility(candidate, 'software_engineer')
        
        print(f"\n📌 Candidate {result['candidate_id']}:")
        print(f"   ATS Score: {result['ats_score']}")
        print(f"   Decision : {result['decision']}")
        print(f"   Reasons  :")
        for reason in result['reasons']:
            print(f"      • {reason}")
    
    # Show summary
    summary = engine.generate_report()
    print("\n" + "="*70)
    print("📊 ELIGIBILITY SUMMARY")
    print("="*70)
    print(f"Total Candidates: {summary['total_candidates']}")
    print(f"✅ Eligible      : {summary['eligible']}")
    print(f"⚠️ Review        : {summary['review']}")
    print(f"❌ Rejected      : {summary['rejected']}")
    
    # Show by role
    print("\n📋 BY ROLE:")
    for role, stats in summary['by_role'].items():
        print(f"   {role}: Eligible={stats['eligible']}, Review={stats['review']}, Rejected={stats['rejected']}")
    
    # Export results
    engine.export_results()
    
    print("\n" + "="*70)
    print("✅ DAY 21 COMPLETED - ELIGIBILITY DECISION ENGINE")
    print("="*70)

if __name__ == "__main__":
    main()