// normalizer.js - Skill Normalization
const normalizationMap = {
  "nodejs": "Node.js",
  "node js": "Node.js",
  "reactjs": "React",
  "react js": "React",
  "js": "JavaScript",
  "py": "Python",
  "cpp": "C++"
};

function normalizeSkill(skill) {
  const lowerSkill = skill.toLowerCase();
  
  for (let [variant, standard] of Object.entries(normalizationMap)) {
    if (lowerSkill === variant || lowerSkill.includes(variant)) {
      return standard;
    }
  }
  
  return skill.charAt(0).toUpperCase() + skill.slice(1);
}

function normalizeSkills(skillsArray) {
  return [...new Set(skillsArray.map(normalizeSkill))];
}

module.exports = { normalizeSkills };