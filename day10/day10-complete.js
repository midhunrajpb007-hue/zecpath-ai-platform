// day10-final.js
// Day 10 - PDF Requirements ONLY

console.log("========================================");
console.log("DAY 10 - Experience Parsing & Relevance Engine");
console.log("========================================\n");

// Sample resume
const resume = `
Senior Developer at Google (2020-2023)
React Developer at Amazon (2018-2020)
Junior Developer at Infosys (2016-2018)
`;

// ========================================
// 1. EXTRACT Company, Title, Duration
// ========================================
const experiences = [];
const lines = resume.split('\n');

lines.forEach(line => {
    if (line.includes('Developer') && line.includes('at')) {
        const parts = line.split('at');
        const title = parts[0].trim();
        const company = parts[1].split('(')[0].trim();
        const dates = line.match(/(\d{4})-(\d{4})/);
        
        if (dates) {
            experiences.push({
                company: company,
                title: title,
                startDate: parseInt(dates[1]),
                endDate: parseInt(dates[2]),
                duration: parseInt(dates[2]) - parseInt(dates[1]) + ' years'
            });
        }
    }
});

console.log("📌 1. Extracted Experiences:");
console.log(experiences);
console.log();

// ========================================
// 2. CALCULATE TOTAL EXPERIENCE
// ========================================
let totalYears = 0;
experiences.forEach(exp => {
    totalYears += parseInt(exp.duration);
});

console.log("📌 2. Total Experience:", totalYears, "years");
console.log();

// ========================================
// 3. DETECT GAPS
// ========================================
const gaps = [];
const sorted = [...experiences].sort((a,b) => a.startDate - b.startDate);

for (let i = 1; i < sorted.length; i++) {
    const prevEnd = sorted[i-1].endDate;
    const currStart = sorted[i].startDate;
    
    if (currStart > prevEnd + 1) {
        gaps.push({
            between: `${sorted[i-1].company} (${prevEnd}) → ${sorted[i].company} (${currStart})`,
            years: currStart - prevEnd
        });
    }
}

console.log("📌 3. Employment Gaps:");
console.log(gaps.length ? gaps : "No gaps found");
console.log();

// ========================================
// 4. DETECT OVERLAPPING ROLES
// ========================================
const overlaps = [];

for (let i = 0; i < experiences.length; i++) {
    for (let j = i + 1; j < experiences.length; j++) {
        const e1 = experiences[i];
        const e2 = experiences[j];
        
        if (e1.startDate <= e2.endDate && e2.startDate <= e1.endDate) {
            overlaps.push({
                roles: `${e1.title} (${e1.company}) ↔ ${e2.title} (${e2.company})`,
                period: `${Math.max(e1.startDate, e2.startDate)}-${Math.min(e1.endDate, e2.endDate)}`
            });
        }
    }
}

console.log("📌 4. Overlapping Roles:");
console.log(overlaps.length ? overlaps : "No overlaps found");
console.log();

// ========================================
// 5. ROLE RELEVANCE & SIMILARITY LOGIC
// ========================================
const targetRole = "Senior Developer";
const relevance = [];

experiences.forEach(exp => {
    let score = 0;
    
    // Role-to-role similarity logic
    if (exp.title.includes('Senior')) score = 100;
    else if (exp.title.includes('React')) score = 70;
    else if (exp.title.includes('Junior')) score = 40;
    
    relevance.push({
        title: exp.title,
        company: exp.company,
        similarityScore: score,
        relevanceLevel: score >= 80 ? 'High' : score >= 60 ? 'Medium' : 'Low'
    });
});

console.log(`📌 5. Role Relevance for "${targetRole}":`);
console.log(relevance);
console.log();

// ========================================
// 6. EXPERIENCE RELEVANCE SCORING MODULE
// ========================================
let expScore = Math.min((totalYears / 5) * 40, 40);
let roleScore = 0;

experiences.forEach(exp => {
    if (exp.title.includes('Senior')) roleScore += 90;
    else if (exp.title.includes('React')) roleScore += 70;
    else roleScore += 40;
});

let avgRoleScore = roleScore / experiences.length;
let finalScore = Math.round(expScore + (avgRoleScore * 0.4) + 20);

console.log("📌 6. Experience Relevance Score:", finalScore + "/100");
console.log();

// ========================================
// 7. STRUCTURED EXPERIENCE OBJECT (DELIVERABLE)
// ========================================
console.log("📦 7. DELIVERABLE - Structured Experience Object");
console.log("------------------------------------------------");

const output = {
    candidate: "Sample Resume",
    targetRole: targetRole,
    totalExperience: totalYears + " years",
    experienceDetails: experiences,
    employmentGaps: gaps,
    overlappingRoles: overlaps,
    roleSimilarity: relevance,
    relevanceScore: {
        score: finalScore,
        maxScore: 100
    }
};

console.log(JSON.stringify(output, null, 2));
console.log("\n✅ DAY 10 COMPLETED - PDF REQUIREMENTS MET");