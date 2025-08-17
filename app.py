import streamlit as st
import re
import random
import datetime
import spacy
<<<<<<< HEAD
import fitz  # PyMuPDF for better PDF extraction (fitz is the module name for PyMuPDF)
from difflib import SequenceMatcher
import docx  # For .docx support

nlp = spacy.load("en_core_web_sm")

# --- Enhanced PDF Text Extraction ---
def extract_text_from_pdf(file_path):
    """Improved PDF text extraction using PyMuPDF"""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from .docx files"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_from_file(file_path, file_type):
    """Extract text based on file type"""
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "docx":
        return extract_text_from_docx(file_path)
    else:
        return ""

# --- Enhanced Skill Keywords with Synonyms and Abbreviations ---
SKILL_KEYWORDS = {
    "Data Science": [
        "python", "machine learning", "pandas", "numpy", "tensorflow", "data analysis",
        "scikit-learn", "sklearn", "jupyter", "matplotlib", "seaborn", "plotly",
        "sql", "postgresql", "mysql", "mongodb", "spark", "hadoop", "kafka",
        "powerbi", "tableau", "excel", "r", "statistics", "regression", "classification",
        "clustering", "nlp", "natural language processing", "deep learning", "neural networks"
    ],
    "Web Development": [
        "html", "css", "javascript", "js", "react", "vue", "angular", "node", "nodejs",
        "flask", "django", "express", "mongodb", "mysql", "postgresql", "rest api",
        "graphql", "typescript", "ts", "bootstrap", "tailwind", "sass", "less",
        "webpack", "babel", "npm", "yarn", "git", "github", "docker", "kubernetes"
    ],
    "Android Development": [
        "android", "kotlin", "java", "xml", "gradle", "android studio", "firebase",
        "room database", "retrofit", "okhttp", "glide", "picasso", "jetpack compose",
        "material design", "mvvm", "mvp", "dagger", "hilt", "coroutines", "flow"
    ],
    "UI/UX": [
        "figma", "adobe xd", "photoshop", "sketch", "invision", "protopie", "framer",
        "wireframing", "prototyping", "user research", "usability testing", "design systems",
        "responsive design", "accessibility", "wcag", "user personas", "journey mapping"
    ],
    "Artificial Intelligence": [
        "deep learning", "neural networks", "nlp", "bert", "transformers", "pytorch", "keras",
        "tensorflow", "opencv", "computer vision", "cnn", "rnn", "lstm", "gru", "gan",
        "reinforcement learning", "q-learning", "openai", "gpt", "chatgpt", "langchain"
    ],
    "Cybersecurity": [
        "network security", "penetration testing", "pen testing", "firewalls", "siem",
        "vulnerability assessment", "encryption", "ssl", "tls", "wireshark", "nmap",
        "metasploit", "burp suite", "owasp", "ethical hacking", "ceh", "comptia security+",
        "cryptography", "hash functions", "digital signatures", "vpn", "ids", "ips"
    ],
    "Cloud Computing": [
        "aws", "amazon web services", "azure", "gcp", "google cloud", "cloud", "devops",
        "docker", "kubernetes", "k8s", "ci/cd", "jenkins", "gitlab", "github actions",
        "terraform", "ansible", "serverless", "lambda", "ec2", "s3", "rds", "vpc",
        "load balancer", "auto scaling", "cloudformation", "cloudwatch"
    ],
    "Software Development": [
        "c++", "cpp", "java", "python", "oop", "object oriented programming", "git",
        "algorithms", "data structures", "leetcode", "hackerrank", "design patterns",
        "microservices", "api", "rest", "graphql", "testing", "unit testing", "integration testing",
        "tdd", "bdd", "agile", "scrum", "kanban", "jira", "confluence"
    ],
    "Business Analyst": [
        "business analysis", "requirement gathering", "process modeling", "sql", "excel",
        "powerbi", "tableau", "jira", "confluence", "user stories", "use cases",
        "bpmn", "uml", "data modeling", "er diagrams", "stakeholder management",
        "gap analysis", "swot analysis", "root cause analysis"
    ],
    "Product Management": [
        "roadmap", "product strategy", "user stories", "agile", "scrum", "market research",
        "competitive analysis", "user personas", "journey mapping", "a/b testing",
        "analytics", "google analytics", "mixpanel", "amplitude", "jira", "confluence",
        "figma", "prototyping", "mvp", "minimum viable product"
    ],
    "Mobile App Development": [
        "android", "ios", "swift", "kotlin", "flutter", "react native", "xamarin",
        "mobile development", "app store", "google play", "firebase", "push notifications",
        "in-app purchases", "mobile ui", "responsive design", "cross platform"
    ],
    "Game Development": [
        "unity", "unreal", "c#", "game design", "3d modeling", "physics engine",
        "blender", "maya", "3ds max", "game mechanics", "level design", "character design",
        "animation", "rigging", "texturing", "shaders", "game physics", "ai in games"
    ],
    "Finance": [
        "accounting", "financial analysis", "excel", "valuation", "markets", "investment",
        "portfolio management", "risk management", "derivatives", "options", "futures",
        "bonds", "stocks", "mutual funds", "etf", "financial modeling", "dcf", "npv", "irr"
    ],
    "HR": [
        "recruitment", "onboarding", "payroll", "employee engagement", "hrms", "compliance",
        "performance management", "talent acquisition", "employee relations", "benefits",
        "compensation", "training", "development", "diversity", "inclusion", "workplace culture"
    ],
    "Digital Marketing": [
        "seo", "search engine optimization", "sem", "search engine marketing", "google analytics",
        "content marketing", "social media", "email marketing", "ppc", "google ads",
        "facebook ads", "instagram ads", "linkedin ads", "conversion optimization",
        "landing pages", "a/b testing", "marketing automation", "hubspot", "mailchimp"
    ],
    "Blockchain": [
        "blockchain", "bitcoin", "ethereum", "solidity", "smart contracts", "web3",
        "defi", "decentralized finance", "nft", "non-fungible tokens", "cryptocurrency",
        "hyperledger", "consensus algorithms", "proof of work", "proof of stake",
        "metamask", "ipfs", "interplanetary file system"
    ],
    "DevOps": [
        "devops", "ci/cd", "continuous integration", "continuous deployment", "jenkins",
        "gitlab ci", "github actions", "docker", "kubernetes", "terraform", "ansible",
        "prometheus", "grafana", "elk stack", "elasticsearch", "logstash", "kibana",
        "monitoring", "logging", "infrastructure as code", "iac"
    ],
    "UI/UX Design": [
        "ui design", "ux design", "user interface", "user experience", "figma", "sketch",
        "adobe xd", "invision", "prototyping", "wireframing", "user research",
        "usability testing", "design systems", "responsive design", "mobile design",
        "accessibility", "wcag", "user personas", "journey mapping"
    ],
    "AR/VR": [
        "augmented reality", "virtual reality", "ar", "vr", "unity", "unreal engine",
        "oculus", "htc vive", "hololens", "3d modeling", "blender", "maya",
        "spatial computing", "mixed reality", "mr", "computer vision", "tracking"
    ],
    "IoT": [
        "internet of things", "iot", "raspberry pi", "arduino", "sensors", "mqtt",
        "coap", "edge computing", "fog computing", "embedded systems", "microcontrollers",
        "wireless protocols", "bluetooth", "wifi", "zigbee", "lorawan", "nb-iot"
    ]
}

