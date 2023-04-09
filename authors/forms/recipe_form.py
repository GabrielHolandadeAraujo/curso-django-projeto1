from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
# isso serve para listas de erros
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # inicialisamos no construtor o my_erros que cria um dicionário de erros, onde cada erro é uma lista 
        # que começa vazia 
        self.my_errors = defaultdict(list)
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
    
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        # estamos pegando os dados já tratados pelo Django
        cd = self.cleaned_data
        # com os dados tratados pegamos cada item a ser verificado de forma separada com o get e o nome do 
        # campo (string)
        title = cd.get('title')
        description = cd.get('description')
        # aqui fazemos uma validação não muito usada, mas para mostrar que podemos usar vários campos ao
        #  mesmo tempo com o my_erros
        if title == description:
            # o funcionamento é simples, usamos a posição do campo a ser validado no my_erros e fazemos um append
            # para o erro em questão
            self.my_errors['title'].append('Cannot be equal to description')
            self.my_errors['description'].append('Cannot be equal to title')
        # depois verificamos se teve algum erro (se o my_errors tem um valor)
        if self.my_errors:
            # então levantamos o erro de validação passando o my_errors
            raise ValidationError(self.my_errors)
        # por fim retornamos o super_clean
        return super_clean
    # podemos também validar campos separadamente em uma função prórpia usando a mesma lista usada nas funções acima
    # o my_errors foi criado no construtor da classe e é herdado pelas funções da classe
    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            # aqui usamos a mesma lista de title e adicionamos um novo erro
            self.my_errors['title'].append('Must have at least 5 char')

        return title
    
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self.my_errors[field_name].append('Must be a positive number')
        
        return field_value
    
    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value