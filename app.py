import streamlit as st
import re
import random
import datetime
import spacy
from pdfminer.high_level import extract_text

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = {
    "Data Science": ["python", "machine learning", "pandas", "numpy", "tensorflow", "data analysis"],
    "Web Development": ["html", "css", "javascript", "react", "node", "flask", "django"],
    "Android Development": ["android", "kotlin", "java", "xml"],
    "UI/UX": ["figma", "adobe xd", "photoshop", "sketch"],
}

COURSES = {
    "Data Science": ["Data Science with Python", "Machine Learning A-Z"],
    "Web Development": ["React for Beginners", "Full Stack with Django"],
    "Android Development": ["Android with Kotlin", "Build Apps with Firebase"],
    "UI/UX": ["Figma UI Basics", "UX Design Crash Course"]
}

# --- Project Suggestions by Field ---
PROJECT_IDEAS = {
    "Data Science": [
        "Movie Recommendation System (ML)",
        "E-commerce Sales Dashboard (Tableau/Excel)",
        "Customer Churn Prediction",
        "Stock Price Predictor"
    ],
    "Web Development": [
        "Portfolio Website (HTML/CSS/JS)",
        "Blog Platform (Django/Flask)",
        "E-commerce Store (React/Node)"
    ],
    "Android Development": [
        "Expense Tracker App (Kotlin)",
        "Weather App (Java)",
        "Chat App (Firebase)"
    ],
    "UI/UX": [
        "Mobile App Redesign (Figma)",
        "Landing Page UI (Adobe XD)",
        "User Flow Mapping"
    ]
}

TOOLS_LIST = ["VS Code", "Jupyter", "GitHub", "Excel", "Tableau"]

# Expanded known skills and certifications
KNOWN_SKILLS = set([
    "python", "machine learning", "pandas", "numpy", "tensorflow", "data analysis", "html", "css", "javascript", "react", "node", "flask", "django",
    "android", "kotlin", "java", "xml", "figma", "adobe xd", "photoshop", "sketch", "sql", "powerbi", "tableau", "c++", "c#", "aws", "azure", "gcp", "docker", "kubernetes"
])
CERT_PROVIDERS = ["coursera", "udemy", "aws", "google", "microsoft", "edx", "udacity", "ibm", "oracle", "linkedin learning"]


def extract_text_from_pdf(file):
    return extract_text(file)



def extract_info(text):
    doc = nlp(text)
    emails = re.findall(r"\S+@\S+", text)
    phones = re.findall(r"\+?\d[\d\s]{8,}\d", text)
    # 1. Try to extract name from 'Name:' or similar at the top
    name_match = re.search(r"(?i)^(?:name\s*[:\-]?\s*)([A-Z][a-z]+(?: [A-Z][a-z]+)+)", text[:200])
    if name_match:
        name = name_match.group(1).strip()
    else:
        # 2. Fallback to spaCy NER, but ignore common skills/tech words
        skill_words = set([kw.lower() for kws in SKILL_KEYWORDS.values() for kw in kws] + ["java", "python", "html", "css", "sql", "react", "node", "django", "flask"])
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON" and ent.text.lower() not in skill_words and len(ent.text.split()) <= 3 and len(ent.text.split()) > 1]
        name = names[0].strip() if names else "Not found"
    # Education extraction (degree, institute, year)
    edu_pattern = r"((Bachelor|Master|B\.Sc|M\.Sc|B\.Tech|M\.Tech|PhD|MBA)[^\n\r,;]*?(?:at|from)?\s*([A-Za-z .&'-]+)?\s*(\d{4})?)"
    education = re.findall(edu_pattern, text, re.IGNORECASE)
    education = [f"{deg.strip()} {inst.strip() if inst else ''} {yr.strip() if yr else ''}".strip() for _, deg, inst, yr in education]
    # Skills extraction (from known list and NER)
    all_skills = set()
    for skill in KNOWN_SKILLS:
        if re.search(rf"\\b{re.escape(skill)}\\b", text, re.IGNORECASE):
            all_skills.add(skill)
    # Add NER-based skills (ORG, PRODUCT, etc.)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"] and len(ent.text) < 30:
            all_skills.add(ent.text.lower())
        
    # Certifications extraction (provider keywords)

    certs = []
    for prov in CERT_PROVIDERS:
        certs += re.findall(rf"([\w .-]+(?:{prov})[\w .-]*)", text, re.IGNORECASE)
    certs = list(set(certs))
    # URL extraction
    linkedin = re.findall(r"https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9\-_/]+", text)
    github = re.findall(r"https?://(www\.)?github\.com/[a-zA-Z0-9\-_/]+", text)
    portfolio = re.findall(r"https?://[\w\.-]+\.(me|dev|xyz|site|portfolio|io|com)/[a-zA-Z0-9\-_/]*", text)
    return {
        "name": name,
        "email": emails[0] if emails else "Not found",
        "phone": phones[0] if phones else "Not found",
        "education": education if education else ["Not found"],
        "skills": list(all_skills) if all_skills else ["Not found"],
        "certifications": certs if certs else ["Not found"],
        "linkedin": linkedin[0] if linkedin else "Not found",
        "github": github[0] if github else "Not found",
        "portfolio": portfolio[0][0] if portfolio else "Not found"
    }


