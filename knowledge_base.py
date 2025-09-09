"""
knowledge_base.py

This file contains all the data and "knowledge" for the IT Career Consultant Bot.
By separating the data from the logic, we can easily update and expand the bot's
capabilities without changing the core application code in bot.py.
VERSION 2.6 - Added Goodbye Intent
"""

# 1. Intent Keywords: Words or phrases that map to a user's intention.
# Regex-based intent patterns with weighted capture groups
intent_patterns = {
    "career_path": [
        # Career-related terms with optional plurals and variations
        (r'(?:\b|^)(careers?|paths?|pathways?|roadmaps?|trajector(?:y|ies)|progression|development|journey|route|learn|need|require|what.*become|how.*become|technolog|tech|stack|tools|knowledge|study|want.*be|to be$)', 2),
        
        # Phrases about becoming or transitioning to a role (with lookahead for role mentions)
        (r'(?:\b|^)(?:(?:how\s+(?:to|do\s+I|can\s+I)\s+)?(?:become|transition\s+(?:to|into)|train\s+(?:as|for)|qualify\s+(?:as|for)|break\s+into|pursue\s+a\s+career\s+as|enter\s+the\s+field\s+of)|'
         r'become\s+(?:a|an)|path(?:way)?\s+to\s+becoming|steps?\s+to\s+(?:become|be)|requirements?\s+to\s+be)(?:\b|$)', 3),
        
        # Questions about roles and responsibilities (more comprehensive)
        (r'(?:\b|^)(?:what\s+(?:does|do|are|is)\s+(?:a|an)\s+[\w\s]+\s+(?:do|responsible\s+for|entail|involve)|'
         r'role\s+(?:of|for|description|profile)|responsibilities\s+of|duties\s+of|day-to-day\s+(?:of|for)|'
         r'get\s+(?:into|started\s+in|involved\s+in)|what\'s\s+involved\s+in|what\'s\s+it\s+like\s+to\s+be)(?:\b|$)', 2),
        
        # Skills and requirements questions (more comprehensive)
        (r'(?:\b|^)(?:skills?\s*(?:required|needed|essential|necessary|for|to\s+become)?|'
         r'what\s+(?:skills?|qualifications?|requirements?|prerequisites?|education|training|certifications?)'
         r'(?:\s+(?:are|do I|should I|is)\s+(?:needed|required|necessary))?|'
         r'(?:technical|hard|soft)\s+skills?|necessary\s+skills?|what\s+(?:does\s+it\s+take|is\s+needed)|'
         r'learn\s+to\s+become|study\s+to\s+become|training\s+for)(?:\b|$)', 3)
    ],
    "role_suggestion": [
        # Direct questions about career options (more comprehensive)
        (r'(?:\b|^)(?:what\s+(?:can|should|could)\s+I\s+(?:be(?:come)?|do|pursue)|'
         r'(?:most\s+)?suitable\s+(?:roles?|careers?|jobs?|positions?)|'
         r'career\s+(?:options?|for\s+me|suggestions?|advice|recommendations?)|'
         r'prospect(?:ive|s)?\s+career|which\s+(?:role|job|career|position)\s+(?:fits|suits|matches|is\s+right)|'
         r'right\s+career\s+for|what\s+should\s+I\s+do\s+with|what\s+job\s+matches|'
         r'career\s+guidance|career\s+counseling)(?:\b|$|job|what.*do|pursue|with.*skill|become|path|opportunity|ca|profficent|pretty good|familiar|expert|know|knowledge|work|role|roles|field|field of|field in|field with)', 4),
        
        # Questions about jobs based on skills/background (more comprehensive)
        (r'(?:\b|^)(?:what\s+(?:jobs?|roles?|careers?|positions?)\s+(?:can\s+I\s+get|are\s+available|fit|match|pursue)\s+(?:with|for|based\s+on)|'
         r'work\s+prospects?|job\s+opportunities?|employment\s+options?|'
         r'career\s+paths?\s+with|compatible\s+careers?|possible\s+careers?|'
         r'jobs?\s+(?:for|that use|requiring)|roles?\s+(?:for|that use|requiring)|'
         r'what\s+can\s+I\s+do\s+with|where\s+can\s+I\s+work\s+with)(?:\b|$)', 3),
        
        # Expressions of thinking/considering (more comprehensive)
        (r'(?:\b|^)(?:thinking\s+(?:about|of)|considering|contemplating|exploring|'
         r'looking\s+(?:into|at)|interested\s+in|curious\s+about|weighing\s+options|'
         r'evaluating|assessing|thinking\s+of\s+switching|career\s+change|'
         r'want\s+to\s+move\s+into|transitioning|changing\s+careers?)(?:\b|$)', 2),
        
        # Statements about skills and proficiencies (more comprehensive)
        (r'(?:\b|^)(?:(?:I\s+(?:am|have\s+been)\s+)?(?:proficient|skilled|experienced|good|strong|expert|adept|knowledgeable|competent)\s+(?:in|with|at)|'
         r'I\s+(?:know|have\s+experience\s+with|have\s+skills?\s+in|am\s+familiar\s+with|work\s+with|use|mastered)|'
         r'my\s+skills?\s+(?:are|include|consist\s+of)|background\s+in|familiar\s+with|comfortable\s+with|'
         r'could\s+use|have\s+knowledge\s+of|have\s+expertise\s+in)(?:\b|$)', 3),
        
        # Basis for suggestions (more comprehensive)
        (r'(?:\b|^)(?:based\s+on|given|taking\s+into\s+account|considering|with|'
         r'according\s+to|in\s+light\s+of|my\s+(?:skills?|experience|background|education|qualifications?|knowledge)|'
         r'I\s+have|I\'ve\s+worked\s+with|I\s+know|my\s+proficiency\s+in|my\s+expertise\s+in)(?:\b|$)', 1)
    ],
    "consultation_start": [
        # Direct requests for consultation/help
        (r'\b(I\s+(want|wanna|would like|need)\s+(to\s+)?(consult|talk|discuss|get\s+advice)|'
         r'need\s+(your\s+)?help|can\s+you\s+help|could\s+you\s+help|'
         r'would\s+you\s+(help|assist)|looking\s+for\s+guidance|seeking\s+advice)\b', 3),
        
        # Indirect requests for advice
        (r'\b(I\s+need\s+advice|can\s+I\s+ask\s+(something|a question)|'
         r'have\s+a\s+question|want\s+to\s+pick\s+your\s+brain|'
         r'could\s+use\s+some\s+guidance|need\s+direction)\b', 2),
        
        # Affirmative responses and simple requests
        (r'\b(help\s+me|please\s+help|assist\s+me|guide\s+me|'
         r'(yes|yeah|yep|sure|ok(ay)?|absolutely|definitely|of\s+course|certainly)|'
         r'let\'s\s+(do\s+it|get\s+started|begin))\b', 1)
    ],
    "greeting": [
        # Common greetings
        (r'\b(hi|hello|hey|howdy|hiya|greetings|salutations|what\'s\s+up|sup|wassup|yo)\b', 1),
        
        # Time-based greetings
        (r'\b(good\s+(morning|afternoon|evening|day)|mornin\'|evenin\'|'
         r'top\s+of\s+the\s+(morning|day)|happy\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))\b', 1),
        
        # Additional friendly openings
        (r'\b(how\s+(are\s+you|do\s+you\s+do)|how\'s\s+it\s+going|'
         r'nice\s+to\s+(see|meet)\s+you|pleasure\s+to\s+meet\s+you|'
         r'long\s+time\s+no\s+see|hope\s+you\'re\s+doing\s+well)\b', 1)
    ],
    "thanks": [
        # Expressions of gratitude
        (r'\b(thank\s+(you|u)|thanks|many\s+thanks|appreciate\s+it|much\s+obliged|'
         r'thx|ty|gracias|merci|danke|arigato|cheers|ta|big\s+ups|props|shoutout|'
         r'jia\s+yo|you\'re\s+(the\s+best|awesome|amazing|great)|I\s+owe\s+you)\b', 2),
        
        # Acknowledgments of helpful information
        (r'\b(you\s+got\s+it|that\'s\s+(exactly|just)\s+what\s+I\s+(needed|was\s+looking\s+for)|'
         r'perfect|excellent|great\s+info|very\s+helpful|just\s+what\s+I\s+needed|'
         r'this\s+helps\s+a\s+lot|exactly\s+what\s+I\s+wanted\s+to\s+know)\b', 1)
    ],
    "goodbye": [
        # Common farewells
        (r'\b(bye|goodbye|farewell|see\s+ya|see\s+you|catch\s+you\s+later|'
         r'later|laters|peace\s+(out|)|I\'m\s+out|signing\s+off|gotta\s+go|'
         r'take\s+care|until\s+next\s+time|talk\s+to\s+you\s+soon)\b', 2),
        
        # Night-related farewells
        (r'\b(good\s+night|night|nighty\s+night|sweet\s+dreams|'
         r'sleep\s+well|have\s+a\s+good\s+night|rest\s+well)\b', 1),
        
        # Work/day ending phrases
        (r'\b(calling\s+it\s+a\s+day|that\'s\s+all\s+for\s+now|'
         r'wrapping\s+up|done\s+for\s+the\s+day|time\s+to\s+log\s+off)\b', 1)
    ]
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

