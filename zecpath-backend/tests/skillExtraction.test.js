// skillExtraction.test.js - Test File
const { extractSkills } = require('../services/skillExtraction/extractor');
const { normalizeSkills } = require('../services/skillExtraction/normalizer');
const { addConfidence } = require('../services/skillExtraction/confidenceScorer');

const sampleResume = `
Experienced MERN Stack Developer with 4+ years experience.
Proficient in JavaScript, React, Node.js, and MongoDB.
AWS certified. Good at project management and agile.
`;

console.log("🚀 Testing Skill Extraction...\n");

const rawSkills = extractSkills(sampleResume);
console.log("Raw Skills:", rawSkills);

const normalized = normalizeSkills(rawSkills);
console.log("\nNormalized:", normalized);

const withConfidence = addConfidence(normalized, sampleResume);
console.log("\nWith Confidence:", withConfidence);

console.log("\n✅ Day 9 Complete!");