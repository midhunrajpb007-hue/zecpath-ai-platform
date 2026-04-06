# hr_interview_engine.py - Day 33 HR Interview Engine Design
import json
from datetime import datetime

class HRInterviewEngine:
    def __init__(self):
        # HR Interview Categories
        self.categories = {
            'introduction': {
                'name': 'Self Introduction',
                'description': 'Candidate introduces themselves',
                'questions': []
            },
            'career_journey': {
                'name': 'Career Journey',
                'description': 'Past roles and career progression',
                'questions': []
            },
            'strengths_weaknesses': {
                'name': 'Strengths & Weaknesses',
                'description': 'Self-awareness assessment',
                'questions': []
            },
            'teamwork_culture': {
                'name': 'Teamwork & Culture Fit',
                'description': 'Collaboration and value alignment',
                'questions': []
            },
            'career_goals': {
                'name': 'Career Goals',
                'description': 'Future aspirations',
                'questions': []
            },
            'availability': {
                'name': 'Availability & Commitment',
                'description': 'Joining timeline',
                'questions': []
            }
        }
        
        # Role-based question templates
        self.question_bank = {
            'fresher_technical': {
                'introduction': [
                    "Tell me about yourself and why you chose a career in tech.",
                    "What programming languages did you learn during your studies?"
                ],
                'career_journey': [
                    "What projects did you work on during your college days?",
                    "Have you done any internships? Tell me about them."
                ],
                'strengths_weaknesses': [
                    "What are your key technical strengths?",
                    "What areas are you looking to improve?"
                ],
                'teamwork_culture': [
                    "Describe a group project you worked on.",
                    "How do you handle conflicts in a team?"
                ],
                'career_goals': [
                    "Where do you see yourself in 3 years?",
                    "What technologies are you excited to learn?"
                ],
                'availability': [
                    "When can you join if selected?",
                    "Are you willing to relocate if required?"
                ]
            },
            'experienced_technical': {
                'introduction': [
                    "Tell me about your professional journey so far.",
                    "What motivated you to apply for this role?"
                ],
                'career_journey': [
                    "Walk me through your career progression.",
                    "What was your biggest achievement in your last role?"
                ],
                'strengths_weaknesses': [
                    "What are your strongest technical skills?",
                    "What feedback have you received for improvement?"
                ],
                'teamwork_culture': [
                    "Describe a time you led a team successfully.",
                    "How do you handle disagreements with colleagues?"
                ],
                'career_goals': [
                    "What are your career aspirations?",
                    "Why are you looking for a change?"
                ],
                'availability': [
                    "What is your notice period?",
                    "Can you join immediately if required?"
                ]
            },
            'fresher_nontech': {
                'introduction': [
                    "Tell me about yourself and your background.",
                    "Why did you choose this field?"
                ],
                'career_journey': [
                    "What extracurricular activities were you part of?",
                    "Have you done any relevant certifications?"
                ],
                'strengths_weaknesses': [
                    "What are your key strengths?",
                    "What areas do you want to develop?"
                ],
                'teamwork_culture': [
                    "Tell me about a team experience you enjoyed.",
                    "How do you contribute to a positive work environment?"
                ],
                'career_goals': [
                    "What are your career goals?",
                    "Where do you see yourself in 5 years?"
                ],
                'availability': [
                    "When can you join?",
                    "Are you flexible with work location?"
                ]
            },
            'experienced_nontech': {
                'introduction': [
                    "Tell me about your professional background.",
                    "What brings you to this opportunity?"
                ],
                'career_journey': [
                    "Describe your career path so far.",
                    "What has been your most significant achievement?"
                ],
                'strengths_weaknesses': [
                    "What are your professional strengths?",
                    "What constructive feedback have you received?"
                ],
                'teamwork_culture': [
                    "Describe a challenging team situation you handled.",
                    "How do you build relationships with colleagues?"
                ],
                'career_goals': [
                    "What are your long-term career aspirations?",
                    "Why are you considering this role?"
                ],
                'availability': [
                    "What is your notice period?",
                    "When would you be available to start?"
                ]
            }
        }
    
    # ========== QUESTION GENERATOR ==========
    
    def get_questions_for_role(self, role_type, experience_level):
        """Get questions based on role type and experience level"""
        key = f"{experience_level}_{role_type}"
        return self.question_bank.get(key, self.question_bank['experienced_technical'])
    
    def get_interview_flow(self, role_type, experience_level):
        """Get complete interview flow with questions"""
        questions = self.get_questions_for_role(role_type, experience_level)
        
        flow = {
            'phase_1_introduction': {
                'purpose': 'Break ice and understand candidate background',
                'questions': questions.get('introduction', [])
            },
            'phase_2_career_journey': {
                'purpose': 'Understand professional journey',
                'questions': questions.get('career_journey', [])
            },
            'phase_3_strengths_weaknesses': {
                'purpose': 'Assess self-awareness',
                'questions': questions.get('strengths_weaknesses', [])
            },
            'phase_4_teamwork_culture': {
                'purpose': 'Evaluate collaboration skills',
                'questions': questions.get('teamwork_culture', [])
            },
            'phase_5_career_goals': {
                'purpose': 'Understand aspirations',
                'questions': questions.get('career_goals', [])
            },
            'phase_6_availability': {
                'purpose': 'Check joining timeline',
                'questions': questions.get('availability', [])
            }
        }
        
        return flow
    
    # ========== INTERVIEW STATE STRUCTURE ==========
    
    def create_interview_session(self, candidate_id, role_type, experience_level):
        """Create a new interview session with state tracking"""
        session = {
            'session_id': f"HR-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'candidate_id': candidate_id,
            'role_type': role_type,
            'experience_level': experience_level,
            'started_at': datetime.now().isoformat(),
            'current_phase': 'introduction',
            'current_question_index': 0,
            'responses': [],
            'status': 'in_progress'
        }
        return session
    
    def get_next_question(self, session):
        """Get next question based on session state"""
        flow = self.get_interview_flow(session['role_type'], session['experience_level'])
        
        phase_key = f"phase_{self._get_phase_number(session['current_phase'])}"
        
        if phase_key in flow:
            questions = flow[phase_key]['questions']
            if session['current_question_index'] < len(questions):
                question = questions[session['current_question_index']]
                return {
                    'phase': session['current_phase'],
                    'question_id': f"{session['current_phase']}_{session['current_question_index']}",
                    'question': question,
                    'question_number': session['current_question_index'] + 1,
                    'total_in_phase': len(questions)
                }
            else:
                # Move to next phase
                self._move_to_next_phase(session)
                return self.get_next_question(session)
        
        return None
    
    def _get_phase_number(self, phase):
        """Get phase number from phase name"""
        phases = ['introduction', 'career_journey', 'strengths_weaknesses', 
                  'teamwork_culture', 'career_goals', 'availability']
        if phase in phases:
            return phases.index(phase) + 1
        return 1
    
    def _move_to_next_phase(self, session):
        """Move to next phase in interview"""
        phases = ['introduction', 'career_journey', 'strengths_weaknesses', 
                  'teamwork_culture', 'career_goals', 'availability', 'closing']
        current_idx = phases.index(session['current_phase'])
        if current_idx + 1 < len(phases):
            session['current_phase'] = phases[current_idx + 1]
            session['current_question_index'] = 0
        else:
            session['status'] = 'completed'
    
    def record_response(self, session, question_id, answer):
        """Record candidate's response"""
        session['responses'].append({
            'question_id': question_id,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        session['current_question_index'] += 1
    
    # ========== GENERATE DOCUMENTATION ==========
    
    def generate_flow_diagram(self):
        """Generate interview flow diagram as text"""
        diagram = """
+==============================================================================+
|                      HR INTERVIEW FLOW DIAGRAM                               |
+==============================================================================+

                              ┌─────────────┐
                              │   START     │
                              └──────┬──────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │   PHASE 1: INTRODUCTION │
                        │ "Tell me about yourself"│
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │  PHASE 2: CAREER JOURNEY│
                        │   "Walk me through your │
                        │    career progression"  │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │ PHASE 3: STRENGTHS &    │
                        │         WEAKNESSES      │
                        │   "What are your key    │
                        │    strengths?"          │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │ PHASE 4: TEAMWORK &     │
                        │        CULTURE FIT      │
                        │   "Describe a team      │
                        │    experience"          │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │  PHASE 5: CAREER GOALS  │
                        │   "Where do you see     │
                        │    yourself in 3 years?"│
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │ PHASE 6: AVAILABILITY   │
                        │   "What is your notice  │
                        │    period?"             │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │   PHASE 7: CLOSING      │
                        │   "Thank you for your   │
                        │    time"                │
                        └────────────┬────────────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │    END      │
                              └─────────────┘
"""
        return diagram
    
    def generate_question_bank_architecture(self):
        """Generate question bank architecture document"""
        doc = """
+==============================================================================+
|                    QUESTION BANK ARCHITECTURE                                |
+==============================================================================+

1. STRUCTURE
   ==========
   question_bank/
   ├── fresher_technical/
   │   ├── introduction.json
   │   ├── career_journey.json
   │   ├── strengths_weaknesses.json
   │   ├── teamwork_culture.json
   │   ├── career_goals.json
   │   └── availability.json
   ├── experienced_technical/
   │   └── ...
   ├── fresher_nontech/
   │   └── ...
   └── experienced_nontech/
       └── ...

2. QUESTION FORMAT
   ================
   {
     "question_id": "intro_001",
     "category": "introduction",
     "text": "Tell me about yourself",
     "expected_keywords": ["background", "experience", "skills"],
     "follow_up_allowed": true,
     "max_attempts": 2
   }

3. QUESTION COUNTS BY CATEGORY
   ============================
   | Category               | Fresher | Experienced |
   |------------------------|---------|-------------|
   | Introduction           | 2       | 2           |
   | Career Journey         | 2       | 2           |
   | Strengths & Weaknesses | 2       | 2           |
   | Teamwork & Culture     | 2       | 2           |
   | Career Goals           | 2       | 2           |
   | Availability           | 2       | 2           |
   | TOTAL                  | 12      | 12          |

4. ROLE-BASED VARIATIONS
   ======================
   - Technical roles: Focus on projects, technical achievements
   - Non-tech roles: Focus on soft skills, domain knowledge
   - Fresher: Focus on education, internships, learning ability
   - Experienced: Focus on achievements, leadership, career progression
"""
        return doc
    
    def generate_interview_flow_design(self):
        """Generate interview flow design document"""
        doc = """
+==============================================================================+
|                    INTERVIEW FLOW DESIGN DOCUMENT                            |
+==============================================================================+

1. CONVERSATION PHASES
   ====================
   Phase 1: Introduction (2-3 minutes)
     - Ice breaker questions
     - Candidate background overview
   
   Phase 2: Core HR Questions (5-7 minutes)
     - Career journey exploration
     - Strengths & weaknesses assessment
   
   Phase 3: Role-based Evaluation (3-5 minutes)
     - Technical/domain specific questions
     - Culture fit assessment
   
   Phase 4: Closing (1-2 minutes)
     - Candidate questions
     - Next steps communication

2. STATE TRANSITIONS
   ==================
   START → INTRODUCTION → CAREER_JOURNEY → STRENGTHS_WEAKNESSES → 
   TEAMWORK_CULTURE → CAREER_GOALS → AVAILABILITY → CLOSING → END

3. FOLLOW-UP RULES
   ================
   - If answer is vague → Ask follow-up clarification
   - If answer is off-topic → Rephrase question
   - Max 2 follow-ups per question
   - After max attempts → Move to next question

4. RESPONSE CAPTURE
   =================
   Each response includes:
   - question_id
   - answer_text
   - confidence_score
   - timestamp
   - follow_up_used (if any)

5. SCORING CRITERIA
   =================
   - Clarity (0-100)
   - Relevance (0-100)
   - Completeness (0-100)
   - Overall score = weighted average
"""
        return doc
    
    def save_question_bank(self, filename='data/question_bank.json'):
        """Save question bank to JSON"""
        import os
        os.makedirs('data', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.question_bank, f, indent=2)
        print(f"✅ Question bank saved: {filename}")

def main():
    print("="*70)
    print("DAY 33 - HR INTERVIEW ENGINE DESIGN")
    print("="*70)
    
    engine = HRInterviewEngine()
    
    # Display HR categories
    print("\n📋 HR INTERVIEW CATEGORIES")
    print("-"*40)
    for key, cat in engine.categories.items():
        print(f"   {key}: {cat['name']} - {cat['description']}")
    
    # Display role-based questions
    print("\n📋 ROLE-BASED QUESTIONS (Sample)")
    print("-"*40)
    
    roles = [
        ('technical', 'fresher', 'Fresher - Technical'),
        ('technical', 'experienced', 'Experienced - Technical'),
        ('nontech', 'fresher', 'Fresher - Non-Tech'),
        ('nontech', 'experienced', 'Experienced - Non-Tech')
    ]
    
    for role_type, exp_level, title in roles:
        print(f"\n{title}:")
        questions = engine.get_questions_for_role(role_type, exp_level)
        for category, q_list in questions.items():
            if q_list:
                print(f"   {category}: {q_list[0][:60]}...")
    
    # Simulate interview session
    print("\n" + "="*70)
    print("🎙️ SIMULATED INTERVIEW SESSION")
    print("="*70)
    
    session = engine.create_interview_session("C001", "technical", "experienced")
    print(f"\nSession ID: {session['session_id']}")
    print(f"Candidate: {session['candidate_id']}")
    print(f"Role: {session['role_type']} | Level: {session['experience_level']}")
    
    # Simulate asking questions
    print("\n📝 Interview Questions:")
    for i in range(8):  # Get first 8 questions
        next_q = engine.get_next_question(session)
        if next_q:
            print(f"\nQ{next_q['question_number']} ({next_q['phase']}): {next_q['question']}")
            # Simulate answer
            answer = "I have relevant experience in this area."
            engine.record_response(session, next_q['question_id'], answer)
            print(f"   Answer recorded: {answer[:50]}...")
    
    print(f"\n✅ Interview Status: {session['status']}")
    print(f"✅ Responses recorded: {len(session['responses'])}")
    
    # Generate documentation
    print("\n" + engine.generate_flow_diagram())
    print(engine.generate_question_bank_architecture())
    print(engine.generate_interview_flow_design())
    
    # Save question bank
    engine.save_question_bank()
    
    print("\n" + "="*70)
    print("✅ DAY 33 COMPLETED - HR INTERVIEW ENGINE DESIGN")
    print("="*70)

if __name__ == "__main__":
    main()