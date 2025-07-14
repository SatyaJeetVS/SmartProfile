from rest_framework import serializers
from .models import Profile, Skill, Project, Experience, ContactSubmission

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency', 'category']

class ProjectSerializer(serializers.ModelSerializer):
    technologies = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'technologies', 'github_url', 
                 'live_url', 'image', 'category', 'created_at']

class ExperienceSerializer(serializers.ModelSerializer):
    technologies = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company', 'position', 'start_date', 'end_date', 
                 'description', 'technologies']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'tagline', 'bio', 'email', 'github_username', 
                 'linkedin_url', 'resume_file']

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'message', 'timestamp']
