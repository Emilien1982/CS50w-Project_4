from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
        posts = Post.objects.all().order_by("time_last_update").reverse()
        return render(request, "network/index.html", {
            "posts": posts
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
    visitor = request.user
    if request.method == "POST":
        """ is_following = request.POST["is_following"]
        if is_following :
            # Unfollow
            visited_user.followers_set.remove(visitor)
        else :
            # Follow
            visited_user.followers.add(visitor)
        visited_user.save()
        return HttpResponseRedirect(reverse("profile", args=[user_id])) """
    else :
        followers = visited_user.followers.count()
        ##VERIFIER QUE LA SELECTION CI DESSOUS FONCTIONNE BIEN QUAND LA FEATURE "FOLLOW" SERA OK
        followings = User.objects.filter(followers=visited_user).count()
        posts = visited_user.author.order_by("time_last_update").reverse()
        # Check if the logged user is the owner of the visited profile
        # and if the logged user follows the owner of the visited profile
        is_same_user = True
        is_following = False
        if visitor != visited_user:
            is_same_user = False
            if followers != 0:
                ##VERIFIER QUE LA CONDITION CI DESSOUS FONCTIONNE BIEN QUAND LA FEATURE "FOLLOW" SERA OK
                for follower in visited_user.followers.all():
                    if visitor == follower:
                        is_following = True
        return render(request, "network/profile.html", {
            "visited_user": visited_user,
            "followers": followers,
            "followings": followings,
            "posts": posts,
            "is_same_user": is_same_user,
            "is_following": is_following
        })

def follow_toggle(request, user_id):
    visited_user = User.objects.get(pk=user_id)
    visitor = request.user
    # 1st find id the visitor was following the visited_user
    is_following = False
    for follower in visited_user.followers.all():
        if visitor == follower:
            is_following = True

    print("is_following: ", is_following)
    # 2nd update the visited_user.followers according
    if is_following:
        visited_user.followers.remove(visitor)
    else: 
        visited_user.followers.add(visitor)
    visited_user.save()
    return HttpResponse(status=204)