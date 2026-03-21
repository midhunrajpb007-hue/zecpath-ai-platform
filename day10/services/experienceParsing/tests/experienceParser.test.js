// experienceParser.test.js

const { 
    parseExperience, 
    calculateTotalExperience, 
    calculateRelevance 
} = require('../services/experienceParsing/experienceParser');

// Sample resume
const resume = `
WORK EXPERIENCE:

Senior MERN Stack Developer at Google (2021 - Present)
- Developed full stack applications
- Led team of 5 developers

React Developer at Amazon (2019 - 2021)
- Built responsive UI components
- Worked with Redux

Junior Developer at Infosys (2017 - 2019)
- Bug fixing and maintenance
- Assisted in frontend development
`;

console.log('=====================================');
console.log('    DAY 10 - EXPERIENCE PARSER');
console.log('=====================================\n');

// 1. Parse experiences
console.log('📌 Step 1: Parsing experiences...');
const experiences = parseExperience(resume);
console.log('✅ Found', experiences.length, 'experiences');
console.log(JSON.stringify(experiences, null, 2));
console.log();

// 2. Calculate total experience
console.log('📌 Step 2: Calculating total experience...');
const totalExp = calculateTotalExperience(experiences);
console.log('✅ Total Experience:', totalExp.years, 'years');
console.log();

// 3. Calculate relevance
console.log('📌 Step 3: Calculating role relevance...');
const jobRole = 'MERN Stack Developer';
const relevance = calculateRelevance(experiences, jobRole);
console.log('✅ Relevance for "' + jobRole + '":');
console.log(JSON.stringify(relevance, null, 2));
console.log();

// 4. Final output
console.log('=====================================');
console.log('📦 DAY 10 DELIVERABLE - Structured Output');
console.log('=====================================');

const output = {
    candidate: 'Sample Resume',
    jobRole: jobRole,
    totalExperience: totalExp.years + ' years',
    experiences: experiences,
    relevanceAnalysis: relevance,
    recommendation: totalExp.years >= 3 ? 'Recommended' : 'Review'
};

console.log(JSON.stringify(output, null, 2));
console.log('\n✅✅✅ DAY 10 COMPLETED SUCCESSFULLY! ✅✅✅');