# --- Courses by Field ---
COURSES = {
    "Data Science": [
        "Data Science with Python – IBM (Coursera)",
        "Machine Learning A-Z – Udemy",
        "Python for Data Science – DataCamp",
        "SQL for Data Analysis – Mode Analytics",
        "Statistics for Data Science – Coursera",
        "Deep Learning Specialization – DeepLearning.AI (Coursera)"
    ],
    "Web Development": [
        "React for Beginners – Udemy",
        "Full Stack with Django – Udemy",
        "JavaScript Complete Guide – Udemy",
        "Node.js Bootcamp – Udemy",
        "MongoDB Complete Course – Udemy",
        "Git & GitHub Crash Course – Udemy"
    ],
    "Android Development": [
        "Android with Kotlin – Udemy",
        "Build Apps with Firebase – Udemy",
        "Android App Development – Coursera",
        "Kotlin for Android – Udemy",
        "Android Studio Masterclass – Udemy"
    ],
    "UI/UX": [
        "Figma UI Basics – Udemy",
        "UX Design Crash Course – Udemy",
        "Adobe XD Complete Course – Udemy",
        "User Research Methods – Coursera",
        "Prototyping with Figma – Udemy"
    ],
    "Artificial Intelligence": [
        "Deep Learning Specialization – DeepLearning.AI (Coursera)",
        "Natural Language Processing with BERT (Coursera)",
        "AI For Everyone (Coursera)",
        "Computer Vision with OpenCV – Udemy",
        "Machine Learning with Python – Coursera",
        "TensorFlow Developer Certificate – Google"
    ],
    "Cybersecurity": [
        "Introduction to Cyber Security (Coursera)",
        "Network Security (Udemy)",
        "Penetration Testing (NPTEL)",
        "Ethical Hacking Course – Udemy",
        "CompTIA Security+ Certification – Udemy",
        "CEH v12 Complete Course – Udemy"
    ],
    "Cloud Computing": [
        "AWS Cloud Practitioner Essentials (AWS)",
        "Azure Fundamentals (Microsoft)",
        "DevOps on AWS (Coursera)",
        "CI/CD with GitHub Actions (Coursera)",
        "Docker Complete Course – Udemy",
        "Kubernetes for Beginners – Udemy"
    ],
    "Software Development": [
        "Java Programming (Coursera)",
        "Data Structures & Algorithms (Coursera)",
        "Git & GitHub Bootcamp (Udemy)",
        "Python Complete Course – Udemy",
        "C++ Programming – Udemy",
        "System Design Interview Course – Udemy"
    ],
    "Business Analyst": [
        "Business Analysis Fundamentals (Udemy)",
        "Excel to MySQL: Analytics for Business (Coursera)",
        "SQL for Business Analysts – Udemy",
        "Power BI Complete Course – Udemy",
        "Tableau for Data Science – Udemy",
        "Business Process Modeling – Udemy"
    ],
    "Product Management": [
        "Digital Product Management (Coursera)",
        "Product Management by Pragmatic Institute",
        "Agile Project Management – Udemy",
        "User Story Mapping – Udemy",
        "Product Strategy Course – Udemy",
        "A/B Testing for Product Managers – Udemy"
    ],
    "Mobile App Development": [
        "iOS App Development with Swift (Coursera)",
        "Flutter & Dart (Udemy)",
        "React Native Complete Course – Udemy",
        "Mobile App Development – Udemy",
        "Cross-Platform Development – Udemy"
    ],
    "Game Development": [
        "Game Development with Unity (Coursera)",
        "Unreal Engine C++ Developer (Udemy)",
        "Unity 2D Game Development – Udemy",
        "3D Modeling with Blender – Udemy",
        "Game Design Principles – Udemy"
    ],
    "Finance": [
        "Financial Markets – Yale (Coursera)",
        "Accounting Fundamentals (Udemy)",
        "Investment Management – Coursera",
        "Financial Modeling – Udemy",
        "Risk Management – Coursera",
        "Portfolio Management – Udemy"
    ],
    "HR": [
        "Human Resource Management (Coursera)",
        "HR Analytics (Udemy)",
        "Recruitment and Selection – Udemy",
        "Employee Relations – Udemy",
        "HR Compliance – Udemy",
        "Performance Management – Udemy"
    ],
    "Digital Marketing": [
        "Digital Marketing Specialization (Coursera)",
        "SEO Training (Udemy)",
        "Google Analytics (Coursera)",
        "Social Media Marketing – Udemy",
        "Email Marketing – Udemy",
        "Content Marketing – Udemy"
    ],
    "Blockchain": [
        "Blockchain Basics – Coursera",
        "Ethereum Development – Udemy",
        "Solidity Programming – Udemy",
        "Web3 Development – Udemy",
        "Cryptocurrency Trading – Udemy",
        "DeFi Fundamentals – Udemy"
    ],
    "DevOps": [
        "DevOps Fundamentals – Udemy",
        "Docker and Kubernetes – Udemy",
        "CI/CD Pipeline – Udemy",
        "Terraform for Beginners – Udemy",
        "Ansible Automation – Udemy",
        "Monitoring and Logging – Udemy"
    ],
    "UI/UX Design": [
        "UI/UX Design Bootcamp – Udemy",
        "User Experience Design – Coursera",
        "Prototyping with Figma – Udemy",
        "Design Systems – Udemy",
        "User Research Methods – Udemy",
        "Accessibility Design – Udemy"
    ],
    "AR/VR": [
        "Unity AR Development – Udemy",
        "VR Development with Unity – Udemy",
        "3D Modeling for VR – Udemy",
        "Spatial Computing – Coursera",
        "Mixed Reality Development – Udemy"
    ],
    "IoT": [
        "IoT Fundamentals – Coursera",
        "Arduino Programming – Udemy",
        "Raspberry Pi Projects – Udemy",
        "IoT Security – Udemy",
        "Edge Computing – Udemy",
        "Sensor Networks – Udemy"
    ]
}

# --- Enhanced Section Headers with Fuzzy Matching ---
SECTION_HEADERS = {
    "experience": ["experience", "work experience", "employment", "work history", "professional experience", "career", "employment history"],
    "education": ["education", "academic", "academics", "qualifications", "academic background", "educational background"],
    "skills": ["skills", "technical skills", "competencies", "expertise", "technologies", "tools", "programming languages"],
    "projects": ["projects", "project work", "portfolio", "achievements", "key projects", "work samples"],
    "certifications": ["certifications", "certificates", "credentials", "accreditations", "professional certifications"],
    "contact": ["contact", "contact information", "personal information", "details", "contact details"],
    "objective": ["objective", "career objective", "summary", "profile", "personal statement", "career summary"],
    "declaration": ["declaration", "statement", "affirmation", "disclaimer"]
}

def normalize_section_heading(text):
    """Normalize section headings using fuzzy matching"""
    text_lower = text.lower().strip()
    for section, variations in SECTION_HEADERS.items():
        for variation in variations:
            if SequenceMatcher(None, text_lower, variation).ratio() > 0.8:
                return section
    return text_lower

