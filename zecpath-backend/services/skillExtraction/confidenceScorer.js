// confidenceScorer.js - Confidence Scoring
function calculateConfidence(skill, resumeText, context = {}) {
  let score = 70;
  const text = resumeText.toLowerCase();
  const skillLower = skill.toLowerCase();

  if (text.includes(` ${skillLower} `)) score += 15;
  
  const regex = new RegExp(skillLower, 'gi');
  const count = (text.match(regex) || []).length;
  if (count >= 3) score += 10;
  if (count >= 5) score += 5;

  return Math.min(score, 100);
}

function addConfidence(skills, resumeText, context = {}) {
  return skills.map(skill => ({
    skill,
    confidence: calculateConfidence(skill, resumeText, context)
  }));
}

module.exports = { addConfidence };