from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import News
from .forms import CommentForm, NewsForm


def home(request):
    news = News.objects.order_by("-published_date")[:3]
    return render(request, "home.html", {"latest_news": news})


def all_news(request):
    news_all = News.objects.all().order_by("-published_date")
    return render(request, "all_news.html", {"news": news_all})


def single_news(request, news_id: int):
    single_news = get_object_or_404(News, id=news_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = single_news
            comment.user = request.user
            comment.save()
            return redirect("single_news", news_id=news_id)
    else:
        comment_form = CommentForm()
    comments = single_news.comments.all()
    return render(
        request,
        "single_news.html",
        {"news_item": single_news, "comment_form": comment_form, "comments": comments},
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"{username} создан")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    user = request.user
    comments = user.comment_set.all()
    user_news = News.objects.filter(author=user)

    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("profile")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(
        request, "profile.html", {"form": form, "comments": comments, "news": user_news}
    )


@login_required
def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.author = request.user
            news_item.save()
            return redirect("news_list")
    else:
        form = NewsForm()

    return render(request, "add_news.html", {"form": form})


@login_required
def edit_news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect("single_news", news_id=news_item.id)
    else:
        form = NewsForm(instance=news_item)

    return render(request, "edit_news.html", {"form": form, "news_item": news_item})