def detect_field(skills):
    for field, keywords in SKILL_KEYWORDS.items():
        if any(skill in skills.lower() for skill in keywords):
            return field
    return "General"


# --- Ideal Resume Template ---
IDEAL_SECTIONS = ["objective", "projects", "skills", "education", "experience", "certifications", "contact", "declaration"]
IDEAL_SKILLS = set([kw for kws in SKILL_KEYWORDS.values() for kw in kws])
IDEAL_CERTS = set([prov.title() for prov in CERT_PROVIDERS])

# --- Scoring without Job Description ---
def template_score(text, info):
    # Section completeness
    section_score = int(40 * sum(1 for s in IDEAL_SECTIONS if s in text.lower()) / len(IDEAL_SECTIONS))
    # Skill diversity
    skill_score = int(30 * len([s for s in info['skills'] if s in IDEAL_SKILLS]) / len(IDEAL_SKILLS))
    # Certification diversity
    cert_score = int(15 * len([c for c in info['certifications'] if any(p.lower() in c.lower() for p in CERT_PROVIDERS)]) / len(CERT_PROVIDERS))
    # Education presence
    edu_score = 15 if info['education'] and info['education'][0] != 'Not found' else 0
    return section_score + skill_score + cert_score + edu_score

# --- Resume Clarity Helper ---
def clarity_score(text):
    # Metrics: presence of numbers/percentages, bullet points, concise sentences
    metrics = 0
    if any(x in text for x in ["%", "percent", "improved", "reduced", "increased", "decreased"]):
        metrics += 1
    if "•" in text or "- " in text:
        metrics += 1
    if len([s for s in text.split(". ") if len(s) < 120]) > 3:
        metrics += 1
    return int((metrics / 3) * 15)  # up to 15 points for clarity

# --- YouTube Video Recommendation ---
YOUTUBE_VIDEO = {
    "title": "How to Make a Resume Stand Out in 2024 (5 Tips)",
    "summary": "A concise guide to making your resume stand out with actionable tips and real examples.",
    "url": "https://www.youtube.com/watch?v=Qb1b1s4A4gI"
}

# --- Relevant/Irrelevant Courses/Certs ---
def classify_courses_certs(info, field):
    relevant_courses = [c for c in COURSES.get(field, []) if any(kw in c.lower() for kw in info['skills'])]
    irrelevant_courses = [c for c in COURSES.get(field, []) if c not in relevant_courses]
    relevant_certs = [c for c in info['certifications'] if any(p in c.lower() for p in CERT_PROVIDERS if p in field.lower() or p in ' '.join(info['skills']).lower())]
    irrelevant_certs = [c for c in info['certifications'] if c not in relevant_certs]
    return relevant_courses, irrelevant_courses, relevant_certs, irrelevant_certs

# --- Suggest Missing from Template ---
def suggest_missing(info, text):
    missing_sections = [s for s in IDEAL_SECTIONS if s not in text.lower()]
    missing_skills = [s for s in IDEAL_SKILLS if s not in [sk.lower() for sk in info['skills']]]
    missing_certs = [p.title() for p in CERT_PROVIDERS if not any(p in c.lower() for c in info['certifications'])]
    return missing_sections, missing_skills, missing_certs


# Recommend missing skills for the predicted field

