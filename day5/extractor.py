#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RESUME TEXT EXTRACTION ENGINE
Day 5 Task - Complete Working Implementation
"""

import os
import re
from datetime import datetime

print("="*70)
print("RESUME TEXT EXTRACTION ENGINE")
print("Day 5 Task Implementation")
print("="*70)

def create_sample_resume():
    """Create a sample resume if none exists"""
    sample_dir = "test_resumes"
    os.makedirs(sample_dir, exist_ok=True)
    
    sample_file = os.path.join(sample_dir, "sample_resume.txt")
    
    sample_content = """JOHN DOE
Software Developer

CONTACT INFORMATION:
Email: john.doe@example.com
Phone: (123) 456-7890
Location: San Francisco, CA
LinkedIn: linkedin.com/in/johndoe

PROFESSIONAL SUMMARY:
Experienced software developer with 5+ years in full-stack web development.
Proficient in Python, JavaScript, and cloud technologies. Strong problem-solving
skills and experience in Agile development environments.

TECHNICAL SKILLS:
• Programming Languages: Python, JavaScript, Java, SQL
• Web Technologies: HTML5, CSS3, React.js, Node.js, Express.js
• Databases: MySQL, MongoDB, PostgreSQL
• Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, Git
• Tools: VS Code, Postman, JIRA, Confluence

WORK EXPERIENCE:

Senior Software Developer
Tech Solutions Inc., San Francisco, CA | Jan 2021 - Present
- Led development of customer-facing web applications using React and Node.js
- Implemented RESTful APIs that served 10,000+ daily requests
- Improved application performance by 40% through code optimization
- Mentored 3 junior developers and conducted code reviews
- Collaborated with cross-functional teams using Agile/Scrum methodology

Software Developer
Innovate Startups, Seattle, WA | Jun 2018 - Dec 2020
- Developed and maintained multiple web applications using Python/Django
- Integrated third-party APIs including payment gateways and SMS services
- Reduced server costs by 25% through AWS optimization
- Implemented automated testing, increasing code coverage to 85%

EDUCATION:

Bachelor of Science in Computer Science
University of California, Berkeley | 2014 - 2018
- GPA: 3.8/4.0
- Relevant Coursework: Data Structures, Algorithms, Database Systems
- Senior Project: Developed a machine learning-based recommendation system

CERTIFICATIONS:
- AWS Certified Solutions Architect - Associate (2022)
- Microsoft Azure Fundamentals (2021)
- Google Cloud Professional Developer (2020)

PROJECTS:

E-Commerce Platform (MERN Stack)
- Developed full-featured e-commerce website with React frontend and Node.js backend
- Implemented user authentication, product catalog, shopping cart, and payment processing
- Used MongoDB for database and Redux for state management

Task Management Application
- Created productivity app with real-time collaboration features
- Implemented using Socket.io for live updates
- Features: Task assignment, progress tracking, file attachments

LANGUAGES:
- English (Native)
- Spanish (Professional Proficiency)

AVAILABILITY:
- Immediate
- Open to relocation
- Available for full-time positions"""
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    return sample_file

def extract_text_from_file(filepath):
    """Extract and clean text from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Store original for comparison
        original_length = len(content)
        
        # CLEANING PROCESS
        cleaned = content
        
        # 1. Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        # 2. Protect privacy - mask emails and phones
        cleaned = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL_PROTECTED]', cleaned)
        cleaned = re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '[PHONE_PROTECTED]', cleaned)
        
        # 3. Standardize section headers
        sections = {
            r'\b(contact information|contact details|contact)\b': 'CONTACT INFORMATION',
            r'\b(professional summary|summary|objective)\b': 'PROFESSIONAL SUMMARY',
            r'\b(technical skills|skills|key skills)\b': 'TECHNICAL SKILLS',
            r'\b(work experience|experience|employment history)\b': 'WORK EXPERIENCE',
            r'\b(education|academic background|qualifications)\b': 'EDUCATION',
            r'\b(certifications|certificate|courses)\b': 'CERTIFICATIONS',
            r'\b(projects|personal projects|project experience)\b': 'PROJECTS',
            r'\b(languages|language skills)\b': 'LANGUAGES'
        }
        
        for pattern, replacement in sections.items():
            cleaned = re.sub(pattern, f'\n{replacement}:\n', cleaned, flags=re.IGNORECASE)
        
        # 4. Standardize bullet points
        cleaned = re.sub(r'[•·▪➢➤\-]\s*', '\n• ', cleaned)
        
        # 5. Clean special characters
        cleaned = re.sub(r'[^\w\s\.,\-\•\:\n\(\)\@]', ' ', cleaned)
        
        # 6. Fix multiple newlines
        cleaned = re.sub(r'\n\s*\n+', '\n\n', cleaned)
        
        cleaned_length = len(cleaned)
        
        return {
            'filename': os.path.basename(filepath),
            'original': content,
            'cleaned': cleaned,
            'original_length': original_length,
            'cleaned_length': cleaned_length,
            'reduction': original_length - cleaned_length
        }
        
    except Exception as e:
        print(f"  ❌ Error reading {filepath}: {e}")
        return None

