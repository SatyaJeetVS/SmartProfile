from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import Profile, Skill, Project, Experience

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create Profile
        profile = Profile.objects.create(
            name='Satyajeet Suryawanshi',
            tagline='Python Backend Developer | API & Automation Expert',
            bio='''Python Backend Developer with over 3 years of experience building robust, scalable APIs using FastAPI. 
            Expert in asynchronous programming, RESTful architecture, and Kubernetes-based environments. Strong focus on 
            creating efficient, maintainable code and automating complex workflows.''',
            email='satyajeet1400@gmail.com',
            github_username='satyajeet1400',
            linkedin_url='https://www.linkedin.com/in/satyajeet-suryawanshi/'
        )

        # Create Skills
        skills = {
            'Python': ('BACKEND', 90),
            'FastAPI': ('BACKEND', 85),
            'SQLAlchemy': ('BACKEND', 85),
            'Pydantic': ('BACKEND', 80),
            'SQL': ('DATABASE', 85),
            'PostgreSQL': ('DATABASE', 85),
            'MySQL': ('DATABASE', 80),
            'Kubernetes': ('DEVOPS', 80),
            'Docker': ('DEVOPS', 85),
            'Shell Scripting': ('DEVOPS', 75),
            'Git': ('DEVOPS', 85),
            'Prometheus': ('DEVOPS', 75),
            'OAuth2': ('BACKEND', 80),
            'REST APIs': ('BACKEND', 90),
        }

        created_skills = {}
        for name, (category, proficiency) in skills.items():
            skill = Skill.objects.create(
                name=name,
                category=category,
                proficiency=proficiency
            )
            created_skills[name] = skill

        # Create Projects
        projects = [
            {
                'title': 'DBaaS Backend Service',
                'description': '''Developed a Database-as-a-Service backend using FastAPI, handling automated database 
                provisioning and management. Implemented OAuth2 authentication, monitoring with Prometheus, and integration 
                with PostgreSQL/MySQL.''',
                'technologies': ['Python', 'FastAPI', 'PostgreSQL', 'MySQL', 'Kubernetes', 'OAuth2', 'Prometheus'],
                'category': 'BACKEND'
            },
            {
                'title': 'Automated Remediation Framework',
                'description': '''Created a framework for automating security incident response and system remediation tasks. 
                Developed Python scripts for analyzing security events and implementing automated fixes.''',
                'technologies': ['Python', 'Shell Scripting', 'Git'],
                'category': 'DEVOPS'
            },
            {
                'title': 'Kubernetes Automation Scripts',
                'description': '''Developed a suite of Python scripts for automating Kubernetes resource management, including 
                deployment orchestration, scaling, and monitoring.''',
                'technologies': ['Python', 'Kubernetes', 'Docker', 'Shell Scripting'],
                'category': 'DEVOPS'
            }
        ]

        for project_data in projects:
            project = Project.objects.create(
                title=project_data['title'],
                description=project_data['description'],
                category=project_data['category']
            )
            for tech in project_data['technologies']:
                project.technologies.add(created_skills[tech])

        # Create Experience
        experience = Experience.objects.create(
            company='Jio Platforms Limited',
            position='Python Backend Developer',
            start_date=timezone.datetime(2022, 7, 1).date(),
            end_date=None,
            description='''• Architected and developed highly scalable backend services using FastAPI and PostgreSQL/MySQL
• Designed and implemented RESTful APIs with OAuth2 authentication and role-based access control
• Created automated deployment pipelines and managed Kubernetes-based infrastructure
• Developed monitoring solutions using Prometheus for system metrics and performance analysis
• Implemented database migration and backup strategies for critical services
• Mentored junior developers and conducted code reviews to maintain code quality'''
        )
        
        tech_skills = ['Python', 'FastAPI', 'PostgreSQL', 'MySQL', 'Kubernetes', 'OAuth2', 'Prometheus']
        for skill_name in tech_skills:
            experience.technologies.add(created_skills[skill_name])

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))
