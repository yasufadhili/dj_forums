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

    @decorators.action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        forum = self.get_object()
        if request.user not in forum.subscribers.all():
            return response.Response({"message": "Not subscribed to the forum."}, status=status.HTTP_400_BAD_REQUEST)
        forum.subscribers.remove(request.user)
        forum.save()
        return response.Response({"message": "Unsubscribed from the forum."}, status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q')
        if not query:
            return response.Response({"message": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)
        results = Forum.objects.filter(title__icontains=query)
        serialized_results = ForumSerializer(results, many=True)
        return response.Response(serialized_results.data, status=status.HTTP_200_OK)

    






