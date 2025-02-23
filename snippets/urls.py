from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views

router = DefaultRouter()

router.register("snippets", views.SnippetViewSet, basename="snippet")
router.register("users", views.UserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
]