# --- Enhanced Personal Info Extraction ---
def extract_personal_info(text):
    """Enhanced personal information extraction"""
    # Improved name extraction
    name_patterns = [
        r"(?i)^(?:name\s*[:\-]?\s*)([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
        r"(?i)([A-Z][a-z]+ [A-Z][a-z]+)(?:\s*[-|]\s*[A-Za-z\s]+)?$",
        r"(?i)([A-Z][a-z]+ [A-Z][a-z]+)(?:\s*[-|]\s*[A-Za-z\s]+)?$"
    ]
    
    name = "Not found"
    for pattern in name_patterns:
        match = re.search(pattern, text[:500])
        if match:
            candidate_name = match.group(1).strip()
            # Filter out common tech words that might be mistaken for names
            tech_words = {"java", "python", "html", "css", "sql", "react", "node", "django", "flask", "aws", "azure"}
            if candidate_name.lower() not in tech_words and len(candidate_name.split()) <= 3:
                name = candidate_name
                break
    
    # Enhanced email extraction
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else "Not found"
    
    # Enhanced phone extraction
    phone_patterns = [
        r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
        r'\+?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}',
        r'\+?[0-9]{10,15}'
    ]
    phone = "Not found"
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            if isinstance(phones[0], tuple):
                phone = ''.join(phones[0])
            else:
                phone = phones[0]
            break
    
    # Enhanced URL extraction
    linkedin_pattern = r'(?:linkedin\s*[:\-]?\s*)?(https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_/?=]+|www\.linkedin\.com/in/[a-zA-Z0-9\-_/?=]+|linkedin\.com/in/[a-zA-Z0-9\-_/?=]+)'
    linkedin_matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
    linkedin = linkedin_matches[0] if linkedin_matches else "Not found"
    
    github_pattern = r'(?:github\s*[:\-]?\s*)?(https?://(?:www\.)?github\.com/[a-zA-Z0-9\-_/?=]+|www\.github\.com/[a-zA-Z0-9\-_/?=]+|github\.com/[a-zA-Z0-9\-_/?=]+)'
    github_matches = re.findall(github_pattern, text, re.IGNORECASE)
    github = github_matches[0] if github_matches else "Not found"
    
    portfolio_pattern = r'(?:portfolio\s*[:\-]?\s*)?(https?://[\w\.-]+\.(me|dev|xyz|site|portfolio|io|com)/[a-zA-Z0-9\-_/?=]*)'
    portfolio_matches = re.findall(portfolio_pattern, text, re.IGNORECASE)
    portfolio = portfolio_matches[0][0] if portfolio_matches else "Not found"
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio
    }

# --- Enhanced Education Extraction ---
def extract_education_info(text):
    """Enhanced education information extraction"""
    education_patterns = [
        r'((?:Bachelor|Master|B\.Sc|M\.Sc|B\.Tech|M\.Tech|PhD|MBA|BBA|MBA|Associate|Diploma)[^\n\r,;]?(?:at|from|in)?\s*([A-Za-z .&\'-]+)?\s*(\d{4})?)',
        r'((?:Bachelor|Master|B\.Sc|M\.Sc|B\.Tech|M\.Tech|PhD|MBA|BBA|MBA|Associate|Diploma)[^\n\r,;]?(?:at|from|in)?\s*([A-Za-z .&\'-]+)?\s*(\d{4})?)',
        r'([A-Za-z .&\'-]+(?:University|College|Institute|School)[^\n\r,;]*\s*(\d{4})?)'
    ]
    
    education = []
    for pattern in education_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                edu_text = ' '.join([m for m in match if m]).strip()
            else:
                edu_text = match.strip()
            if edu_text and len(edu_text) > 5:
                education.append(edu_text)
    
    return education if education else ["Not found"]

# --- Enhanced Skills Extraction with Preprocessing ---
def preprocess_text(text):
    """Preprocess text for better skill matching"""
    # Normalize case and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills_enhanced(text):
    """Enhanced skills extraction with preprocessing and soft skills detection"""
    processed_text = preprocess_text(text)
    doc = nlp(processed_text)
    
    # Technical skills from known keywords
    technical_skills = set()
    for field, skills in SKILL_KEYWORDS.items():
        for skill in skills:
            if skill.lower() in processed_text:
                technical_skills.add(skill.lower())
    
    # Soft skills detection
    soft_skills = [
        "leadership", "communication", "teamwork", "problem solving", "critical thinking",
        "creativity", "adaptability", "time management", "organization", "attention to detail",
        "analytical", "strategic thinking", "project management", "customer service",
        "negotiation", "presentation", "research", "collaboration", "initiative",
        "flexibility", "multitasking", "decision making", "mentoring", "coaching"
    ]
    
    detected_soft_skills = set()
    for skill in soft_skills:
        if skill.lower() in processed_text:
            detected_soft_skills.add(skill.lower())
    
    # Named entity recognition for additional skills
    ner_skills = set()
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"] and len(ent.text) < 30:
            ner_skills.add(ent.text.lower())
    
    all_skills = technical_skills.union(detected_soft_skills).union(ner_skills)
    return list(all_skills) if all_skills else ["Not found"]

# --- Enhanced Certifications Extraction ---
def extract_certifications_enhanced(text):
    """Enhanced certifications extraction"""
    # Known certification providers and keywords
    cert_providers = [
        "coursera", "udemy", "edx", "udacity", "aws", "google", "microsoft", "ibm",
        "oracle", "linkedin learning", "skillshare", "pluralsight", "datacamp",
        "deeplearning.ai", "fast.ai", "kaggle", "hackerrank", "leetcode"
    ]
    
    # Certification keywords
    cert_keywords = [
        "certified", "certification", "certificate", "accredited", "professional",
        "specialist", "expert", "master", "foundation", "associate", "professional"
    ]
    
    certifications = []
    lines = text.lower().split('\n')
    
    for line in lines:
        line = line.strip()
        if any(provider in line for provider in cert_providers):
            certifications.append(line)
        elif any(keyword in line for keyword in cert_keywords):
            # Check if it's not just a common word
            if len(line) > 10 and not any(word in line for word in ["university", "college", "school", "degree"]):
                certifications.append(line)
    
    return certifications if certifications else ["Not found"]

# --- Enhanced Info Extraction Function ---
def extract_info(text):
    """Enhanced information extraction with all improvements"""
    # Extract personal info
    personal_info = extract_personal_info(text)
    
    # Extract education
    education = extract_education_info(text)
    
    # Extract skills
    skills = extract_skills_enhanced(text)
    
    # Extract certifications
    certifications = extract_certifications_enhanced(text)
    
    return {
        "name": personal_info["name"],
        "email": personal_info["email"],
        "phone": personal_info["phone"],
        "education": education,
        "skills": skills,
        "certifications": certifications,
        "linkedin": personal_info["linkedin"],
        "github": personal_info["github"],
        "portfolio": personal_info["portfolio"]
    }

# --- Resume Format Validation ---
def validate_resume_format(text):
    """Validate resume format and warn about potential issues"""
    warnings = []
    
    # Check for very short content (might be scanned)
    if len(text.strip()) < 500:
        warnings.append("⚠️ Very short content detected. This might be a scanned PDF or image-based resume.")
    
    # Check for weird symbols (OCR artifacts)
    weird_symbols = re.findall(r'[^\w\s\.\,\-\+\@\#\$\%\(\)\[\]\{\}\:\;\?\!]', text)
    if len(weird_symbols) > len(text) * 0.1:  # More than 10% weird symbols
        warnings.append("⚠️ Many unusual symbols detected. This might be a scanned PDF with poor OCR.")
    
    # Check for multi-column indicators
    multi_column_indicators = ["|", "  ", "\t\t"]
    if any(indicator in text for indicator in multi_column_indicators):
        warnings.append("⚠️ Multi-column layout detected. Consider using a single-column format for better ATS compatibility.")
    
    # Check for image-heavy indicators (very few words)
    words = text.split()
    if len(words) < 100:
        warnings.append("⚠️ Very few words detected. This might be an image-heavy resume.")
    
    return warnings

