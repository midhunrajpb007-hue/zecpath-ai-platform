# follow_up_engine.py - Day 34 Dynamic Follow-Up Logic (Fixed)
import re
import json
import os
from datetime import datetime

class FollowUpEngine:
    def __init__(self):
        # Vague answer indicators
        self.vague_phrases = [
            'not sure', 'i don\'t know', 'maybe', 'probably', 
            'i think', 'some', 'around', 'approximately', 'kind of'
        ]
        # Keywords that indicate confidence
        self.confident_keywords = ['definitely', 'absolutely', 'sure', 'yes', 'always', 'strongly']
        # Store conversation state
        self.conversation_state = {}
        self.asked_questions = {}  # track per question type to avoid repetition
    
    # ========== VAGUE/INCOMPLETE DETECTION ==========
    
    def is_vague(self, answer):
        """Check if answer is vague or incomplete"""
        answer_lower = answer.lower()
        # Check vague phrases
        for phrase in self.vague_phrases:
            if phrase in answer_lower:
                return True, f"Vague phrase: '{phrase}'"
        # Very short answer (threshold lowered to 3 words)
        if len(answer.split()) < 3:
            return True, "Answer too short (less than 3 words)"
        # Lacks specific details
        if 'year' not in answer_lower and 'experience' not in answer_lower and 'skill' not in answer_lower:
            if len(answer.split()) < 10:
                return True, "Lacks specific details"
        return False, "Clear answer"
    
    def is_confident(self, answer):
        """Check if answer shows confidence"""
        answer_lower = answer.lower()
        for kw in self.confident_keywords:
            if kw in answer_lower:
                return True
        # Long and detailed answer also indicates confidence
        if len(answer.split()) > 15:
            return True
        return False
    
    # ========== FOLLOW-UP TRIGGERS ==========
    
    def get_followup_type(self, answer, question_category):
        """Determine what type of follow-up to use"""
        is_vague, reason = self.is_vague(answer)
        if is_vague:
            return 'clarification', reason
        # If answer is confident and detailed, go deeper
        if self.is_confident(answer):
            return 'deepening', "Confident answer – ask scenario-based"
        # Otherwise, simple answer but not vague – ask example-based
        return 'example', "Simple but clear – ask for example"
    
    def generate_followup(self, question_category, followup_type, original_question):
        """Generate appropriate follow-up question"""
        if followup_type == 'clarification':
            return f"Could you please clarify? {original_question}"
        elif followup_type == 'deepening':
            if 'experience' in question_category:
                return "Can you describe a specific challenge you faced and how you solved it?"
            elif 'skills' in question_category:
                return "Tell me about a project where you used those skills effectively."
            else:
                return "Could you give me a more detailed example?"
        else:  # example-based
            if 'experience' in question_category:
                return "Can you share an example from your work experience?"
            elif 'skills' in question_category:
                return "Can you give an example of how you applied that skill?"
            else:
                return "Can you provide a specific example?"
    
    # ========== DIFFICULTY ADAPTATION ==========
    
    def adapt_difficulty(self, answer, question_category):
        """Decide next question difficulty based on answer quality"""
        if self.is_confident(answer) and not self.is_vague(answer)[0]:
            return 'advanced'
        elif self.is_vague(answer)[0]:
            return 'basic'
        else:
            return 'medium'
    
    # ========== STATE TRACKING ==========
    
    def init_session(self, candidate_id):
        """Initialize conversation state for a candidate"""
        self.conversation_state[candidate_id] = {
            'candidate_id': candidate_id,
            'started_at': datetime.now().isoformat(),
            'questions_asked': [],
            'followups_used': 0,          # fixed: counter added
            'current_difficulty': 'medium',
            'answers': []
        }
        self.asked_questions[candidate_id] = set()
        return self.conversation_state[candidate_id]
    
    def record_interaction(self, candidate_id, question, answer, followup_type=None):
        """Record question-answer pair"""
        state = self.conversation_state.get(candidate_id)
        if state:
            state['answers'].append({
                'question': question,
                'answer': answer,
                'followup_type': followup_type,
                'timestamp': datetime.now().isoformat()
            })
            self.asked_questions[candidate_id].add(question)
            # Increment follow-up count if this is a follow-up question
            if followup_type:
                state['followups_used'] = state.get('followups_used', 0) + 1
    
    def has_question_been_asked(self, candidate_id, question):
        """Check if same question already asked"""
        return question in self.asked_questions.get(candidate_id, set())
    
    # ========== MAIN PROCESSING ==========
    
    def process_answer(self, candidate_id, question_category, original_question, answer):
        """Main entry: process answer and return next action"""
        # Ensure session exists
        if candidate_id not in self.conversation_state:
            self.init_session(candidate_id)
        
        # Record the answer (without followup_type yet)
        self.record_interaction(candidate_id, original_question, answer)
        
        # Check if answer is vague/incomplete
        is_vague, reason = self.is_vague(answer)
        if is_vague:
            # Prevent repetitive questioning: if already asked same follow-up, skip
            followup = self.generate_followup(question_category, 'clarification', original_question)
            if self.has_question_been_asked(candidate_id, followup):
                # Already asked clarification, move on
                return {'action': 'next_question', 'message': 'Moving to next question', 'followup': None}
            else:
                self.asked_questions[candidate_id].add(followup)
                # Record the follow-up as an interaction (optional)
                self.record_interaction(candidate_id, followup, "[follow-up question]", followup_type='clarification')
                return {'action': 'ask_followup', 'followup': followup, 'reason': reason}
        
        # Determine follow-up type
        followup_type = self.get_followup_type(answer, question_category)[0]
        if followup_type != 'clarification':  # for confident answers, ask deepening/example
            followup = self.generate_followup(question_category, followup_type, original_question)
            if not self.has_question_been_asked(candidate_id, followup):
                self.asked_questions[candidate_id].add(followup)
                # Record follow-up interaction
                self.record_interaction(candidate_id, followup, "[follow-up question]", followup_type=followup_type)
                return {'action': 'ask_followup', 'followup': followup, 'reason': f'{followup_type} follow-up'}
        
        # Otherwise, move to next question
        return {'action': 'next_question', 'message': 'Answer sufficient, moving to next', 'followup': None}
    
    def get_state_summary(self, candidate_id):
        """Get current conversation state for reporting"""
        return self.conversation_state.get(candidate_id, {})

