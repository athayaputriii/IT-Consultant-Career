intent_keywords = {
    "career_path": {
        "career": 3, "path": 2, "pathway": 2, "roadmap": 2, "become a": 3, 
        "transition": 3, "switch": 3, "how to": 1, "what does": 1, "get started": 2, 
        "first step": 2, "future": 2, "day in the life": 2, "role of": 2,
        "responsibilities": 2, "choose between": 2, "from": 1, "to": 1
    },
    "technology": {
        "technology": 3, "technologies": 3, "tools": 2, "stack": 2, "framework": 2, 
        "library": 2, "language": 2, "platform": 2, "python": 1, "react": 1, "aws": 1, 
        "kubernetes": 1, "compare": 2, "vs": 2, "difference between": 2, "recommend": 1
    },
    "salary": {
        "salary": 3, "salaries": 3, "pay": 3, "compensation": 3, "how much": 2, 
        "earn": 2, "earnings": 2, "negotiate": 3, "raise": 2, "range": 1
    },
    "certification": {
        "certification": 3, "certifications": 3, "certs": 2, "certificate": 2, 
        "exam": 2, "certified": 2, "aws certified": 3, "azure": 2, "comptia": 2
    },
    "interview": {
        "interview": 3, "interviews": 3, "prep": 2, "questions": 2, "technical": 2,
        "prepare": 2, "behavioral": 2, "whiteboard": 2
    },
    "greeting": {
        "hi": 1, "hello": 1, "hey": 1, "greetings": 1, "good morning": 1,
        "good afternoon": 1, "what's up": 1
    },
    "thanks": {
        "thank": 2, "thanks": 2, "appreciate": 2, "thx": 1, "ty": 1
    }
}


entity_patterns = {
    "role": [
        r"\b(backend|frontend|full.?stack|software|web|mobile|android|ios|flutter) developer\b",
        r"\b(game|embedded|firmware|kernel|compiler|QA|test|automation) developer\b",
        r"\b(devops|site reliability|SRE|cloud|data|machine learning|AI|ML|big data) engineer\b",
        r"\b(security|cyber(security)?|network|systems|reliability|automation) engineer\b",
        r"\b(solutions|infrastructure|platform|database|ETL|analytics) engineer\b",
        r"\b(data scientist|data analyst|data engineer|ML engineer|AI engineer|business intelligence|BI developer)\b",
        r"\b(IT support|system administrator|sysadmin|network administrator|cloud administrator)\b",
        r"\b(security engineer|cybersecurity analyst|penetration tester|ethical hacker|security consultant)\b",
        r"\b(project manager|product manager|tech lead|engineering manager|CTO|chief technology officer)\b",
        r"\b(software architect|solutions architect|system architect|technical architect)\b",
        r"\b(blockchain developer|smart contract developer|Web3 developer|solidity developer)\b",
        r"\b(AR developer|VR developer|metaverse developer|computer vision engineer|NLP engineer)\b"
    ],
    "technology": [
        r"\b(python|java|javascript|js|typescript|ts|go|golang|rust|c#|c\+\+|php|ruby|swift|kotlin|dart)\b",
        r"\b(react|angular|vue|svelte|ember|backbone|jquery|next\.?js|nuxt\.?js|gatsby|remix)\b",
        r"\b(node\.?js|express|nestjs|fastify|koa|django|flask|fastapi|spring|quarkus|micronaut)\b",
        r"\b(ruby on rails|laravel|symfony|asp\.net|core\.net|phoenix|gin|fiber|actix|rocket)\b",
        r"\b(react native|flutter|ionic|native script|xamarin|swiftui|jetpack compose|kotlin multiplatform)\b",
        r"\b(AWS|Amazon Web Services|Azure|Google Cloud|GCP|IBM Cloud|Oracle Cloud|DigitalOcean|Linode)\b",
        r"\b(heroku|netlify|vercel|firebase|supabase|cloudflare|render|fly\.io|digitalocean|linode)\b",
        r"\b(kubernetes|k8s|docker|containerd|podman|terraform|pulumi|ansible|chef|puppet|saltstack)\b",
        r"\b(jenkins|gitlab|github actions|circleci|travisci|argo(cd|workflows)|flux|spinnaker)\b",
        r"\b(prometheus|grafana|elk|elasticsearch|kibana|splunk|datadog|newrelic|jaeger|loki)\b",
        r"\b(SQL|MySQL|PostgreSQL|SQLite|oracle|sql server|mariaDB|cockroachDB|timescaleDB)\b",
        r"\b(MongoDB|redis|cassandra|dynamoDB|cosmosDB|firestore|neo4j|arangodb|influxDB|snowflake)\b",
        r"\b(tensorflow|pytorch|keras|scikit.?learn|opencv|pandas|numpy|jupyter|apache spark|hadoop)\b",
        r"\b(kafka|rabbitMQ|nats|airflow|prefect|dagster|dbt|tableau|powerbi|looker|metabase)\b",
        r"\b(blockchain|ethereum|bitcoin|smart contract|web3|ipfs|arweave|graphql|grpc|webRTC)\b"
    ],
    "experience_level": [
        r"\b(intern|internship|apprentice|entry.?level|junior|graduate|fresh graduate|first job)\b",
        r"\b(mid.?level|mid.?senior|experienced|senior|lead|staff|principal|architect|fellow)\b"
    ]
}

