# conversation_flow.py - Day 29 AI Conversation Flow Design
import json
from datetime import datetime

class ConversationFlow:
    def __init__(self):
        self.flow = {
            'start': {'next': 'introduction', 'description': 'Start the call'},
            'introduction': {
                'question': "Hello! I'm calling from Zecpath. May I speak with {name}?",
                'next_success': 'skills',
                'next_failure': 'reask_intro',
                'max_attempts': 2,
                'description': 'Confirm candidate identity'
            },
            'reask_intro': {
                'question': "Sorry, could you please confirm if this is {name}?",
                'next_success': 'skills',
                'next_failure': 'end_failure',
                'max_attempts': 1,
                'description': 'Re-ask identity confirmation'
            },
            'skills': {
                'question': "What are your main technical skills?",
                'next_success': 'experience',
                'next_failure': 'fallback_skills',
                'max_attempts': 2,
                'description': 'Ask about technical skills'
            },
            'fallback_skills': {
                'question': "Could you tell me about your programming experience?",
                'next_success': 'experience',
                'next_failure': 'skip_skills',
                'max_attempts': 1,
                'description': 'Fallback for skills question'
            },
            'skip_skills': {
                'question': "Let's move on. How many years of experience do you have?",
                'next': 'experience',
                'description': 'Skip skills section'
            },
            'experience': {
                'question': "How many years of experience do you have in software development?",
                'next_success': 'salary',
                'next_failure': 'fallback_exp',
                'max_attempts': 2,
                'description': 'Ask about experience'
            },
            'fallback_exp': {
                'question': "I didn't catch that. Could you tell me your years of experience?",
                'next_success': 'salary',
                'next_failure': 'skip_exp',
                'max_attempts': 1,
                'description': 'Fallback for experience'
            },
            'skip_exp': {
                'question': "What are your salary expectations?",
                'next': 'salary',
                'description': 'Skip experience section'
            },
            'salary': {
                'question': "What is your expected annual salary?",
                'next_success': 'availability',
                'next_failure': 'fallback_salary',
                'max_attempts': 2,
                'description': 'Ask about salary'
            },
            'fallback_salary': {
                'question': "Could you give me a salary range you're comfortable with?",
                'next_success': 'availability',
                'next_failure': 'skip_salary',
                'max_attempts': 1,
                'description': 'Fallback for salary'
            },
            'skip_salary': {
                'question': "When can you join if selected?",
                'next': 'availability',
                'description': 'Skip salary section'
            },
            'availability': {
                'question': "What is your notice period?",
                'next_success': 'confirmation',
                'next_failure': 'fallback_availability',
                'max_attempts': 2,
                'description': 'Ask about availability'
            },
            'fallback_availability': {
                'question': "When would you be able to join?",
                'next_success': 'confirmation',
                'next_failure': 'end_partial',
                'max_attempts': 1,
                'description': 'Fallback for availability'
            },
            'confirmation': {
                'question': "Thank you for your time. We'll review your profile and get back to you.",
                'next': 'end',
                'description': 'End call positively'
            },
            'end': {'description': 'Call ended successfully'},
            'end_partial': {'description': 'Call ended with partial information'},
            'end_failure': {'description': 'Call ended - could not verify identity'}
        }
    
    def get_next_question(self, state, answer=None, previous_answer=None):
        node = self.flow.get(state, {})
        if not answer or len(answer.strip()) < 1:
            return self._handle_silence(state, node)
        if self._is_confused(answer):
            return self._handle_confusion(state, node)
        if previous_answer and answer.lower() == previous_answer.lower():
            return self._handle_repeated(state, node)
        return self._handle_normal(state, answer, node)
    
    def _is_confused(self, answer):
        confused = ['i don\'t know', 'not sure', 'what?', 'huh?', 'repeat']
        return any(p in answer.lower() for p in confused) or len(answer.split()) < 2
    
    def _handle_silence(self, state, node):
        attempts = node.get('attempt_count', 0) + 1
        max_attempts = node.get('max_attempts', 2)
        if attempts >= max_attempts:
            return {'action': 'move_to_fallback', 'next_state': node.get('next_failure', 'end_partial'), 'message': "Let's move to the next question.", 'attempts': attempts}
        else:
            return {'action': 'retry', 'next_state': state, 'message': "I didn't hear you. " + node.get('question', ''), 'attempts': attempts}
    
    def _handle_confusion(self, state, node):
        attempts = node.get('attempt_count', 0) + 1
        max_attempts = node.get('max_attempts', 2)
        if attempts >= max_attempts:
            return {'action': 'use_fallback', 'next_state': node.get('next_failure', 'end_partial'), 'message': "Let me ask differently.", 'attempts': attempts}
        else:
            return {'action': 'rephrase', 'next_state': state, 'message': "Let me rephrase. " + node.get('question', ''), 'attempts': attempts}
    
    def _handle_repeated(self, state, node):
        return {'action': 'acknowledge_and_move', 'next_state': node.get('next_success', node.get('next', 'end')), 'message': "Thanks. Let's move on.", 'repeated': True}
    
    def _handle_normal(self, state, answer, node):
        success = len(answer.split()) >= node.get('min_words', 1) if node.get('min_words') else True
        if success:
            return {'action': 'next', 'next_state': node.get('next_success', node.get('next', 'end')), 'answer_valid': True}
        else:
            attempts = node.get('attempt_count', 0) + 1
            max_attempts = node.get('max_attempts', 2)
            if attempts >= max_attempts:
                return {'action': 'skip', 'next_state': node.get('next_failure', 'end_partial'), 'message': "Let's move to the next question.", 'attempts': attempts}
            else:
                return {'action': 'retry', 'next_state': state, 'message': "I didn't quite get that. " + node.get('question', ''), 'attempts': attempts}
    
    def get_question_text(self, state, name=None):
        node = self.flow.get(state, {})
        q = node.get('question', '')
        if name and '{name}' in q:
            q = q.replace('{name}', name)
        return q
    
    def generate_flow_diagram(self):
        diagram = """
+----------------------------------------------------------------------+
|                       AI CONVERSATION FLOW                           |
+----------------------------------------------------------------------+

                                START
                                  |
                                  v
                         +----------------+
                         |  INTRODUCTION  |
                         | (Confirm name) |
                         +----------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v (Success)                                 v (Fail)
      +----------------+                       +----------------+
      |    SKILLS      |                       |  REASK INTRO   |
      | (Ask skills)   |                       | (Confirm again)|
      +----------------+                       +----------------+
            |                                           |
            v (Success)                                 v (Fail)
      +----------------+                       +----------------+
      |  EXPERIENCE    |                       |  END FAILURE   |
      | (Ask years)    |                       | (Call failed)  |
      +----------------+                       +----------------+
            |
            v (Success)
      +----------------+
      |    SALARY      |
      | (Ask salary)   |
      +----------------+
            |
            v (Success)
      +----------------+
      |  AVAILABILITY  |
      | (Ask notice)   |
      +----------------+
            |
            v
      +----------------+
      |  CONFIRMATION  |
      | (Thank you)    |
      +----------------+
            |
            v
      +----------------+
      |      END       |
      | (Call ended)   |
      +----------------+

+----------------------------------------------------------------------+
|                         FALLBACK PATHS                               |
+----------------------------------------------------------------------+

   SKILLS → FALLBACK SKILLS → SKIP SKILLS → EXPERIENCE
   EXPERIENCE → FALLBACK EXP → SKIP EXP → SALARY
   SALARY → FALLBACK SALARY → SKIP SALARY → AVAILABILITY
   AVAILABILITY → FALLBACK AVAILABILITY → END PARTIAL

+----------------------------------------------------------------------+
|                         ERROR HANDLING                               |
+----------------------------------------------------------------------+

   SILENCE:    "I didn't hear you" → Retry (2 times) → Fallback
   CONFUSION:  "Let me rephrase" → Retry (2 times) → Fallback
   REPEATED:   "Thanks, let's move on" → Skip to next

+----------------------------------------------------------------------+
|                         ALL STATES (18)                              |
+----------------------------------------------------------------------+

   start
   introduction
   reask_intro
   skills
   fallback_skills
   skip_skills
   experience
   fallback_exp
   skip_exp
   salary
   fallback_salary
   skip_salary
   availability
   fallback_availability
   confirmation
   end
   end_partial
   end_failure
"""
        return diagram
    
    def export_to_json(self, filename='output/conversation_flow.json'):
        import os
        os.makedirs('output', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.flow, f, indent=2)
        print(f"✅ Flow exported: {filename}")

def main():
    print("="*70)
    print("DAY 29 - AI CONVERSATION FLOW DESIGN")
    print("="*70)
    
    flow = ConversationFlow()
    print(flow.generate_flow_diagram())
    
    print("\n📋 STATE MACHINE STATES")
    for state in ['start', 'introduction', 'reask_intro', 'skills', 'fallback_skills', 'experience', 'fallback_exp', 'salary', 'fallback_salary', 'availability', 'fallback_availability', 'confirmation', 'end', 'end_partial', 'end_failure']:
        desc = flow.flow.get(state, {}).get('description', '')
        print(f"   {state}: {desc}")
    
    flow.export_to_json()
    print("\n✅ DAY 29 COMPLETED")

if __name__ == "__main__":
    main()