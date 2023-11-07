from django.contrib.auth import get_user_model

from rest_framework import (
    viewsets,
    permissions,
    generics,
    status,
)

from forums.models.ForumModel import Forum, ForumRating

from forums.serializers import ForumSerializer

from forums.permissions import IsAuthorOrReadOnly

User = get_user_model()


class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




