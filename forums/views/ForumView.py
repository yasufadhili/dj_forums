from django.contrib.auth import get_user_model

from rest_framework import (
    viewsets,
    permissions,
    generics,
    status,
)

from forums.models.ForumModel import Forum, ForumRating

from forums.serializers import ForumSerializer

User = get_user_model()


class ForumViewSet(viewsets.ModelViewSet):
    serializer_class = ForumSerializer
    queryset = Forum.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"
