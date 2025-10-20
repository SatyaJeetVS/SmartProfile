from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from .tasks import send_contact_email
import logging

logger = logging.getLogger('portfolio.views')
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from .models import Profile, Skill, Project, Experience, ContactSubmission, PageVisit
from .serializers import (ProfileSerializer, SkillSerializer, ProjectSerializer,
                        ExperienceSerializer, ContactSubmissionSerializer)

class HomeView(TemplateView):
    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        context['skills'] = Skill.objects.all()
        context['projects'] = Project.objects.all()
        context['experiences'] = Experience.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        # Track page visit
        PageVisit.objects.create(
            page='home',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return super().get(request, *args, **kwargs)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def github_activity(self, request):
        profile = self.get_queryset().first()
        if not profile:
            return Response([])
        
        url = f"https://api.github.com/users/{profile.github_username}/events/public"
        response = requests.get(url)
        if response.status_code == 200:
            return Response(response.json()[:10])  # Return last 10 activities
        return Response([])


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        skills = self.get_queryset()
        data = {}
        for category, _ in Skill.CATEGORY_CHOICES:
            category_skills = skills.filter(category=category)
            data[category] = SkillSerializer(category_skills, many=True).data
        return Response(data)

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Project.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ContactSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    # Allow unauthenticated users to submit the contact form
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Send email notification asynchronously via Celery
        logger.info('ContactSubmission created: %s <%s>', serializer.data.get('name'), serializer.data.get('email'))
        try:
            send_contact_email.delay(
                serializer.data['name'],
                serializer.data['email'],
                serializer.data['message'],
            )
            logger.info('Enqueued send_contact_email task for %s', serializer.data.get('email'))
        except Exception:
            logger.exception('Failed to enqueue send_contact_email; falling back to synchronous send')
            # fallback synchronous send
            try:
                from django.core.mail import send_mail
                profile = Profile.objects.first()
                recipient = profile.email if profile else settings.DEFAULT_FROM_EMAIL
                send_mail(
                    subject=f'New Contact Form Submission from {serializer.data["name"]}',
                    message=f'Name: {serializer.data["name"]}\nEmail: {serializer.data["email"]}\nMessage: {serializer.data["message"]}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                logger.info('Synchronous contact email sent to %s', recipient)
            except Exception:
                logger.exception('Synchronous fallback send also failed')
        return Response(serializer.data)