def main():
    """Main function"""
    # Create output directory
    output_dir = "extraction_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Check test_resumes directory
    input_dir = "test_resumes"
    
    if not os.path.exists(input_dir):
        print(f"\n📁 '{input_dir}' folder not found.")
        print("Creating sample resume for demonstration...")
        sample_file = create_sample_resume()
        print(f"✅ Created sample: {sample_file}")
        input_dir = "test_resumes"
    
    # Get all text files
    text_files = []
    for file in os.listdir(input_dir):
        if file.lower().endswith('.txt'):
            text_files.append(os.path.join(input_dir, file))
    
    if not text_files:
        print(f"\n⚠️ No text files found in '{input_dir}'")
        print("Please add .txt files with resume content")
        return
    
    print(f"\n🔍 Found {len(text_files)} text file(s) to process")
    
    results = []
    
    # Process each file
    for filepath in text_files:
        filename = os.path.basename(filepath)
        print(f"\n📄 Processing: {filename}")
        
        result = extract_text_from_file(filepath)
        
        if result:
            # Save cleaned output
            output_file = os.path.join(output_dir, f"cleaned_{filename}")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"RESUME TEXT EXTRACTION OUTPUT\n")
                f.write("="*60 + "\n\n")
                f.write(f"Original file: {filename}\n")
                f.write(f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Original size: {result['original_length']} characters\n")
                f.write(f"Cleaned size: {result['cleaned_length']} characters\n")
                f.write(f"Reduction: {result['reduction']} characters ({result['reduction']/result['original_length']*100:.1f}%)\n")
                f.write("="*60 + "\n\n")
                f.write(result['cleaned'])
            
            print(f"  ✅ Original: {result['original_length']} chars")
            print(f"  ✅ Cleaned: {result['cleaned_length']} chars")
            print(f"  ✅ Reduction: {result['reduction']} chars ({result['reduction']/result['original_length']*100:.1f}%)")
            print(f"  💾 Saved to: {output_file}")
            
            results.append(result)
    
    # Generate report
    if results:
        report_file = os.path.join(output_dir, "EXTRACTION_REPORT.txt")
        
        total_original = sum(r['original_length'] for r in results)
        total_cleaned = sum(r['cleaned_length'] for r in results)
        total_reduction = total_original - total_cleaned
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("RESUME TEXT EXTRACTION ENGINE - PROCESSING REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total files processed: {len(results)}\n\n")
            
            f.write("SUMMARY:\n")
            f.write("-"*70 + "\n")
            f.write(f"{'Filename':<30} {'Original':<12} {'Cleaned':<12} {'Reduction':<12} {'%':<6}\n")
            f.write("-"*70 + "\n")
            
            for result in results:
                reduction_pct = (result['reduction'] / result['original_length']) * 100
                f.write(f"{result['filename'][:28]:<30} ")
                f.write(f"{result['original_length']:<12} ")
                f.write(f"{result['cleaned_length']:<12} ")
                f.write(f"{result['reduction']:<12} ")
                f.write(f"{reduction_pct:<6.1f}\n")
            
            f.write("-"*70 + "\n")
            f.write(f"{'TOTAL':<30} {total_original:<12} {total_cleaned:<12} {total_reduction:<12} {(total_reduction/total_original*100):<6.1f}\n\n")
            
            f.write("TEXT CLEANING PROCESS APPLIED:\n")
            f.write("-"*70 + "\n")
            f.write("1. Extra whitespace removal\n")
            f.write("2. Privacy protection (email/phone masking)\n")
            f.write("3. Section header standardization\n")
            f.write("4. Bullet point normalization\n")
            f.write("5. Special character cleaning\n")
            f.write("6. Formatting normalization\n\n")
            
            f.write("OUTPUT FILES:\n")
            f.write("-"*70 + "\n")
            for result in results:
                f.write(f"• cleaned_{result['filename']}\n")
            f.write(f"• EXTRACTION_REPORT.txt\n")
        
        print("\n" + "="*70)
        print("📊 PROCESSING COMPLETE!")
        print("="*70)
        
        print(f"\n📁 Output folder: {output_dir}/")
        print(f"📄 Report file: {report_file}")
        
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"   Total files: {len(results)}")
        print(f"   Total characters processed: {total_original:,}")
        print(f"   Total after cleaning: {total_cleaned:,}")
        print(f"   Total reduction: {total_reduction:,} characters ({(total_reduction/total_original*100):.1f}%)")
        
        # Show sample of cleaned text
        if results:
            sample = results[0]['cleaned']
            preview = sample[:300] + "..." if len(sample) > 300 else sample
            print(f"\n📋 SAMPLE CLEANED OUTPUT:")
            print("-"*50)
            print(preview)
            print("-"*50)
    
    print("\n" + "="*70)
    print("✅ DAY 5 TASK - RESUME TEXT EXTRACTION ENGINE")
    print("   Implementation Completed Successfully!")
    print("="*70)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()