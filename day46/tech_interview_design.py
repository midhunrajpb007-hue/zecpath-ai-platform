# tech_interview_design.py - Day 46 Technical Interview System Design (UTF-8 Fixed)
import json
import os

class TechInterviewDesign:
    def __init__(self):
        # Role to skill domain mapping
        self.role_domains = {
            "mern": ["mongodb", "express", "react", "nodejs", "javascript", "rest", "graphql"],
            "java": ["java", "spring", "hibernate", "jpa", "microservices", "maven"],
            "devops": ["docker", "kubernetes", "jenkins", "terraform", "aws", "ci/cd"],
            "data_scientist": ["python", "pandas", "scikit-learn", "tensorflow", "sql", "statistics"],
            "frontend": ["javascript", "react", "angular", "vue", "css", "html", "webpack"]
        }
        
        self.exp_levels = {
            "fresher": (0, 2),
            "mid": (3, 5),
            "senior": (6, 99)
        }
        
        self.difficulty_levels = {
            "basic": {"weight": 1, "type": "conceptual"},
            "intermediate": {"weight": 2, "type": "practical"},
            "advanced": {"weight": 3, "type": "system_design"}
        }
        
        self.flow_states = [
            "start", "introduction", "experience_assessment",
            "technical_basics", "technical_intermediate", "technical_advanced",
            "scenario_question", "code_review", "closing", "end"
        ]
    
    def get_skill_domain(self, role):
        return self.role_domains.get(role.lower(), ["programming", "algorithms", "problem-solving"])
    
    def get_experience_level(self, years):
        if years <= 2:
            return "fresher", "basic"
        elif years <= 5:
            return "mid", "intermediate"
        else:
            return "senior", "advanced"
    
    def generate_question_hierarchy(self):
        return {
            "root": {
                "introduction": ["Tell me about your technical background.", "What technologies are you most comfortable with?"]
            },
            "experience_based": {
                "fresher": {"basics": ["What is a variable?", "Explain the difference between stack and heap."]},
                "mid": {"intermediate": ["Explain the difference between REST and GraphQL.", "How do you handle database transactions?"]},
                "senior": {"advanced": ["Design a URL shortener system.", "How would you scale a service to millions of users?"]}
            },
            "conceptual": {
                "basic": ["What is OOP?", "Define polymorphism."],
                "intermediate": ["Explain SOLID principles.", "What is dependency injection?"],
                "advanced": ["Compare microservices vs monolith.", "Discuss eventual consistency."]
            },
            "scenario": {
                "basic": ["Debug a simple function.", "Write a query to get top 5 products."],
                "intermediate": ["Design a task scheduler.", "Optimize a slow API endpoint."],
                "advanced": ["Handle a data inconsistency across services.", "Design a real-time chat system."]
            }
        }
    
    def generate_flow_diagram(self):
        return """
+----------------------------------------------------------------------+
|                 TECHNICAL INTERVIEW FLOW                             |
+----------------------------------------------------------------------+

                              START
                                |
                                v
                        +-----------------+
                        |  INTRODUCTION   |
                        | (Role, company) |
                        +--------+--------+
                                 |
                                 v
                        +-----------------+
                        |  EXPERIENCE     |
                        |  ASSESSMENT     |
                        | (Years of exp)  |
                        +--------+--------+
                                 |
           +---------------------+---------------------+
           |                                           |
           v (0-2 yrs)          v (3-5 yrs)          v (6+ yrs)
      +----------+          +----------+          +----------+
      | BASICS   |          | INTERMEDIATE|        | ADVANCED |
      | (Concept)|          | (Practical) |        |(System   |
      |          |          |             |        | Design)  |
      +----+-----+          +-----+-------+        +----+-----+
           |                      |                      |
           +----------------------+----------------------+
                                 |
                                 v
                        +-----------------+
                        | SCENARIO & CODE |
                        |   (Adaptive)    |
                        +--------+--------+
                                 |
                                 v
                        +-----------------+
                        |    CLOSING      |
                        | (Feedback, next)|
                        +--------+--------+
                                 |
                                 v
                                END
"""
    
    def generate_blueprint(self):
        return """# Technical Interview AI – System Blueprint

## 1. High-Level Architecture

The system consists of these components:

- **Role Mapper** – determines skill domain from job title (MERN, Java, DevOps, etc.)
- **Experience Analyzer** – selects difficulty level based on candidate's stated years of experience.
- **Question Bank** – categorized by skill domain, difficulty level, and question type (conceptual, practical, scenario, system design).
- **Difficulty Progression Engine** – adapts next question difficulty based on previous answer quality.
- **State Manager** – tracks current phase (introduction, assessment, conceptual, scenario, closing) and question index.
- **Scoring & Feedback** – evaluates answers (simulated) and provides final technical score.

## 2. Data Flow

Candidate -> Role -> Skills Domain -> Experience -> Difficulty -> Question -> Answer -> Scoring -> Next Question (adaptive) -> Final Score

## 3. Key Design Decisions

- **Experience-based progression:** Avoid asking very hard questions to juniors or too easy to seniors.
- **Adaptive difficulty:** If candidate answers well, move to next difficulty level; if struggling, stay or fallback.
- **Domain-specific questions:** Tailored to the actual job (e.g., MERN stack for full-stack developer).
"""
    
    def save_design(self):
        os.makedirs("data", exist_ok=True)
        os.makedirs("output", exist_ok=True)
        
        with open("data/question_hierarchy.json", "w", encoding="utf-8") as f:
            json.dump(self.generate_question_hierarchy(), f, indent=2)
        print("✅ Question hierarchy saved: data/question_hierarchy.json")
        
        with open("output/tech_interview_blueprint.md", "w", encoding="utf-8") as f:
            f.write(self.generate_blueprint())
        print("✅ Blueprint saved: output/tech_interview_blueprint.md")
        
        with open("output/interview_flow_diagram.txt", "w", encoding="utf-8") as f:
            f.write(self.generate_flow_diagram())
        print("✅ Flow diagram saved: output/interview_flow_diagram.txt")
        
        print("\n📋 TECHNICAL INTERVIEW DESIGN COMPLETE")
        print("   Role domains:", list(self.role_domains.keys()))
        print("   Experience levels:", list(self.exp_levels.keys()))
        print("   Difficulty progression:", list(self.difficulty_levels.keys()))
        print("   Flow states:", len(self.flow_states))

def main():
    print("="*70)
    print("DAY 46 - TECHNICAL INTERVIEW SYSTEM DESIGN")
    print("="*70)
    designer = TechInterviewDesign()
    designer.save_design()
    print("\n" + "="*70)
    print("✅ DAY 46 COMPLETED – DESIGN READY FOR IMPLEMENTATION")
    print("="*70)

if __name__ == "__main__":
    main()