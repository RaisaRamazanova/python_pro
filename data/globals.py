import logging
import threading
from telegram.ext import ApplicationBuilder

TOKEN = "6914866790:AAHQFOHkYzPqRSByECISnNwGRLy1uXFieU8"
PAYMENTS_TOKEN = '381764678:TEST:76546'

data_path = '/Users/raisatramazanova/development/python_bot/python_pro_bot/data.sqlite'

logger = logging.getLogger(__name__)
application = ApplicationBuilder().token(TOKEN).build()
lock = threading.Lock()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

types_of_topics = {
    'languages': 1,
    'frameworks': 2,
    'tools': 3,
    'options': 4,
}

STAGE_MAPPING_LEVELS = ['Junior', 'Middle', 'Senior']

STAGE_MAPPING = {}

# STAGE_MAPPING = {
#     "Backend": {
#         "options": ["API Development", "Microservices", "Database Management", "Cloud Services",
#                     "Serverless Architecture"],
#         "next": {
#             "API Development": {
#                 "languages": ["Python", "Java", "Node.js", "Go"],
#                 "frameworks": ["Django", "Spring Boot", "Express", "Gin"],
#                 "tools": ["Postman", "Swagger", "Docker", "Kubernetes"]
#             },
#             "Microservices": {
#                 "languages": ["Python", "Java", "C#", "Go"],
#                 "frameworks": ["Flask", "Spring Boot", ".NET Core", "Gin"],
#                 "tools": ["Docker", "Kubernetes", "RabbitMQ", "Consul"]
#             },
#             "Database Management": {
#                 "languages": ["SQL", "NoSQL"],
#                 "frameworks": ["MySQL", "PostgreSQL", "MongoDB", "Cassandra"],
#                 "tools": ["DBeaver", "MongoDB Compass", "pgAdmin"]
#             },
#             "Cloud Services": {
#                 "languages": ["Python", "Java", "Node.js"],
#                 "frameworks": ["AWS Lambda", "Google Cloud Functions", "Azure Functions"],
#                 "tools": ["Terraform", "CloudFormation", "Google Cloud Deployment Manager"]
#             },
#             "Serverless Architecture": {
#                 "languages": ["Python", "Node.js", "Go"],
#                 "frameworks": ["Serverless Framework", "SAM", "Cloudflare Workers"],
#                 "tools": ["Serverless Framework", "AWS SAM CLI", "Google Cloud CLI"]
#             }
#         }
#     },
#     "Frontend": {
#         "options": ["iOS Development", "Android Development", "Web Development", "Cross-platform Development",
#                     "Desktop Development"],
#         "next": {
#             "iOS Development": {
#                 "languages": ["Swift", "Objective-C"],
#                 "frameworks": ["UIKit", "SwiftUI"],
#                 "tools": ["Xcode", "CocoaPods", "Fastlane"]
#             },
#             "Android Development": {
#                 "languages": ["Kotlin", "Java"],
#                 "frameworks": ["Android SDK", "Jetpack"],
#                 "tools": ["Android Studio", "Gradle", "Firebase"]
#             },
#             "Web Development": {
#                 "languages": ["HTML", "CSS", "JavaScript", "TypeScript"],
#                 "frameworks": ["React", "Vue.js", "Angular", "Svelte"],
#                 "tools": ["Webpack", "Babel", "ESLint"]
#             },
#             "Cross-platform Development": {
#                 "languages": ["Dart", "JavaScript", "C#"],
#                 "frameworks": ["Flutter", "React Native", "Xamarin"],
#                 "tools": ["Visual Studio Code", "Android Studio", "Xcode"]
#             },
#             "Desktop Development": {
#                 "languages": ["C#", "Java", "JavaScript"],
#                 "frameworks": [".NET", "JavaFX", "Electron"],
#                 "tools": ["Visual Studio", "IntelliJ IDEA", "Electron Packager"]
#             }
#         }
#     }
#     # "DevOps": {
#     #     "options": ["Cloud Infrastructure", "CI/CD Pipelines", "Monitoring and Logging", "Infrastructure as Code",
#     #                 "Containerization"],
#     #     "next": {
#     #         "Cloud Infrastructure": {
#     #             "languages": ["Python", "Ruby", "Shell Scripting"],
#     #             "frameworks": ["AWS Cloud Development Kit (CDK)", "Google Cloud Deployment Manager"],
#     #             "tools": ["Terraform", "CloudFormation", "Ansible"]
#     #         },
#     #         "CI/CD Pipelines": {
#     #             "languages": ["Python", "Groovy", "YAML"],
#     #             "tools": ["Jenkins", "GitLab CI", "CircleCI"],
#     #             "frameworks": ["Jenkins Pipelines", "GitLab CI/CD"]
#     #         },
#     #         "Monitoring and Logging": {
#     #             "languages": ["Python", "Go", "JavaScript"],
#     #             "tools": ["Prometheus", "Grafana", "ELK Stack"],
#     #             "frameworks": ["ELK Stack (Elasticsearch, Logstash, Kibana)", "Prometheus + Grafana"]
#     #         },
#     #         "Infrastructure as Code": {
#     #             "languages": ["Python", "Ruby", "YAML"],
#     #             "tools": ["Terraform", "Ansible", "Puppet"],
#     #             "frameworks": ["Terraform", "CloudFormation", "Ansible"]
#     #         },
#     #         "Containerization": {
#     #             "languages": ["Python", "Go", "Shell Scripting"],
#     #             "tools": ["Docker", "Kubernetes", "Docker Swarm"],
#     #             "frameworks": ["Docker Compose", "Kubernetes"]
#     #         }
#     #     }
#     # },
#     # "QA": {
#     #     "options": ["Manual Testing", "Automated Testing", "Performance Testing", "Security Testing", "API Testing"],
#     #     "next": {
#     #         "Manual Testing": {
#     #             "languages": ["-", "Markdown (for documentation)"],
#     #             "tools": ["JIRA", "TestRail", "Confluence"]
#     #         },
#     #         "Automated Testing": {
#     #             "languages": ["Python", "Java", "JavaScript"],
#     #             "frameworks": ["Selenium WebDriver", "Cypress", "Appium"],
#     #             "tools": ["Selenium", "Cypress", "Puppeteer"]
#     #         },
#     #         "Performance Testing": {
#     #             "languages": ["Java", "Python", "JavaScript"],
#     #             "frameworks": ["Apache JMeter", "LoadRunner", "Gatling"],
#     #             "tools": ["JMeter", "LoadRunner", "Gatling"]
#     #         },
#     #         "Security Testing": {
#     #             "languages": ["Python", "Ruby", "Shell Scripting"],
#     #             "tools": ["OWASP ZAP", "Burp Suite", "Nessus"],
#     #             "frameworks": ["PyTest", "Metasploit Framework", "Nmap Scripting Engine (NSE)"],
#     #         },
#     #         "API Testing": {
#     #             "languages": ["Python", "JavaScript", "Groovy"],
#     #             "tools": ["Postman", "SoapUI", "Katalon Studio"],
#     #             "frameworks": ["Requests", "Mocha с Chai", "Spock"],
#     #         }
#     #     }
#     # },
#     # "Architect": {
#     #     "options": ["System Design", "Microservices Architecture", "Cloud Architecture", "High Availability Systems",
#     #                 "Scalable Systems"],
#     #     "next": {
#     #         "System Design": {
#     #             "languages": ["UML", "Markdown", "PlantUML"],
#     #             "tools": ["Lucidchart", "Microsoft Visio", "Draw.io"],
#     #             "frameworks": ["Spring Cloud", "Netflix OSS"]
#     #         },
#     #         "Microservices Architecture": {
#     #             "languages": ["Python", "Java", "Go"],
#     #             "tools": ["Docker", "Kubernetes", "Istio"],
#     #             "frameworks": ["Spring Boot", "Docker", "Kubernetes"]
#     #         },
#     #         "Cloud Architecture": {
#     #             "languages": ["Python", "Go", "Shell Scripting"],
#     #             "tools": ["AWS Lambda", "Azure Functions", "Google Cloud Functions"],
#     #             "frameworks": ["AWS CloudFormation", "Terraform"]
#     #         },
#     #         "High Availability Systems": {
#     #             "languages": ["Python", "Go", "Shell Scripting"],
#     #             "tools": ["NGINX", "HAProxy", "Keepalived"],
#     #             "frameworks": ["Apache ZooKeeper", "Consul"]
#     #         },
#     #         "Scalable Systems": {
#     #             "languages": ["Python", "Go", "Java"],
#     #             "tools": ["Redis", "Memcached", "Varnish"],
#     #             "frameworks": ["Akka", "RabbitMQ"]
#     #         }
#     #     }
#     # },
#     # "Security": {
#     #     "options": ["Application Security", "Network Security", "Cloud Security", "Penetration Testing",
#     #                 "Cryptography"],
#     #     "next": {
#     #         "Application Security": {
#     #             "languages": ["Python", "JavaScript", "Java"],
#     #             "tools": ["OWASP ZAP", "Burp Suite", "SonarQube"],
#     #             "frameworks": ["OWASP ESAPI", "Spring Security"]
#     #         },
#     #         "Network Security": {
#     #             "languages": ["Python", "Shell Scripting"],
#     #             "tools": ["Wireshark", "Nmap", "Metasploit"],
#     #             "frameworks": ["OpenSSL", "WireGuard"]
#     #         },
#     #         "Cloud Security": {
#     #             "languages": ["Python", "Shell Scripting", "YAML"],
#     #             "tools": ["AWS Security Tools", "Azure Security Center", "Google Cloud Security Command Center"],
#     #             "frameworks": ["HashiCorp Vault", "AWS IAM"]
#     #         },
#     #         "Penetration Testing": {
#     #             "languages": ["Python", "Ruby", "Shell Scripting"],
#     #             "tools": ["Metasploit", "Burp Suite", "OWASP ZAP"],
#     #             "frameworks": ["Metasploit Framework", "Burp Suite"]
#     #         },
#     #         "Cryptography": {
#     #             "languages": ["Python", "C++", "Java"],
#     #             "tools": ["OpenSSL", "GnuPG", "Libsodium"],
#     #             "frameworks": ["Crypto++", "Libsodium"]
#     #         }
#     #     }
#     # },
#     # "Data Science": {
#     #     "options": ["Machine Learning", "Data Analysis", "Big Data", "AI Development", "Statistical Modeling"],
#     #     "next": {
#     #         "Machine Learning": {
#     #             "languages": ["Python", "R", "Scala"],
#     #             "tools": ["TensorFlow", "PyTorch", "Scikit-learn"],
#     #             "frameworks": ["TensorFlow", "PyTorch", "Scikit-learn"]
#     #         },
#     #         "Data Analysis": {
#     #             "languages": ["Python", "R", "SQL"],
#     #             "tools": ["Pandas", "NumPy", "Matplotlib"],
#     #             "frameworks": ["Pandas", "NumPy"]
#     #         },
#     #         "Big Data": {
#     #             "languages": ["Scala", "Java", "Python"],
#     #             "tools": ["Apache Hadoop", "Apache Spark", "Apache Flink"],
#     #             "frameworks": ["Apache Hadoop", "Apache Spark"]
#     #         },
#     #         "AI Development": {
#     #             "languages": ["Python", "C++", "Java"],
#     #             "tools": ["TensorFlow", "Keras", "PyTorch"],
#     #             "frameworks": ["TensorFlow", "Keras"]
#     #         },
#     #         "Statistical Modeling": {
#     #             "languages": ["R", "Python", "SAS"],
#     #             "tools": ["RStudio", "Jupyter Notebook", "Anaconda"],
#     #             "frameworks": ["R", "Stan"]
#     #         }
#     #     }
#     # },
#     # "Systems Analysis": {
#     #     "options": ["Business Analysis", "Systems Design", "Requirement Analysis", "Process Modeling", "Data Modeling"],
#     #     "next": {
#     #         "Business Analysis": {
#     #             "languages": ["UML", "Markdown", "SQL"],
#     #             "tools": ["Microsoft Visio", "Lucidchart", "Balsamiq"],
#     #             "frameworks": ["Babok", "UML"]
#     #         },
#     #         "Systems Design": {
#     #             "languages": ["UML", "PlantUML", "Markdown"],
#     #             "tools": ["Lucidchart", "Microsoft Visio", "Draw.io"],
#     #             "frameworks": ["System Architect", "Enterprise Architect"]
#     #         },
#     #         "Requirement Analysis": {
#     #             "languages": ["Markdown", "UML"],
#     #             "tools": ["JIRA", "Confluence", "Trello"],
#     #             "frameworks": ["ReqIF", "Rational RequisitePro"]
#     #         },
#     #         "Process Modeling": {
#     #             "languages": ["BPMN", "UML"],
#     #             "tools": ["Bizagi", "Lucidchart", "Microsoft Visio"],
#     #             "frameworks": ["BPMN", "Aris"]
#     #         },
#     #         "Data Modeling": {
#     #             "languages": ["SQL", "UML", "ERD"],
#     #             "tools": ["ER/Studio", "Navicat", "Microsoft Visio"],
#     #             "frameworks": ["ER/Studio", "PowerDesigner"]
#     #         }
#     #     }
#     # }
# }
