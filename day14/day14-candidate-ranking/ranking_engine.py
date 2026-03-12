# ranking_engine.py - Candidate Ranking & Shortlisting (Day 14)
import json
import pandas as pd
from datetime import datetime
import os

class RankingEngine:
    def __init__(self, shortlist_threshold=70, review_threshold=50):
        """
        Initialize ranking engine with thresholds
        shortlist_threshold: Minimum score to auto-shortlist
        review_threshold: Minimum score to consider for review
        """
        self.shortlist_threshold = shortlist_threshold
        self.review_threshold = review_threshold
        self.candidates = []
    
    def add_candidate(self, candidate_id, name, score, skills=None, experience=None):
        """Add a candidate to the ranking pool"""
        candidate = {
            'candidate_id': candidate_id,
            'name': name,
            'score': score,
            'skills': skills or [],
            'experience': experience or 0,
            'status': self._determine_status(score)
        }
        self.candidates.append(candidate)
        return candidate
    
    def _determine_status(self, score):
        """Determine candidate status based on score"""
        if score >= self.shortlist_threshold:
            return 'SHORTLISTED'
        elif score >= self.review_threshold:
            return 'REVIEW'
        else:
            return 'REJECTED'
    
    def rank_candidates(self):
        """Sort candidates by score (highest first)"""
        return sorted(self.candidates, key=lambda x: x['score'], reverse=True)
    
    def get_top_n(self, n=5):
        """Get top N candidates by score"""
        ranked = self.rank_candidates()
        return ranked[:n]
    
    def get_shortlisted(self):
        """Get all shortlisted candidates"""
        return [c for c in self.candidates if c['status'] == 'SHORTLISTED']
    
    def get_review_zone(self):
        """Get candidates in review zone"""
        return [c for c in self.candidates if c['status'] == 'REVIEW']
    
    def get_rejected(self):
        """Get auto-rejected candidates"""
        return [c for c in self.candidates if c['status'] == 'REJECTED']
    
    def generate_summary(self):
        """Generate summary statistics"""
        ranked = self.rank_candidates()
        return {
            'total_candidates': len(self.candidates),
            'shortlisted': len(self.get_shortlisted()),
            'review_zone': len(self.get_review_zone()),
            'rejected': len(self.get_rejected()),
            'top_score': ranked[0]['score'] if ranked else 0,
            'bottom_score': ranked[-1]['score'] if ranked else 0,
            'average_score': sum(c['score'] for c in self.candidates) / len(self.candidates) if self.candidates else 0
        }
    
    def export_to_csv(self, filename='ranked_candidates.csv'):
        """Export ranked candidates to CSV"""
        df = pd.DataFrame(self.rank_candidates())
        os.makedirs('output', exist_ok=True)
        path = f'output/{filename}'
        df.to_csv(path, index=False)
        print(f"✅ CSV exported: {path}")
        return path
    
    def export_to_json(self, filename='ranked_candidates.json'):
        """Export ranked candidates to JSON"""
        os.makedirs('output', exist_ok=True)
        path = f'output/{filename}'
        with open(path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'thresholds': {
                    'shortlist': self.shortlist_threshold,
                    'review': self.review_threshold
                },
                'summary': self.generate_summary(),
                'candidates': self.rank_candidates()
            }, f, indent=2)
        print(f"✅ JSON exported: {path}")
        return path
    
    def print_ranked_table(self):
        """Print ranked candidates in table format"""
        print("\n" + "="*80)
        print(f"CANDIDATE RANKING (Shortlist ≥ {self.shortlist_threshold}, Review ≥ {self.review_threshold})")
        print("="*80)
        print(f"{'Rank':<5} {'ID':<10} {'Name':<20} {'Score':<8} {'Status':<12} {'Skills':<20}")
        print("-"*80)
        
        for i, c in enumerate(self.rank_candidates(), 1):
            status_display = {
                'SHORTLISTED': '✅ SHORTLISTED',
                'REVIEW': '⚠️ REVIEW',
                'REJECTED': '❌ REJECTED'
            }.get(c['status'], c['status'])
            
            skills_str = ', '.join(c['skills'][:3]) + ('...' if len(c['skills']) > 3 else '')
            print(f"{i:<5} {c['candidate_id']:<10} {c['name']:<20} {c['score']:<8} {status_display:<12} {skills_str:<20}")
        
        print("="*80)
        
        # Summary
        summary = self.generate_summary()
        print(f"\n📊 SUMMARY:")
        print(f"   Total: {summary['total_candidates']} | "
              f"✅ Shortlisted: {summary['shortlisted']} | "
              f"⚠️ Review: {summary['review_zone']} | "
              f"❌ Rejected: {summary['rejected']}")
        print(f"   Score Range: {summary['bottom_score']} – {summary['top_score']} | "
              f"Average: {summary['average_score']:.1f}")

