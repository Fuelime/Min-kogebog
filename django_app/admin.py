from django.contrib import admin
from .models import Recipe, Topic, Message, Ingredients, CookbookItem

# Register your models here.

admin.site.register(Recipe)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Ingredients)
admin.site.register(CookbookItem)
