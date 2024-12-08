from django.urls import path
from .views import (
    home,
    single_news,
    all_news,
    register,
    login_view,
    logout_view,
    profile,
    add_news,
    edit_news,
)

urlpatterns = [
    path("", home, name="home"),
    path("news/", all_news, name="news_list"),
    path("news/<int:news_id>/", single_news, name="single_news"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path("add_news/", add_news, name="add_news"),
    path("edit_news/<int:news_id>/", edit_news, name="edit_news"),
]
