# edu_cert_parser.py - COMPLETE FIXED VERSION
import re
import json
import os
from datetime import datetime

class EducationCertificationParser:
    def __init__(self):
        # Degree patterns
        self.degree_patterns = {
            'bachelor': ['b.tech', 'b.e', 'b.sc', 'bachelor', 'b.com', 'ba', 'bca'],
            'master': ['m.tech', 'm.e', 'm.sc', 'master', 'm.com', 'mba', 'mca'],
            'doctorate': ['ph.d', 'doctorate', 'phd'],
            'diploma': ['diploma', 'pg diploma'],
            'higher_secondary': ['12th', 'hsc', 'intermediate'],
            'secondary': ['10th', 'ssc', 'matriculation']
        }
        
        # Field of study keywords
        self.field_keywords = {
            'computer_science': ['computer science', 'cs', 'cse', 'information technology', 'it', 'software'],
            'electronics': ['electronics', 'ece', 'electrical', 'eee'],
            'mechanical': ['mechanical', 'mech'],
            'civil': ['civil'],
            'business': ['business', 'management', 'mba', 'finance', 'marketing', 'hr'],
            'science': ['physics', 'chemistry', 'mathematics', 'maths', 'statistics'],
            'arts': ['english', 'history', 'economics', 'psychology']
        }
        
        # Certification patterns
        self.cert_patterns = {
            'aws': ['aws certified', 'amazon web services'],
            'google': ['google certified', 'gcp', 'google cloud'],
            'microsoft': ['microsoft certified', 'azure', 'ms certified'],
            'pmp': ['pmp', 'project management professional'],
            'scrum': ['scrum master', 'agile certified', 'csm'],
            'security': ['ceh', 'cissp', 'security+', 'network+'],
            'data_science': ['data science', 'machine learning', 'ai certified', 'tensorflow'],
            'language': ['ielts', 'toefl', 'german', 'french']
        }
    
    # Helper method to extract degree name
    def _extract_degree_name(self, line, pattern):
        """Extract full degree name from line"""
        words = line.split()
        
        for i, word in enumerate(words):
            if pattern in word.lower():
                end = min(len(words), i + 3)
                return ' '.join(words[i:end])
        return pattern.title()
    
    # Extract education section
    def _extract_section(self, text, keywords):
        """Extract specific section from resume"""
        lines = text.split('\n')
        in_section = False
        section_lines = []
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check if this line starts a section
            for keyword in keywords:
                if keyword in line_lower and len(line_lower.split()) < 6:
                    in_section = True
                    continue
            
            # Check if next section starts
            if in_section and i > 0:
                next_line = lines[i-1].lower() if i-1 >= 0 else ''
                for end_keyword in ['experience', 'skills', 'projects', 'work', 'certification']:
                    if end_keyword in next_line and len(next_line.split()) < 6:
                        in_section = False
                        break
            
            if in_section and line.strip() and len(line.strip()) > 3:
                section_lines.append(line.strip())
        
        return '\n'.join(section_lines) if section_lines else None
    
    # Parse single education line
    def _parse_education_line(self, line):
        """Parse one line of education"""
        line_lower = line.lower()
        entry = {}
        
        # Skip if too short
        if len(line.split()) < 2:
            return None
        
        # Find degree
        for level, patterns in self.degree_patterns.items():
            for pattern in patterns:
                if pattern in line_lower:
                    entry['degree_level'] = level
                    entry['degree'] = self._extract_degree_name(line, pattern)
                    break
        
        # Find field
        for field, keywords in self.field_keywords.items():
            for keyword in keywords:
                if keyword in line_lower:
                    entry['field'] = field.replace('_', ' ').title()
                    break
        
        # Find institution
        inst_words = ['university', 'college', 'institute', 'school']
        words = line.split()
        for i, word in enumerate(words):
            if any(inst in word.lower() for inst in inst_words):
                start = max(0, 0)
                end = min(len(words), i + 2)
                entry['institution'] = ' '.join(words[start:end])
                break
        
        # Find year
        year_match = re.search(r'\b(19|20)\d{2}\b', line)
        if year_match:
            entry['year'] = int(year_match.group())
        
        # Return only if we have meaningful data
        if entry.get('degree') or entry.get('year') or entry.get('institution'):
            return entry
        return None
    
    # Main education parser
    def parse_education(self, text):
        """Extract all education entries"""
        education = []
        edu_section = self._extract_section(text, ['education', 'academic', 'qualification'])
        
        if edu_section:
            lines = edu_section.split('\n')
            for line in lines:
                if line.strip():
                    edu = self._parse_education_line(line)
                    if edu and edu not in education:
                        education.append(edu)
        return education
    
    # Parse certification line
    def _parse_certification_line(self, line):
        """Parse one certification line"""
        line_lower = line.lower()
        
        for category, patterns in self.cert_patterns.items():
            for pattern in patterns:
                if pattern in line_lower:
                    return {
                        'name': line.strip(),
                        'category': category.upper(),
                        'confidence': 85
                    }
        return None
    
    # Main certification parser
    def parse_certifications(self, text):
        """Extract all certifications"""
        certs = []
        cert_section = self._extract_section(text, ['certification', 'certificate', 'professional'])
        
        if cert_section:
            lines = cert_section.split('\n')
            for line in lines:
                if line.strip():
                    cert = self._parse_certification_line(line)
                    if cert and cert not in certs:
                        certs.append(cert)
        
        # Remove duplicates by name
        unique = []
        seen = set()
        for cert in certs:
            if cert['name'] not in seen:
                seen.add(cert['name'])
                unique.append(cert)
        
        return unique
    
    # Normalize education
    def normalize_education(self, education_list):
        """Clean and standardize education entries"""
        normalized = []
        for edu in education_list:
            clean = {}
            if 'degree' in edu:
                clean['degree'] = edu['degree'].title()
            if 'field' in edu:
                clean['field'] = edu['field']
            if 'institution' in edu:
                clean['institution'] = ' '.join(edu['institution'].split()).title()
            if 'year' in edu:
                clean['year'] = edu['year']
            if 'degree_level' in edu:
                clean['level'] = edu['degree_level'].title()
            if clean:
                normalized.append(clean)
        return normalized
    
    # Calculate relevance score
    def calculate_relevance(self, education, target_role):
        """Score education relevance for target role"""
        if not education:
            return 0
        
        weights = {
            'computer_science': 1.0,
            'electronics': 0.8,
            'mechanical': 0.6,
            'civil': 0.5,
            'business': 0.7,
            'science': 0.6,
            'arts': 0.4
        }
        
        total = 0
        for edu in education:
            field = edu.get('field', '').lower().replace(' ', '_')
            total += weights.get(field, 0.3)
        
        return min(round((total / len(education)) * 100), 100)
    
    # Main parse function
    def parse_resume(self, text, target_role=None):
        """Parse complete resume for education and certifications"""
        education = self.parse_education(text)
        certifications = self.parse_certifications(text)
        
        normalized_edu = self.normalize_education(education)
        relevance = self.calculate_relevance(normalized_edu, target_role) if target_role else None
        
        return {
            'education': normalized_edu,
            'certifications': certifications,
            'relevance_score': relevance,
            'metadata': {
                'parsed_at': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
    
    # Save to JSON
    def save_output(self, data, filename):
        """Save parsed data to JSON file"""
        os.makedirs('output', exist_ok=True)
        path = f'output/{filename}'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return path

def main():
    print("=" * 60)
    print("DAY 11 - EDUCATION & CERTIFICATION PARSING")
    print("=" * 60)
    
    # Sample resume
    sample = """
    EDUCATION
    B.Tech Computer Science, ABC University, 2020
    M.Sc Data Science, XYZ Institute, 2022
    
    CERTIFICATIONS
    AWS Certified Developer Associate
    Google Cloud Fundamentals
    Project Management Professional (PMP)
    Scrum Master Certified
    """
    
    print("\n📄 Processing sample resume...")
    
    parser = EducationCertificationParser()
    result = parser.parse_resume(sample, target_role="Data Scientist")
    
    print("\n✅ PARSED EDUCATION:")
    for i, edu in enumerate(result['education'], 1):
        print(f"\n   {i}. {edu.get('degree', 'N/A')}")
        print(f"      Field: {edu.get('field', 'N/A')}")
        print(f"      Institution: {edu.get('institution', 'N/A')}")
        print(f"      Year: {edu.get('year', 'N/A')}")
        print(f"      Level: {edu.get('level', 'N/A')}")
    
    print(f"\n✅ CERTIFICATIONS: {len(result['certifications'])}")
    for cert in result['certifications']:
        print(f"   • {cert['name']} ({cert['category']})")
    
    if result['relevance_score']:
        print(f"\n📊 RELEVANCE SCORE: {result['relevance_score']}%")
    
    # Save
    filename = f"edu_cert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    saved = parser.save_output(result, filename)
    print(f"\n💾 Saved: {saved}")
    
    print("\n" + "=" * 60)
    print("✅ DAY 11 COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()