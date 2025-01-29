from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Blog, BlogContent, BlogReaction, Comment
import cloudinary
import cloudinary.uploader
import json
from rest_framework.permissions import IsAuthenticated
from .serializer import BlogSerializer, BlogCommentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        content_json = request.data.get('content')
        content = json.loads(content_json)

        blog = Blog.objects.create(
            user=request.user,
            title=title
        )

        for content_item in content:
            block_data = {
                'blog': blog,
                'content_type': content_item['type'],
                'order': content_item['order'],
                'content_data': content_item['content']
            }

            if content_item['type'] == 'image':
                image_file = request.FILES.get('image_files')
                if image_file:
                    cloudinary_response = cloudinary.uploader.upload(image_file)
                    block_data['image_url'] = cloudinary_response['secure_url']

            BlogContent.objects.create(**block_data)

        return Response({'message': 'Blog created successfully'}, status=status.HTTP_201_CREATED)
    

    def get(self, request):
        try:
            blogs = Blog.objects.exclude(user=request.user)
            serializer = BlogSerializer(blogs, many=True, context={'request': request}).data
            if serializer:
                return Response(serializer)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            serializer = BlogSerializer(blogs, context={'request': request}, many=True).data
            if serializer:
                return Response(serializer)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error rere: ", str(e))
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class AdminUserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, userId):
        if userId:
            try:
                user = User.objects.get(id=userId)
                print("usre: ", user)
                blogs = Blog.objects.filter(user=user)
                serializer = BlogSerializer(blogs, many=True, context={'request': request}).data
                if serializer:
                    return Response(serializer)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message":"User Not found"}, status=status.HTTP_200_OK)
            

class HandleReactioView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, userReaction, blogId):
        try:
            blog = Blog.objects.get(id = blogId)
            user = User.objects.get(id = request.user.id)
            reaction = BlogReaction.objects.get(blog=blog, user=user)
            if reaction.reaction == userReaction:
                reaction.delete()

            else:
                reaction.reaction = userReaction
                reaction.save()
            return Response(status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"message":"Blog not found"},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
        except BlogReaction.DoesNotExist:
            BlogReaction.objects.create(blog=blog, user=user, reaction=userReaction)
            return Response(status=status.HTTP_200_OK)
        


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, blogId):
        try:
            comments = Comment.objects.filter(blog__id=blogId)
            
            serializer = BlogCommentSerializer(comments, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, blogId):
        user = request.user
        data = request.data
        
        data['blog'] = blogId

        try:
            serializer = BlogCommentSerializer(data=data, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Comment created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist:
            return Response({"message": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            
            
        