# --- Pre-upload Guidelines ---
PRE_UPLOAD_GUIDELINES = """
📋 **Before Uploading Your Resume:**

✅ **Format Requirements:**
• Use single-column layout (avoid multi-column formats)
• Use clear, readable fonts (Arial, Calibri, Times New Roman)
• Keep file size under 5MB
• Use PDF or DOCX format

✅ **Content Guidelines:**
• Include clear section headings (EXPERIENCE, EDUCATION, SKILLS, etc.)
• Use bullet points for descriptions
• Include contact information (email, phone, LinkedIn)
• Add quantifiable achievements (e.g., "Increased sales by 25%")
• List relevant skills and certifications

❌ **Avoid:**
• Image-heavy resumes (logos, graphics)
• Scanned documents
• Multi-column layouts
• Very small fonts
• Overly creative designs

💡 **Tips for Better Results:**
• Use consistent formatting throughout
• Include keywords relevant to your target role
• Keep descriptions concise and impactful
• Proofread for spelling and grammar errors
"""

=======
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

>>>>>>> 1a206628 (Initial commit)
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
<<<<<<< HEAD
    ],
    "Artificial Intelligence": ["Fake News Detection using BERT", "Image Captioning with CNN+RNN", "Speech Recognition System (Deep Learning)", "Chatbot with Transformers"],
    "Cybersecurity": ["Network Vulnerability Scanner", "Phishing Detection System", "Firewall Rule Automation", "SIEM Log Analyzer"],
    "Cloud Computing": ["Deploy a CI/CD pipeline with GitHub Actions and AWS", "Serverless Web App (AWS Lambda)", "Multi-cloud Monitoring Dashboard"],
    "Software Development": ["Library Management System (Java)", "Task Manager App (Python)", "REST API with Flask/Django"],
    "Business Analyst": ["Sales Data Dashboard (PowerBI)", "Process Optimization Case Study", "Customer Segmentation Analysis"],
    "Product Management": ["Go-to-Market Strategy Plan", "User Feedback Analysis Tool", "Product Roadmap Dashboard"],
    "Mobile App Development": ["Fitness Tracker App (Flutter)", "Recipe App (iOS/Swift)", "Event Planner App (React Native)"],
    "Game Development": ["2D Platformer Game (Unity)", "Multiplayer Card Game (Unreal)", "VR Puzzle Game"],
    "Finance": ["Stock Portfolio Tracker (Excel/Python)", "Loan Default Prediction (ML)", "Financial Statement Analyzer"],
    "HR": ["Employee Onboarding Portal", "HR Analytics Dashboard", "Leave Management System"],
    "Digital Marketing": ["SEO Audit & Digital Campaign (Google Analytics)", "Social Media Sentiment Analysis", "Email Campaign Automation"]
}

CERTIFICATIONS = {
    "Data Science": ["Google Data Analytics", "IBM Data Science", "Microsoft Data Analyst Associate","CISCO","EDUSKILLS"],
    "Web Development": ["Meta Front-End Certificate", "FreeCodeCamp Responsive Web Design"],
    "Artificial Intelligence": ["DeepLearning.AI Specialization", "Google AI Professional Certificate"],
    "Cybersecurity": ["CompTIA Security+", "Certified Ethical Hacker (CEH)", "Cisco CCNA Security"],
    "Cloud Computing": ["AWS Cloud Practitioner", "Azure Fundamentals", "Google Associate Cloud Engineer"],
    "Software Development": ["Oracle Certified Java Programmer", "Microsoft Certified: Azure Developer Associate"],
    "Business Analyst": ["IIBA ECBA", "CBAP Certification"],
    "Product Management": ["Pragmatic Institute Product Management", "Certified Scrum Product Owner (CSPO)"],
    "Mobile App Development": ["Google Associate Android Developer", "Apple Certified iOS Developer"],
    "Game Development": ["Unity Certified Developer", "Unreal Engine Certification"],
    "Finance": ["CFA Level 1", "CPA", "Financial Risk Manager (FRM)"],
    "HR": ["SHRM-CP", "HRCI PHR"],
    "Digital Marketing": ["Google Analytics Individual Qualification", "HubSpot Content Marketing"],
    "UI/UX": ["NN/g UX Certification", "Adobe Certified Expert"]
=======
    ]
>>>>>>> 1a206628 (Initial commit)
}

TOOLS_LIST = ["VS Code", "Jupyter", "GitHub", "Excel", "Tableau"]

# Expanded known skills and certifications
KNOWN_SKILLS = set([
    "python", "machine learning", "pandas", "numpy", "tensorflow", "data analysis", "html", "css", "javascript", "react", "node", "flask", "django",
    "android", "kotlin", "java", "xml", "figma", "adobe xd", "photoshop", "sketch", "sql", "powerbi", "tableau", "c++", "c#", "aws", "azure", "gcp", "docker", "kubernetes"
])
CERT_PROVIDERS = ["coursera", "udemy", "aws", "google", "microsoft", "edx", "udacity", "ibm", "oracle", "linkedin learning"]


<<<<<<< HEAD
# --- Detect Field ---
def detect_field(text_or_skills):
    skill_set = set([s.lower() for s in text_or_skills.split()] if isinstance(text_or_skills, str) else [s.lower() for s in text_or_skills])
    max_matches = 0
    best_field = "General"
    for field, keywords in SKILL_KEYWORDS.items():
        match_count = sum(1 for kw in keywords if kw.lower() in skill_set)
        if match_count > max_matches:
            max_matches = match_count
            best_field = field
    return best_field
=======
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
>>>>>>> 1a206628 (Initial commit)


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

