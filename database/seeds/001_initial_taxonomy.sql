BEGIN;

INSERT INTO job_roles (title, description)
VALUES
    ('Software Engineer', 'Designs, implements, and maintains software applications.'),
    ('Frontend Developer', 'Builds browser-based interfaces and web experiences.'),
    ('Backend Developer', 'Builds server-side services, APIs, and data access layers.'),
    ('Full-Stack Developer', 'Develops both browser-based interfaces and server-side applications.'),
    ('Mobile Application Developer', 'Builds and maintains mobile applications.'),
    ('QA Automation Engineer', 'Designs automated software quality and regression tests.'),
    ('DevOps Engineer', 'Automates software delivery, infrastructure, and operations.'),
    ('Cloud Engineer', 'Builds and operates cloud infrastructure and services.'),
    ('Data Analyst', 'Analyzes structured data and communicates findings.'),
    ('Data Engineer', 'Builds data ingestion, transformation, and analytics pipelines.'),
    ('Data Scientist', 'Uses statistical and machine-learning methods to analyze data.'),
    ('Machine Learning Engineer', 'Develops and operates machine-learning applications.'),
    ('Cybersecurity Analyst', 'Monitors systems and investigates technical security risks.'),
    ('Network Engineer', 'Designs, configures, and troubleshoots computer networks.'),
    ('Database Administrator', 'Operates, secures, and maintains database systems.'),
    ('UI/UX Engineer', 'Designs and implements accessible user-interface experiences.'),
    ('IT Support Engineer', 'Troubleshoots end-user, operating-system, and network issues.'),
    ('Business Analyst', 'Translates business needs into measurable technical requirements.'),
    ('Systems Analyst', 'Analyzes application and information-system requirements and interfaces.')
ON CONFLICT (title) DO NOTHING;

INSERT INTO skills (canonical_name, domain_cluster)
VALUES
    ('Python', 'Programming'),
    ('Java', 'Programming'),
    ('JavaScript', 'Programming'),
    ('TypeScript', 'Programming'),
    ('C#', 'Programming'),
    ('Kotlin', 'Programming'),
    ('Flutter', 'Mobile Development'),
    ('SQL', 'Data and Databases'),
    ('HTML', 'Web Development'),
    ('CSS', 'Web Development'),
    ('React', 'Web Development'),
    ('Angular', 'Web Development'),
    ('Node.js', 'Backend Development'),
    ('FastAPI', 'Backend Development'),
    ('ASP.NET Core', 'Backend Development'),
    ('Spring Boot', 'Backend Development'),
    ('REST APIs', 'Backend Development'),
    ('PostgreSQL', 'Data and Databases'),
    ('MongoDB', 'Data and Databases'),
    ('Git', 'Development Tools'),
    ('Linux', 'Systems and Networking'),
    ('Docker', 'Cloud and DevOps'),
    ('Kubernetes', 'Cloud and DevOps'),
    ('CI/CD', 'Cloud and DevOps'),
    ('Terraform', 'Cloud and DevOps'),
    ('AWS', 'Cloud and DevOps'),
    ('Microsoft Azure', 'Cloud and DevOps'),
    ('Power BI', 'Data and Analytics'),
    ('Tableau', 'Data and Analytics'),
    ('Pandas', 'Data and Analytics'),
    ('NumPy', 'Data and Analytics'),
    ('Apache Spark', 'Data and Analytics'),
    ('Apache Airflow', 'Data and Analytics'),
    ('scikit-learn', 'Machine Learning'),
    ('TensorFlow', 'Machine Learning'),
    ('PyTorch', 'Machine Learning'),
    ('Natural Language Processing', 'Machine Learning'),
    ('OWASP Top 10', 'Cybersecurity'),
    ('Burp Suite', 'Cybersecurity'),
    ('Wireshark', 'Systems and Networking'),
    ('TCP/IP Networking', 'Systems and Networking'),
    ('Selenium', 'Quality Engineering'),
    ('Playwright', 'Quality Engineering'),
    ('Figma', 'UI/UX')
ON CONFLICT (canonical_name) DO NOTHING;

