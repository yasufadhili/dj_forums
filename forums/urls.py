from django.urls import path, include

from rest_framework import urls, routers

from forums.views.ForumView import ForumViewSet


router = routers.DefaultRouter()
router.register(r"", ForumViewSet, basename="forum")

urlpatterns = [
    path("", include(router.urls))
]

