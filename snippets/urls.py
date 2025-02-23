from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path("", views.api_root, name="index"),
    path("snippets/", views.SnippetList.as_view(), name="snippet-list"),
    path("snippets/<int:pk>", views.SnippetDetail.as_view(), name="snippet-details"),
    path("snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view(), name="snippet-highlight"),

    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)