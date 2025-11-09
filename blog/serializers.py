from rest_framework import serializers
from .models import Post, Category, Tag, Comment
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['created_at']


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'author_email', 'content', 
                 'is_approved', 'parent', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['is_approved', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_approved=True), many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all(), 
        source='categories', 
        write_only=True,
        required=False
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.all(), 
        source='tags', 
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'author', 'author_username',
                 'featured_image', 'status', 'published_date', 'created_at', 'updated_at',
                 'categories', 'tags', 'comments', 'category_ids', 'tag_ids']
        read_only_fields = ['slug', 'created_at', 'updated_at', 'author']

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True, parent__isnull=True)
        return CommentSerializer(approved_comments, many=True).data

    def create(self, validated_data):
        # Set author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