<<<<<<< HEAD
# --- Professional Resume Scoring System (Enhancv-inspired) ---
def dynamic_resume_score(text, info, field="General"):
    """
    Comprehensive resume scoring based on industry standards and ATS optimization.
    Scoring criteria inspired by professional resume analyzers like Enhancv.
    """
    score = 0
    breakdown = {}
    
    # === 1. CONTENT COMPLETENESS (25 points) ===
    content_score = 0
    
    # Essential sections (15 points)
    essential_sections = ["experience", "education", "skills"]
    present_essential = sum(1 for section in essential_sections if section in text.lower())
    content_score += (present_essential / len(essential_sections)) * 15
    
    # Optional sections (10 points)
    optional_sections = ["objective", "summary", "projects", "certifications", "achievements", "volunteer"]
    present_optional = sum(1 for section in optional_sections if section in text.lower())
    content_score += min((present_optional / len(optional_sections)) * 10, 10)
    
    score += content_score
    breakdown["Content Completeness"] = round(content_score, 1)
    
    # === 2. SKILLS ASSESSMENT (25 points) ===
    skills_score = 0
    
    # Skills quantity and relevance (15 points)
    valid_skills = [s for s in info['skills'] if s != 'Not found' and len(s.strip()) > 0]
    skills_count = len(valid_skills)
    
    if skills_count >= 8:
        skills_score += 10
    elif skills_count >= 5:
        skills_score += 7
    elif skills_count >= 3:
        skills_score += 5
    elif skills_count >= 1:
        skills_score += 3
    
    # Field-specific skills (10 points)
    field_skills = SKILL_KEYWORDS.get(field, [])
    if field_skills:
        relevant_skills = [s for s in valid_skills if s.lower() in [sk.lower() for sk in field_skills]]
        relevance_ratio = len(relevant_skills) / max(1, len(valid_skills))
        skills_score += relevance_ratio * 10
    
    score += skills_score
    breakdown["Skills Assessment"] = round(skills_score, 1)
    
    # === 3. EXPERIENCE & IMPACT (20 points) ===
    experience_score = 0
    
    # Action verbs and metrics (15 points)
    action_verbs = ["achieved", "developed", "implemented", "managed", "led", "created", "designed", 
                   "improved", "increased", "reduced", "optimized", "launched", "coordinated", "analyzed"]
    metrics_indicators = ["%", "percent", "improved", "reduced", "increased", "decreased", "by", "from", "to"]
    
    action_verb_count = sum(1 for verb in action_verbs if verb in text.lower())
    metrics_count = sum(1 for metric in metrics_indicators if metric in text.lower())
    
    if action_verb_count >= 5 and metrics_count >= 3:
        experience_score += 15
    elif action_verb_count >= 3 and metrics_count >= 1:
        experience_score += 10
    elif action_verb_count >= 2:
        experience_score += 7
    elif action_verb_count >= 1:
        experience_score += 3
    
    # Experience length and depth (5 points)
    if len(text) > 2000:  # Substantial content
        experience_score += 5
    elif len(text) > 1000:
        experience_score += 3
    elif len(text) > 500:
        experience_score += 1
    
    score += experience_score
    breakdown["Experience & Impact"] = round(experience_score, 1)
    
    # === 4. PROFESSIONAL PRESENTATION (15 points) ===
    presentation_score = 0
    
    # Contact information (5 points)
    contact_info = 0
    if info['email'] != 'Not found':
        contact_info += 2
    if info['phone'] != 'Not found':
        contact_info += 2
    if info['linkedin'] != 'Not found':
        contact_info += 1
    presentation_score += min(contact_info, 5)
    
    # Professional formatting (5 points)
    formatting_indicators = 0
    if "•" in text or "- " in text:  # Bullet points
        formatting_indicators += 2
    if any(char in text for char in ["|", "•", "-"]):  # Consistent formatting
        formatting_indicators += 2
    if len([s for s in text.split(". ") if len(s) < 150]) > 5:  # Concise sentences
        formatting_indicators += 1
    presentation_score += min(formatting_indicators, 5)
    
    # Certifications and credentials (5 points)
    valid_certs = [c for c in info['certifications'] if c != 'Not found' and len(c.strip()) > 0]
    if len(valid_certs) >= 3:
        presentation_score += 5
    elif len(valid_certs) >= 1:
        presentation_score += 3
    
    score += presentation_score
    breakdown["Professional Presentation"] = round(presentation_score, 1)
    
    # === 5. ATS OPTIMIZATION (15 points) ===
    ats_score = 0
    
    # Keyword optimization (8 points)
    field_keywords = SKILL_KEYWORDS.get(field, [])
    if field_keywords:
        keyword_matches = sum(1 for keyword in field_keywords if keyword.lower() in text.lower())
        keyword_ratio = keyword_matches / max(1, len(field_keywords))
        ats_score += keyword_ratio * 8
    
    # Standard section headers (4 points)
    standard_headers = ["experience", "education", "skills", "certifications", "projects", "summary"]
    header_matches = sum(1 for header in standard_headers if header in text.lower())
    ats_score += (header_matches / len(standard_headers)) * 4
    
    # File format and readability (3 points)
    if len(text) > 500 and len(text) < 5000:  # Optimal length
        ats_score += 3
    elif len(text) > 200:
        ats_score += 1
    
    score += ats_score
    breakdown["ATS Optimization"] = round(ats_score, 1)
    
    # === BONUS POINTS (up to 10 points) ===
    bonus_points = 0
    
    # Projects section
    if 'projects' in text.lower():
        bonus_points += 3
    
    # GitHub/Portfolio links
    if any(url in text.lower() for url in ['github.com', 'portfolio', 'behance.net']):
        bonus_points += 2
    
    # Education details
    if info['education'] and info['education'][0] != 'Not found':
        bonus_points += 2
    
    # Professional summary/objective
    if any(section in text.lower() for section in ['summary', 'objective', 'profile']):
        bonus_points += 2
    
    # Recent experience (if mentioned)
    if any(year in text for year in ['2024', '2023', '2022']):
        bonus_points += 1
    
    score += bonus_points
    breakdown["Bonus Points"] = round(bonus_points, 1)
    
    # === FINAL SCORE CALCULATION ===
    final_score = min(100, round(score))
    
    # Adjust score based on field-specific requirements
    if field in ["Cybersecurity", "Cloud Computing"] and len(valid_certs) < 1:
        final_score = max(0, final_score - 10)  # Certifications are crucial for these fields
    
    if field in ["Data Science", "Artificial Intelligence"] and skills_count < 5:
        final_score = max(0, final_score - 8)  # Technical skills are essential
    
    if field in ["Product Management", "Business Analyst"] and action_verb_count < 3:
        final_score = max(0, final_score - 5)  # Leadership/management skills important
    
    breakdown["Total Score"] = final_score
    
    return final_score, breakdown

# --- Enhanced Dynamic Strengths/Weaknesses Analysis ---
def get_strengths_weaknesses(text, info):
    """
    Comprehensive analysis of resume strengths and weaknesses based on industry standards.
    """
    strengths = []
    weaknesses = []
    
    # === STRENGTHS ANALYSIS ===
    
    # Contact Information
    if info['email'] != 'Not found' and info['phone'] != 'Not found':
        strengths.append("Complete contact information provided")
    elif info['email'] != 'Not found':
        strengths.append("Email address included")
    
    # Professional Presence
    if info['linkedin'] != 'Not found':
        strengths.append("LinkedIn profile linked for professional networking")
    
    # Content Structure
    if 'projects' in text.lower():
        strengths.append("Projects section demonstrates practical experience")
    if 'summary' in text.lower() or 'objective' in text.lower():
        strengths.append("Professional summary/objective provides clear direction")
    if 'certifications' in text.lower():
        strengths.append("Certifications section shows continuous learning")
    
    # Skills Assessment
    valid_skills = [s for s in info['skills'] if s != 'Not found' and len(s.strip()) > 0]
    if len(valid_skills) >= 8:
        strengths.append("Comprehensive skill set with 8+ technical skills")
    elif len(valid_skills) >= 5:
        strengths.append("Good range of technical skills (5+ skills listed)")
    
    # Impact and Metrics
    action_verbs = ["achieved", "developed", "implemented", "managed", "led", "created", "designed", 
                   "improved", "increased", "reduced", "optimized", "launched", "coordinated", "analyzed"]
    action_verb_count = sum(1 for verb in action_verbs if verb in text.lower())
    if action_verb_count >= 5:
        strengths.append("Strong use of action verbs demonstrates leadership")
    elif action_verb_count >= 3:
        strengths.append("Good use of action verbs shows initiative")
    
    # Quantifiable Results
    metrics_indicators = ["%", "percent", "improved", "reduced", "increased", "decreased", "by", "from", "to"]
    metrics_count = sum(1 for metric in metrics_indicators if metric in text.lower())
    if metrics_count >= 3:
        strengths.append("Quantifiable achievements with measurable impact")
    elif metrics_count >= 1:
        strengths.append("Some quantifiable results included")
    
    # Formatting and Presentation
    if "•" in text or "- " in text:
        strengths.append("Professional bullet-point formatting")
    if len([s for s in text.split(". ") if len(s) < 150]) > 5:
        strengths.append("Concise, readable writing style")
    
    # === WEAKNESSES ANALYSIS ===
    
    # Contact Information Issues
    if info['email'] == 'Not found':
        weaknesses.append("Missing email address - essential for contact")
    if info['phone'] == 'Not found':
        weaknesses.append("Missing phone number - limits communication options")
    if info['linkedin'] == 'Not found':
        weaknesses.append("No LinkedIn profile - missing professional networking opportunity")
    
    # Content Gaps
    if 'projects' not in text.lower():
        weaknesses.append("No projects section - missing practical experience demonstration")
    if 'summary' not in text.lower() and 'objective' not in text.lower():
        weaknesses.append("No professional summary/objective - unclear career direction")
    if 'certifications' not in text.lower():
        weaknesses.append("No certifications section - missing credential validation")
    
    # Skills Issues
    if len(valid_skills) < 3:
        weaknesses.append("Limited technical skills (less than 3 skills listed)")
    elif len(valid_skills) < 5:
        weaknesses.append("Moderate skill set - consider adding more relevant skills")
    
    # Impact and Results Issues
    if action_verb_count < 2:
        weaknesses.append("Limited use of action verbs - weakens impact statements")
    if metrics_count == 0:
        weaknesses.append("No quantifiable results - missing measurable achievements")
    
    # Formatting Issues
    if "•" not in text and "- " not in text:
        weaknesses.append("No bullet points - reduces readability and scannability")
    if len([s for s in text.split(". ") if len(s) > 200]) > 3:
        weaknesses.append("Some sentences too long - affects readability")
    
    # Content Quality
    if len(text) < 500:
        weaknesses.append("Resume too brief - may lack sufficient detail")
    elif len(text) > 3000:
        weaknesses.append("Resume too lengthy - may lose reader attention")
    
    # Professional Development
    if not info['certifications'] or info['certifications'][0] == 'Not found':
        weaknesses.append("No certifications - missing professional development evidence")
    
    # Recent Experience
    if not any(year in text for year in ['2024', '2023', '2022']):
        weaknesses.append("No recent experience mentioned - may appear outdated")
    
    # Remove duplicates and ensure quality
    strengths = list(set([s for s in strengths if s and len(s.strip()) > 0]))
    weaknesses = list(set([w for w in weaknesses if w and len(w.strip()) > 0]))
    
    # Limit to top 5 most important items
    return strengths[:5], weaknesses[:5]

