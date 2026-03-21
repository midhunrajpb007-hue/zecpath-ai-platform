const fs = require('fs');
const path = require('path');

// Folder structure
const structure = {
  'services/skillExtraction': {
    'skillDictionary.js': `// skillDictionary.js - Master Skill Dictionary
const skillDictionary = {
  tech: [
    "javascript", "python", "java", "c++", "react", "node.js",
    "mongodb", "mysql", "aws", "docker", "kubernetes", "mern",
    "mean", "typescript", "next.js", "graphql"
  ],
  business: [
    "project management", "agile", "scrum", "business analysis",
    "sales", "marketing", "crm", "negotiation"
  ],
  creative: [
    "photoshop", "illustrator", "figma", "ui design", "ux design",
    "video editing", "content writing"
  ],
  soft: [
    "communication", "teamwork", "problem solving", "time management"
  ]
};

const skillSynonyms = {
  "javascript": ["js", "ecmascript"],
  "python": ["py"],
  "react": ["reactjs", "react.js"],
  "node.js": ["node", "nodejs"],
  "mern": ["mongodb express react node"],
  "mean": ["mongodb express angular node"]
};

const skillStacks = {
  "mern": ["mongodb", "express", "react", "node.js"],
  "mean": ["mongodb", "express", "angular", "node.js"]
};

module.exports = { skillDictionary, skillSynonyms, skillStacks };`,
    
    'extractor.js': `// extractor.js - Skill Extraction Engine
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

module.exports = { extractSkills };`,
    
    'normalizer.js': `// normalizer.js - Skill Normalization
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

module.exports = { normalizeSkills };`,
    
    'confidenceScorer.js': `// confidenceScorer.js - Confidence Scoring
function calculateConfidence(skill, resumeText, context = {}) {
  let score = 70;
  const text = resumeText.toLowerCase();
  const skillLower = skill.toLowerCase();

  if (text.includes(\` \${skillLower} \`)) score += 15;
  
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

module.exports = { addConfidence };`
  },
  'tests': {
    'skillExtraction.test.js': `// skillExtraction.test.js - Test File
const { extractSkills } = require('../services/skillExtraction/extractor');
const { normalizeSkills } = require('../services/skillExtraction/normalizer');
const { addConfidence } = require('../services/skillExtraction/confidenceScorer');

const sampleResume = \`
Experienced MERN Stack Developer with 4+ years experience.
Proficient in JavaScript, React, Node.js, and MongoDB.
AWS certified. Good at project management and agile.
\`;

console.log("🚀 Testing Skill Extraction...\\n");

const rawSkills = extractSkills(sampleResume);
console.log("Raw Skills:", rawSkills);

const normalized = normalizeSkills(rawSkills);
console.log("\\nNormalized:", normalized);

const withConfidence = addConfidence(normalized, sampleResume);
console.log("\\nWith Confidence:", withConfidence);

console.log("\\n✅ Day 9 Complete!");`
  }
};

// Create folders and files
Object.entries(structure).forEach(([folderPath, files]) => {
  // Create folder if not exists
  if (!fs.existsSync(folderPath)) {
    fs.mkdirSync(folderPath, { recursive: true });
    console.log(`✅ Created folder: ${folderPath}`);
  }

  // Create files
  Object.entries(files).forEach(([fileName, content]) => {
    const filePath = path.join(folderPath, fileName);
    fs.writeFileSync(filePath, content);
    console.log(`✅ Created file: ${filePath}`);
  });
});

console.log('\n🎉 ALL DONE! Skill Extraction Engine setup complete!');
console.log('🚀 Run: node tests/skillExtraction.test.js\n');
