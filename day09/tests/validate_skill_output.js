// test_skill_output.js
// Simple test for Day 9 output

console.log('🔍 Testing Day 9 Skill Extraction Output...\n');

// Your actual output from the test
const yourOutput = [
    { skill: 'Javascript', confidence: 70 },
    { skill: 'Java', confidence: 70 },
    { skill: 'React', confidence: 70 },
    { skill: 'JavaScript', confidence: 70 },
    { skill: 'Mongodb', confidence: 70 },
    { skill: 'Aws', confidence: 70 },
    { skill: 'Mern', confidence: 85 },
    { skill: 'Project management', confidence: 85 },
    { skill: 'Agile', confidence: 70 },
    { skill: 'MERN', confidence: 85 },
    { skill: 'Express', confidence: 70 }
];

// Validation checks
console.log('📊 VALIDATION RESULTS:');
console.log('----------------------');

// Check 1: Duplicates
const skills = yourOutput.map(s => s.skill.toLowerCase());
const uniqueSkills = [...new Set(skills)];
const duplicateCount = skills.length - uniqueSkills.length;
console.log(`${duplicateCount === 0 ? '✅' : '❌'} Duplicate Check: ${duplicateCount} duplicates found`);

// Check 2: JavaScript normalization
const jsSkills = yourOutput.filter(s => 
    s.skill.toLowerCase() === 'javascript' || 
    s.skill.toLowerCase() === 'js' ||
    s.skill.toLowerCase() === 'javascript'
);
const hasExactJavaScript = yourOutput.some(s => s.skill === 'JavaScript');
console.log(`${hasExactJavaScript && jsSkills.length === 1 ? '✅' : '❌'} JavaScript Normalization: ${hasExactJavaScript ? 'OK' : 'Missing'}`);

// Check 3: MERN normalization
const mernSkills = yourOutput.filter(s => 
    s.skill.toLowerCase() === 'mern' || 
    s.skill.toLowerCase() === 'mern'
);
const hasExactMERN = yourOutput.some(s => s.skill === 'MERN');
console.log(`${hasExactMERN && mernSkills.length === 1 ? '✅' : '❌'} MERN Normalization: ${hasExactMERN ? 'OK' : 'Missing'}`);

// Check 4: Confidence variation
const confidences = yourOutput.map(s => s.confidence);
const uniqueConfidences = [...new Set(confidences)];
console.log(`${uniqueConfidences.length > 2 ? '✅' : '❌'} Confidence Variation: ${uniqueConfidences.length} unique values`);

console.log('\n' + '='.repeat(50));
console.log('📝 SUMMARY:');
console.log(`Total Skills: ${yourOutput.length}`);
console.log(`Unique Skills: ${uniqueSkills.length}`);
console.log(`Confidence Range: ${Math.min(...confidences)}-${Math.max(...confidences)}%`);

// Final verdict
const score = (duplicateCount === 0 ? 25 : 0) + 
              (hasExactJavaScript && jsSkills.length === 1 ? 25 : 0) +
              (hasExactMERN && mernSkills.length === 1 ? 25 : 0) +
              (uniqueConfidences.length > 2 ? 25 : 0);

console.log('\n' + '='.repeat(50));
console.log(`🏆 FINAL SCORE: ${score}%`);
console.log('='.repeat(50));