
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API routes
    path("follow/<int:user_id>", views.follow_toggle, name="follow_toggle"),
    path("post-update/<int:post_id>", views.post_update, name="post_update")
]
