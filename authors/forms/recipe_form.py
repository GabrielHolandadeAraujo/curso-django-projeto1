from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # estamos usando a função que criamos em utils para adicionar atributos, adicionando a classe span-2 que 
        # é para que os dois comapos ocupem os dois lados do grid
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    # É interessante criar um arquivo forms.py para controlar os formulários, nele precisa criar uma classe que
    # herda de forms.ModelForm pq ele é atrlado ao model do User que foi importado
    # Dentro dela é importante uma classe meta que serve para passar metadados do formulário para o django
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                # o choices recebe várias tuplas que serão exibidas no campo como escolhas ao invés de digitar
                # qualquer coisa
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }
    