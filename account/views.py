from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,BlogSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Recipe,User
# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),

    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'id':user.id,'isadmin':user.is_admin, 'msg': 'User is Successfully registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email= email, password= password)

            if user is not None:
                # print("Hello")
                token = get_tokens_for_user(user)
                return Response({'token':token,'id':user.id,'isadmin':user.is_admin,'msg': 'User Login Successfully '}, status=status.HTTP_200_OK)

            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_200_OK)



class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request, format = None):
        serializer = UserProfileSerializer(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import permissions
class RecipeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]

            
    def get(self, request, format=None):
        try:
                
            data = Recipe.objects.all()
            ser = BlogSerializer(data ,many = True)
            return Response(ser.data,status = status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response({'message': 'No Blogs found.'}, status=status.HTTP_404_NOT_FOUND)
                 
        

class RecipePostView(APIView):
    renderer_classes = [UserRenderer]  # Assuming UserRenderer is a custom renderer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_id = request.data.get('user')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            serializer = BlogSerializer(data=request.data)

            if serializer.is_valid():
              
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
    def put(self, request, format=None):
        user_id = request.data.get('user')
        pk = request.data.get('pk')
        
        try:
            user = User.objects.get(id=user_id)
            
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(pk)

        if user:
            # Get the existing blog post by its primary key (pk)
            try:
                blog_post = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response({'message': 'Blog post not found.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user is the owner of the blog post or has the necessary permission to update it
            if blog_post.user != user:
                return Response({'message': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = BlogSerializer(blog_post, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        pk = request.data.get('pk')
    
        try:
            blog_post = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response({'message': 'Blog post not found.'}, status=status.HTTP_400_BAD_REQUEST)

        blog_post.delete()
        return Response({'message': 'Blog post deleted.'}, status=status.HTTP_204_NO_CONTENT)
    

