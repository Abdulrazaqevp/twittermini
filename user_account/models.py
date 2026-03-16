from operator import index
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class CustomUser(AbstractUser):

    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    dob = models.DateField(blank=True, null=True)

    is_private = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    #Relationship count

    def followers_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]


class Follow(models.Model): #following-follower relationship

    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower',
                         'following'], name='unique_follow_relationship'),
        ]

        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]


    def clean(self):
            if self.follower == self.following:
                raise ValidationError("users cannot follow yourself.")
            

    def save(self,*args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"