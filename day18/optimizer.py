# optimizer.py - Day 18 Optimization & Performance Tuning
import time
import psutil
import re
import json
import os
import cProfile
import pstats
from datetime import datetime
import pandas as pd

class ATSEngine:
    def __init__(self, use_cache=True):
        self.use_cache = use_cache
        self.cache = {}
        self.stats = {
            'total_processed': 0,
            'total_time': 0,
            'total_memory': 0,
            'avg_time': 0,
            'avg_memory': 0,
            'errors': 0
        }
    
    # ==================== OPTIMIZATION 1: TEXT EXTRACTION SPEED ====================
    def extract_text_fast(self, file_path):
        """Optimized text extraction with caching"""
        start = time.time()
        
        # Check cache first
        if self.use_cache and file_path in self.cache:
            return self.cache[file_path]
        
        # Fast extraction - assume .txt for demo
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Cache if enabled
        if self.use_cache:
            self.cache[file_path] = text
        
        end = time.time()
        self._record_stats('extract', end-start, file_path)
        return text
    
    # ==================== OPTIMIZATION 2: NOISY RESUME HANDLING ====================
    def clean_noisy_resume(self, text):
        """Remove noise, fix formatting, handle messy resumes"""
        original_len = len(text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix broken lines (join hyphenated words)
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\-\:\/\(\)\[\]]', '', text)
        
        # Normalize bullet points
        text = re.sub(r'[•·●○◆]', '•', text)
        
        cleaned_len = len(text)
        reduction = original_len - cleaned_len
        
        return text, reduction
    
    # ==================== OPTIMIZATION 3: ENTITY DETECTION ====================
    def extract_entities_fast(self, text):
        """Fast entity extraction using optimized regex"""
        entities = {
            'emails': [],
            'phones': [],
            'skills': [],
            'experience': []
        }
        
        # Email extraction - optimized regex
        emails = re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
        entities['emails'] = list(set(emails))[:5]  # Limit to 5
        
        # Phone extraction
        phones = re.findall(r'\b\d{10}\b', text)
        entities['phones'] = list(set(phones))[:3]
        
        # Quick skill detection (common tech skills)
        skill_patterns = [
            r'\b(Python|Java|JavaScript|React|Node|SQL|AWS|Docker)\b',
            r'\b(MongoDB|PostgreSQL|TensorFlow|Pandas|NumPy)\b',
            r'\b(Django|Flask|Spring|Git|Linux|Kubernetes)\b'
        ]
        
        skills = set()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)
        entities['skills'] = list(skills)[:10]
        
        # Experience extraction
        exp_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?',
            r'experience.*?(\d+)\s*years?'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities['experience'].append(f"{match.group(1)} years")
                break
        
        return entities
    
    # ==================== OPTIMIZATION 4: MEMORY HANDLING ====================
    def _record_stats(self, operation, duration, file_path):
        """Record performance metrics"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        self.stats['total_processed'] += 1
        self.stats['total_time'] += duration
        self.stats['total_memory'] += memory_mb
        self.stats['avg_time'] = self.stats['total_time'] / self.stats['total_processed']
        self.stats['avg_memory'] = self.stats['total_memory'] / self.stats['total_processed']
    
    def clear_cache(self):
        """Free memory by clearing cache"""
        cache_size = len(self.cache)
        self.cache.clear()
        print(f"✅ Cache cleared: {cache_size} entries removed")
    
    # ==================== OPTIMIZATION 5: PROFILE CODE ====================
    def profile_function(self, func, *args):
        """Profile a function to find bottlenecks"""
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args)
        profiler.disable()
        
        # Save profile stats
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 bottlenecks
        
        return result
    
    # ==================== PERFORMANCE TESTING ====================
    def run_performance_test(self, test_files, iterations=5):
        """Run performance tests on multiple files"""
        print("\n" + "="*80)
        print("📊 PERFORMANCE TEST RESULTS")
        print("="*80)
        
        results = []
        
        for file_path in test_files:
            print(f"\n📄 Testing: {file_path}")
            
            # Test without cache
            print("   Without Cache:")
            times_no_cache = []
            for i in range(iterations):
                self.use_cache = False
                start = time.time()
                text = self.extract_text_fast(file_path)
                entities = self.extract_entities_fast(text)
                end = time.time()
                times_no_cache.append(end-start)
            avg_no_cache = sum(times_no_cache) / len(times_no_cache)
            print(f"      Avg time: {avg_no_cache*1000:.2f} ms")
            
            # Test with cache
            print("   With Cache:")
            times_cache = []
            for i in range(iterations):
                self.use_cache = True
                start = time.time()
                text = self.extract_text_fast(file_path)
                entities = self.extract_entities_fast(text)
                end = time.time()
                times_cache.append(end-start)
            avg_cache = sum(times_cache) / len(times_cache)
            print(f"      Avg time: {avg_cache*1000:.2f} ms")
            
            # Speed improvement
            improvement = ((avg_no_cache - avg_cache) / avg_no_cache) * 100
            print(f"   ⚡ Speed improvement: {improvement:.1f}%")
            
            results.append({
                'file': file_path,
                'avg_time_no_cache_ms': round(avg_no_cache*1000, 2),
                'avg_time_cache_ms': round(avg_cache*1000, 2),
                'improvement_percent': round(improvement, 1)
            })
        
        return results
    
    def test_noisy_resume_handling(self, noisy_text):
        """Test handling of messy resumes"""
        print("\n" + "="*80)
        print("🧹 NOISY RESUME HANDLING TEST")
        print("="*80)
        
        print("\n📄 Original (noisy):")
        print(noisy_text)
        
        cleaned, reduction = self.clean_noisy_resume(noisy_text)
        
        print("\n✅ Cleaned:")
        print(cleaned)
        print(f"\n📊 Reduction: {reduction} characters removed")
        
        entities = self.extract_entities_fast(cleaned)
        print("\n🔍 Extracted Entities:")
        for key, value in entities.items():
            if value:
                print(f"   {key}: {value}")
        
        return cleaned, entities
    
    def generate_performance_report(self, test_results):
        """Generate comprehensive performance report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'engine_version': '1.0.0',
            'optimizations_applied': [
                'Text extraction caching',
                'Optimized regex patterns',
                'Memory cache management',
                'Noise reduction pipeline',
                'Entity detection optimization'
            ],
            'performance_tests': test_results,
            'statistics': self.stats,
            'recommendations': []
        }
        
        # Add recommendations based on stats
        if self.stats['avg_time'] > 0.1:
            report['recommendations'].append("Consider further regex optimization")
        
        if self.stats['avg_memory'] > 500:
            report['recommendations'].append("Implement batch processing to reduce memory")
        
        if len(self.cache) > 100:
            report['recommendations'].append("Implement LRU cache eviction policy")
        
        return report
    
    def save_report(self, report, filename='performance_report.json'):
        """Save report to JSON"""
        os.makedirs('reports', exist_ok=True)
        path = f'reports/{filename}'
        with open(path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report saved: {path}")
        return path

def create_sample_files():
    """Create sample resume files for testing"""
    os.makedirs('data', exist_ok=True)
    
    # Clean resume
    clean_resume = """
    midhun raj
    Email: midhunraj@email.com
    Phone: 9037095458
    
    Skills: Python, JavaScript, React, Node.js, SQL
    
    Experience:
    Software Engineer at Google (2020-2023)
    - Developed web applications
    - Led team of 5 developers
    
    Education:
    B.Tech Computer Science, ABC University, 2020
    """
    
    # Noisy resume
    noisy_resume = """
    Jane    Smith
    Email:   jane.smith@email.com   
    Phone:   9876543211
    
    Skills:   Python  ,  Java  ,  Spring ,  SQL  
    
    Experience-
    Developer at Amazon
    (2019-2022)
    - Built microservices
    - API development
    
    Education:
    M.Sc Computer Sci-
    ence, XYZ Institute, 2019
    """
    
    with open('data/clean_resume.txt', 'w') as f:
        f.write(clean_resume)
    
    with open('data/noisy_resume.txt', 'w') as f:
        f.write(noisy_resume)
    
    print("✅ Sample files created in data/")

def main():
    print("="*80)
    print("DAY 18 - OPTIMIZATION & PERFORMANCE TUNING")
    print("="*80)
    
    # Create sample files
    create_sample_files()
    
    # Initialize engine
    engine = ATSEngine()
    
    # Test files
    test_files = ['data/clean_resume.txt', 'data/noisy_resume.txt']
    
    # Run performance tests
    results = engine.run_performance_test(test_files, iterations=3)
    
    # Test noisy resume handling
    with open('data/noisy_resume.txt', 'r') as f:
        noisy = f.read()
    engine.test_noisy_resume_handling(noisy)
    
    # Generate report
    report = engine.generate_performance_report(results)
    engine.save_report(report)
    
    # Show summary
    print("\n" + "="*80)
    print("📈 OPTIMIZATION SUMMARY")
    print("="*80)
    print(f"✅ Total processed: {engine.stats['total_processed']}")
    print(f"✅ Avg time: {engine.stats['avg_time']*1000:.2f} ms")
    print(f"✅ Avg memory: {engine.stats['avg_memory']:.2f} MB")
    print(f"✅ Cache size: {len(engine.cache)} entries")
    
    print("\n" + "="*80)
    print("✅ DAY 18 COMPLETED - OPTIMIZATION & PERFORMANCE TUNING")
    print("="*80)

if __name__ == "__main__":
    main()