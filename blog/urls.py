from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router - will be included in main urls.py
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'comments', views.CommentViewSet, basename='comment')

app_name = 'blog'

urlpatterns = [
    # Frontend URLs
    path('', views.BlogListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category_detail'),
    path('tag/<slug:slug>/', views.TagListView.as_view(), name='tag_detail'),
    path('<slug:slug>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
]