def recommend_skills(extracted_skills, field):
    if field in SKILL_KEYWORDS:
        missing = [kw for kw in SKILL_KEYWORDS[field] if kw not in [s.lower() for s in extracted_skills]]
        return missing
    return []


# --- NLP-based keyword extraction ---
def extract_keywords(text):
    doc = nlp(text)
    # Use noun chunks and named entities as keywords
    keywords = set()
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 2:
            keywords.add(chunk.text.strip().lower())
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "GPE", "PERSON", "SKILL", "WORK_OF_ART", "EVENT"]:
            keywords.add(ent.text.strip().lower())
    # Add unique words longer than 4 chars (excluding stopwords)
    for token in doc:
        if not token.is_stop and not token.is_punct and len(token.text) > 4:
            keywords.add(token.text.strip().lower())
    return keywords


# --- Course Relevance Helper ---
def course_relevance(course, missing_skills):
    for skill in missing_skills:
        if skill.lower() in course.lower():
            return "✅ Strongly Recommended"
    if any(word in course.lower() for word in ["crash", "introduction", "beginner"]):
        return "✅ Add after completion"
    return "✅ Must Have"


# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Resume Analyzer | Smart Feedback",
    page_icon="🧑‍💼",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Custom CSS for Neatness ---
st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa;}
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
    }
    .st-bb {border-bottom: 2px solid #e0e0e0; margin: 1.5em 0 1em 0;}
    .st-section {padding: 1em 1.5em; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #e0e0e0; margin-bottom: 1.5em;}
    .st-emoji {font-size: 1.3em; margin-right: 0.3em;}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Icon URLs ---
ICON_RESUME = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
ICON_SKILLS = "https://cdn-icons-png.flaticon.com/512/1055/1055687.png"
ICON_CERT = "https://cdn-icons-png.flaticon.com/512/190/190411.png"
ICON_PROJECT = "https://cdn-icons-png.flaticon.com/512/906/906175.png"
ICON_VIDEO = "https://cdn-icons-png.flaticon.com/512/1384/1384060.png"
ICON_SUGGEST = "https://cdn-icons-png.flaticon.com/512/1828/1828884.png"
ICON_FEEDBACK = "https://cdn-icons-png.flaticon.com/512/1828/1828919.png"

# --- UI: Multiple Resume Uploads ---
st.title("🧑‍💼 Resume Analyzer")
st.markdown("<div class='st-bb'></div>", unsafe_allow_html=True)
st.markdown("<h4>Upload your resume(s) and get instant, actionable feedback! 🚀</h4>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("📤 Upload Resume(s) (PDF)", type=["pdf"], accept_multiple_files=True)
st.markdown("<div class='st-bb'></div>", unsafe_allow_html=True)
job_desc = st.text_area("📝 Paste Job Description Here (optional)", "", height=150)
st.markdown("<div class='st-bb'></div>", unsafe_allow_html=True)

if uploaded_files:
    cols = st.columns(len(uploaded_files))
    for idx, uploaded in enumerate(uploaded_files):
        with cols[idx]:
            st.markdown(f"<div class='st-section'>", unsafe_allow_html=True)
            st.image(ICON_RESUME, width=48)
            st.markdown(f"### 📄 <span class='st-emoji'>Resume {idx+1}</span>", unsafe_allow_html=True)
            with open(f"temp_resume_{idx}.pdf", "wb") as f:
                f.write(uploaded.read())
            text = extract_text_from_pdf(f"temp_resume_{idx}.pdf")
            info = extract_info(text)
            field = detect_field(text)

            # --- Extracted Info Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("🔍 Extracted Info")
                st.image(ICON_FEEDBACK, width=32)
                st.write(f"👤 **Name:** {info['name']}")
                st.write(f"✉️ **Email:** {info['email']}")
                st.write(f"📞 **Phone:** {info['phone']}")
                st.write(f"🎓 **Education:** {', '.join(info['education'])}")
                st.write(f"🛠️ **Skills:** {', '.join(info['skills'])}")
                st.write(f"📄 **Certifications:** {', '.join(info['certifications'])}")
                st.write(f"🔗 **LinkedIn:** {info['linkedin']}")
                st.write(f"🐙 **GitHub:** {info['github']}")
                st.write(f"🌐 **Portfolio:** {info['portfolio']}")
                st.write(f"💼 **Predicted Field:** {field}")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Resume Score Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                tscore = template_score(text, info)
                cscore = clarity_score(text)
                resume_score = min(100, tscore + cscore)
                st.subheader(f"📊 Resume Score: {resume_score}/100")
                st.image(ICON_FEEDBACK, width=32)
                st.progress(resume_score)
                if resume_score >= 80:
                    st.success("Great job! Your resume is strong.")
                elif resume_score >= 60:
                    st.info("Good resume, but there are areas to improve.")
                else:
                    st.warning("Consider improving your resume for better results.")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Strengths & Areas for Improvement Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.markdown("<span class='st-emoji'>👍</span> <b>Strengths:</b>", unsafe_allow_html=True)
                st.image(ICON_SUGGEST, width=28)
                strengths = []
                if 'contact' in text.lower(): strengths.append("Clean layout, contact info present")
                if any(s in [sk.lower() for sk in info['skills']] for s in ["python", "ml", "machine learning"]): strengths.append("Technical terms like 'Python', 'ML' appear")
                if 'projects' in text.lower(): strengths.append("Projects section included")
                for s in strengths:
                    st.markdown(f"• {s}")
                st.markdown("<span class='st-emoji'>👎</span> <b>Areas for Improvement:</b>", unsafe_allow_html=True)
                st.markdown("• Did You Know? Adding actionable metrics (e.g. 'Improved X by 20%') increases readability")
                st.markdown("• Tip: Add a 'Projects' section with 2–3 real-world examples")
                if info['linkedin'] == 'Not found':
                    st.markdown("• Tip: Add your LinkedIn URL")
                if 'certifications' not in text.lower():
                    st.markdown("• Tip: Include a 'Certifications' section")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Missing Skills & Recommended Courses Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("✅ Missing Skills & Recommended Courses:")
                st.image(ICON_SKILLS, width=32)
                for skill in IDEAL_SKILLS:
                    if skill in [sk.lower() for sk in info['skills']]:
                        st.markdown(f"{skill.title()} – Already present ✅")
                    else:
                        course = next((c for c in sum(COURSES.values(), []) if skill in c.lower()), None)
                        if course:
                            st.markdown(f"{skill.title()} – Missing -> Take '{course}' ✔️")
                        else:
                            st.markdown(f"{skill.title()} – Missing")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Certifications Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("📚 Certifications to Include or Remove:")
                st.image(ICON_CERT, width=32)
                for cert in info['certifications']:
                    if any(p in cert.lower() for p in CERT_PROVIDERS):
                        st.markdown(f"'{cert}' – Should keep")
                    else:
                        st.markdown(f"'{cert}' – Remove (irrelevant to tech roles)")
                for cert in [p.title() for p in CERT_PROVIDERS if not any(p in c.lower() for c in info['certifications'])]:
                    st.markdown(f"'{cert}' – Add if completed")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Project Ideas Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("🛠️ Project Ideas to Add:")
                st.image(ICON_PROJECT, width=32)
                suggested_projects = [p for p in PROJECT_IDEAS.get(field, []) if p.lower() not in text.lower()]
                extra_projects = [
                    "Build a sentiment analysis app with Twitter API",
                    "Movie recommendation engine with Python + ML",
                    "Portfolio website using HTML/CSS/JS"
                ]
                for proj in suggested_projects + extra_projects:
                    st.markdown(f"- {proj}")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Final Suggestions Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("🎯 Final Suggestions:")
                st.image(ICON_SUGGEST, width=32)
                if info['linkedin'] == 'Not found':
                    st.markdown("Add LinkedIn URL")
                st.markdown("Use bullet metrics like 'Reduced process time by 30%'")
                if 'certifications' not in text.lower():
                    st.markdown("Include a 'Certifications' section")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- YouTube Video Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("🎥 Bonus Video:")
                st.image(ICON_VIDEO, width=32)
                st.write(f"**{YOUTUBE_VIDEO['title']}**")
                st.write(YOUTUBE_VIDEO['summary'])
                st.markdown(f"[▶️ Watch here]({YOUTUBE_VIDEO['url']})")
                st.markdown("</div>", unsafe_allow_html=True)

            st.success("✅ Analysis complete!")
            st.balloons()
            st.markdown("</div>", unsafe_allow_html=True)
