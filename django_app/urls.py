from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.logIn, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("sign-up/", views.signUp, name="sign-up"),
    path("profile/<str:pk>", views.userProfile, name="profile"),

    path("", views.home, name="home"),
    path("recipe/<str:pk>", views.recipe, name="recipe"),
    path("search", views.search, name="search"),
    path("browse-recipes/", views.browseRecipes, name="browse-recipes"),
    path("cookbook/<str:pk>", views.userCookbook, name="cookbook"),

    path("create-recipe/", views.createRecipe, name="create-recipe"),
    path("edit-recipe/<str:pk>", views.editRecipe, name="edit-recipe"),
    path("delete-recipe/<str:pk>", views.deleteRecipe, name="delete-recipe"),

]