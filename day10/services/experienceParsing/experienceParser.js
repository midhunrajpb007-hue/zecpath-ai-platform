// experienceParser.js - Day 10
// Extract experience from resume text

function parseExperience(resumeText) {
    const experiences = [];
    const lines = resumeText.split('\n');
    
    lines.forEach(line => {
        // Look for job titles
        if (line.includes('Developer') || line.includes('Engineer')) {
            
            // Extract company name
            let company = '';
            if (line.includes('at')) {
                company = line.split('at')[1].split('(')[0].trim();
            }
            
            // Extract job title
            let title = line.split('at')[0].trim();
            
            // Extract dates (2020-2023)
            const dateMatch = line.match(/(\d{4})\s*[-–]\s*(\d{4}|Present)/i);
            
            if (dateMatch) {
                const startYear = parseInt(dateMatch[1]);
                const endYear = dateMatch[2].toLowerCase() === 'present' 
                    ? new Date().getFullYear() 
                    : parseInt(dateMatch[2]);
                
                const years = endYear - startYear;
                
                experiences.push({
                    title: title,
                    company: company,
                    startDate: startYear,
                    endDate: dateMatch[2],
                    years: years,
                    months: years * 12
                });
            }
        }
    });
    
    return experiences;
}

function calculateTotalExperience(experiences) {
    let totalYears = 0;
    experiences.forEach(exp => {
        totalYears += exp.years;
    });
    
    return {
        years: totalYears,
        months: totalYears * 12
    };
}

function calculateRelevance(experiences, jobRole) {
    const roleKeywords = {
        'frontend': ['react', 'angular', 'vue', 'html', 'css'],
        'backend': ['node', 'python', 'java', 'database'],
        'fullstack': ['react', 'node', 'mongodb', 'express'],
        'mern': ['mongodb', 'express', 'react', 'node'],
        'senior': ['lead', 'senior', 'architect'],
        'junior': ['junior', 'trainee', 'intern']
    };
    
    const relevance = [];
    const jobLower = jobRole.toLowerCase();
    
    experiences.forEach(exp => {
        let score = 50; // Base score
        const titleLower = exp.title.toLowerCase();
        
        // Exact match
        if (titleLower.includes(jobLower)) {
            score = 100;
        }
        // Partial match
        else {
            Object.keys(roleKeywords).forEach(key => {
                if (jobLower.includes(key) && titleLower.includes(key)) {
                    score += 30;
                }
            });
        }
        
        // Cap at 100
        score = Math.min(score, 100);
        
        relevance.push({
            title: exp.title,
            company: exp.company,
            duration: `${exp.years} years`,
            relevanceScore: score
        });
    });
    
    return relevance;
}

module.exports = {
    parseExperience,
    calculateTotalExperience,
    calculateRelevance
};