from rest_framework import serializers
from django.contrib.auth import get_user_model
# from AnjaliBlogApp.admin import Blog
from AnjaliBlogApp.models import CustomUser, Blog


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Assuming CustomUser is defined in models.py
        # These fields are used to create a new user and will be passing in view.py
        fields = ('username', 'email', 'password', 'first_name', 'last_name','bio', 'profile_picture', 'facebook', 'youtube', 'instagram', 'twitter', 'linkedin', 'github')
        
class UserRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Assuming CustomUser is defined in models.py
        # These fields are used to create a new user and will be passing in view.py
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            } 
        
    def create(self, validated_data):
        first_name = validated_data['first_name'] 
        last_name = validated_data['last_name']
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']
        
        user =get_user_model()
        new_user = user.objects.create(email=email, username=username, first_name=first_name, last_name=last_name)
        
        new_user.set_password(password)
        new_user.save() 
        return new_user
    
    
        
        
    # def create(self, validated_data):
    #     user = CustomUser(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data.get('first_name', ''),
    #         last_name=validated_data.get('last_name', ''), 
    #         bio=validated_data.get('bio', ''),
    #         facebook=validated_data.get('facebook', ''),
    #         youtube=validated_data.get('youtube', ''),
    #         instagram=validated_data.get('instagram', ''),
    #         twitter=validated_data.get('twitter', ''),
    #         linkedin=validated_data.get('linkedin', ''),
    #         github=validated_data.get('github', '')
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class SimpleAuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name')


class BlogSerializer(serializers.ModelSerializer):
    author = SimpleAuthorSerializers(read_only=True)
    class Meta:
        model = Blog
        fields = ('title', 'slug', 'content', 'is_draft', 'category', 'featured_image', 'author', 'created_at', 'updated_at', 'published_date')
        
    