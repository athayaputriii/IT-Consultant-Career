"""
knowledge_base.py

This file contains all the data and "knowledge" for the IT Career Consultant Bot.
By separating the data from the logic, we can easily update and expand the bot's
capabilities without changing the core application code in bot.py.
VERSION 2.6 - Added Goodbye Intent
"""

# 1. Intent Keywords: Words or phrases that map to a user's intention.
intent_keywords = {
    "career_path": {
        "career": 2, "path": 2, "pathway": 2, "roadmap": 2, "become a": 3,
        "how to be a": 3, "what does a": 2, "skills for": 3, "what is the skill to become": 3,
        "skill needed for": 3, "skills needed for": 3, "what skills": 2,
        "role of": 2, "responsibilities": 2, "get into": 2
    },
    "role_suggestion": {
        "what can i be": 4, "suitable role": 4, "career for me": 4, "prospect career": 3,
        "what job can i get with": 4, "work prospects": 3, "thinking about": 2, "thinking of": 2,
        # Increased weight of these keywords to meet the confidence threshold
        "i know": 2, "i have skill": 2, "proficient in": 2, "proficient with": 2,
        "good with": 3, "good at": 3, "could use": 3,
        "my skills are": 2, "potential job": 2, "based on": 1, "i have": 1
    },
    "consultation_start": {
        "i want to consult": 3, "need your help": 3, "can you help me": 3,
        "i need advice": 2, "can i ask something": 2, "help me": 1,
        "sure": 1, "yes": 1, "ok": 1, "okay": 1
    },
    "greeting": {
        "hi": 1, "hello": 1, "hey": 1, "greetings": 1, "good morning": 1, "morning": 1,
        "good afternoon": 1, "what's up": 1, "good evening": 1
    },
    "thanks": {
        "thank": 2, "thanks": 2, "appreciate": 2, "thx": 1, "ty": 1, "jia yo": 1,
        "you got it": 1, "that's what i need to study": 2
    },
    "goodbye": {
        "bye": 2, "goodbye": 2, "good night": 2, "night": 1, "see you": 1, "later": 1
    }
}

# 2. Entity Patterns: Regular expressions to extract specific pieces of information.
entity_patterns = {
    "role": [
        # Development Roles
        r"\b(backend|frontend|full.?stack|software|web) developer\b",
        r"\b(mobile developer|android developer|ios developer)\b",
        r"\b(game developer|ar/vr developer)\b",
        r"\b(embedded systems engineer|blockchain developer|robotics engineer)\b",
        # Data Roles
        r"\b(data scientist|data analyst|ml engineer|ai engineer|bi developer|ai researcher)\b",
        # Operations & Infrastructure Roles
        r"\b(devops?|site reliability|sre|cloud|network|hardware) engineer\b",
        r"\b(database administrator|dba|system administrator|sysadmin)\b",
        # Security Roles
        r"\b(security engineer|cybersecurity analyst|penetration tester|pen tester|ethical hacker|information security analyst)\b",
        # Quality & Testing Roles
        r"\b(qa engineer|test automation engineer)\b",
        # Management & Strategy Roles
        r"\b(solutions architect|software architect|cloud architect|it consultant|it auditor)\b",
        r"\b(product manager|project manager|business analyst)\b",
        # User & Content Roles
        r"\b(ui/ux designer|technical writer)\b",
        # Support Roles
        r"\b(it support specialist)\b"
    ],
    "technology": [
        # Languages & OS (Special characters removed and handled in a separate pattern below)
        r"\b(python|java|javascript|js|typescript|ts|go|golang|rust|php|r|sql|swift|kotlin|solidity|bash|ruby|html|css|linux)\b",
        # Frontend Frameworks
        r"\b(react|angular|vue|svelte|next\.?js|jquery)\b",
        # Backend Frameworks (Special characters removed)
        r"\b(node\.?js|django|flask|fastapi|spring|ruby on rails)\b",
        # Cloud & DevOps
        r"\b(aws|azure|google cloud|gcp|docker|kubernetes|k8s|terraform|ansible|jenkins|gitlab|github actions)\b",
        # Data & ML
        r"\b(pandas|numpy|scikit-learn|tensorflow|pytorch|keras|tableau|powerbi|power bi|jupyter|apache spark|hadoop)\b",
        # Databases
        r"\b(mysql|postgresql|mongodb|redis|oracle|sql server)\b",
        # Mobile
        r"\b(react native|flutter|xcode|android studio)\b",
        # Game Dev & AR/VR
        r"\b(unity|unreal engine)\b", # C++ removed and handled below
        # QA & Testing
        r"\b(selenium|cypress|jest|junit|pytest)\b",
        # Security Tools
        r"\b(wireshark|metasploit|nmap|burp suite)\b",
        # Design & Project Management
        r"\b(figma|sketch|adobe xd|jira|asana|trello)\b",
        # FINAL FIX: Removed the trailing word boundary `\b` to match at end of string
        r"(c\+\+|c\#|\.net)",
    ]
}

