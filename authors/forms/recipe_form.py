from django import forms
from recipes.models import Recipe

class AuthorRecipeForm(forms.ModelForm):
    # É interessante criar um arquivo forms.py para controlar os formulários, nele precisa criar uma classe que
    # herda de forms.ModelForm pq ele é atrlado ao model do User que foi importado
    # Dentro dela é importante uma classe meta que serve para passar metadados do formulário para o django
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        
    