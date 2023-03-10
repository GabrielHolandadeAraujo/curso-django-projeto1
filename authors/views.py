from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.

# É necessário importar o redenr de django.shortcuts para renderizar a url, para isso precisamos de uma função 
# que retorne o redenr passando a requisição e o caminho para o template em questão
def register_view(request):
    #  Aqui temos uma estrátegia de rota, se o form tiver o método POST, então enviaremos os dados do post na função
     if request.POST:
        form = RegisterForm(request.POST)
    # Caso não tenha o post, a função não tem parametros
    else:
        form = RegisterForm()
    # Aqui estamos renderizando a URL para o template e a request, também passamos o form via variável django
    # se for método post
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })