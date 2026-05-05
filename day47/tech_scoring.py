# tech_scoring.py - Day 47 Technical Skill Scoring Model (Fixed)
import json
import re
from datetime import datetime

class TechScoringEngine:
    def __init__(self):
        self.weights = {
            "accuracy": 0.35,
            "depth_explanation": 0.30,
            "logical_reasoning": 0.20,
            "real_world_applicability": 0.15
        }
        self.rubrics = {
            "conceptual": {"accuracy": 80, "depth_explanation": 70, "logical_reasoning": 60, "real_world_applicability": 50},
            "practical": {"accuracy": 85, "depth_explanation": 65, "logical_reasoning": 75, "real_world_applicability": 70},
            "system_design": {"accuracy": 70, "depth_explanation": 75, "logical_reasoning": 80, "real_world_applicability": 85}
        }
        self.difficulty_factors = {"basic": 0.9, "intermediate": 1.0, "advanced": 1.1}
        self.deep_indicators = ["because", "therefore", "for example", "such as", "trade-off",
                                "pros and cons", "alternatives", "edge case", "scalability", "performance"]
        self.shallow_indicators = ["i don't know", "not sure", "maybe", "yes", "no", "um", "uh"]
    
    def score_accuracy(self, answer, expected_keywords):
        if not expected_keywords:
            return 50
        answer_lower = answer.lower()
        matched = sum(1 for kw in expected_keywords if kw in answer_lower)
        return (matched / len(expected_keywords)) * 100
    
    def score_depth_explanation(self, answer):
        words = len(answer.split())
        depth = 0
        if words > 50:
            depth += 40
        elif words > 25:
            depth += 25
        elif words > 10:
            depth += 10
        for indicator in self.deep_indicators:
            if indicator in answer.lower():
                depth += 5
        for indicator in self.shallow_indicators:
            if indicator in answer.lower():
                depth -= 10
        return max(0, min(100, depth + 30))
    
    def score_logical_reasoning(self, answer):
        answer_lower = answer.lower()
        score = 40
        step_indicators = ["first", "second", "then", "next", "finally", "step"]
        for ind in step_indicators:
            if ind in answer_lower:
                score += 10
                break
        if "because" in answer_lower or "therefore" in answer_lower:
            score += 15
        if len(answer.split()) > 30:
            score += 10
        return min(100, score)
    
    def score_real_world(self, answer):
        answer_lower = answer.lower()
        score = 30
        practical_terms = ["real world", "example", "implementation", "database", "api", "server", "client", "scalability", "performance"]
        for term in practical_terms:
            if term in answer_lower:
                score += 8
        if "trade-off" in answer_lower or "pros" in answer_lower:
            score += 10
        return min(100, score)
    
    def evaluate_answer(self, answer, question_type, difficulty, expected_keywords=None):
        if expected_keywords is None:
            expected_keywords = []
        accuracy = self.score_accuracy(answer, expected_keywords)
        depth = self.score_depth_explanation(answer)
        logic = self.score_logical_reasoning(answer)
        real = self.score_real_world(answer)
        
        rubric = self.rubrics.get(question_type, self.rubrics["conceptual"])
        accuracy = (accuracy + rubric["accuracy"]) / 2
        depth = (depth + rubric["depth_explanation"]) / 2
        logic = (logic + rubric["logical_reasoning"]) / 2
        real = (real + rubric["real_world_applicability"]) / 2
        
        factor = self.difficulty_factors.get(difficulty, 1.0)
        raw_final = (accuracy * self.weights["accuracy"] +
                     depth * self.weights["depth_explanation"] +
                     logic * self.weights["logical_reasoning"] +
                     real * self.weights["real_world_applicability"])
        final_score = min(100, raw_final * factor)
        
        shallowness = "shallow" if (depth < 40 and logic < 40) else "deep"
        
        return {
            "answer": answer[:100],
            "question_type": question_type,
            "difficulty": difficulty,
            "component_scores": {
                "accuracy": round(accuracy, 2),
                "depth_explanation": round(depth, 2),
                "logical_reasoning": round(logic, 2),
                "real_world_applicability": round(real, 2)
            },
            "raw_score": round(raw_final, 2),
            "normalized_score": round(final_score, 2),
            "shallowness": shallowness,
            "details": {
                "word_count": len(answer.split()),
                "has_step_indicators": any(w in answer.lower() for w in ["first", "second", "then"])
            }
        }
    
    # FIXED: use 'normalized_score' instead of 'score'
    def skill_wise_breakdown(self, answers):
        breakdown = {}
        for ans in answers:
            skill = ans.get("skill", "general")
            if skill not in breakdown:
                breakdown[skill] = []
            breakdown[skill].append(ans["normalized_score"])
        return {skill: round(sum(scores)/len(scores), 2) for skill, scores in breakdown.items()}
    
    def generate_report(self, candidate_id, answers):
        overall = sum(a["normalized_score"] for a in answers) / len(answers)
        report = {
            "candidate_id": candidate_id,
            "overall_technical_score": round(overall, 2),
            "skill_wise_breakdown": self.skill_wise_breakdown(answers),
            "detailed_results": answers,
            "generated_at": datetime.now().isoformat()
        }
        return report