def main():
    print("="*70)
    print("DAY 34 - DYNAMIC FOLLOW-UP LOGIC")
    print("="*70)
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    engine = FollowUpEngine()
    
    # Sample conversation
    candidate_id = "C001"
    engine.init_session(candidate_id)
    
    test_cases = [
        ("experience", "How many years of experience do you have?", "I have some experience"),
        ("skills", "What are your technical skills?", "Python, React, SQL"),
        ("experience", "Tell me about a challenging project", "I once worked on a large e-commerce platform and optimized database queries."),
        ("skills", "How confident are you in Python?", "I'm very confident, I use it daily for backend development."),
        ("experience", "Describe your leadership experience", "I don't know, maybe a little")
    ]
    
    print("\n📋 SIMULATED CONVERSATION WITH FOLLOW-UP")
    print("-"*50)
    
    for cat, question, answer in test_cases:
        print(f"\nQ: {question}")
        print(f"A: {answer}")
        result = engine.process_answer(candidate_id, cat, question, answer)
        if result['action'] == 'ask_followup':
            print(f"🤖 FOLLOW-UP: {result['followup']} (Reason: {result['reason']})")
        else:
            print(f"✅ {result['message']}")
    
    # Show final state
    state = engine.get_state_summary(candidate_id)
    print("\n" + "="*70)
    print("📊 CONVERSATION STATE SUMMARY")
    print("="*70)
    print(f"Candidate: {state['candidate_id']}")
    print(f"Questions asked: {len(state['answers'])}")
    print(f"Follow-ups used: {state.get('followups_used', 0)}")
    print(f"Final difficulty: {state['current_difficulty']}")
    
    # Save report
    report = {
        'generated_at': datetime.now().isoformat(),
        'session': state,
        'test_cases': len(test_cases)
    }
    with open('output/followup_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("\n✅ Report saved: output/followup_report.json")
    
    print("\n" + "="*70)
    print("✅ DAY 34 COMPLETED - DYNAMIC FOLLOW-UP LOGIC")
    print("="*70)

if __name__ == "__main__":
    main()