# 3. Simple Responses: For straightforward intents that don't need complex logic.
simple_responses = {
    "greeting": ["Hi there! I'm here to help as your IT career counselor.", "Hello! I'm your IT career consultant bot. How can I assist you today?"],
    "consultation_start": ["Of course. I can help you in two main ways: you can tell me a job role to see the required skills, or you can tell me your skills to find matching job roles. What would you like to do?", "I'm ready to help. I can match your prospect role based on your skills, and vice-versa. Just let me know what you need."],
    "thanks": ["You're welcome! Happy to help with your career journey! Jia yo! 💪", "Anytime! Feel free to ask more questions. Good luck!"],
    "goodbye": ["Goodbye! Feel free to reach out again anytime.", "Good night! Take care.", "See you later!"]
}

# 4. Role-Skill Map: The core "brain" of the bot. (Content is unchanged from the previous version)
role_skill_map = {
    # --- Existing Roles (Refined) ---
    "data_scientist": {"display_name": "Data Scientist", "description": "...", "skills": {"languages": ["python", "r", "sql"], "core_concepts": ["statistics", "machine learning", "data modeling"], "libraries": ["pandas", "numpy", "scikit-learn", "tensorflow"], "tools": ["jupyter", "tableau", "apache spark"]}},
    "backend_developer": {"display_name": "Backend Developer", "description": "...", "skills": {"languages": ["python", "java", "go", "c#"], "frameworks": ["django", "spring", "node.js", ".net"], "databases": ["sql", "mongodb", "redis"], "concepts": ["api design", "docker", "kubernetes"]}},
    "frontend_developer": {"display_name": "Frontend Developer", "description": "...", "skills": {"languages": ["html", "css", "javascript", "typescript"], "frameworks": ["react", "vue", "angular"], "concepts": ["responsive design", "state management", "ui/ux principles"], "tools": ["npm", "webpack", "figma"]}},
    "devops_engineer": {"display_name": "DevOps Engineer", "description": "...", "skills": {"cloud": ["aws", "azure", "gcp"], "iac": ["terraform", "ansible"], "containerization": ["docker", "kubernetes"], "ci/cd": ["jenkins", "gitlab"], "scripting": ["bash", "python", "linux"]}},
    "cloud_engineer": {"display_name": "Cloud Engineer", "description": "...", "skills": {"platforms": ["aws", "azure", "gcp"], "infrastructure": ["terraform", "networking", "security"], "containers": ["docker", "kubernetes"], "automation": ["python", "bash", "linux"]}},
    "data_analyst": {"display_name": "Data Analyst", "description": "...", "skills": {"core": ["sql", "excel", "statistics"], "visualization": ["tableau", "powerbi"], "languages": ["python", "r"], "libraries": ["pandas", "numpy"]}},
    "machine_learning_engineer": {"display_name": "Machine Learning Engineer", "description": "...", "skills": {"languages": ["python", "java", "c++"], "frameworks": ["tensorflow", "pytorch", "scikit-learn"], "big_data": ["apache spark", "kafka"], "infrastructure": ["docker", "kubernetes", "aws", "linux"]}},
    "full_stack_developer": {
        "display_name": "Full Stack Developer", "description": "A versatile developer who works on both the frontend (client-side) and backend (server-side) of an application.",
        "skills": {"frontend": ["html", "css", "javascript", "react", "vue"], "backend": ["node.js", "python", "java", "sql", "mongodb"], "devops": ["git", "docker", "aws", "linux"]}},
    "mobile_developer": {
        "display_name": "Mobile Developer", "description": "Specializes in creating applications for mobile devices like smartphones and tablets, for either Android or iOS.",
        "skills": {"platforms": ["android (kotlin/java)", "ios (swift)"], "cross_platform": ["react native", "flutter"], "tools": ["xcode", "android studio", "git"], "concepts": ["ui/ux principles", "api integration"]}},
    "game_developer": {
        "display_name": "Game Developer", "description": "Designs, programs, and tests video games for computers, consoles, or mobile devices.",
        "skills": {"engines": ["unity", "unreal engine"], "languages": ["c#", "c++"], "concepts": ["3d math", "game physics", "ai for games"], "tools": ["blender", "git", "linux"]}},
    "embedded_systems_engineer": {
        "display_name": "Embedded Systems Engineer", "description": "Works with hardware and software for devices that are not traditional computers, such as IoT devices, wearables, and automotive systems.",
        "skills": {"languages": ["c", "c++", "python"], "hardware": ["microcontrollers (arduino, raspberry pi)", "circuit design"], "concepts": ["real-time operating systems (rtos)", "low-level programming", "linux"]}},
    "blockchain_developer": {
        "display_name": "Blockchain Developer", "description": "Develops decentralized applications (dApps) and smart contracts on blockchain platforms.",
        "skills": {"languages": ["solidity", "rust", "javascript"], "platforms": ["ethereum", "solana"], "concepts": ["smart contracts", "cryptography", "web3"], "tools": ["hardhat", "truffle", "linux"]}},
    "database_administrator": {
        "display_name": "Database Administrator (DBA)", "description": "Manages and maintains an organization's databases, ensuring data integrity, performance, and security.",
        "skills": {"databases": ["mysql", "postgresql", "sql server", "oracle"], "languages": ["sql"], "concepts": ["database design", "backup and recovery", "performance tuning"], "cloud": ["aws rds", "azure sql"], "os": ["linux"]}},
    "qa_engineer": {
        "display_name": "QA Engineer / Test Automation", "description": "Ensures software quality by designing and executing tests, both manual and automated, to find and report bugs.",
        "skills": {"automation_tools": ["selenium", "cypress", "playwright"], "languages": ["python", "java", "javascript"], "frameworks": ["pytest", "junit", "jest"], "concepts": ["test planning", "bug tracking", "linux"]}},
    "site_reliability_engineer": {
        "display_name": "Site Reliability Engineer (SRE)", "description": "A software engineer focused on reliability, scalability, and performance of production systems.",
        "skills": {"automation": ["python", "go"], "infrastructure": ["kubernetes", "terraform", "aws", "gcp", "linux"], "monitoring": ["prometheus", "grafana", "datadog"], "concepts": ["slos/slis", "incident response"]}},
    "it_support_specialist": {
        "display_name": "IT Support Specialist", "description": "Provides technical assistance and troubleshooting for hardware, software, and network issues within an organization.",
        "skills": {"os": ["windows", "macos", "linux"], "hardware": ["pc assembly", "troubleshooting"], "networking": ["tcp/ip", "dns", "dhcp"], "software": ["active directory", "office 3d"]}},
    "system_administrator": {
        "display_name": "System Administrator", "description": "Manages and maintains an organization's IT infrastructure, including servers, networks, and software.",
        "skills": {"os": ["linux (red hat, ubuntu)", "windows server"], "scripting": ["bash", "powershell"], "virtualization": ["vmware", "hyper-v"], "networking": ["dns", "dhcp", "firewalls"]}},
    "network_engineer": {
        "display_name": "Network Engineer", "description": "Designs, implements, and manages an organization's computer networks.",
        "skills": {"protocols": ["tcp/ip", "bgp", "ospf"], "hardware": ["cisco", "juniper (routers, switches)"], "concepts": ["firewalls", "vpn", "sd-wan"], "certifications": ["ccna", "comptia network+"], "os": ["linux"]}},
    "security_engineer": {
        "display_name": "Security Engineer", "description": "Designs and builds systems to protect an organization's computer networks and systems from cyber threats.",
        "skills": {"concepts": ["network security", "cryptography", "iam"], "tools": ["firewalls", "siem", "ids/ips"], "cloud": ["aws security", "azure security"], "scripting": ["python", "bash", "linux"]}},
    "cybersecurity_analyst": {
        "display_name": "Cybersecurity Analyst", "description": "Monitors networks for security breaches, investigates incidents, and implements security measures.",
        "skills": {"tools": ["siem (splunk, qradar)", "wireshark", "nmap", "linux"], "concepts": ["threat intelligence", "incident response", "vulnerability assessment"], "compliance": ["nist", "iso 2d"]}},
    "penetration_tester": {
        "display_name": "Penetration Tester (Ethical Hacker)", "description": "Simulates cyberattacks on systems to identify security vulnerabilities before malicious hackers can.",
        "skills": {"tools": ["metasploit", "burp suite", "nmap", "kali linux"], "techniques": ["web app testing", "network penetration", "social engineering"], "scripting": ["python", "bash"]}},
    "solutions_architect": {
        "display_name": "Solutions Architect", "description": "Designs high-level, comprehensive technology solutions to meet specific business needs, often in a cloud environment.",
        "skills": {"cloud": ["aws", "azure", "gcp"], "concepts": ["system design", "microservices", "enterprise architecture"], "business": ["stakeholder management", "cost analysis"], "os": ["linux"]}},
    "product_manager": {
        "display_name": "Product Manager", "description": "Defines the 'why,' 'what,' and 'when' of a product, focusing on market needs, user experience, and business goals.",
        "skills": {"methodologies": ["agile", "scrum"], "tools": ["jira", "trello", "figma"], "concepts": ["user stories", "product roadmaps", "market research"], "soft_skills": ["communication", "leadership"]}},
    "project_manager": {
        "display_name": "Project Manager", "description": "Responsible for planning, executing, and closing projects, managing resources, budgets, and timelines.",
        "skills": {"methodologies": ["agile", "scrum", "waterfall"], "tools": ["jira", "asana", "microsoft project"], "concepts": ["risk management", "resource allocation"], "soft_skills": ["organization", "communication"]}},
    "ui/ux_designer": {
        "display_name": "UI/UX Designer", "description": "Focuses on the user's experience (UX) and the visual interface (UI) of a product to make it intuitive and appealing.",
        "skills": {"tools": ["figma", "sketch", "adobe xd"], "concepts": ["wireframing", "prototyping", "user research", "usability testing"], "principles": ["design theory", "typography", "color theory"]}},
    "technical_writer": {
        "display_name": "Technical Writer", "description": "Creates clear and concise documentation for complex technical products, such as user manuals, API guides, and tutorials.",
        "skills": {"tools": ["markdown", "git", "confluence"], "concepts": ["api documentation", "instructional design"], "soft_skills": ["clarity", "attention to detail", "communication"]}}
}