# --- Enhanced Personalized Tips ---
def get_personalized_tips(text, info):
    """
    Generate personalized, actionable tips based on resume analysis.
    """
    tips = []
    
    # Contact Information Tips
    if info['linkedin'] == 'Not found':
        tips.append("🔗 **Add LinkedIn Profile**: Include your LinkedIn URL to enhance professional credibility and networking opportunities.")
    
    if info['email'] == 'Not found':
        tips.append("📧 **Add Email Address**: Include a professional email address for direct communication.")
    
    if info['phone'] == 'Not found':
        tips.append("📱 **Add Phone Number**: Include your phone number for immediate contact options.")
    
    # Content Structure Tips
    if 'projects' not in text.lower():
        tips.append("💼 **Add Projects Section**: Include 2-3 relevant projects with technologies used and outcomes achieved.")
    
    if 'summary' not in text.lower() and 'objective' not in text.lower():
        tips.append("📝 **Add Professional Summary**: Include a 2-3 sentence summary highlighting your key strengths and career goals.")
    
    if 'certifications' not in text.lower():
        tips.append("🏆 **Add Certifications**: Include relevant certifications to demonstrate continuous learning and expertise.")
    
    # Skills Enhancement Tips
    valid_skills = [s for s in info['skills'] if s != 'Not found' and len(s.strip()) > 0]
    if len(valid_skills) < 5:
        tips.append("🛠️ **Expand Skills Section**: List at least 5-8 relevant technical skills for your target role.")
    
    # Impact and Results Tips
    action_verbs = ["achieved", "developed", "implemented", "managed", "led", "created", "designed", 
                   "improved", "increased", "reduced", "optimized", "launched", "coordinated", "analyzed"]
    action_verb_count = sum(1 for verb in action_verbs if verb in text.lower())
    if action_verb_count < 3:
        tips.append("🚀 **Use Action Verbs**: Start bullet points with strong action verbs like 'Developed', 'Implemented', 'Led'.")
    
    metrics_indicators = ["%", "percent", "improved", "reduced", "increased", "decreased", "by", "from", "to"]
    metrics_count = sum(1 for metric in metrics_indicators if metric in text.lower())
    if metrics_count < 2:
        tips.append("📊 **Add Quantifiable Results**: Include specific metrics like 'Increased efficiency by 25%' or 'Reduced costs by $10K'.")
    
    # Formatting Tips
    if "•" not in text and "- " not in text:
        tips.append("📋 **Use Bullet Points**: Format experience and skills with bullet points for better readability.")
    
    # Content Quality Tips
    if len(text) < 800:
        tips.append("📄 **Expand Content**: Add more detail to experience descriptions and achievements.")
    
    if len(text) > 2500:
        tips.append("✂️ **Condense Content**: Keep resume concise and focused on most relevant information.")
    
    # Professional Development Tips
    if not info['certifications'] or info['certifications'][0] == 'Not found':
        tips.append("🎓 **Pursue Certifications**: Consider industry-relevant certifications to strengthen your profile.")
    
    # Recent Experience Tips
    if not any(year in text for year in ['2024', '2023', '2022']):
        tips.append("🕒 **Update Recent Experience**: Ensure your most recent work experience is prominently featured.")
    
    # ATS Optimization Tips
    if not any(section in text.lower() for section in ['experience', 'education', 'skills']):
        tips.append("🔍 **Use Standard Headers**: Include standard section headers like 'Experience', 'Education', 'Skills' for ATS compatibility.")
    
    # Limit to most important tips
    return tips[:6]

