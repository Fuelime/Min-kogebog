from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/topic-images/", null=True, blank=True)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    edited = models.BooleanField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]
        
    def __str__(self):
        return self.name
    
# class Likes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return self.recipe


class Ingredients(models.Model):
    ingredient = models.CharField(max_length=255, blank=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.ingredient

class CookbookItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
class Message(models.Model):
    body = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.body
    