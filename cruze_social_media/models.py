from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Use a string to refer to the Post model
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    on_created = models.DateTimeField(auto_now_add=True)
    on_updated = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', default='default.jpg')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(
        User, through=Like, related_name='liked_posts')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    on_created = models.DateTimeField(auto_now_add=True)
    on_updated = models.DateTimeField(auto_now=True)


class CreateForum(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    on_created = models.DateTimeField(auto_now_add=True)
    on_updated = models.DateTimeField(auto_now=True)
