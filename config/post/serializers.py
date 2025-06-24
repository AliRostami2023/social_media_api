from rest_framework import serializers
from .models import *


class ExplorPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'description', 'image', 'video', 'public']


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'video', 'image', 'public']



class RepostSerializers(serializers.ModelSerializer):
    post_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['post_id']
        read_only_fields = ['id', 'user', 'title','slug', 'description',
                   'image', 'video', 'created', 'updated',
                     'public', 'like_count', 'orginal_post']


class LikePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['id', 'user', 'post', 'created']


class UserSimpleSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'avatar']

    def get_avatar(self, obj):
        request = self.context.get('request')
        profile = getattr(obj, 'profile', None)
        if profile and profile.avatar:
            return request.build_absolute_uri(profile.avatar.url) if request else profile.avatar.url
        return None


class CommentCreateSerializers(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    post = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "body"]


class CommentListSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    post = serializers.CharField(source="post.title")

    class Meta:
        model = Comment
        fields = "__all__"


class CommentUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
        

class ReplyCreateSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    post = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ReplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
