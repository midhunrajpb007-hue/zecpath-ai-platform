// experience.js - Day 10 Complete Version

console.log("🚀 DAY 10 - Experience Parsing & Relevance Engine");
console.log("================================================\n");

// Sample resume
const resume = `
Senior Developer at Google (2020-2023)
React Developer at Amazon (2018-2020)  
Junior Developer at Infosys (2016-2018)
Freelance Developer (2014-2015)
`;

// 1. Extract experiences
const experiences = [];
const lines = resume.split('\n');

lines.forEach(line => {
    if (line.includes('Developer') || line.includes('Freelance')) {
        const parts = line.split('at');
        const title = parts[0].trim();
        const company = parts[1] ? parts[1].split('(')[0].trim() : 'Freelance';
        const dates = line.match(/(\d{4})-(\d{4}|\w+)/);
        
        if (dates) {
            const start = parseInt(dates[1]);
            const end = dates[2].toLowerCase() === 'present' 
                ? new Date().getFullYear() 
                : parseInt(dates[2]);
            
            experiences.push({
                title,
                company,
                start,
                end,
                years: end - start
            });
        }
    }
});

console.log("📌 Experiences:");
console.log(JSON.stringify(experiences, null, 2));
console.log();

// 2. Total experience
let totalYears = 0;
experiences.forEach(exp => totalYears += exp.years);
console.log("📌 Total Experience:", totalYears, "years");
console.log();

// 3. Detect gaps
console.log("📌 Experience Gaps:");
const sorted = [...experiences].sort((a,b) => a.start - b.start);
const gaps = [];

for (let i = 1; i < sorted.length; i++) {
    const prevEnd = sorted[i-1].end;
    const currStart = sorted[i].start;
    
    if (currStart > prevEnd + 1) {
        const gapYears = currStart - prevEnd;
        gaps.push({
            between: `${sorted[i-1].company} (${prevEnd}) → ${sorted[i].company} (${currStart})`,
            years: gapYears,
            months: gapYears * 12
        });
    }
}

if (gaps.length === 0) {
    console.log("✅ No gaps found");
} else {
    console.log(JSON.stringify(gaps, null, 2));
}
console.log();

// 4. Detect overlapping roles
console.log("📌 Overlapping Roles:");
const overlaps = [];

for (let i = 0; i < experiences.length; i++) {
    for (let j = i + 1; j < experiences.length; j++) {
        const exp1 = experiences[i];
        const exp2 = experiences[j];
        
        if (exp1.start <= exp2.end && exp2.start <= exp1.end) {
            overlaps.push({
                roles: `${exp1.title} (${exp1.company}) ↔ ${exp2.title} (${exp2.company})`,
                period: `${Math.max(exp1.start, exp2.start)}-${Math.min(exp1.end, exp2.end)}`
            });
        }
    }
}

if (overlaps.length === 0) {
    console.log("✅ No overlapping roles found");
} else {
    console.log(JSON.stringify(overlaps, null, 2));
}
console.log();

// 5. Role relevance
const jobRole = "Senior Developer";
console.log("📌 Role Relevance for:", jobRole);

let relevanceScore = 0;
const roleSimilarity = [];

experiences.forEach(exp => {
    let score = 0;
    
    // Role-to-role similarity logic
    if (exp.title.includes('Senior')) score = 100;
    else if (exp.title.includes('React')) score = 70;
    else if (exp.title.includes('Junior')) score = 50;
    else score = 30;
    
    roleSimilarity.push({
        title: exp.title,
        company: exp.company,
        duration: `${exp.years} years`,
        similarity: score,
        relevance: score >= 80 ? 'High' : score >= 60 ? 'Medium' : 'Low'
    });
    
    relevanceScore += score * (exp.years / totalYears);
});

console.log(JSON.stringify(roleSimilarity, null, 2));
console.log();

// 6. Final score
const expScore = Math.min((totalYears / 5) * 40, 40);
const relScore = relevanceScore * 0.4;
const finalScore = Math.round(expScore + relScore + 20);

console.log("📌 FINAL EXPERIENCE RELEVANCE SCORE:", finalScore, "/100");
console.log();

// 7. STRUCTURED EXPERIENCE OBJECT (Deliverable)
console.log("📦 DAY 10 DELIVERABLE - Structured Experience Object");
console.log("====================================================");

const structuredExperience = {
    candidate_id: "CAND001",
    target_role: jobRole,
    total_experience_years: totalYears,
    experiences: experiences.map(exp => ({
        role: exp.title,
        company: exp.company,
        from: exp.start,
        to: exp.end === new Date().getFullYear() ? 'Present' : exp.end,
        duration_years: exp.years
    })),
    gaps: gaps,
    overlapping_roles: overlaps,
    role_similarity_analysis: roleSimilarity,
    relevance_score: {
        total: finalScore,
        breakdown: {
            experience_weight: Math.round(expScore),
            role_relevance_weight: Math.round(relScore),
            recency_weight: 20
        }
    },
    recommendation: finalScore >= 70 ? 'Strongly Recommended' : 
                    finalScore >= 50 ? 'Recommended' : 'Needs Review'
};

console.log(JSON.stringify(structuredExperience, null, 2));
console.log("\n✅✅✅ DAY 10 COMPLETED SUCCESSFULLY! ✅✅✅");