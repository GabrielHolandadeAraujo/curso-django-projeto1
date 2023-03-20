from django.core.exceptions import ValidationError
import re

# É interessante criar um arquivo forms.py para controlar os formulários, nele precisa criar uma classe que
# herda de forms.ModelForm pq ele é atrlado ao model do User que foi importado
# Dentro dela é importante uma classe meta que serve para passar metadados do formulário para o django

# essa funçãop serve para adicionar atributos aos campos. Primeiro acessamos o atributo que queremos 
# add via get e caso não tenha nada, setamos um valor em branco. Após isso adicionamos o novo valor e usamos o stip para remover possíveis espaços em branco no inicio e fim da String 
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

# essa uma função para facilitar colocar um placeholder, passamos o campo e o nome do placeholder para 
# add, usamos a função anterior para alterar o valor do placeholder no campo escolhido
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    # isso é uma expressão regular para validar a senha, basicamente ela confere se a senha tem pelo menos 1 de 
    # caracteres minúsculos, maiúsculos e númros e tbm se tem pelo menos 8 dígitos (precisa importar re)
    # Tem um curso gratuito de expressões regulares na Udemy
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    # se a senha não tiver os requisitos acima ela gera o erro abaixo
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        ) 