=======
>>>>>>> 1a206628 (Initial commit)
# --- YouTube Video Recommendation ---
YOUTUBE_VIDEO = {
    "title": "How to Make a Resume Stand Out in 2024 (5 Tips)",
    "summary": "A concise guide to making your resume stand out with actionable tips and real examples.",
<<<<<<< HEAD
    "url": "https://youtu.be/IIGWpw1FXhk?si=eaG2uk0OCHGvm7Tw"
=======
    "url": "https://www.youtube.com/watch?v=Qb1b1s4A4gI"
>>>>>>> 1a206628 (Initial commit)
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
<<<<<<< HEAD
    .stAlert-success {
        color: #222 !important;
    }
    body, .main {
        background: linear-gradient(120deg, #e0e7ff 0%, #c9e4ff 40%, #f8fafc 100%) !important;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    .st-bb {border-bottom: 2px solid #e0e0e0; margin: 1.5em 0 1em 0;}
    .st-section {
        padding: 1.2em 1.5em;
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 8px 32px 0 rgba(80,120,200,0.18), 0 2px 8px 0 rgba(80,120,200,0.12);
        margin-bottom: 1.2em;
        transition: box-shadow 0.2s;
    }
    .st-section:hover {
        box-shadow: 0 12px 40px 0 rgba(80,120,200,0.22), 0 4px 16px 0 rgba(80,120,200,0.16);
    }
    .st-emoji {font-size: 1.3em; margin-right: 0.3em;}
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI Semibold', 'Roboto', 'Arial', sans-serif;
        color: #2d3a4a;
        letter-spacing: 0.5px;
    }
    .section-title {
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 0.5em;
        padding: 0.2em 0.8em;
        border-radius: 8px;
        display: inline-block;
    }
    .section-title-blue { background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); color: #fff; }
    .section-title-green { background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%); color: #222; }
    .section-title-orange { background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%); color: #222; }
    .section-title-red { background: linear-gradient(90deg, #f9536b 0%, #b91d73 100%); color: #fff; }
    .section-title-purple { background: linear-gradient(90deg, #a18cd1 0%, #fbc2eb 100%); color: #222; }
    .score-badge {
        font-size: 2.2em;
        font-weight: 800;
        color: #fff;
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        border-radius: 16px;
        padding: 0.2em 0.7em;
        margin-bottom: 0.5em;
        display: inline-block;
        box-shadow: 0 2px 8px 0 rgba(80,120,200,0.18);
    }
    .suggestion-card {
        background: linear-gradient(120deg, #f8fafc 60%, #e0e7ff 100%);
        border-radius: 12px;
        box-shadow: 0 2px 8px 0 rgba(80,120,200,0.10);
        padding: 1em 1.2em;
        margin-bottom: 0.7em;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(120deg, #e0e7ff 0%, #c9e4ff 100%) !important;
        border-right: 2px solid #bfc9d9;
    }
=======
    .main {background-color: #f8f9fa;}
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
    }
    .st-bb {border-bottom: 2px solid #e0e0e0; margin: 1.5em 0 1em 0;}
    .st-section {padding: 1em 1.5em; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #e0e0e0; margin-bottom: 1.5em;}
    .st-emoji {font-size: 1.3em; margin-right: 0.3em;}
>>>>>>> 1a206628 (Initial commit)
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

<<<<<<< HEAD
# --- User Greeting and Title ---
st.markdown("""
<div style='margin-bottom: 1.5em;'>
  <h2 style='margin-bottom:0.2em;'>🤖 Welcome to <span style='color:#2575fc;'>ProFile Analyzer</span>!</h2>
  <span style='font-size:1.1em; color:#4a5a6a;'>Upload your resume(s) and get instant, actionable feedback.</span>
</div>
""", unsafe_allow_html=True)

st.title("🤖 ProFile Analyzer")

# --- Pre-upload Guidelines ---
with st.expander("📋 Upload Guidelines", expanded=False):
    st.markdown(PRE_UPLOAD_GUIDELINES)

# --- Summary Row (Dashboard Cards) ---
uploaded_files = st.file_uploader("📤 Upload Resume(s) (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
st.markdown("<div class='st-bb'></div>", unsafe_allow_html=True)

if uploaded_files:
    tab_labels = [f"Resume {i+1}" for i in range(len(uploaded_files))]
    tabs = st.tabs(tab_labels)
    for idx, uploaded in enumerate(uploaded_files):
        with tabs[idx]:
            st.markdown(f"<div class='st-section'>", unsafe_allow_html=True)
            st.image(ICON_RESUME, width=48)
            st.markdown(f"### 📄 <span class='st-emoji'>Resume {idx+1}</span>", unsafe_allow_html=True)
            # Determine file type and save accordingly
            file_extension = uploaded.name.split('.')[-1].lower()
            temp_file_path = f"temp_resume_{idx}.{file_extension}"
            
            with open(temp_file_path, "wb") as f:
                f.write(uploaded.read())
            
            # Extract text based on file type
            if file_extension == "pdf":
                text = extract_text_from_pdf(temp_file_path)
            elif file_extension == "docx":
                text = extract_text_from_docx(temp_file_path)
            else:
                text = ""
            
            # Validate resume format
            format_warnings = validate_resume_format(text)
            if format_warnings:
                st.warning("**Resume Format Issues Detected:**")
                for warning in format_warnings:
                    st.markdown(f"• {warning}")
            
            info = extract_info(text)
            field = detect_field(text)

            # --- Sliders for dynamic display ---
            skill_count = st.slider("How many skills to show?", 1, 10, 1, key=f"skill_slider_{idx}")
            cert_count = st.slider("How many certifications to show?", 1, 10, 1, key=f"cert_slider_{idx}")
            proj_count = st.slider("How many project ideas to show?", 1, 10, 1, key=f"proj_slider_{idx}")

            # --- Extracted Info Block (Expander) ---
            with st.expander("🔍 Extracted Info", expanded=False):
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.image(ICON_FEEDBACK, width=32)
                st.write(f"👤 *Name:* {info['name']}")
                st.write(f"✉ *Email:* {info['email']}")
                st.write(f"📞 *Phone:* {info['phone']}")
                st.write(f"🎓 *Education:* {', '.join(info['education'])}")
                st.write(f"🛠 *Skills:* {', '.join(info['skills'][:skill_count])}")
                st.write(f"📄 *Certifications:* {', '.join(info['certifications'][:cert_count])}")
                st.write(f"🔗 *LinkedIn:* {info['linkedin']}")
                st.write(f"🐙 *GitHub:* {info['github']}")
                st.write(f"🌐 *Portfolio:* {info['portfolio']}")
                st.write(f"💼 *Predicted Field:* {field}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # --- Manual Edit Section ---
            with st.expander("✏️ Edit Extracted Information", expanded=False):
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.markdown("**Edit any incorrectly extracted information:**")
                
                # Create session state for edited info
                if f'edited_info_{idx}' not in st.session_state:
                    st.session_state[f'edited_info_{idx}'] = info.copy()
                
                edited_info = st.session_state[f'edited_info_{idx}']
                
                # Editable fields
                edited_info['name'] = st.text_input("Name:", value=edited_info['name'], key=f"name_{idx}")
                edited_info['email'] = st.text_input("Email:", value=edited_info['email'], key=f"email_{idx}")
                edited_info['phone'] = st.text_input("Phone:", value=edited_info['phone'], key=f"phone_{idx}")
                edited_info['linkedin'] = st.text_input("LinkedIn:", value=edited_info['linkedin'], key=f"linkedin_{idx}")
                edited_info['github'] = st.text_input("GitHub:", value=edited_info['github'], key=f"github_{idx}")
                edited_info['portfolio'] = st.text_input("Portfolio:", value=edited_info['portfolio'], key=f"portfolio_{idx}")
                
                # Skills editing
                st.markdown("**Skills (one per line):**")
                skills_text = st.text_area("Skills:", value="\n".join(edited_info['skills'] if edited_info['skills'] != ["Not found"] else []), key=f"skills_{idx}")
                edited_info['skills'] = [s.strip() for s in skills_text.split('\n') if s.strip()]
                
                # Certifications editing
                st.markdown("**Certifications (one per line):**")
                certs_text = st.text_area("Certifications:", value="\n".join(edited_info['certifications'] if edited_info['certifications'] != ["Not found"] else []), key=f"certs_{idx}")
                edited_info['certifications'] = [c.strip() for c in certs_text.split('\n') if c.strip()]
                
                # Education editing
                st.markdown("**Education (one per line):**")
                edu_text = st.text_area("Education:", value="\n".join(edited_info['education'] if edited_info['education'] != ["Not found"] else []), key=f"edu_{idx}")
                edited_info['education'] = [e.strip() for e in edu_text.split('\n') if e.strip()]
                
                # Update session state
                st.session_state[f'edited_info_{idx}'] = edited_info
                
                # Use edited info for scoring if user has made changes
                if st.button("Update Analysis with Edited Info", key=f"update_{idx}"):
                    info = edited_info
                    field = detect_field(" ".join(edited_info['skills']))
                
=======
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
>>>>>>> 1a206628 (Initial commit)
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Resume Score Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
<<<<<<< HEAD
                resume_score, score_breakdown = dynamic_resume_score(text, info, field)
                st.markdown(f'<div class="score-badge">{resume_score}/100</div>', unsafe_allow_html=True)
                st.image(ICON_FEEDBACK, width=32)
                st.progress(resume_score / 100)
                
                # Score interpretation
                if resume_score >= 85:
                    st.success("🎯 **Excellent!** Your resume meets professional standards.")
                elif resume_score >= 75:
                    st.success("✅ **Strong Resume!** Minor improvements can make it outstanding.")
                elif resume_score >= 65:
                    st.info("📈 **Good Foundation!** Focus on the areas below for better results.")
                elif resume_score >= 50:
                    st.warning("⚠️ **Needs Improvement.** Consider the suggestions below.")
                else:
                    st.error("🔴 **Requires Major Updates.** Follow the recommendations below.")
                
                # Detailed Score Breakdown
                with st.expander("📊 **Detailed Score Breakdown**", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        for category, points in list(score_breakdown.items())[:3]:
                            st.metric(category, f"{points} pts")
                    with col2:
                        for category, points in list(score_breakdown.items())[3:]:
                            st.metric(category, f"{points} pts")
                
                # Strengths and Weaknesses
                strengths, weaknesses = get_strengths_weaknesses(text, info)
                if strengths:
                    st.markdown('<span class="section-title section-title-green">✅ Strengths</span>', unsafe_allow_html=True)
                    for s in strengths:
                        st.markdown(f'<div class="suggestion-card">✓ {s}</div>', unsafe_allow_html=True)
                
                if weaknesses:
                    st.markdown('<span class="section-title section-title-red">⚠️ Areas for Improvement</span>', unsafe_allow_html=True)
                    for w in weaknesses:
                        st.markdown(f'<div class="suggestion-card">• {w}</div>', unsafe_allow_html=True)
                
                # Personalized Tips
                tips = get_personalized_tips(text, info)
                if tips:
                    st.markdown('<span class="section-title section-title-purple">💡 Personalized Tips</span>', unsafe_allow_html=True)
                    for tip in tips:
                        st.markdown(f'<div class="suggestion-card">💡 {tip}</div>', unsafe_allow_html=True)
                
=======
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
>>>>>>> 1a206628 (Initial commit)
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
<<<<<<< HEAD
            with st.expander("✅ Missing Skills & Recommended Courses", expanded=False):
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.image(ICON_SKILLS, width=32)
                shown = 0
                for skill in IDEAL_SKILLS:
                    if shown >= skill_count:
                        break
                    if skill in [sk.lower() for sk in info['skills']]:
                        st.markdown(f"{skill.title()} – Already present ✅")
                        shown += 1
                    else:
                        course = next((c for c in sum(COURSES.values(), []) if skill in c.lower()), None)
                        if course:
                            st.markdown(f"{skill.title()} – Missing -> Take '{course}' ✔")
                        else:
                            st.markdown(f"{skill.title()} – Missing")
                        shown += 1
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Certifications Block ---
            with st.expander("📚 Certifications to Include or Remove", expanded=False):
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.image(ICON_CERT, width=32)
                certs_shown = 0
                for cert in info['certifications']:
                    if certs_shown >= cert_count:
                        break
=======
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
>>>>>>> 1a206628 (Initial commit)
                    if any(p in cert.lower() for p in CERT_PROVIDERS):
                        st.markdown(f"'{cert}' – Should keep")
                    else:
                        st.markdown(f"'{cert}' – Remove (irrelevant to tech roles)")
<<<<<<< HEAD
                    certs_shown += 1
                for cert in [p.title() for p in CERTIFICATIONS.get(field, []) if not any(p in c.lower() for c in info['certifications'])][:cert_count-certs_shown]:
=======
                for cert in [p.title() for p in CERT_PROVIDERS if not any(p in c.lower() for c in info['certifications'])]:
>>>>>>> 1a206628 (Initial commit)
                    st.markdown(f"'{cert}' – Add if completed")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Project Ideas Block ---
<<<<<<< HEAD
            with st.expander("🛠 Project Ideas to Add", expanded=False):
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
=======
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("🛠️ Project Ideas to Add:")
>>>>>>> 1a206628 (Initial commit)
                st.image(ICON_PROJECT, width=32)
                suggested_projects = [p for p in PROJECT_IDEAS.get(field, []) if p.lower() not in text.lower()]
                extra_projects = [
                    "Build a sentiment analysis app with Twitter API",
                    "Movie recommendation engine with Python + ML",
                    "Portfolio website using HTML/CSS/JS"
                ]
<<<<<<< HEAD
                all_projects = suggested_projects + extra_projects
                for proj in all_projects[:proj_count]:
=======
                for proj in suggested_projects + extra_projects:
>>>>>>> 1a206628 (Initial commit)
                    st.markdown(f"- {proj}")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Final Suggestions Block ---
<<<<<<< HEAD
            with st.expander("🎯 Final Suggestions", expanded=False):
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
=======
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("🎯 Final Suggestions:")
>>>>>>> 1a206628 (Initial commit)
                st.image(ICON_SUGGEST, width=32)
                if info['linkedin'] == 'Not found':
                    st.markdown("Add LinkedIn URL")
                st.markdown("Use bullet metrics like 'Reduced process time by 30%'")
                if 'certifications' not in text.lower():
                    st.markdown("Include a 'Certifications' section")
<<<<<<< HEAD
                st.markdown("✅ Add a section explicitly titled 'Objective' or 'Career Objective'")
                st.markdown("✅ Use labeled sections for LinkedIn, GitHub, Phone, etc.")
                st.markdown("✅ Include more common tools/skills in data science: e.g., SQL, PowerBI, scikit-learn, etc.")
                st.markdown("✅ Mention your skills and certifications in a bullet format for better detection")
                st.markdown("✅ Include a 'Declaration' or 'Contact' section (these are checked by many ATS systems)")
                st.markdown("✅ Use headings with consistent casing: e.g., 'PROJECTS', 'INTERNSHIPS', 'CERTIFICATIONS' in uppercase")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- YouTube Video Block ---
            with st.expander("🎥 Bonus Video", expanded=False):
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.image(ICON_VIDEO, width=32)
                st.write(f"{YOUTUBE_VIDEO['title']}")
                st.write(YOUTUBE_VIDEO['summary'])
                st.markdown(f"[▶ Watch here]({YOUTUBE_VIDEO['url']})")
=======
                st.markdown("</div>", unsafe_allow_html=True)

            # --- YouTube Video Block ---
            with st.container():
                st.markdown("<div class='st-section'>", unsafe_allow_html=True)
                st.subheader("🎥 Bonus Video:")
                st.image(ICON_VIDEO, width=32)
                st.write(f"**{YOUTUBE_VIDEO['title']}**")
                st.write(YOUTUBE_VIDEO['summary'])
                st.markdown(f"[▶️ Watch here]({YOUTUBE_VIDEO['url']})")
>>>>>>> 1a206628 (Initial commit)
                st.markdown("</div>", unsafe_allow_html=True)

            st.success("✅ Analysis complete!")
            st.balloons()
            st.markdown("</div>", unsafe_allow_html=True)
<<<<<<< HEAD

    # --- Summary Row (Dashboard Cards) ---
    if uploaded_files:
        avg_score = 0
        if uploaded_files:
            scores = []
            for idx, uploaded in enumerate(uploaded_files):
                file_extension = uploaded.name.split('.')[-1].lower()
                temp_file_path = f"temp_resume_{idx}.{file_extension}"
                
                if file_extension == "pdf":
                    text = extract_text_from_pdf(temp_file_path)
                elif file_extension == "docx":
                    text = extract_text_from_docx(temp_file_path)
                else:
                    text = ""
                
                info = extract_info(text)
                tscore = template_score(text, info)
                cscore = clarity_score(text)
                scores.append(min(100, tscore + cscore))
            avg_score = int(sum(scores)/len(scores))
        col1, col2, col3 = st.columns(3)
        col1.metric("📄 Resumes Uploaded", len(uploaded_files))
        col2.metric("⭐ Avg. Resume Score", avg_score)
        col3.metric("🕒 Last Analysis", "Just now")
        st.markdown("<div class='st-bb'></div>", unsafe_allow_html=True)

# --- Theme Toggle Note ---
st.sidebar.markdown("""
#### 🎨 Theme
You can switch between dark and light mode from the Streamlit settings menu (top-right ☰ > Settings > Theme), or set a default in .streamlit/config.toml.
""")
=======
>>>>>>> 1a206628 (Initial commit)
