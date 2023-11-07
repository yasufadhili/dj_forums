
from rest_framework import (
    permissions,
    viewsets
)

from forums.models.PostModel import Post

from forums.serializers import PostSerializer

from forums.permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = "id"

