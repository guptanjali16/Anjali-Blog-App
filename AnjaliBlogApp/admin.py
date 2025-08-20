from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Blog


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','bio', 'profile_picture', 'facebook', 'youtube', 'instagram', 'twitter', 'linkedin', 'github')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    
admin.site.register(CustomUser, CustomUserAdmin)

#superuser
# user name : anjalig
# Anjali Password : A@nju2001
# email : anjaligup16@gmail.com

#user -1
# username : danny
# Daniel Password : Danny@123
# email :  daniel1@gmail.com

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published_date', 'is_draft')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('is_draft', 'category')
    
admin.site.register(Blog, BlogAdmin)