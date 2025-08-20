from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
# from .models import Blog

# Create your models here.
# Note : After every class added in models.py, we have to run migration commands below:
# command 1: python manage.py makemigrations
# command 2: python manage.py migrate
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    facebook = models.URLField(max_length=255,blank=True, null=True)
    youtube = models.URLField(max_length=255,blank=True, null=True)
    instagram = models.URLField(max_length=255,blank=True, null=True)
    twitter = models.URLField(max_length=255,blank=True, null=True)
    linkedin = models.URLField(max_length=255,blank=True, null=True)
    github = models.URLField(max_length=255,blank=True, null=True)
    
    #other permission field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_group_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
        )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permission_set',
        blank=True,
        help_text='Specific permissions for this user. Use with caution as it can override group permissions.',
        related_query_name='custom_user',
    )


    def __str__(self):
        return self.username
    
class Blog(models.Model):
    CATEGORY = (
        ('Technology', 'Technology'),
        ('Lifestyle', 'Lifestyle'),
        ('Travel', 'Travel'),
        ('Food', 'Food'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Finance', 'Finance'),
        ('Economy', 'Economy'),
        ('Politics', 'Politics'),
        ('Sports', 'Sports'),
        ('Science', 'Science'),
        ('Other', 'Other'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    category = models.CharField(max_length=255, choices=CATEGORY, default='Other',blank=True, null=True)
    featured_image = models.ImageField(upload_to='featured_images/', blank=True, null=True)
    
    class Meta:
        ordering = ['-published_date']
        
    def __call__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        unique_slug = base_slug
        counter = 1
        while Blog.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = unique_slug
        
        if not self.is_draft and self.published_date is None:
            self.published_date = timezone.now()
            
        super().save(*args, **kwargs)
            
    
    