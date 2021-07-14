import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import User, Post, Following


def index(request):
    post_list = Post.objects.all().order_by("-timestamp")
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {
        "posts": posts,
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

@csrf_exempt
@login_required(login_url="login")
def compose(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    # Get contents of post
    body = data.get("body", "")
    post = Post(body=body, user_id=request.user)
    try:
        post.full_clean()
        post.save()
    except ValidationError:
        print(ValidationError)
    return JsonResponse({"message": "Post sent successfully."}, status=201)

def profile(request, user):
    try:
        poster = User.objects.get(username=user)
        post_list = Post.objects.filter(user_id=poster).order_by("-timestamp")
        user_followers = poster.following.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(post_list, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        followers = Following.objects.filter(user_id=poster)
        following = Following.objects.filter(following_user_id=poster)

        if Following.objects.filter(following_user_id=request.user, user_id=poster).exists():
            follow = "Unfollow"
        else:
            follow = "Follow"
    except User.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: User does not exist")
    return render(request, "network/profile.html", {
        "posts": posts , 
        "perfil": user,
        "following":following,
        "followers":followers,
        "follow":follow
    })

@csrf_exempt
@login_required(login_url="login")
def like(request):

    data = json.loads(request.body)
    postId = data.get("body", "")

    post = Post.objects.get(id=postId)

    if request.user in post.like.all() :
        post.like.remove(request.user)
        return JsonResponse({"postCount": post.like.count(), "like":False}, status=201)
    else :
        post.like.add(request.user)
        return JsonResponse({"postCount": post.like.count(),"like":True}, status=201)

@csrf_exempt
@login_required(login_url="login")
def follow(request):

    data = json.loads(request.body)
    profile = data.get("body", "")
    following = User.objects.get(username=profile)
    followers = Following.objects.filter(user_id=following).count()
    try:
        follow = Following.objects.get(user_id=following, following_user_id=request.user)
        followers = followers - 1
        follow.delete()
        return JsonResponse({"follow":False, "followers":followers}, status=201)
    except Following.DoesNotExist:
        follow = Following(user_id=following, following_user_id=request.user)
        followers = followers + 1
        follow.save()
        return JsonResponse({"follow":True, "followers":followers}, status=201)

@csrf_exempt
@login_required(login_url="login")
def following(request):
    follower_user_ids = Following.objects.filter(following_user_id = request.user).values_list('user_id', flat=True)
    post_list = Post.objects.filter(user_id__in=follower_user_ids).order_by("-timestamp")
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/following.html", {
        "posts": posts
    })

@csrf_exempt
@login_required(login_url="login")
def save(request):
    data = json.loads(request.body)
    body = data.get("body", "")
    postid = data.get("id", "")
    post = Post.objects.get(id=postid)
    post.body = body
    post.save()
    posts = Post.objects.get(id=postid)
    return JsonResponse({"posts":True}, status=201)
