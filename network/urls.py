
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("post", views.compose, name="compose"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("likes", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("save", views.save, name="save"),
]
