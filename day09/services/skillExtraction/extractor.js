// extractor.js - Skill Extraction Engine
const { skillDictionary, skillSynonyms, skillStacks } = require('./skillDictionary');

function extractSkills(resumeText) {
  const text = resumeText.toLowerCase();
  let foundSkills = new Set();

  Object.values(skillDictionary).flat().forEach(skill => {
    if (text.includes(skill.toLowerCase())) {
      foundSkills.add(skill);
    }
  });

  Object.entries(skillSynonyms).forEach(([mainSkill, synonyms]) => {
    synonyms.forEach(syn => {
      if (text.includes(syn.toLowerCase())) {
        foundSkills.add(mainSkill);
      }
    });
  });

  Object.entries(skillStacks).forEach(([stack, skills]) => {
    if (text.includes(stack.toLowerCase())) {
      foundSkills.add(stack.toUpperCase());
      skills.forEach(skill => foundSkills.add(skill));
    }
  });

  return Array.from(foundSkills);
}

module.exports = { extractSkills };