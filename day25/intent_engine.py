# intent_engine.py - Day 25 Answer Intent & Understanding Engine (UPDATED)
import re
import json
from datetime import datetime

class IntentEngine:
    def __init__(self):
        # Intent patterns (UPDATED - fixed availability and location)
        self.intent_patterns = {
            'introduction': ['myself', 'about me', 'intro', 'background', 'name'],
            'skills': ['skill', 'know', 'proficient', 'experience in', 'worked with', 'technologies'],
            'experience': ['years', 'experience', 'worked', 'job', 'company', 'role'],
            'education': ['degree', 'college', 'university', 'studied', 'b.tech', 'm.sc', 'b.e'],
            'location': ['location', 'city', 'place', 'relocate', 'move', 'based', 'live', 'reside', 'from'],
            'salary': ['salary', 'ctc', 'package', 'pay', 'expectation', 'lakh', 'thousand', 'lpa'],
            'notice_period': ['notice', 'joining', 'days', 'month'],
            'availability': ['available', 'join', 'start', 'ready', 'immediate']
        }
        
        # Pattern for extracting numbers (years, salary)
        self.number_pattern = r'\b(\d+(?:\.\d+)?)\s*(?:years?|yrs?|lakhs?|lpa|k|thousand)?\b'
        
        # Pattern for skills (common tech skills)
        self.skill_patterns = [
            r'\b(Python|Java|JavaScript|React|Node|SQL|MongoDB|AWS|Docker|Kubernetes)\b',
            r'\b(Spring|Django|Flask|Angular|Vue|TensorFlow|Pandas|NumPy)\b',
            r'\b(Git|Linux|Jenkins|Kubernetes|Docker|AWS|Azure|GCP)\b'
        ]
    
    # ========== INTENT CLASSIFICATION ==========
    
    def classify_intent(self, text):
        """Determine what the candidate is talking about"""
        text_lower = text.lower()
        scores = {}
        
        for intent, keywords in self.intent_patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            scores[intent] = score
        
        # Get highest scoring intent
        if max(scores.values()) == 0:
            return 'unknown'
        
        best_intent = max(scores, key=scores.get)
        return best_intent
    
    # ========== SKILL EXTRACTION ==========
    
    def extract_skills(self, text):
        """Extract technical skills from answer"""
        skills = []
        text_lower = text.lower()
        
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend(matches)
        
        # Remove duplicates and sort
        skills = list(set(skills))
        skills.sort()
        
        return skills
    
    # ========== EXPERIENCE EXTRACTION ==========
    
    def extract_experience(self, text):
        """Extract years of experience"""
        text_lower = text.lower()
        
        # Look for patterns like "3 years", "3+ years", "3 years experience"
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
            r'experience\s*(?:of)?\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            r'(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return float(match.group(1))
        
        # Look for words like "three", "five"
        word_numbers = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        
        words = text_lower.split()
        for word in words:
            if word in word_numbers:
                return word_numbers[word]
        
        return None
    
    # ========== SALARY EXTRACTION ==========
    
    def extract_salary(self, text):
        """Extract salary expectation"""
        text_lower = text.lower()
        
        # Patterns for salary
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:lakhs?|lpa)',
            r'(\d+(?:\.\d+)?)\s*k',
            r'(\d+(?:\.\d+)?)\s*thousand'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return {
                    'amount': float(match.group(1)),
                    'unit': 'lakhs' if 'lakh' in text_lower else 'thousands'
                }
        
        return None
    
    # ========== AVAILABILITY EXTRACTION ==========
    
    def extract_availability(self, text):
        """Extract joining availability"""
        text_lower = text.lower()
        
        if 'immediate' in text_lower or 'right away' in text_lower or 'now' in text_lower:
            return {'status': 'immediate', 'days': 0}
        
        # Look for days
        days_match = re.search(r'(\d+)\s*(?:days?|day)', text_lower)
        if days_match:
            return {'status': 'notice_period', 'days': int(days_match.group(1))}
        
        # Look for weeks
        weeks_match = re.search(r'(\d+)\s*(?:weeks?|week)', text_lower)
        if weeks_match:
            return {'status': 'notice_period', 'days': int(weeks_match.group(1)) * 7}
        
        # Look for months
        months_match = re.search(r'(\d+)\s*(?:months?|month)', text_lower)
        if months_match:
            return {'status': 'notice_period', 'days': int(months_match.group(1)) * 30}
        
        if 'available' in text_lower or 'join' in text_lower or 'start' in text_lower:
            return {'status': 'available', 'days': None}
        
        return None
    
    # ========== OFF-TOPIC DETECTION ==========
    
    def is_off_topic(self, text, expected_intent):
        """Check if answer is off-topic"""
        detected_intent = self.classify_intent(text)
        
        # If detected intent doesn't match expected, it might be off-topic
        if detected_intent != expected_intent:
            return True, f"Expected {expected_intent}, got {detected_intent}"
        
        # If answer is very short
        if len(text.split()) < 3:
            return True, "Answer too short"
        
        return False, "On topic"
    
    # ========== VAGUE ANSWER DETECTION ==========
    
    def is_vague(self, text):
        """Check if answer is vague"""
        vague_phrases = [
            'not sure', 'i don\'t know', 'maybe', 'probably', 'i think',
            'something like', 'around', 'approximately', 'some'
        ]
        
        text_lower = text.lower()
        
        for phrase in vague_phrases:
            if phrase in text_lower:
                return True, f"Contains vague phrase: '{phrase}'"
        
        # Check if very short
        if len(text.split()) < 3:
            return True, "Very short answer (less than 3 words)"
        
        return False, "Clear answer"
    
    # ========== STRUCTURED ANSWER ==========
    
    def parse_answer(self, text, question_intent):
        """Complete answer parsing into structured object"""
        
        # Classify intent
        detected_intent = self.classify_intent(text)
        
        # Check off-topic
        off_topic, off_reason = self.is_off_topic(text, question_intent)
        
        # Check vague
        is_vague, vague_reason = self.is_vague(text)
        
        # Extract structured data based on intent
        structured = {
            'original': text,
            'detected_intent': detected_intent,
            'expected_intent': question_intent,
            'is_off_topic': off_topic,
            'off_topic_reason': off_reason if off_topic else None,
            'is_vague': is_vague,
            'vague_reason': vague_reason if is_vague else None,
            'extracted': {}
        }
        
        # Extract based on intent
        if detected_intent == 'skills' or question_intent == 'skills':
            structured['extracted']['skills'] = self.extract_skills(text)
        
        if detected_intent == 'experience' or question_intent == 'experience':
            structured['extracted']['experience_years'] = self.extract_experience(text)
        
        if detected_intent == 'salary' or question_intent == 'salary':
            structured['extracted']['salary'] = self.extract_salary(text)
        
        if detected_intent == 'availability' or question_intent == 'availability':
            structured['extracted']['availability'] = self.extract_availability(text)
        
        # Calculate confidence
        structured['confidence'] = self.calculate_confidence(structured)
        
        return structured
    
    def calculate_confidence(self, structured):
        """Calculate confidence score for parsed answer"""
        confidence = 80  # base
        
        # Penalize off-topic
        if structured['is_off_topic']:
            confidence -= 30
        
        # Penalize vague
        if structured['is_vague']:
            confidence -= 20
        
        # Boost if extracted data found
        if structured['extracted']:
            confidence += 10
        
        # Cap between 0 and 100
        return max(0, min(100, confidence))
    
    # ========== TEST FUNCTIONS ==========
    
    def test_intent_classification(self):
        """Test intent classification"""
        print("\n" + "="*60)
        print("📋 INTENT CLASSIFICATION TEST")
        print("="*60)
        
        test_cases = [
            ("I know Python and React", "skills"),
            ("I have 3 years of experience", "experience"),
            ("I have a B.Tech in Computer Science", "education"),
            ("My expected salary is 10 lakhs", "salary"),
            ("I can join immediately", "availability"),
            ("I live in Bangalore", "location"),
            ("My notice period is 30 days", "notice_period")
        ]
        
        for text, expected in test_cases:
            detected = self.classify_intent(text)
            status = "✅" if detected == expected else "❌"
            print(f"{status} Text: '{text}'")
            print(f"   Expected: {expected} | Detected: {detected}\n")
    
    def test_extraction(self):
        """Test extraction functions"""
        print("\n" + "="*60)
        print("📋 EXTRACTION TEST")
        print("="*60)
        
        print("\nSkills Extraction:")
        print(f"  'I know Python, Java, and React' → {self.extract_skills('I know Python, Java, and React')}")
        print(f"  'I have experience with AWS and Docker' → {self.extract_skills('I have experience with AWS and Docker')}")
        
        print("\nExperience Extraction:")
        print(f"  'I have 3 years of experience' → {self.extract_experience('I have 3 years of experience')}")
        print(f"  '5 years in software development' → {self.extract_experience('5 years in software development')}")
        print(f"  'three years' → {self.extract_experience('three years')}")
        
        print("\nSalary Extraction:")
        print(f"  'I expect 8 lakhs' → {self.extract_salary('I expect 8 lakhs')}")
        print(f"  'around 12 LPA' → {self.extract_salary('around 12 LPA')}")
        
        print("\nAvailability Extraction:")
        print(f"  'I can join immediately' → {self.extract_availability('I can join immediately')}")
        print(f"  'I have 30 days notice period' → {self.extract_availability('I have 30 days notice period')}")
    
    def test_off_topic_detection(self):
        """Test off-topic detection"""
        print("\n" + "="*60)
        print("📋 OFF-TOPIC DETECTION TEST")
        print("="*60)
        
        test_cases = [
            ("I know Python", "skills", False),
            ("I like pizza", "skills", True),
            ("I have 3 years experience", "experience", False),
            ("I love movies", "experience", True)
        ]
        
        for text, intent, expected in test_cases:
            is_off, reason = self.is_off_topic(text, intent)
            status = "✅" if is_off == expected else "❌"
            print(f"{status} Text: '{text}' | Intent: {intent}")
            print(f"   Off-topic: {is_off} | Reason: {reason}\n")
    
    def test_vague_detection(self):
        """Test vague answer detection"""
        print("\n" + "="*60)
        print("📋 VAGUE ANSWER DETECTION TEST")
        print("="*60)
        
        test_cases = [
            ("I have 3 years of experience", False),
            ("I'm not sure about the years", True),
            ("Maybe around 5 years", True),
            ("I don't know", True),
            ("Yes", True)
        ]
        
        for text, expected in test_cases:
            is_vague, reason = self.is_vague(text)
            status = "✅" if is_vague == expected else "❌"
            print(f"{status} Text: '{text}'")
            print(f"   Vague: {is_vague} | Reason: {reason}\n")
    
    def test_full_pipeline(self):
        """Test complete answer parsing pipeline"""
        print("\n" + "="*60)
        print("📋 FULL PIPELINE TEST")
        print("="*60)
        
        test_cases = [
            ("I know Python and React. I have 3 years experience.", "skills"),
            ("I have 5 years of experience in data science.", "experience"),
            ("My expected salary is 12 lakhs.", "salary"),
            ("I can join in 30 days.", "availability"),
            ("I like watching movies.", "skills"),
            ("I'm not sure about salary.", "salary")
        ]
        
        for text, intent in test_cases:
            result = self.parse_answer(text, intent)
            print(f"\nQ: {intent} | A: '{text}'")
            print(f"   Detected: {result['detected_intent']}")
            print(f"   Off-topic: {result['is_off_topic']}")
            print(f"   Vague: {result['is_vague']}")
            print(f"   Extracted: {result['extracted']}")
            print(f"   Confidence: {result['confidence']}%")
    
    def generate_report(self):
        """Generate test report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'features': {
                'intent_classification': ['introduction', 'skills', 'experience', 'education', 'location', 'salary', 'notice_period', 'availability'],
                'extraction': ['skills', 'experience_years', 'salary', 'availability'],
                'detection': ['off_topic', 'vague']
            },
            'test_summary': {
                'intent_tests': 7,
                'extraction_tests': 8,
                'off_topic_tests': 4,
                'vague_tests': 5,
                'pipeline_tests': 6
            }
        }
        return report
    
    def save_report(self, report, filename='output/intent_report.json'):
        """Save report"""
        import os
        os.makedirs('output', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✅ Report saved: {filename}")

def main():
    print("="*70)
    print("DAY 25 - ANSWER INTENT & UNDERSTANDING ENGINE")
    print("="*70)
    
    engine = IntentEngine()
    
    # Run all tests
    engine.test_intent_classification()
    engine.test_extraction()
    engine.test_off_topic_detection()
    engine.test_vague_detection()
    engine.test_full_pipeline()
    
    # Generate and save report
    report = engine.generate_report()
    engine.save_report(report)
    
    print("\n" + "="*70)
    print("✅ DAY 25 COMPLETED - INTENT & UNDERSTANDING ENGINE")
    print("="*70)

if __name__ == "__main__":
    main()