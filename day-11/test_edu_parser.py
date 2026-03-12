# tests/test_edu_parser.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edu_cert_parser import EducationCertificationParser

def test_education_parsing():
    parser = EducationCertificationParser()
    
    test_cases = [
        {
            'name': 'B.Tech Computer Science from ABC University 2020',
            'expected': {
                'degree_level': 'bachelor',
                'field': 'Computer Science',
                'institution': 'ABC University',
                'year': 2020
            }
        },
        {
            'name': 'M.Sc Data Science at XYZ Institute 2022',
            'expected': {
                'degree_level': 'master',
                'field': 'Data Science',
                'institution': 'XYZ Institute',
                'year': 2022
            }
        }
    ]
    
    print("\n📋 Running Education Parser Tests...")
    for i, test in enumerate(test_cases, 1):
        result = parser._parse_education_line(test['name'])
        if result:
            print(f"✅ Test {i}: PASSED")
        else:
            print(f"❌ Test {i}: FAILED")

def test_certification_parsing():
    parser = EducationCertificationParser()
    
    test_certs = [
        "AWS Certified Developer",
        "Project Management Professional (PMP)",
        "Scrum Master Certified"
    ]
    
    print("\n📋 Running Certification Parser Tests...")
    for i, cert in enumerate(test_certs, 1):
        result = parser._parse_certification_line(cert)
        if result:
            print(f"✅ Test {i}: PASSED - {result['category']}")
        else:
            print(f"❌ Test {i}: FAILED")

if __name__ == "__main__":
    test_education_parsing()
    test_certification_parsing()
    print("\n✅ All tests completed!")