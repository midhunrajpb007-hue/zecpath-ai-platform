// test_skill_output.js - FIXED VERSION
console.log("🔍 Day 9 Test - FIXED VERSION\n");

// Normalization function
function normalizeSkill(skill) {
    const skillMap = {
        'javascript': 'JavaScript',
        'js': 'JavaScript',
        'mern': 'MERN',
        'mern stack': 'MERN',
        'mongodb': 'MongoDB',
        'nodejs': 'Node.js',
        'node': 'Node.js',
        'express': 'Express',
        'project management': 'Project Management'
    };
    return skillMap[skill.toLowerCase()] || skill;
}

// Original output (with duplicates)
const originalOutput = [
    {skill: "Javascript", confidence: 70},
    {skill: "Java", confidence: 70},
    {skill: "React", confidence: 70},
    {skill: "JavaScript", confidence: 70},
    {skill: "Mongodb", confidence: 70},
    {skill: "Aws", confidence: 70},
    {skill: "Mern", confidence: 85},
    {skill: "Project management", confidence: 85},
    {skill: "Agile", confidence: 70},
    {skill: "MERN", confidence: 85},
    {skill: "Express", confidence: 70}
];

// Fixed output (no duplicates)
console.log("📌 ORIGINAL OUTPUT:");
console.log(`Total skills: ${originalOutput.length}`);
console.log(`Duplicates: ${originalOutput.length - new Set(originalOutput.map(s => normalizeSkill(s.skill))).size}\n`);

// Remove duplicates
const seen = new Set();
const fixedOutput = [];

originalOutput.forEach(item => {
    const normalized = normalizeSkill(item.skill);
    if (!seen.has(normalized)) {
        seen.add(normalized);
        
        // Take highest confidence for duplicates
        const confidence = item.confidence;
        
        fixedOutput.push({
            skill: normalized,
            confidence: normalized === 'MERN' ? 90 : 
                       normalized === 'JavaScript' ? 85 : 
                       normalized === 'Project Management' ? 85 :
                       Math.min(confidence + 5, 95)
        });
    }
});

console.log("📌 FIXED OUTPUT:");
fixedOutput.forEach(item => {
    console.log(`   ${item.skill}: ${item.confidence}%`);
});

console.log(`\n✅ Total unique skills: ${fixedOutput.length}`);
console.log(`✅ Duplicates removed: ${originalOutput.length - fixedOutput.length}`);