def create_sample_data():
    """Create sample candidates with scores from Day 13"""
    engine = RankingEngine(shortlist_threshold=70, review_threshold=50)
    
    # Add sample candidates (simulating ATS scores from Day 13)
    engine.add_candidate('C001', 'midhun raj', 96.5, 
                        ['Python', 'Django', 'React'], 5)
    engine.add_candidate('C002', 'adarsh ', 44.8, 
                        ['Python', 'Flask'], 2)
    engine.add_candidate('C003', 'tiby tomy', 82.3, 
                        ['Java', 'Spring', 'SQL'], 4)
    engine.add_candidate('C004', 'abin tom', 67.5, 
                        ['JavaScript', 'React', 'Node'], 3)
    engine.add_candidate('C005', 'jithin sam', 91.2, 
                        ['Python', 'TensorFlow', 'Pandas'], 6)
    engine.add_candidate('C006', 'Diana Prince', 55.0, 
                        ['HTML', 'CSS', 'JavaScript'], 2)
    engine.add_candidate('C007', 'Evan Wright', 38.2, 
                        ['Excel', 'Word'], 1)
    engine.add_candidate('C008', 'Fiona Green', 78.9, 
                        ['Python', 'Django', 'PostgreSQL'], 4)
    engine.add_candidate('C009', 'George King', 62.4, 
                        ['Java', 'Spring'], 3)
    engine.add_candidate('C010', 'Hannah Lee', 49.7, 
                        ['JavaScript', 'React'], 2)
    
    return engine

def test_different_thresholds():
    """Test ranking with different thresholds"""
    print("\n" + "="*80)
    print("TESTING DIFFERENT SHORTLISTING THRESHOLDS")
    print("="*80)
    
    thresholds = [(80, 60), (70, 50), (60, 40)]
    
    for short, review in thresholds:
        engine = RankingEngine(shortlist_threshold=short, review_threshold=review)
        
        # Add same candidates
        engine.add_candidate('C001', 'midhun raj', 96.5)
        engine.add_candidate('C002', 'adarsh', 44.8)
        engine.add_candidate('C003', 'tiby tomy', 82.3)
        engine.add_candidate('C004', 'abin tom', 67.5)
        engine.add_candidate('C005', 'jithin sam', 91.2)
        
        print(f"\n📊 Thresholds: Shortlist ≥ {short}, Review ≥ {review}")
        summary = engine.generate_summary()
        print(f"   Shortlisted: {summary['shortlisted']}, "
              f"Review: {summary['review_zone']}, "
              f"Rejected: {summary['rejected']}")

def main():
    print("="*80)
    print("DAY 14 - CANDIDATE RANKING & SHORTLISTING ENGINE")
    print("="*80)
    
    # Create ranking engine with sample data
    engine = create_sample_data()
    
    # Display ranked candidates
    engine.print_ranked_table()
    
    # Show top 5 candidates
    print("\n" + "="*80)
    print("🏆 TOP 5 CANDIDATES")
    print("="*80)
    top5 = engine.get_top_n(5)
    for i, c in enumerate(top5, 1):
        print(f"{i}. {c['name']} (ID: {c['candidate_id']}) – Score: {c['score']} – {c['status']}")
    
    # Export results
    engine.export_to_csv()
    engine.export_to_json()
    
    # Test different thresholds
    test_different_thresholds()
    
    # Generate recruiter-friendly summary
    print("\n" + "="*80)
    print("📋 RECRUITER SUMMARY")
    print("="*80)
    
    shortlisted = engine.get_shortlisted()
    review = engine.get_review_zone()
    rejected = engine.get_rejected()
    
    print(f"\n✅ SHORTLISTED CANDIDATES ({len(shortlisted)}):")
    for c in shortlisted[:3]:  # Show first 3
        print(f"   • {c['name']} – Score: {c['score']} – Skills: {', '.join(c['skills'][:3])}")
    
    print(f"\n⚠️ REVIEW ZONE ({len(review)}):")
    for c in review[:3]:
        print(f"   • {c['name']} – Score: {c['score']}")
    
    print(f"\n❌ AUTO-REJECTED ({len(rejected)}):")
    for c in rejected[:3]:
        print(f"   • {c['name']} – Score: {c['score']}")
    
    print("\n" + "="*80)
    print("✅ DAY 14 COMPLETED - CANDIDATE RANKING & SHORTLISTING")
    print("="*80)

if __name__ == "__main__":
    main()