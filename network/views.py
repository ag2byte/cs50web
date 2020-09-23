from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, Post, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            post_list = Post.objects.all().order_by('id').reverse()

            return HttpResponseRedirect(reverse("posts"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@login_required
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
            profile = Profile.objects.create(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def posts(request):

    post_list = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    if page != None:

        try:
            post_list = paginator.page(page)

        except:
            post_list = paginator.page(1)
    else:
        post_list = paginator.page(1)

    return render(request, "network/posts.html", {'post_list': post_list, })


@login_required
def newpost(request):

    if request.method == "POST":
        author = User.objects.get(username=request.user.username)
        content = request.POST['post']

        post = Post.objects.create(author=author, content=content)
        return HttpResponseRedirect(reverse('posts'))

    return render(request, "network/create.html")


def profile(request, username):

    author = User.objects.get(username=username)
    post_list = Post.objects.all().filter(
        author=author).order_by('id').reverse()
    profile = Profile.objects.get(user=author)
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    if page != None:

        try:
            post_list = paginator.page(page)

        except:
            post_list = paginator.page(1)
    else:
        post_list = paginator.page(1)

    return render(request, "network/profile.html", {'post_list': post_list, 'cur_user': author, 'profile': profile})


@login_required
def following(request):

    following = Profile.objects.get(user=request.user).following.all()
    post_list = Post.objects.filter(author__in=following).order_by(
        '-last_edited_on')  # rev chronology

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    if page != None:

        try:
            post_list = paginator.page(page)

        except:
            post_list = paginator.page(1)
    else:
        post_list = paginator.page(1)

    return render(request, "network/posts.html", {'post_list': post_list})


@login_required
@csrf_exempt
def follow(request):
    user_name = request.POST.get('user')
    target_name = request.POST.get('cur_user')
    command = request.POST.get('command')
    cur_user = User.objects.get(username=user_name)
    target = User.objects.get(username=target_name)
    profile = Profile.objects.get(user=cur_user)
    profile2 = Profile.objects.get(user=target)
    if command == 'Follow':

        profile.following.add(target)
        profile.save()  # cur_user follows target

        profile2.follower.add(cur_user)
        profile2.save()  # target followers list has cur_user now
        return JsonResponse({'status': 201, 'command': 'Unfollow', 'follow_count': profile2.follower.count()}, status=201)

    elif command == 'Unfollow':
        profile.following.remove(target)
        profile.save()  # cur_user unfollows target

        profile2.follower.remove(cur_user)
        profile2.save()  # target followers list does not have cur_user now
        return JsonResponse({'status': 201, 'command': 'Follow', 'follow_count': profile2.follower.count()}, status=201)


@login_required
@csrf_exempt
def like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        is_liked = request.POST.get('is_liked')
        # print(post_id, is_liked)

        try:
            post = Post.objects.get(pk=post_id)
            if is_liked == 'false':
                post.like.add(request.user)
                is_liked = 'true'
                post.save()

            elif is_liked == 'true':
                post.like.remove(request.user)
                is_liked = 'false'
                post.save()

            print(post.like.count())
            return JsonResponse({'like_count': post.like.count(), 'is_liked': is_liked, 'status': 201})
        except:
            return JsonResponse({'error': 'Post not found ', 'status': 404})
    return JsonResponse({}, status=400)


@login_required
@csrf_exempt
def editpost(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        new_value = request.POST.get('new_value')
        # print(post_id, new_value)
        try:
            post = Post.objects.get(pk=post_id)
            if post.author == request.user:
                post.content = new_value.strip()
                post.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)
    return JsonResponse({}, status=400)
