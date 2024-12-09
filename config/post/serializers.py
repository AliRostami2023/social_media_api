from rest_framework import serializers
from .models import *


class ExplorPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'title', 'description', 'image', 'video', 'public']



class RepostSerializers(serializers.ModelSerializer):
    post_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['post_id']
        read_only_fields = ['id', 'user', 'title','slug', 'description',
                   'image', 'video', 'created', 'updated',
                     'public', 'like_count', 'orginal_post']




class PostListSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'title','slug', 'description',
                   'image', 'video', 'created', 'updated',
                     'public', 'orginal_post', 'is_repost']



class UpdatePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'video', 'image', 'public']
    


class LikePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['id', 'user', 'post', 'created']
    


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



class CommentUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
        