"""
CareerPilot AI - Resume Evaluator Module
Multidimensional evaluation engine calculating ATS Compatibility, Resume Quality, Job Match, and Overall Readiness Scores.
Identifies weak action verbs, metric counts, recruiter red flags, priority improvement plans, and before/after bullet suggestions.
"""

import re
from typing import Dict, Any, List, Tuple


class ResumeEvaluator:
    """Core evaluation engine for Resume ATS & Quality Intelligence."""

    # Role Skill Mapping Profiles
    ROLE_PROFILES = {
        "Data Analyst": {
            "required": ["SQL", "Excel", "Python", "Power BI", "Tableau", "Statistics", "Data Visualization"],
            "preferred": ["Pandas", "NumPy", "ETL", "Data Cleaning", "R", "SQL Server", "PostgreSQL"],
            "keywords": ["sql", "excel", "power bi", "tableau", "statistics", "visualization", "data analysis", "reporting", "dashboard", "metrics"]
        },
        "Data Scientist": {
            "required": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "NumPy", "Scikit-Learn"],
            "preferred": ["Deep Learning", "TensorFlow", "PyTorch", "NLP", "Big Data", "Spark", "Data Pipelines"],
            "keywords": ["python", "sql", "machine learning", "statistics", "scikit-learn", "deep learning", "model", "prediction", "feature engineering"]
        },
        "AI/ML Engineer": {
            "required": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "NLP", "SQL"],
            "preferred": ["Docker", "MLOps", "Computer Vision", "REST API", "Git", "Model Deployment", "FastAPI"],
            "keywords": ["python", "machine learning", "deep learning", "pytorch", "tensorflow", "nlp", "model deployment", "transformers", "opencv"]
        },
        "Software Engineer": {
            "required": ["Data Structures", "Algorithms", "Java", "Python", "C++", "SQL", "Git", "OOP"],
            "preferred": ["DBMS", "Operating Systems", "Computer Networks", "Docker", "REST API", "CI/CD"],
            "keywords": ["dsa", "data structures", "algorithms", "java", "python", "sql", "git", "oop", "system design", "rest api"]
        },
        "Full Stack Developer": {
            "required": ["JavaScript", "HTML", "CSS", "React", "Node.js", "SQL", "Git", "REST API"],
            "preferred": ["TypeScript", "Next.js", "MongoDB", "Express", "Docker", "AWS", "Tailwind CSS"],
            "keywords": ["javascript", "react", "node.js", "html", "css", "sql", "rest api", "frontend", "backend", "full stack"]
        },
        "Backend Developer": {
            "required": ["Python", "Java", "Node.js", "SQL", "REST API", "Database Design", "Git"],
            "preferred": ["PostgreSQL", "Redis", "Docker", "Microservices", "Kafka", "Django", "Spring Boot"],
            "keywords": ["python", "java", "sql", "rest api", "backend", "postgresql", "database", "microservices", "docker"]
        },
        "Frontend Developer": {
            "required": ["JavaScript", "HTML", "CSS", "React", "TypeScript", "UI/UX", "Git"],
            "preferred": ["Next.js", "Redux", "Tailwind CSS", "Vue", "Web Performance", "REST API"],
            "keywords": ["javascript", "react", "html", "css", "typescript", "frontend", "ui/ux", "responsive", "redux"]
        },
        "Business Analyst": {
            "required": ["Excel", "SQL", "Business Requirements", "Data Analysis", "Power BI", "Documentation"],
            "preferred": ["Jira", "Agile", "Process Mapping", "Tableau", "UML", "Stakeholder Management"],
            "keywords": ["excel", "sql", "requirements", "business analysis", "power bi", "documentation", "stakeholder", "process", "agile"]
        },
        "Cloud Engineer": {
            "required": ["AWS", "Azure", "Linux", "Docker", "Networking", "Python", "Git"],
            "preferred": ["Kubernetes", "Terraform", "CI/CD", "Ansible", "Cloud Security", "Bash"],
            "keywords": ["aws", "azure", "cloud", "linux", "docker", "kubernetes", "terraform", "ci/cd", "networking"]
        },
        "Cybersecurity Analyst": {
            "required": ["Network Security", "Ethical Hacking", "Linux", "SIEM", "Python", "Vulnerability Assessment"],
            "preferred": ["Wireshark", "Firewalls", "SOC", "Incident Response", "CISSP", "Cryptography"],
            "keywords": ["cybersecurity", "security", "linux", "siem", "ethical hacking", "vulnerability", "firewall", "network security"]
        },
        "Product Analyst": {
            "required": ["Excel", "SQL", "Product Analytics", "A/B Testing", "Python", "Google Analytics"],
            "preferred": ["Mixpanel", "Amplitude", "User Metrics", "Data Visualization", "Product Roadmap"],
            "keywords": ["product", "analytics", "sql", "excel", "a/b testing", "user retention", "funnel", "metrics", "dashboard"]
        }
    }

    WEAK_ACTION_VERBS = ["worked", "helped", "did", "made", "responsible for", "participated", "assisted", "handled", "involved in"]
    STRONG_ACTION_VERBS = [
        "developed", "engineered", "designed", "architected", "automated", "optimized", "built", "deployed",
        "implemented", "analyzed", "spearheaded", "accelerated", "crafted", "integrated", "transformed"
    ]

    @classmethod
    def evaluate_all(
        cls,
        text: str,
        metadata: Dict[str, Any],
        contact: Dict[str, Any],
        sections: Dict[str, Any],
        completeness_score: float,
        target_role: str = "Software Engineer",
        job_description: str = "",
        target_company: str = "General Placement"
    ) -> Dict[str, Any]:
        """Runs comprehensive evaluation and produces json structures and subscores."""

        lowered_text = text.lower()
        extracted_skills = sections.get("extracted_skills", [])

        # 1. Job Match & Keyword Analysis
        role_profile = cls.ROLE_PROFILES.get(target_role, cls.ROLE_PROFILES["Software Engineer"])
        
        # If Job Description is provided, extract custom keywords from JD
        jd_keywords = []
        if job_description and len(job_description.strip()) > 20:
            jd_words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())
            freq = {}
            for w in jd_words:
                if w not in {"the", "and", "for", "with", "that", "this", "from", "you", "are", "have", "will"}:
                    freq[w] = freq.get(w, 0) + 1
            jd_keywords = [w for w, c in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:25]]

        target_keywords = list(set(role_profile["keywords"] + jd_keywords))
        
        found_keywords = []
        partial_keywords = []
        missing_keywords = []

        for kw in target_keywords:
            pattern = r'(?<![a-zA-Z0-9#+])' + re.escape(kw.lower()) + r'(?![a-zA-Z0-9#+])'
            if re.search(pattern, lowered_text):
                found_keywords.append(kw.title())
            elif any(kw[:4] in sk.lower() for sk in extracted_skills if len(kw) >= 4):
                partial_keywords.append(kw.title())
            else:
                missing_keywords.append(kw.title())

        top_10_to_add = missing_keywords[:10]
        
        # Calculate Keyword Match % and Skill Match %
        total_kw = max(1, len(target_keywords))
        keyword_match_pct = round(((len(found_keywords) + len(partial_keywords) * 0.5) / total_kw) * 100, 1)

        req_skills = role_profile["required"]
        matched_req = [s for s in req_skills if any(s.lower() in sk.lower() for sk in extracted_skills)]
        skill_match_pct = round((len(matched_req) / max(1, len(req_skills))) * 100, 1)

        # 2. Skill Gap Analysis & Integration
        high_gap = [s for s in req_skills if s not in matched_req]
        med_gap = [s for s in role_profile["preferred"] if not any(s.lower() in sk.lower() for sk in extracted_skills)][:3]
        low_gap = [kw for kw in missing_keywords if kw not in high_gap and kw not in med_gap][:3]

        skills_analysis = {
            "target_role": target_role,
            "skill_match_pct": skill_match_pct,
            "required_skills": req_skills,
            "matched_required": matched_req,
            "high_priority_gaps": high_gap,
            "medium_priority_gaps": med_gap,
            "low_priority_gaps": low_gap,
            "learning_recommendations": [f"Learn {sk} to satisfy core requirements for {target_role}." for sk in high_gap[:3]]
        }

        # 3. Action Verbs & Bullets Quality Analysis
        bullets = [line.strip() for line in text.split('\n') if len(line.strip()) > 25 and (line.strip().startswith(('•', '-', '*')) or line.strip()[0].isupper())]
        
        weak_verbs_found = []
        strong_verbs_found = []
        metrics_count = 0
        before_after_suggestions = []

        for b in bullets:
            b_lower = b.lower()
            # Metric detection regex (percentages, dollar amounts, multipliers, numbers)
            if re.search(r'(\d+%\s*|\$\d+|\d+\+|\d+x|\b\d+\b\s*(users|clients|time|reduction|growth|accuracy|speed|records))', b_lower):
                metrics_count += 1

            # Check weak verbs
            for wv in cls.WEAK_ACTION_VERBS:
                if b_lower.startswith(wv) or f" {wv} " in b_lower:
                    weak_verbs_found.append(wv)
                    suggested_verb = cls.STRONG_ACTION_VERBS[hash(b) % len(cls.STRONG_ACTION_VERBS)]
                    clean_b = re.sub(r'^[•\-\*\s]*(?:worked on|helped with|responsible for|participated in|assisted with|handled|involved in|did|made)\s*', '', b, flags=re.IGNORECASE).strip()
                    suggested_b = f"{suggested_verb.capitalize()} {clean_b} [Note: Add a verifiable metric if applicable]"
                    before_after_suggestions.append({
                        "current": b,
                        "suggested": suggested_b,
                        "reason": f"Replaced weak phrasing '{wv}' with impact action verb '{suggested_verb.capitalize()}'."
                    })
                    break

            # Check strong verbs
            for sv in cls.STRONG_ACTION_VERBS:
                if b_lower.startswith(sv) or f" {sv} " in b_lower:
                    strong_verbs_found.append(sv)
                    break

        bullets_analysis = {
            "total_bullets_analyzed": len(bullets),
            "weak_verbs_found": list(set(weak_verbs_found)),
            "strong_verbs_found": list(set(strong_verbs_found)),
            "metrics_count": metrics_count,
            "metric_presence_pct": round((metrics_count / max(1, len(bullets))) * 100, 1),
            "before_after_suggestions": before_after_suggestions[:5]
        }

        # 4. Project Analyzer & Tech Extraction
        project_score = 85.0 if sections.get("sections_found", {}).get("projects") else 40.0
        if any("github.com" in line.lower() for line in text.split('\n')):
            project_score += 10.0
        project_score = min(100.0, project_score)

        project_analysis = {
            "project_strength_score": project_score,
            "extracted_tech_stack": extracted_skills,
            "suggestions": [
                "Mention quantifiable metrics (e.g. accuracy %, performance improvement, latency reduction).",
                "Include GitHub or live deployment links for each major project."
            ] if project_score < 90 else ["Project section is well-structured with clear technical context."]
        }

        # 5. Formatting & Language Quality
        page_count = metadata.get("page_count", 1)
        word_count = metadata.get("word_count", 200)

        formatting_risks = []
        if metadata.get("has_tables"):
            formatting_risks.append("Tables detected: Some traditional ATS parsers struggle to read table contents accurately.")
        if page_count > 2:
            formatting_risks.append(f"Length warning: Document is {page_count} pages. For freshers/early career candidates, 1-2 pages is recommended.")
        if word_count < 200:
            formatting_risks.append("Low word count: Document appears brief. Elaborate on projects and technical experience.")

        formatting_score = max(50.0, 100.0 - (len(formatting_risks) * 15.0))
        language_score = 90.0 if len(weak_verbs_found) <= 2 else max(60.0, 90.0 - (len(weak_verbs_found) * 5.0))

        # 6. Recruiter Red Flags & Strengths
        red_flags = []
        strengths = []

        if not contact.get("github") and target_role in ["Software Engineer", "Full Stack Developer", "Backend Developer", "Frontend Developer", "AI/ML Engineer"]:
            red_flags.append("Missing GitHub profile link for technical candidate profile.")
        if metrics_count == 0:
            red_flags.append("No quantifiable metrics or measurable outcomes found in experience/projects.")
        if not sections.get("sections_found", {}).get("summary"):
            red_flags.append("Missing target-focused professional summary section.")
        if len(weak_verbs_found) >= 3:
            red_flags.append(f"Multiple passive action verbs detected ({', '.join(weak_verbs_found[:3])}).")

        if len(extracted_skills) >= 6:
            strengths.append(f"Diverse technical skill profile ({len(extracted_skills)} tools/frameworks detected).")
        if contact.get("linkedin"):
            strengths.append("LinkedIn profile link included for recruiter verification.")
        if sections.get("sections_found", {}).get("projects"):
            strengths.append("Dedicated projects section highlighting practical software application.")
        if completeness_score >= 80:
            strengths.append("High resume structural completeness score.")

        # 7. Priority Improvement Plan ("Fix These First")
        priority_plan = {
            "high_priority": [
                f"Add missing core skills for {target_role}: {', '.join(high_gap[:3])}." if high_gap else "Add GitHub portfolio link to demonstrate technical codebase.",
                "Incorporate measurable outcomes (%, $, time saved, user scale) into project bullet points."
            ],
            "medium_priority": [
                "Replace weak/passive action verbs with strong impact verbs (e.g., Developed, Engineered, Automated).",
                "Ensure date formats are standardized across education and experience sections."
            ],
            "low_priority": [
                "Fine-tune professional summary to directly address target role keywords.",
                "Verify standard single/double column layout for optimal ATS readability."
            ]
        }

        # 8. Calculating 3 Sub-scores and Overall Readiness Score
        ats_score = min(100.0, round(0.4 * keyword_match_pct + 0.3 * formatting_score + 0.3 * completeness_score, 1))
        raw_quality = round(0.35 * (bullets_analysis["metric_presence_pct"] + 40) + 0.35 * project_score + 0.3 * language_score, 1)
        quality_score = min(100.0, raw_quality)
        job_match_score = min(100.0, round(0.5 * skill_match_pct + 0.5 * keyword_match_pct, 1))
        
        overall_readiness_score = min(100.0, round(0.25 * ats_score + 0.35 * quality_score + 0.40 * job_match_score, 1))

        # 9. Recruiter First Impression Synthesis
        recruiter_impression = (
            f"Candidate displays a viable technical profile for '{target_role}' with a strong foundation in "
            f"{', '.join(extracted_skills[:4]) if extracted_skills else 'core software principles'}. "
            f"ATS compatibility is solid ({ats_score}/100), but recruiter impact can be significantly boosted by "
            f"addressing missing role keywords ({', '.join(top_10_to_add[:3]) if top_10_to_add else 'advanced topics'}) "
            f"and adding quantifiable metric outcomes to project bullet points."
        )

        summary_rewrite = (
            f"Results-oriented {target_role} proficient in {', '.join(extracted_skills[:5]) if extracted_skills else 'software development'}. "
            f"Demonstrated experience in building robust applications, optimizing technical workflows, and delivering quality projects. "
            f"Targeting growth-focused opportunities in software engineering and data systems."
        )

        return {
            "scores": {
                "overall_score": min(100.0, overall_readiness_score),
                "ats_score": min(100.0, ats_score),
                "quality_score": min(100.0, quality_score),
                "job_match_score": min(100.0, job_match_score),
                "completeness_score": completeness_score
            },
            "parsed_data": {
                "contact": contact,
                "sections": sections,
                "extracted_skills": extracted_skills,
                "metadata": metadata
            },
            "keyword_analysis": {
                "found": found_keywords,
                "partial": partial_keywords,
                "missing": missing_keywords,
                "top_10_to_add": top_10_to_add,
                "keyword_match_pct": keyword_match_pct
            },
            "skills_analysis": skills_analysis,
            "bullets_analysis": bullets_analysis,
            "project_analysis": project_analysis,
            "red_flags": red_flags,
            "strengths": strengths,
            "priority_plan": priority_plan,
            "formatting": {
                "score": formatting_score,
                "risks": formatting_risks,
                "page_count": page_count,
                "word_count": word_count
            },
            "language": {
                "score": language_score,
                "weak_verbs_count": len(weak_verbs_found)
            },
            "recruiter_impression": recruiter_impression,
            "summary_rewrite": summary_rewrite
        }
