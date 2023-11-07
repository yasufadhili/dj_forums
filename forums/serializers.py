from django.contrib.auth import get_user_model

from rest_framework import (
    serializers,
)

from forums.models.ForumModel import Forum
from forums.models.ThreadModel import Thread
from forums.models.PostModel import Post
from forums.models.CommentModel import Comment
from forums.models.EngagementModel import UpVote, DownVote


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class DownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownVote
        fields = "__all__"


class UpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpVote
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"


class ForumSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=False, required=True)
    #author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Forum
        fields = (
            "id",
            "title",
            "slug",
            "image",
            "description",
            "accessibility",
            "posting_permissions",
            "author",
            "created_at",
            "updated_at"
        )
