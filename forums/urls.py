from django.urls import path, include
from rest_framework.routers import DefaultRouter

from forums.views.ForumView import ForumViewSet
from forums.views.ThreadView import ThreadViewSet
from forums.views.PostView import PostViewSet
from forums.views.CommentView import CommentViewSet
from forums.views.EngagementView import UpVoteViewSet, DownVoteViewSet

router = DefaultRouter()
router.register(r"", ForumViewSet)
router.register(r"threads", ThreadViewSet)
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"engagements/upvotes", UpVoteViewSet)
router.register(r"engagements/downvotes", DownVoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("<uuid:forum_id>/", include([
        path("", ForumViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
        path("threads/", include([
            path("", ThreadViewSet.as_view({"get": "list"})),
            path("<uuid:thread_id>/", include([
                path("", ThreadViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
                path("posts/", include([
                    path("", PostViewSet.as_view({"get": "list"})),
                    path("<uuid:post_id>/", include([
                        path("", PostViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
                        path("comments/", include([
                            path("", CommentViewSet.as_view({"get": "list"})),
                            path("<uuid:comment_id>/", CommentViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
                        ])),
                    ])),
                ])),
            ])),
        ])),
    ])),
]

