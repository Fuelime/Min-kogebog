from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from .models import Recipe, Message, Topic, Ingredients, CookbookItem
from .forms import RecipeForm, SignUpForm, IngredientFormset, Formset

# Create your views here.

def logIn(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Brugernavn eller adgangskode er forkert.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        # else:
        #     messages.error(request, "Brugernavn eller adgangskode er forkert")
    context = {"page":page}

    return render(request, "django_app/login_register.html", context)
    
def logoutUser(request):
    logout(request)
    return redirect("home")


def signUp(request):
    # form = SignUpForm()
    # if request.method == "POST":
    #     form = SignUpForm(request.POST)
    #     if form.is_valid:
    #         save = form.save()
    #         login(request, save)
    #         return redirect("home")
    if request.method == "POST":
        password_1 = request.POST.get("password1")
        password_2 = request.POST.get("password2")
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            messages.error(request, "brugeren findes allerede")
        else:
            if password_1 == password_2:
                user = User.objects.create(
                    username = request.POST.get("username"),
                    email = request.POST.get("email"),
                    password = request.POST.get("password1"),
                )
                logout(request)
                login(request, user)

                return redirect("home")
            else:
                messages.error(request, "Adgangskoderne er ikke den samme")
            

    context = {}
    return render(request, "django_app/login_register.html", context)

def home(request):
    
    return render(request, "django_app/home.html")

def search(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    #recipe = Recipe.objects.get(id=pk)
    recipes = Recipe.objects.filter(
        Q(topic__name__istartswith=q) |
        Q(name__istartswith=q) |
        Q(description__icontains=q) |
        Q(host__username__istartswith=q)
    )

    recipe_count = recipes.count()

    context = {"recipes":recipes.order_by("-likes"), "recipe_count":recipe_count, "q":q, }
    return render(request, "django_app/search.html", context)


def recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    ingredients = recipe.ingredients_set.all()
    recipe_messages = recipe.message_set.all().order_by("-created")
    user_like = recipe.likes.filter(username=request.user)
    user_item = CookbookItem.objects.filter(user=request.user, recipe=recipe)

    if request.method == "POST":
        if "like" in request.POST:
            if user_like.exists():
                recipe.likes.remove(request.user)
                #return redirect("recipe", pk=recipe.id)
            else:
                recipe.likes.add(request.user)
                #return redirect("recipe", pk=recipe.id)
        elif "message" in request.POST:
            message = Message.objects.create(
                user = request.user,
                room = recipe,
                body = request.POST.get("message")
            )

        elif "add_item" in request.POST:
            if user_item.exists():
                user_item.delete()

            else:
                CookbookItem.objects.create(
                    user = request.user,
                    recipe = recipe
                )
            #return redirect("recipe", pk=recipe.id)
    
    likes_count = recipe.likes.count()
    context = {"recipe": recipe, "recipe_messages": recipe_messages,  "likes_count": likes_count, "ingredients":ingredients, "user_like":user_like, "user_item":user_item}

    return render(request, "django_app/recipe.html", context)

@login_required(login_url="login")
def createRecipe(request):
    topics = Topic.objects.all()
    # formset = Formset(queryset=Ingredients.objects.none())
    formset = IngredientFormset(instance=None, prefix="form")
    if request.method == "POST":
        formset = Formset(request.POST)
        topic = request.POST.get("topic")
        if Topic.objects.filter(name=topic).exists():
            topic_name = Topic.objects.get(name=topic)
            recipe = Recipe.objects.create(
                host = request.user,
                image = request.FILES.get("image"),
                topic = topic_name,
                name = request.POST.get("name"),
                description = request.POST.get("description"),
        )
            if formset.is_valid():

                instances = formset.save(commit=False)
                for instance in instances:
                    if instance.ingredient:
                        instance.recipe = recipe
                        instance.save()
                # for form in formset:
                #     ingredient = form.cleaned_data.get("ingredient")
                #     if ingredient:
                #         Ingredients(ingredient=ingredient, recipe=recipe).save()
                #         form.save()

                return redirect("home")

        else:
            messages.error(request, "Overemnet findes ikke. Prøv at tjekke, at du har stavet det ordentligt.")


    context = {"topics":topics, "formset":formset}
    return render(request, "django_app/recipe_form.html", context)

@login_required(login_url="login")
def editRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    topics = Topic.objects.all()
    if request.method == "POST":
        topic = request.POST.get("topic")
        formset = IngredientFormset(request.POST, instance=recipe, prefix="form")
        if Topic.objects.filter(name=topic).exists():
            topic_name = Topic.objects.get(name=topic)
            recipe.topic = topic_name
            recipe.name = request.POST.get("name")
            recipe.description = request.POST.get("description")
            recipe.edited = True
            if request.FILES.get("image") is not None:
                recipe.image = request.FILES.get("image")
            recipe.save()
            
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    if instance.ingredient:
                        instance.recipe = recipe
                        instance.save()
            return redirect("home")
    else:
        formset = IngredientFormset(instance=recipe, prefix="form")

    context = {"topics":topics, "recipe":recipe, "formset":formset}
    return render(request, "django_app/recipe_form.html", context)

@login_required(login_url="login")
def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if request.method == "POST":
        recipe.delete()
        return redirect("home")
    return render(request, "django_app/delete_object.html", {"obj":recipe})

def browseRecipes(request):
    topics = Topic.objects.all()
    context = {"topics":topics}
    return render(request, "django_app/find-recipes.html", context)


def userProfile(request, pk):

    user = User.objects.get(username=pk)
    recipes = Recipe.objects.filter(host=user)
    likes = Recipe.objects.filter(likes=user)
    likes_recieved = recipes.aggregate(total_likes=Count("likes"))["total_likes"] or 0
    context = {"user":user, "recipes":recipes, "likes":likes, "likes_recieved":likes_recieved}
    return render(request, "django_app/profile.html", context)

def userCookbook(request, pk):


    user = User.objects.get(id=pk)
    items = CookbookItem.objects.filter(user=request.user).all()
    if user != request.user:
        return redirect("home")
    
    context = {"user":user, "items":items}
    return render(request, "django_app/cookbook.html", context)
    