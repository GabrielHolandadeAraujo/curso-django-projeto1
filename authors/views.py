from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import RegisterForm

# Create your views here.

# É necessário importar o redenr de django.shortcuts para renderizar a url, para isso precisamos de uma função 
# que retorne o redenr passando a requisição e o caminho para o template em questão
def register_view(request):
    # Aqui temos duas possibilidades, ou recebe o parâmetro ou recebe none
    register_form_data = request.session.get('register_form_data', None)
    # Caso tenha parâmetro será get, caso não tenha será post
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        # aqui estamos colocando uma valor de chave para renderizar a url do form
        'form_action': reverse('authors:create'),
    })


def register_create(request):
    # se o método for get (tentar reenviar um msm form) ele da um 404 
    if not request.POST:
        raise Http404()
    #caso o método for post vai receber os dados e repassar para a função de view mandando get para evitar 
    # o reenvio do form
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    # estamos verificando se o formulario foi validado, se sim o django vai salvar na base de dados e exibir 
    # uma menssagem de sucesso.
    if form.is_valid():
        # estamos salvando os dados do form em uma varipavel ao invés de salvar no banco de dados, pois não 
        # estamos comitando e assim podemos manipular os dados
        user = form.save(commit=False)
        # estamos encriptografando a senha para não ficar visível nem mesmo para os administradores
        user.set_password(user.password)
        # agora sim vamos salvos os dados no banco de dados
        user.save()
        messages.success(request, 'Your user was created, please log in.')
        # Após salvar precisamos apagar os dados que foram preenchidos nos campos para ficar em branco novamente
        del (request.session['register_form_data'])

    # o redirect é para madar o retorno para outra tela, no caso essa de authors:register que será usada na 
    # função de register_view acima
    return redirect('authors:register')