responses = {
    "greeting": {
        "default": [
            "Hello! I'm your IT Career Consultant bot! 🚀",
            "Hi there! Ready to explore IT career paths?",
            "Hey! Let's talk about technology careers! 👨‍💻"
        ]
    },
    "thanks": {
        "default": [
            "You're welcome! Happy to help with your career journey!",
            "Anytime! Good luck with your IT career path!",
            "Glad I could help! Feel free to ask more questions."
        ]
    },
    "career_path": {
        "backend developer": [
            "To become a backend developer: Start with a language like Python, Java, or Node.js. Learn about databases (SQL & NoSQL), API design, and server management. Build projects with frameworks like Django, Spring, or Express.js.",
            "Backend developer path: Master a programming language → Learn databases → Understand APIs → Study system design → Build portfolio projects → Apply for junior positions."
        ],
        "frontend developer": [
            "Frontend developer roadmap: HTML → CSS → JavaScript → React/Vue/Angular → State management → Build tools → Responsive design → Portfolio projects.",
            "For frontend development: Focus on JavaScript fundamentals, then choose a framework (React is most popular). Learn CSS frameworks like Tailwind and build interactive projects."
        ],
        "data scientist": [
            "Data scientist career: Statistics → Python/R → SQL → Machine Learning → Data visualization → Domain knowledge → Build data projects → Portfolio.",
            "To become a data scientist: Strong math foundation, programming (Python), machine learning, statistics, and business acumen. Consider a Master's degree for advanced roles."
        ],
        "devops engineer": [
            "DevOps engineer path: Linux → Scripting → Cloud basics → Containers → Kubernetes → CI/CD → Infrastructure as Code → Monitoring → Security.",
            "DevOps career: Start with Linux administration, learn a scripting language, understand cloud services, master Docker/Kubernetes, then learn automation tools."
        ],
        "cloud engineer": [
            "Cloud engineer roadmap: Linux/Networking → AWS/Azure/GCP fundamentals → Infrastructure as Code → Containers → Security → Certification → Real projects.",
            "For cloud engineering: Get cloud certified (AWS/Azure), learn Terraform, understand networking, and build projects deploying applications to the cloud."
        ],
        "default": [
            "Great career question! For most IT roles: Learn fundamentals → Build projects → Get certified → Gain experience → Specialize → Keep learning.",
            "IT career general path: Foundation skills → Specialization → Practical experience → Continuous learning → Networking → Career advancement."
        ]
    },
    "technology": {
        "python": [
            "Python is excellent for beginners! Great for web development (Django/Flask), data science (Pandas/NumPy), automation, and AI/ML. High demand in job market.",
            "Python: Versatile language used in web dev, data science, automation, and AI. Easy to learn with huge community support. Start with Python if you're new to programming."
        ],
        "javascript": [
            "JavaScript is essential for web development. Learn vanilla JS first, then frameworks like React, Vue, or Angular. Also used in backend (Node.js) and mobile (React Native).",
            "JavaScript: The language of the web. Must-learn for frontend, also powerful for backend with Node.js. High demand across all experience levels."
        ],
        "react": [
            "React is the most popular frontend framework. Learn JavaScript first, then React fundamentals, state management, hooks, and modern React patterns.",
            "React: Component-based library maintained by Facebook. Great job opportunities. Learn with official documentation and build projects with Next.js."
        ],
        "aws": [
            "AWS is the leading cloud platform. Start with Cloud Practitioner, then Solutions Architect. Learn EC2, S3, Lambda, and infrastructure as code with Terraform.",
            "AWS skills are in high demand. Learn core services, get certified, and practice with real projects. Essential for DevOps and cloud roles."
        ],
        "kubernetes": [
            "Kubernetes is the container orchestration standard. Learn Docker first, then K8s fundamentals, deployments, services, and Helm charts. High demand in DevOps.",
            "Kubernetes: Essential for modern cloud infrastructure. Learn container basics, then K8s concepts, and practice with minikube or cloud Kubernetes services."
        ],
        "default": [
            "Technology learning path: Start with fundamentals → Build small projects → Learn advanced concepts → Contribute to open source → Stay updated with trends.",
            "When choosing technology: Consider job market demand, community support, learning curve, and your career goals. Focus on fundamentals first."
        ]
    },
    "salary": {
        "default": [
            "IT salaries vary by role, experience, location, and company. Junior: $50-80K, Mid: $80-120K, Senior: $120-180K+, with higher ranges in tech hubs.",
            "Salary ranges: Entry-level positions typically start at $50-70K, mid-level $80-120K, senior roles $120-200K+. Specialized roles and FAANG companies pay higher."
        ]
    },
    "certification": {
        "default": [
            "Popular certifications: AWS/Azure/GCP cloud certs, CompTIA A+/Network+/Security+, CISSP, PMP, and specialized certs for specific technologies.",
            "Certifications can help: Cloud certifications (AWS, Azure, GCP), security certs (CISSP, CEH), and vendor-specific certs demonstrate expertise to employers."
        ]
    },
    "interview": {
        "default": [
            "Technical interview prep: Practice coding problems (LeetCode), system design, behavioral questions, and know your resume well. Mock interviews help!",
            "Interview preparation: Study data structures & algorithms, practice whiteboarding, prepare STAR stories for behavioral questions, and research the company."
        ]
    }
}

response_connectors = [
    "\n\nAlso, regarding your question about {intent_name}:\n",
    "\n\nAs for {intent_name}:\n",
    "\n\nTo address your point on {intent_name}:\n"
]