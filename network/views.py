from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

@login_required
def profile(request, user_id):
    visitor = request.user
    visited_user = User.objects.get(pk=user_id)
    followers = visited_user.followers.count()
    followings = User.objects.filter(followers=visited_user).count()
    posts_page = get_posts_page(request, user_id)
    # Check if the logged user is the owner of the visited profile
    # and if the logged user follows the owner of the visited profile
    is_same_user = True
    is_following = False
    if visitor != visited_user:
        is_same_user = False
        if followers != 0:
            for follower in visited_user.followers.all():
                if visitor == follower:
                    is_following = True
    return render(request, "network/profile.html", {
        "visited_user": visited_user,
        "followers": followers,
        "followings": followings,
        "posts": posts_page,
        "is_same_user": is_same_user,
        "is_following": is_following
    })

@login_required
def following(request):
    user = request.user
    followed = User.objects.filter(followers=user)
    print("TTTTTYYYYPPPPEEEE: ",type(followed))
    #posts = Post.objects.filter(author__in=followed).order_by("time_last_update").reverse()
    posts_page = get_posts_page(request, followed)
    return render(request, "network/index.html", {
        "h1": "Following",
        "posts": posts_page,
        "display_new_post": False
        })



##### API features:

def follow_toggle(request, user_id):
    visited_user = User.objects.get(pk=user_id)
    visitor = request.user
    # 1st find id the visitor was following the visited_user
    is_following = False
    for follower in visited_user.followers.all():
        if visitor == follower:
            is_following = True

    # 2nd update the visited_user.followers according
    if is_following:
        visited_user.followers.remove(visitor)
    else: 
        visited_user.followers.add(visitor)
    visited_user.save()
    return HttpResponse(status=204)


def get_posts_page(request, user_id):
    # get all the posts according the user_id or all users
    if user_id == "all":
        posts = Post.objects.all().order_by("time_last_update").reverse()
    elif type(user_id) == type(User.objects.filter(followers=1)):
        # COMPARAISON DE TYPE PAS BELLE !!!
        posts = Post.objects.filter(author__in=user_id).order_by("time_last_update").reverse()
    else:
        visited_user = User.objects.get(pk=user_id)
        posts = visited_user.author.order_by("time_last_update").reverse()
    # paginate the posts object
    posts_paginated = Paginator(posts, 3)
    # get the page number  defaut is 1
    page_number = int(request.GET.get("page", 1))
    # return the right posts page
    return posts_paginated.get_page(page_number)
