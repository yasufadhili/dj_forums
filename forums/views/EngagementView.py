
from rest_framework import (
    permissions,
    viewsets
)

from forums.models.EngagementModel import UpVote, DownVote

from forums.serializers import UpVoteSerializer, DownVoteSerializer

from forums.permissions import IsAuthorOrReadOnly


class UpVoteViewSet(viewsets.ModelViewSet):
    queryset = UpVote.objects.all()
    serializer_class = UpVoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class DownVoteViewSet(viewsets.ModelViewSet):
    queryset = DownVote.objects.all()
    serializer_class = DownVoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

