
from rest_framework import (
    permissions,
    viewsets,
    response,
    decorators,
    status
)

from forums.models.PostModel import Post
from forums.models.CommentModel import Comment
from forums.models.EngagementModel import UpVote, DownVote

from forums.serializers import PostSerializer, CommentSerializer

from forums.permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = "id"

    @decorators.action(detail=True, methods=['get'])
    def post_comments(self, request, id=None):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serialized_comments = CommentSerializer(comments, many=True)
        return response.Response(serialized_comments.data, status=status.HTTP_200_OK)

    @decorators.action(detail=True, methods=['post'])
    def like_post(self, request, id=None):
        post = self.get_object()
        upvote, created = UpVote.objects.get_or_create(author=request.user, content_object=post, upvote_type='P')
        if created:
            post.likes += 1
            post.save()
            return response.Response({"message": "Liked the post."}, status=status.HTTP_200_OK)
        else:
            return response.Response({"message": "You have already liked the post."}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True, methods=['post'])
    def dislike_post(self, request, id=None):
        post = self.get_object()
        downvote, created = DownVote.objects.get_or_create(author=request.user, content_object=post, upvote_type='P')
        if created:
            post.dislikes += 1
            post.save()
            return response.Response({"message": "Disliked the post."}, status=status.HTTP_200_OK)
        else:
            return response.Response({"message": "You have already disliked the post."}, status=status.HTTP_400_BAD_REQUEST)


