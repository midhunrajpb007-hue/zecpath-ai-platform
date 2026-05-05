# Technical Interview AI – System Blueprint

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