def main():
    print("="*70)
    print("DAY 47 - TECHNICAL SKILL SCORING MODEL")
    print("="*70)
    
    engine = TechScoringEngine()
    
    sample_answers = [
        {
            "text": "A variable is a container for storing data values. In Python, you don't need to declare type. For example, x = 5. Variables can hold different types like int, float, string.",
            "type": "conceptual",
            "difficulty": "basic",
            "expected_keywords": ["variable", "container", "data", "store"],
            "skill": "programming_basics"
        },
        {
            "text": "REST uses HTTP methods like GET, POST, PUT, DELETE. GraphQL allows clients to request exactly what they need. REST is simpler for caching, GraphQL reduces over-fetching. I would choose REST for simple CRUD apps, GraphQL for complex data requirements.",
            "type": "practical",
            "difficulty": "intermediate",
            "expected_keywords": ["rest", "graphql", "http", "cache", "over-fetching"],
            "skill": "api_design"
        },
        {
            "text": "To scale a service to millions of users, you need horizontal scaling (add more servers), load balancing, database sharding, caching (Redis), CDN for static content, and asynchronous processing with message queues. Also consider database replication and microservices architecture.",
            "type": "system_design",
            "difficulty": "advanced",
            "expected_keywords": ["scaling", "load balancing", "sharding", "caching", "microservices"],
            "skill": "system_design"
        },
        {
            "text": "I don't know, maybe use more servers? Not sure.",
            "type": "conceptual",
            "difficulty": "basic",
            "expected_keywords": ["scaling", "servers"],
            "skill": "system_design"
        }
    ]
    
    results = []
    for ans in sample_answers:
        result = engine.evaluate_answer(ans["text"], ans["type"], ans["difficulty"], ans["expected_keywords"])
        result["skill"] = ans["skill"]
        results.append(result)
        print(f"\n📌 Skill: {ans['skill']} | Type: {ans['type']} | Difficulty: {ans['difficulty']}")
        print(f"   Answer: {ans['text'][:80]}...")
        print(f"   Normalized Score: {result['normalized_score']}% ({result['shallowness']})")
        print(f"   Accuracy: {result['component_scores']['accuracy']}% | Depth: {result['component_scores']['depth_explanation']}%")
        print(f"   Logic: {result['component_scores']['logical_reasoning']}% | Real-world: {result['component_scores']['real_world_applicability']}%")
    
    print("\n📊 SKILL-WISE BREAKDOWN")
    breakdown = engine.skill_wise_breakdown(results)
    for skill, score in breakdown.items():
        print(f"   {skill}: {score}%")
    
    report = engine.generate_report("C1001", results)
    import os
    os.makedirs("output", exist_ok=True)
    with open("output/technical_evaluation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\n✅ Technical evaluation report saved: output/technical_evaluation_report.json")
    
    print("\n" + "="*70)
    print("✅ DAY 47 COMPLETED – TECHNICAL SCORING ENGINE READY")
    print("="*70)

if __name__ == "__main__":
    main()