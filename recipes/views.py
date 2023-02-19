from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'recipes/pages/home.html')

def recipes(request, id):
    return render(request, 'recipes/pages/recipes-view.html')