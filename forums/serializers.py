from django.contrib.auth import get_user_model

from rest_framework import (
    serializers,
)

from forums.models.ForumModel import Forum
from forums.models.ThreadModel import Thread
from forums.models.PostModel import Post
from forums.models.CommentModel import Comment
from forums.models.EngagementModel import Upvote, Downvote


User = get_user_model()


class DownvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Downvote
        fields = "__all__"

class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = "__all__"



