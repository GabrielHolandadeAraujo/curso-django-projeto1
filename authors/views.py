from django.shortcuts import render

# Create your views here.

# É necessário importar o redenr de django.shortcuts para renderizar a url, para isso precisamos de uma função 
# que retorne o redenr passando a requisição e o caminho para o template em questão
def register_view(request):
    return render(request, 'authors/pages/register_view.html')