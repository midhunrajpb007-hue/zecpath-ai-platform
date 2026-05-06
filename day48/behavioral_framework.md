# Behavioral Analysis Framework

## Step 1: Capture signals
- Eye tracking (gaze coordinates)
- Head pose (angles)
- Facial expressions (smile detection)

## Step 2: Normalize signals
Convert raw measurements to 0‑1 scale.

## Step 3: Detect patterns
- Distraction: frequent gaze shifts
- Engagement: smiling, nodding
- Nervousness: excessive head movement

## Step 4: Calculate score
Use `calculate_behavior_score()` with weights.

## Step 5: Generate insights
- Focus level: High / Medium / Low
- Risk: Low / Moderate / High