import json
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    if request.method == "POST":
        # Get the new post's text
        text = request.POST["text"]
        author = User.objects.get(pk=request.user.id)
        new_post = Post(author=author, text=text)
        new_post.save()
        # time_creation auto-incremente on 1st save.
        # auto incrementing time_last_update appear some few microseconds after time_creation
        # the difference between those to time have to be null to evaluate a never-edited post
        # that why time_last_update is just copying time_creation on the first save
        new_post.time_last_update = new_post.time_creation
        new_post.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        posts_page = get_posts_page(request, "all")
        return render(request, "network/index.html", {
            "h1": "All Posts",
            "posts": posts_page,
            "display_new_post": True
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, user_id):
    visited_user = User.objects.get(pk=user_id)
    followings = User.objects.filter(followers=visited_user).count()
    posts_page = get_posts_page(request, user_id)
    # last line sound weird but usefull to block new post from another user profile
    return render(request, "network/index.html", {
        "visited_user": visited_user,
        "followings": followings,
        "posts": posts_page,
        "display_new_post": request.user == visited_user,
        # allow new post only when the current user visit its how profile
        "h1": "profile"
    })

@login_required
def following(request):
    user = request.user
    followed = User.objects.filter(followers=user)
    posts_page = get_posts_page(request, followed)
    following_count = followed.count()
    return render(request, "network/index.html", {
        "h1": "Following",
        "posts": posts_page,
        "display_new_post": False,
        "following_count": following_count
        })



########### API features:  ##############
@login_required
def follow_toggle(request, user_id):
    visited_user = User.objects.get(pk=user_id)
    visitor = request.user
    # 1st find if the visitor was following the visited_user
    is_following = False
    for follower in visited_user.followers.all():
        if visitor == follower:
            is_following = True
            break
    # 2nd update the visited_user.followers according
    if is_following:
        visited_user.followers.remove(visitor)
    else: 
        visited_user.followers.add(visitor)
    visited_user.save()
    return HttpResponse(status=204)


def get_posts_page(request, user_id):
    # get all the posts according the need: all users, a list of followed users or a specific user_id
    if user_id == "all":
        posts = Post.objects.all().order_by("time_last_update").reverse()
    elif type(user_id) == type(User.objects.filter(followers=1)):
        # COMPARAISON DE TYPE PAS BELLE !!!
        posts = Post.objects.filter(author__in=user_id).order_by("time_last_update").reverse()
    else:
        visited_user = User.objects.get(pk=user_id)
        posts = visited_user.author.order_by("time_last_update").reverse()
    # paginate the posts object
    posts_paginated = Paginator(posts, 10)
    # get the page number  defaut is 1
    page_number = int(request.GET.get("page", 1))
    # return the right posts page
    return posts_paginated.get_page(page_number)

@login_required
@csrf_exempt
def post_update(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        new_content = json.loads(request.body)
        post.text = new_content
        post.time_last_update = datetime.now()
        post.save()
        return HttpResponse(status=204)

@login_required
@csrf_exempt
def like_toggle(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    post.save()
    return HttpResponse(status=204)
