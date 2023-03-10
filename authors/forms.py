from django import forms
from django.contrib.auth.models import User

# É interessante criar um arquivo forms.py para controlar os formulários, nele precisa criar uma classe que 
# herda de forms.ModelForm pq ele é atrlado ao model do User que foi importado
# Dentro dela é importante uma classe meta que serve para passar metadados do formulário para o django
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        # nos fields podemos passar quais campos usar (os msm do model User), para passar tudo usamos __all__
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]