INSERT INTO skill_aliases (raw_term, skill_id)
SELECT alias.raw_term, skill.skill_id
FROM (
    VALUES
        ('py', 'Python'),
        ('python3', 'Python'),
        ('js', 'JavaScript'),
        ('ecmascript', 'JavaScript'),
        ('ts', 'TypeScript'),
        ('c sharp', 'C#'),
        ('kotlin lang', 'Kotlin'),
        ('flutter framework', 'Flutter'),
        ('structured query language', 'SQL'),
        ('hypertext markup language', 'HTML'),
        ('cascading style sheets', 'CSS'),
        ('react.js', 'React'),
        ('reactjs', 'React'),
        ('angular.js', 'Angular'),
        ('nodejs', 'Node.js'),
        ('fast api', 'FastAPI'),
        ('asp.net', 'ASP.NET Core'),
        ('dotnet core', 'ASP.NET Core'),
        ('spring', 'Spring Boot'),
        ('restful api', 'REST APIs'),
        ('postgres', 'PostgreSQL'),
        ('postgresql database', 'PostgreSQL'),
        ('mongo', 'MongoDB'),
        ('version control with git', 'Git'),
        ('gnu/linux', 'Linux'),
        ('containerization with docker', 'Docker'),
        ('k8s', 'Kubernetes'),
        ('continuous integration and delivery', 'CI/CD'),
        ('amazon web services', 'AWS'),
        ('azure', 'Microsoft Azure'),
        ('powerbi', 'Power BI'),
        ('scikit learn', 'scikit-learn'),
        ('sklearn', 'scikit-learn'),
        ('natural language processing (nlp)', 'Natural Language Processing'),
        ('owasp', 'OWASP Top 10'),
        ('burp', 'Burp Suite'),
        ('tcp/ip', 'TCP/IP Networking'),
        ('selenium webdriver', 'Selenium'),
        ('playwright test', 'Playwright'),
        ('figma design', 'Figma')
) AS alias(raw_term, canonical_name)
JOIN skills AS skill ON skill.canonical_name = alias.canonical_name
ON CONFLICT DO NOTHING;

