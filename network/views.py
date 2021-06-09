from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Page, Paginator
from django.contrib.auth.decorators import login_required

import json

from .models import User, Post, Comment, Follow


def index(request):

    item1 = Post.objects.all().order_by('-date')

    p = Paginator(item1, 10)

    pagination_index = []

    if p.num_pages <= 5:
        for n in range(p.num_pages):
            pagination_index.append(n + 1)
    else:
        pagination_index = [1, 2, 3, 4, 5]

    return render(request, "network/index.html", {
        "posts": p.page(1),
        "pages": pagination_index,
        "selected": 1
    })


def pages(request, page_visiting):

    post = Post.objects.all().order_by('-date')

    p = Paginator(post, 10)

    print(f"This is the page_visiting: {page_visiting}")

    try:
        page = p.page(page_visiting)
    except paginator.EmptyPage:
        if page_visiting > p.num_pages:
            return HttpResponseRedirect(reverse('pages', args=[page_visiting - 1]))
        else:
            return HttpResponseRedirect(reverse('pages', args=[page_visiting + 1]))

    distance = p.num_pages - page_visiting

    if p.num_pages <= 5:
        pagination_index = [i + 1 for i in range(p.num_pages)]

    elif distance < 5 and p.num_pages > 5:
        pagination_index = [p.num_pages - 4, p.num_pages -
                            3, p.num_pages - 2, p.num_pages-1, p.num_pages]

    elif distance >= 5 and p.num_pages > 5:
        pagination_index = [page_visiting - 2, page_visiting -
                            1, page_visiting, page_visiting + 1, page_visiting + 2]

    return render(request, "network/index.html", {
        "posts": page,
        "pages": pagination_index,
        "selected": page_visiting
    })


