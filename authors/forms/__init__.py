# flake8: noqa
from .login import LoginForm
from .register_forms import RegisterForm

# esse arquivo serve para enganar o django e pensar que essa pasta na vdd é um arquivo forms.py na raiz da pasta
# authors, junto com os demais arquivos do app. Basta importar os forms criados aqui dentro e poderá importa-los
# no resto do código ignorando a pasta forms, como se fosse importar de um forms.py na raiz