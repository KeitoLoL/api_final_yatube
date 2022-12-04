from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('text', 'created', 'id', 'author', 'post')
        model = Comment
        read_only_fields = ['post']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'slug', 'description')
        model = Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('text', 'author', 'pub_date', 'group', 'id')
        model = Post


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('following', 'user')
        model = Follow
        unique_together = ('user', 'following',)

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

        def validate_following(self, data):
            if self.context['request'].user == data['following']:
                raise serializers.ValidationError(
                    'Подписка на самого себя-невозможна.'
                )
            return data
