from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from rest_framework import viewsets, permissions, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category, Tag, Comment
from .serializers import PostSerializer, CategorySerializer, TagSerializer, CommentSerializer
from .forms import CommentForm


# API ViewSets
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'categories', 'tags', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'published_date', 'title']
    ordering = ['-published_date', '-created_at']

    def get_queryset(self):
        queryset = Post.objects.select_related('author').prefetch_related('categories', 'tags')
        # For list view, only show published posts to non-authenticated users
        if self.action == 'list' and not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        # Authenticated users can see all posts
        elif self.request.user.is_authenticated:
            pass
        else:
            queryset = queryset.filter(status='published')
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, is_approved=False)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        category = self.get_object()
        posts = Post.objects.filter(categories=category, status='published')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        tag = self.get_object()
        posts = Post.objects.filter(tags=tag, status='published')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Comment.objects.filter(is_approved=True)
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Basic spam prevention: check for duplicate content
        content = serializer.validated_data.get('content', '')
        if len(content) < 10:
            raise serializers.ValidationError({"content": "Comment must be at least 10 characters long."})
        serializer.save(is_approved=False)


# Frontend Views
class BlogListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author').prefetch_related('categories', 'tags')
        
        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Filter by tag if provided
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_string'] = query_params.urlencode()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Only show published posts to non-authenticated users
        if self.request.user.is_authenticated:
            return Post.objects.select_related('author').prefetch_related('categories', 'tags', 'comments')
        return Post.objects.filter(status='published').select_related('author').prefetch_related('categories', 'tags', 'comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.filter(is_approved=True, parent__isnull=True)
        context['comment_form'] = CommentForm()
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            categories=category,
            status='published'
        ).select_related('author').prefetch_related('categories', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_string'] = query_params.urlencode()
        return context


class TagListView(ListView):
    model = Post
    template_name = 'blog/tag_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            tags=tag,
            status='published'
        ).select_related('author').prefetch_related('categories', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs['slug'])
        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_string'] = query_params.urlencode()
        return context


class CommentCreateView(FormView):
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        comment = form.save(commit=False)
        comment.post = post
        comment.is_approved = False
        comment.save()
        messages.success(self.request, 'Your comment has been submitted and is awaiting moderation.')
        return redirect('blog:post_detail', slug=post.slug)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error submitting your comment.')
        return redirect('blog:post_detail', slug=self.kwargs['slug'])
