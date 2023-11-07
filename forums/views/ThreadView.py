
from django.db import models


from rest_framework import (
    permissions,
    viewsets,
    decorators,
    response,
    status
)

from forums.models.ThreadModel import Thread

from forums.serializers import ThreadSerializer

from forums.permissions import IsAuthorOrReadOnly


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = "id"

    @decorators.action(detail=True, methods=['get'])
    def related_threads(self, request, forum_id=None, id=None):
        thread = self.get_object()
        related_threads = Thread.objects.filter(forum=thread.forum).exclude(id=thread.id)[:5]
        serialized_related_threads = ThreadSerializer(related_threads, many=True)
        return response.Response(serialized_related_threads.data, status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=['get'])
    def top_threads(self, request):
        # Implement logic to retrieve top threads
        # Example: Get threads with the highest number of likes
        top_threads = Thread.objects.annotate(like_count=models.Count('upvotes')).order_by('-like_count')[:10]
        serialized_top_threads = ThreadSerializer(top_threads, many=True)
        return response.Response(serialized_top_threads.data, status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=['post'])
    def create_thread_with_attributes(self, request, forum_id=None):
        # Customize thread creation logic with additional attributes
        # Example: Custom attribute handling
        custom_attribute = request.data.get('custom_attribute')
        if not custom_attribute:
            return response.Response({"message": "Custom attribute is required."}, status=status.HTTP_400_BAD_REQUEST)
        forum = Forum.objects.get(id=forum_id)
        thread = Thread(forum=forum, author=request.user, title=request.data['title'], content=request.data['content'])
        thread.custom_attribute = custom_attribute
        thread.save()
        return response.Response({"message": "Thread created with custom attributes"}, status=status.HTTP_201_CREATED)

