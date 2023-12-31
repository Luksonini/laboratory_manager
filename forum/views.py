# Django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


# DRF (Django Rest Framework) imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Local imports
from .models import PostModel, LikeModel, CommentModel
from . serializers import PostModelSerializer, CommentModelSerializer
from accounts.models.user import User


@login_required(login_url='login')
def index(request, username="all"):
    """Render the main page."""
    return render(request, "forum/index.html", {"username": username})

@login_required(login_url='login')
def profile(request, username):
    """Display user profile and handle follow/unfollow actions."""
    if username != 'all':
        current_user = request.user 
        user = get_object_or_404(User, username=username)
        followers = user.followers.all()
        followings = user.following.all()
        is_follower_value = current_user in followers

        if request.method == "POST":
            # Check if the user wants to update their photo
            if 'avatar' in request.FILES:
                user.profile_picture = request.FILES['avatar']
                user.save()
                return redirect('forum:profile', username=username)
            
            # Follow/unfollow logic
            user_to_follow_username = request.POST.get("follow")
            if user_to_follow_username:
                current_user = request.user
                user_to_follow = User.objects.get(username=user_to_follow_username)
                is_follower_value = current_user in user_to_follow.followers.all()

                if not is_follower_value:
                    current_user.following.add(user_to_follow)
                    user_to_follow.followers.add(current_user)
                else:
                    current_user.following.remove(user_to_follow)
                    user_to_follow.followers.remove(current_user)

                return redirect('forum:profile', username=username)

    return render(request, "forum/index.html", {
        "username": username,
        "followers": followers,
        "followings": followings,
        'is_follower': is_follower_value
    })

def is_following(current_user, followers):
    return current_user in followers



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
    """Handle fetching and creating posts."""
    if request.method == 'GET':
        if 'username' in request.query_params:
            username = request.query_params['username']
            if username == 'all':
                posts = PostModel.objects.all().order_by('-created_at')
            elif username == 'following':
                following = request.user.following.all()
                posts = PostModel.objects.filter(author__in=following).order_by('-created_at')
                print(posts)
            else:
                user = get_object_or_404(User, username=username)
                posts = PostModel.objects.filter(author=user).order_by('-created_at')
        else:
            posts = PostModel.objects.all().order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Ustaw liczbę postów na stronę
        result_page = paginator.paginate_queryset(posts, request)

        serializer = PostModelSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def post_update(request, id):
    """Handle updating a post."""
    try:
        post = PostModel.objects.get(id=id)
    except PostModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostModelSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    """Handle post liking and unliking."""
    post = PostModel.objects.get(id=post_id)  
    
    if LikeModel.objects.filter(user=request.user, post=post).exists():
        LikeModel.objects.filter(user=request.user, post=post).delete()
        return Response({'status': 'unliked'}) 

    LikeModel.objects.create(user=request.user, post=post)
    return Response({'status': 'liked'}) 


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_comment_to_post(request, post_id):
    """Handle fetching and adding comments to a post."""
    post = get_object_or_404(PostModel, id=post_id)
    
    if request.method == 'GET':
        comments = CommentModel.objects.filter(post=post)
        serializer = CommentModelSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

