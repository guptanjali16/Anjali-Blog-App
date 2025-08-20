from django.shortcuts import render

from AnjaliBlogApp.models import Blog
from .serializers import UpdateUserProfileSerializer, UserRegisterationSerializer, BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

# Create your views here.
@api_view(['POST'])
@csrf_exempt  # Use this if you want to disable CSRF protection for this view
def register_user(request): 
    serializer = UserRegisterationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
# @csrf_exempt
@permission_classes([IsAuthenticated])  #only logged-in users can update their profile
def update_user_profile(request):
    user = request.user
    if request.method == 'PUT':
        serializer = UpdateUserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  

@api_view(['POST']) 
@csrf_exempt
@permission_classes([IsAuthenticated])  #only logged-in users can create blogs
def create_blog(request):
    user = request.user  # Get the currently authenticated user
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_blogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@csrf_exempt
@permission_classes([IsAuthenticated])  #only logged-in users can create blogs
def update_blog(request, pk):
    user = request.user
    try:
        blog = Blog.objects.get(id=pk)
        if blog.author != user:
            return Response({'error': 'As you are not author of this blog, You do not have permission to update this blog.'}, status=status.HTTP_403_FORBIDDEN)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)  
    serializer = BlogSerializer(blog, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_blog(request, pk):
    user = request.user
    try:
        blog = Blog.objects.get(id=pk)
        if blog.author != user:
            return Response({'error': 'As you are not author of this blog, You do not have permission to delete this blog.'}, status=status.HTTP_403_FORBIDDEN)
        blog.delete()
        return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
