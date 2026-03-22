# question_bank_creator.py - Day 22 HR Screening Dataset
import json
import csv
import os

# Question categories
categories = {
    'introduction': 'Basic intro questions',
    'education': 'Educational background',
    'experience': 'Work experience details',
    'skills': 'Technical and soft skills',
    'location': 'Work location preferences',
    'salary': 'Salary expectations',
    'notice_period': 'Notice period details'
}

# Questions for different roles
questions = []

# Role: Software Engineer
software_questions = [
    {
        'role': 'Software Engineer',
        'category': 'introduction',
        'question': 'Tell me about yourself and your career background.',
        'answer_type': 'free_text',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Software Engineer',
        'category': 'education',
        'question': 'What is your highest educational qualification?',
        'answer_type': 'text',
        'mandatory': True,
        'score_importance': 'medium'
    },
    {
        'role': 'Software Engineer',
        'category': 'experience',
        'question': 'How many years of experience do you have in software development?',
        'answer_type': 'number',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Software Engineer',
        'category': 'skills',
        'question': 'What programming languages and frameworks are you proficient in?',
        'answer_type': 'list',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Software Engineer',
        'category': 'location',
        'question': 'Are you willing to relocate if required?',
        'answer_type': 'yes_no',
        'mandatory': False,
        'score_importance': 'low'
    },
    {
        'role': 'Software Engineer',
        'category': 'salary',
        'question': 'What is your expected annual salary?',
        'answer_type': 'number',
        'mandatory': False,
        'score_importance': 'medium'
    },
    {
        'role': 'Software Engineer',
        'category': 'notice_period',
        'question': 'What is your current notice period?',
        'answer_type': 'text',
        'mandatory': True,
        'score_importance': 'medium'
    }
]

# Role: Data Scientist
ds_questions = [
    {
        'role': 'Data Scientist',
        'category': 'introduction',
        'question': 'Tell me about your background in data science.',
        'answer_type': 'free_text',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Data Scientist',
        'category': 'education',
        'question': 'What is your educational background?',
        'answer_type': 'text',
        'mandatory': True,
        'score_importance': 'medium'
    },
    {
        'role': 'Data Scientist',
        'category': 'experience',
        'question': 'How many years of experience in data science?',
        'answer_type': 'number',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Data Scientist',
        'category': 'skills',
        'question': 'Which tools and technologies do you use for data analysis?',
        'answer_type': 'list',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Data Scientist',
        'category': 'location',
        'question': 'Are you open to working from office?',
        'answer_type': 'yes_no',
        'mandatory': False,
        'score_importance': 'low'
    },
    {
        'role': 'Data Scientist',
        'category': 'salary',
        'question': 'What is your expected salary range?',
        'answer_type': 'text',
        'mandatory': False,
        'score_importance': 'medium'
    },
    {
        'role': 'Data Scientist',
        'category': 'notice_period',
        'question': 'What is your notice period?',
        'answer_type': 'text',
        'mandatory': True,
        'score_importance': 'medium'
    }
]

# Role: Marketing Manager
marketing_questions = [
    {
        'role': 'Marketing Manager',
        'category': 'introduction',
        'question': 'Tell me about your marketing experience.',
        'answer_type': 'free_text',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Marketing Manager',
        'category': 'education',
        'question': 'What is your educational qualification?',
        'answer_type': 'text',
        'mandatory': True,
        'score_importance': 'medium'
    },
    {
        'role': 'Marketing Manager',
        'category': 'experience',
        'question': 'How many years of experience in marketing?',
        'answer_type': 'number',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Marketing Manager',
        'category': 'skills',
        'question': 'Which marketing tools and platforms have you used?',
        'answer_type': 'list',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Marketing Manager',
        'category': 'location',
        'question': 'Are you willing to travel for work?',
        'answer_type': 'yes_no',
        'mandatory': False,
        'score_importance': 'low'
    },
    {
        'role': 'Marketing Manager',
        'category': 'salary',
        'question': 'What is your expected salary?',
        'answer_type': 'number',
        'mandatory': False,
        'score_importance': 'medium'
    },
    {
        'role': 'Marketing Manager',
        'category': 'notice_period',
        'question': 'What is your notice period?',
        'answer_type': 'text',
        'mandatory': True,
        'score_importance': 'medium'
    }
]

