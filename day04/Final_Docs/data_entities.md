# AI Data Entity Design Document

## 1. Candidate Profile Entity
| Field | Type | Description |
|-------|------|-------------|
| personal_info | object | name, email, phone |
| skills | array | List of skills |
| experience | array | Work history |
| education | array | Academic background |
| certifications | array | Professional certs |

## 2. Job Profile Entity
| Field | Type | Description |
|-------|------|-------------|
| job_id | string | Unique job ID |
| title | string | Job title |
| company | string | Company name |
| required_skills | array | Must-have skills |
| preferred_skills | array | Nice-to-have skills |
| min_experience | number | Minimum years |
| education_required | string | Degree needed |

## 3. Skill Object
| Field | Type | Description |
|-------|------|-------------|
| name | string | Skill name |
| category | string | Tech/Business/Creative |
| confidence | number | 0-100 score |

## 4. Experience Object
| Field | Type | Description |
|-------|------|-------------|
| company | string | Employer name |
| role | string | Job title |
| start_date | string | Start date |
| end_date | string | End date |
| duration | string | Total experience |
| responsibilities | array | Key achievements |
