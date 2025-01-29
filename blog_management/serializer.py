from rest_framework import serializers
from .models import Blog, BlogContent, Comment, BlogReaction
from accounts.serializers import UserSerializer

class BlogContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogContent
        fields = '__all__'

class BlogReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogReaction
        fields = '__all__'

class BlogCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},  # Hide user in request payload
            'blog': {'write_only': True},  # Hide blog in request payload
        }

    # def get_user(self, obj):
    #     # Detailed or simple user representation based on context
    #     if self.context.get('detailed', False):
    #         return UserSerializer(obj.user).data
    #     return {"id": obj.user.id, "username": obj.user.username}

    def validate(self, attrs):
        # Set the user and blog from the context
        attrs['user'] = self.context['request'].user
        return attrs



class BlogSerializer(serializers.ModelSerializer):
    contents = BlogContentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    reactions = BlogReactionSerializer(many=True, read_only=True)
    user_reaction = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = "__all__"

    def get_user_reaction(self, obj):
        
        user = self.context.get('request').user
        if not user.is_authenticated:
            return None
        
        reaction = BlogReaction.objects.filter(user=user, blog=obj).first()
        return reaction.reaction if reaction else None


    