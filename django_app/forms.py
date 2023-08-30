from django.forms import ModelForm, formset_factory, modelformset_factory, inlineformset_factory
from django import forms
from .models import Recipe, Ingredients
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        #fields = ["topic", "name", "description", "host"]
        fields = "__all__"
        exclude = ["host", "participants", "likes", "edited"]
    
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class IngredientForm(ModelForm):
    ingredient = forms.CharField(label="", required="")
    class Meta:
        model = Ingredients
        fields = "__all__"
        exclude = ["recipe",]

Formset = modelformset_factory(Ingredients, extra=1, form=IngredientForm)
IngredientFormset = inlineformset_factory(Recipe, Ingredients, fields=["ingredient"], extra=1, form=IngredientForm)