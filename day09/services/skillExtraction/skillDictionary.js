// skillDictionary.js - Master Skill Dictionary
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

module.exports = { skillDictionary, skillSynonyms, skillStacks };