@login_required(login_url='/login')
def comment(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        comment = request.POST.get('comment')
        user = User.objects.get(username=request.user.username)
        a = Comment(user=user, post=post, comment=comment)
        a.save()

    return render(request, "network/comment.html", {
        "post": post,
        "comments": post.content.all().order_by('-date')
    })


def change(request, page_visiting, button, from_page, username):

    if button == 'previous':
        page_visiting = page_visiting - 1
    else:
        page_visiting = page_visiting + 1

    if from_page == 'index':
        return HttpResponseRedirect(reverse('pages', args=[page_visiting]))
    elif from_page == 'myprofile':
        return HttpResponseRedirect(reverse('myprofile', args=[username, page_visiting]))
    elif from_page == 'following':
        return HttpResponseRedirect(reverse('following', args=[page_visiting]))


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


@login_required(login_url='/login')
def new_post(request):

    if request.method == "POST":

        user = User.objects.get(username=request.user.username)
        print(request.user.username)

        post = request.POST.get('post')

        item = Post(user=user, post=post)
        item.save()

        return HttpResponseRedirect(reverse('index'))

    return render(request, "network/newpost.html")


def myprofile(request, username, page_visiting):

    user_profile = User.objects.get(username=username)
    post = Post.objects.filter(user=user_profile).order_by('-date')

    p = Paginator(post, 10)

    try:
        page = p.page(page_visiting)
    except paginator.EmptyPage:
        if page_visiting > p.num_pages:
            return HttpResponseRedirect(reverse('myprofile', args=[username, page_visiting - 1]))
        else:
            return HttpResponseRedirect(reverse('myprofile', args=[username, page_visiting + 1]))

    distance = p.num_pages - page_visiting

    if p.num_pages <= 5:
        pagination_index = [i + 1 for i in range(p.num_pages)]

    elif distance < 5 and p.num_pages > 5:
        pagination_index = [p.num_pages - 4, p.num_pages -
                            3, p.num_pages - 2, p.num_pages-1, p.num_pages]

    elif distance >= 5 and p.num_pages > 5:
        pagination_index = [page_visiting - 2, page_visiting -
                            1, page_visiting, page_visiting + 1, page_visiting + 2]

    return render(request, "network/myprofile.html", {
        "posts": page,
        "user_profile": user_profile,
        "follower_count": user_profile.follow_er.all().count,
        "following_count": user_profile.follow_ee.all().count,
        "selected": page_visiting,
        "pages": pagination_index
    })

# Reserve for future following data for testing!


@login_required(login_url='/login')
def following(request, page_visiting):

    item = User.objects.get(username=request.user.username)
    following = Follow.objects.filter(user=item)

    users = [x.followee for x in following]
    print(users)

    try:
        all_post = []
        for i in users:
            posts = Post.objects.filter(user=i).order_by('-date')
            for j in posts:
                all_post.append(j)
    except IndexError:
        return render(request, "network/following.html", {
            "posts": None
        })

    p = Paginator(all_post, 10)

    try:
        page = p.page(page_visiting)
    except paginator.EmptyPage:
        if page_visiting > p.num_pages:
            return HttpResponseRedirect(reverse('following', args=[page_visiting - 1]))
        else:
            return HttpResponseRedirect(reverse('following', args=[page_visiting + 1]))

    distance = p.num_pages - page_visiting

    if p.num_pages <= 5:
        pagination_index = [i + 1 for i in range(p.num_pages)]

    elif distance < 5 and p.num_pages > 5:
        pagination_index = [p.num_pages - 4, p.num_pages -
                            3, p.num_pages - 2, p.num_pages-1, p.num_pages]

    elif distance >= 5 and p.num_pages > 5:
        pagination_index = [page_visiting - 2, page_visiting -
                            1, page_visiting, page_visiting + 1, page_visiting + 2]

    return render(request, "network/following.html", {
        "posts": page,
        "pages": pagination_index,
        "selected": page_visiting
    })


@ csrf_exempt
def like(request, post_id):

    try:
        item = Post.objects.get(id=post_id)
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return JsonResponse({"message": "Please login first."})

    if request.method == "GET":

        a = item.serialize(request.user.username)
        print(a)
        return JsonResponse(item.serialize(request.user.username))

    elif request.method == "PUT":

        data = json.loads(request.body)

        print(data)

        if not Post.objects.get(id=post_id).like.filter(username=request.user.username):

            item.like.add(user)

            print(f"{user.username} just liked the post.")
            print(item.check_like(request.user.username))

            return HttpResponse(status=204)

        else:

            item.like.remove(user)
            print(f"{user.username} just unliked the post.")
            print(item.check_like(request.user.username))
            return HttpResponse(status=204)

    else:
        return JsonResponse({"message": "GET or PUT request required."})


@ csrf_exempt
def follow(request, user_profile):

    try:
        item = User.objects.get(username=request.user.username)
        item2 = User.objects.get(username=user_profile)
    except User.DoesNotExist:
        return JsonResponse({"message": "Please login first."})

    following_check = follow_check(
        request.user.username, user_profile, "following")
    print(following_check)

    if request.method == "GET":

        if following_check == False:
            a = Follow(user=item, followee=item2)
            a.save()
            print(f"{request.user.username} has succcessfully followed.")
            return JsonResponse({"following_check": follow_check(request.user.username, user_profile, "following")})
        else:

            print(f"{request.user.username} has successfully unfollowed.")
            Follow.objects.filter(user=item).filter(followee=item2).delete()
            return JsonResponse({"following_check": follow_check(request.user.username, user_profile, "following")})

    elif request.method == "PUT":
        return JsonResponse({"following_check": following_check})


def follow_check(login_user, user_profile, follow_type):

    item1 = User.objects.get(username=login_user)
    item2 = User.objects.get(username=user_profile)

    if follow_type == "following":
        return True if Follow.objects.filter(user=item1).filter(followee=item2) else False
    elif follow_type == "follower":
        return True if Follow.objects.filter(followee=item1).filter(user=item2) else False


@login_required(login_url='/login')
def edit_html(request, post_id):
    user_login = User.objects.get(username=request.user.username)
    item = Post.objects.get(id=post_id)

    if item.user != user_login:
        return HttpResponseRedirect(reverse('myprofile', args=[item.user, 1]))

    return render(request, "network/edit.html", {
        "post": item
    })


@csrf_exempt
@login_required(login_url='/login')
def edit(request, post_id):

    item = Post.objects.get(id=post_id)

    if request.method == "GET":

        return JsonResponse(item.serialize(request.user.username))
    elif request.method == "POST":

        data = json.loads(request.body)

        text = data.get('text')
        print(text)

        item.post = text
        item.save()
        print(f"New edit has been saved. {item.post}")

        return JsonResponse({"Message": "Post update successfully."})
