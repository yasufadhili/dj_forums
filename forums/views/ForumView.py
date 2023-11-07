from django.contrib.auth import get_user_model
from django.db import models

from rest_framework import (
    viewsets,
    permissions,
    generics,
    status,
    decorators,
    response
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

    def unsubscribe(self):
        pass

    def search(self):
        pass

    def popular(self):
        pass

    def trending(self):
        pass

    @decorators.action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        forum = self.get_object()
        if request.user in forum.subscribers.all():
            return response.Response({"message": "Already subscribed to the forum."}, status=status.HTTP_400_BAD_REQUEST)
        forum.subscribers.add(request.user)
        forum.save()
        return response.Response({"message": "Subscribed to the forum."}, status=status.HTTP_200_OK)

    