INSERT INTO role_skills (role_id, skill_id, required_level, importance_weight)
SELECT role.role_id, skill.skill_id, mapping.required_level, mapping.importance_weight
FROM (
    VALUES
        ('Software Engineer', 'Python', 3, 1.0),
        ('Software Engineer', 'Java', 3, 1.0),
        ('Software Engineer', 'C#', 2, 0.8),
        ('Software Engineer', 'Git', 3, 0.9),
        ('Software Engineer', 'REST APIs', 2, 0.8),

        ('Frontend Developer', 'JavaScript', 4, 1.0),
        ('Frontend Developer', 'TypeScript', 3, 0.9),
        ('Frontend Developer', 'HTML', 4, 1.0),
        ('Frontend Developer', 'CSS', 4, 1.0),
        ('Frontend Developer', 'React', 3, 0.9),
        ('Frontend Developer', 'Angular', 2, 0.7),
        ('Frontend Developer', 'Figma', 2, 0.6),

        ('Backend Developer', 'Python', 3, 1.0),
        ('Backend Developer', 'Node.js', 3, 0.9),
        ('Backend Developer', 'FastAPI', 3, 0.9),
        ('Backend Developer', 'ASP.NET Core', 2, 0.8),
        ('Backend Developer', 'Spring Boot', 2, 0.8),
        ('Backend Developer', 'REST APIs', 4, 1.0),
        ('Backend Developer', 'PostgreSQL', 3, 0.9),

        ('Full-Stack Developer', 'JavaScript', 3, 1.0),
        ('Full-Stack Developer', 'TypeScript', 2, 0.8),
        ('Full-Stack Developer', 'React', 3, 0.9),
        ('Full-Stack Developer', 'Node.js', 3, 0.9),
        ('Full-Stack Developer', 'REST APIs', 3, 0.9),
        ('Full-Stack Developer', 'PostgreSQL', 2, 0.8),

        ('Mobile Application Developer', 'Kotlin', 3, 1.0),
        ('Mobile Application Developer', 'Flutter', 3, 1.0),
        ('Mobile Application Developer', 'Java', 2, 0.7),
        ('Mobile Application Developer', 'REST APIs', 2, 0.8),

        ('QA Automation Engineer', 'Python', 2, 0.8),
        ('QA Automation Engineer', 'Java', 2, 0.8),
        ('QA Automation Engineer', 'Selenium', 4, 1.0),
        ('QA Automation Engineer', 'Playwright', 3, 0.9),
        ('QA Automation Engineer', 'Git', 2, 0.7),
        ('QA Automation Engineer', 'CI/CD', 2, 0.7),

        ('DevOps Engineer', 'Linux', 4, 1.0),
        ('DevOps Engineer', 'Git', 3, 0.8),
        ('DevOps Engineer', 'Docker', 3, 1.0),
        ('DevOps Engineer', 'Kubernetes', 3, 0.9),
        ('DevOps Engineer', 'CI/CD', 4, 1.0),
        ('DevOps Engineer', 'Terraform', 3, 0.9),
        ('DevOps Engineer', 'AWS', 2, 0.8),

        ('Cloud Engineer', 'Linux', 3, 0.8),
        ('Cloud Engineer', 'Docker', 3, 0.9),
        ('Cloud Engineer', 'Kubernetes', 2, 0.8),
        ('Cloud Engineer', 'Terraform', 3, 0.9),
        ('Cloud Engineer', 'AWS', 3, 1.0),
        ('Cloud Engineer', 'Microsoft Azure', 3, 1.0),
        ('Cloud Engineer', 'TCP/IP Networking', 2, 0.8),

        ('Data Analyst', 'SQL', 4, 1.0),
        ('Data Analyst', 'Python', 2, 0.7),
        ('Data Analyst', 'Pandas', 3, 0.9),
        ('Data Analyst', 'Power BI', 3, 0.9),
        ('Data Analyst', 'Tableau', 3, 0.9),
        ('Data Analyst', 'NumPy', 2, 0.6),

        ('Data Engineer', 'Python', 3, 0.9),
        ('Data Engineer', 'SQL', 4, 1.0),
        ('Data Engineer', 'PostgreSQL', 3, 0.9),
        ('Data Engineer', 'Apache Spark', 3, 0.9),
        ('Data Engineer', 'Apache Airflow', 3, 0.9),
        ('Data Engineer', 'Docker', 2, 0.7),
        ('Data Engineer', 'AWS', 2, 0.7),

        ('Data Scientist', 'Python', 4, 1.0),
        ('Data Scientist', 'SQL', 2, 0.7),
        ('Data Scientist', 'Pandas', 4, 0.9),
        ('Data Scientist', 'NumPy', 3, 0.8),
        ('Data Scientist', 'scikit-learn', 3, 0.9),
        ('Data Scientist', 'TensorFlow', 2, 0.7),
        ('Data Scientist', 'PyTorch', 2, 0.7),

        ('Machine Learning Engineer', 'Python', 4, 1.0),
        ('Machine Learning Engineer', 'scikit-learn', 3, 0.9),
        ('Machine Learning Engineer', 'TensorFlow', 3, 0.9),
        ('Machine Learning Engineer', 'PyTorch', 3, 0.9),
        ('Machine Learning Engineer', 'Natural Language Processing', 2, 0.8),
        ('Machine Learning Engineer', 'FastAPI', 2, 0.7),
        ('Machine Learning Engineer', 'Docker', 2, 0.7),

        ('Cybersecurity Analyst', 'Linux', 3, 0.9),
        ('Cybersecurity Analyst', 'Python', 2, 0.7),
        ('Cybersecurity Analyst', 'OWASP Top 10', 3, 0.9),
        ('Cybersecurity Analyst', 'Burp Suite', 3, 0.9),
        ('Cybersecurity Analyst', 'Wireshark', 3, 0.9),
        ('Cybersecurity Analyst', 'TCP/IP Networking', 3, 0.9),

        ('Network Engineer', 'Linux', 2, 0.7),
        ('Network Engineer', 'Wireshark', 3, 0.9),
        ('Network Engineer', 'TCP/IP Networking', 4, 1.0),
        ('Network Engineer', 'AWS', 2, 0.6),
        ('Network Engineer', 'Microsoft Azure', 2, 0.6),

        ('Database Administrator', 'SQL', 4, 1.0),
        ('Database Administrator', 'PostgreSQL', 4, 1.0),
        ('Database Administrator', 'MongoDB', 2, 0.7),
        ('Database Administrator', 'Linux', 3, 0.8),
        ('Database Administrator', 'AWS', 2, 0.6),

        ('UI/UX Engineer', 'Figma', 4, 1.0),
        ('UI/UX Engineer', 'HTML', 2, 0.7),
        ('UI/UX Engineer', 'CSS', 3, 0.8),
        ('UI/UX Engineer', 'JavaScript', 2, 0.6),
        ('UI/UX Engineer', 'React', 2, 0.6),

        ('IT Support Engineer', 'Linux', 3, 0.9),
        ('IT Support Engineer', 'TCP/IP Networking', 3, 0.9),
        ('IT Support Engineer', 'Wireshark', 2, 0.7),
        ('IT Support Engineer', 'Microsoft Azure', 2, 0.6),

        ('Business Analyst', 'SQL', 2, 0.8),
        ('Business Analyst', 'Power BI', 2, 0.7),
        ('Business Analyst', 'Tableau', 2, 0.7),
        ('Business Analyst', 'Figma', 2, 0.6),
        ('Business Analyst', 'REST APIs', 2, 0.7),

        ('Systems Analyst', 'SQL', 3, 0.9),
        ('Systems Analyst', 'REST APIs', 3, 0.9),
        ('Systems Analyst', 'Java', 2, 0.7),
        ('Systems Analyst', 'ASP.NET Core', 2, 0.7),
        ('Systems Analyst', 'Spring Boot', 2, 0.7),
        ('Systems Analyst', 'PostgreSQL', 2, 0.7)
) AS mapping(role_title, canonical_name, required_level, importance_weight)
JOIN job_roles AS role ON role.title = mapping.role_title
JOIN skills AS skill ON skill.canonical_name = mapping.canonical_name
ON CONFLICT (role_id, skill_id) DO NOTHING;

SELECT refresh_skill_demand();

COMMIT;
