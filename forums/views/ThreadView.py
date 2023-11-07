
from rest_framework import (
    permissions,
    viewsets
)

from forums.models.ThreadModel import Thread

from forums.serializers import ThreadSerializer

from forums.permissions import IsAuthorOrReadOnly

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = "id"
