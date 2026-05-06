# Behavioral AI Design Document

## Objective
Candidate-ൻ്റെ video signals വിശകലനം ചെയ്ത് focus, confidence, engagement എന്നിവ അളക്കുക.

## Signals used
- Eye movement (gaze)
- Head movement (pose)
- Facial engagement (smile, neutral)
- Attention pattern (gaze away from screen)

## System Components
1. Video input (webcam)
2. Face detection
3. Eye tracking
4. Head movement analyzer
5. Engagement detector
6. Signal aggregator
7. Scoring engine
8. Report generator

## Non‑invasive design principles
- Raw video സംഭരിക്കില്ല (only scores)
- Consent എടുക്കും
- Emotion inference ഇല്ല (only engagement)