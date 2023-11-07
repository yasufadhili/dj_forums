from rest_framework import (
    permissions,
    viewsets
)

from forums.models.CommentModel import Comment

from forums.serializers import CommentSerializer

from forums.permissions import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = "id"