# Role: Fresher
fresher_questions = [
    {
        'role': 'Fresher',
        'category': 'introduction',
        'question': 'Tell me about yourself.',
        'answer_type': 'free_text',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Fresher',
        'category': 'education',
        'question': 'What is your educational background?',
        'answer_type': 'text',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Fresher',
        'category': 'skills',
        'question': 'What technical skills do you have?',
        'answer_type': 'list',
        'mandatory': True,
        'score_importance': 'high'
    },
    {
        'role': 'Fresher',
        'category': 'location',
        'question': 'Are you willing to relocate?',
        'answer_type': 'yes_no',
        'mandatory': False,
        'score_importance': 'low'
    },
    {
        'role': 'Fresher',
        'category': 'salary',
        'question': 'What is your salary expectation?',
        'answer_type': 'number',
        'mandatory': False,
        'score_importance': 'medium'
    },
    {
        'role': 'Fresher',
        'category': 'notice_period',
        'question': 'When can you join if selected?',
        'answer_type': 'text',
        'mandatory': True,
        'score_importance': 'high'
    }
]

# Combine all questions
all_questions = software_questions + ds_questions + marketing_questions + fresher_questions

print("="*60)
print("DAY 22 - HR SCREENING DATASET")
print("="*60)

# Save as JSON
os.makedirs('data', exist_ok=True)
json_file = 'data/hr_screening_questions.json'
with open(json_file, 'w') as f:
    json.dump(all_questions, f, indent=2)
print(f"✅ JSON saved: {json_file} ({len(all_questions)} questions)")

# Save as CSV
csv_file = 'data/hr_screening_questions.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['role', 'category', 'question', 'answer_type', 'mandatory', 'score_importance'])
    for q in all_questions:
        writer.writerow([q['role'], q['category'], q['question'], q['answer_type'], q['mandatory'], q['score_importance']])
print(f"✅ CSV saved: {csv_file}")

# Category mapping
category_map = {
    'introduction': {'description': 'Basic intro questions', 'mandatory_count': 4, 'total_count': 4},
    'education': {'description': 'Educational background', 'mandatory_count': 4, 'total_count': 4},
    'experience': {'description': 'Work experience', 'mandatory_count': 3, 'total_count': 3},
    'skills': {'description': 'Technical skills', 'mandatory_count': 4, 'total_count': 4},
    'location': {'description': 'Location preference', 'mandatory_count': 0, 'total_count': 4},
    'salary': {'description': 'Salary expectation', 'mandatory_count': 0, 'total_count': 4},
    'notice_period': {'description': 'Notice period', 'mandatory_count': 4, 'total_count': 4}
}

# Save category mapping
cat_file = 'data/category_mapping.json'
with open(cat_file, 'w') as f:
    json.dump(category_map, f, indent=2)
print(f"✅ Category mapping saved: {cat_file}")

# AI conversation-ready question objects
ai_questions = []
for q in all_questions:
    ai_q = {
        'id': f"q_{q['role'].replace(' ', '_').lower()}_{q['category']}",
        'text': q['question'],
        'type': q['answer_type'],
        'required': q['mandatory'],
        'weight': 1 if q['score_importance'] == 'high' else 0.5 if q['score_importance'] == 'medium' else 0.2,
        'category': q['category']
    }
    ai_questions.append(ai_q)

ai_file = 'data/ai_conversation_questions.json'
with open(ai_file, 'w') as f:
    json.dump(ai_questions, f, indent=2)
print(f"✅ AI conversation-ready questions saved: {ai_file}")

# Summary
print("\n" + "="*60)
print("📊 SUMMARY")
print("="*60)
print(f"Total questions: {len(all_questions)}")
print(f"Roles covered: 4 (Software Engineer, Data Scientist, Marketing Manager, Fresher)")
print(f"Categories: 7 (introduction, education, experience, skills, location, salary, notice_period)")
print("\n📋 QUESTIONS BY ROLE:")
roles_count = {}
for q in all_questions:
    roles_count[q['role']] = roles_count.get(q['role'], 0) + 1
for role, count in roles_count.items():
    print(f"   {role}: {count} questions")
print("\n📋 QUESTIONS BY CATEGORY:")
cats_count = {}
for q in all_questions:
    cats_count[q['category']] = cats_count.get(q['category'], 0) + 1
for cat, count in cats_count.items():
    print(f"   {cat}: {count} questions")
print("\n" + "="*60)
print("✅ DAY 22 COMPLETED")
print("="*60)