from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm

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
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    # se o método for get (tentar reenviar um msm form) ele da um 404
    if not request.POST:
        raise Http404()
    # caso o método for post vai receber os dados e repassar para a função de view mandando get para evitar
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
        # estamos mandando o user para a página de login logo após ser registrado
        return redirect(reverse('authors:login'))
    # o redirect é para madar o retorno para outra tela, no caso essa de authors:register que será usada na
    # função de register_view acima
    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()
    # passamos a requisição para o form de login e renderizamos a url
    form = LoginForm(request.POST)
    login_url = reverse('authors:login')
    # se os dados de login forem válidos, verificamos se o usuário pode ser loado
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        # se puder ser logado, verificamos se os dados não são vazios e fazemos o loing
        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')
    # todos os casos dos if else redirecionam para a msm url e por isso usanos apenas o return
    return redirect(reverse('authors:dashboard'))

# esse decorator precisa ser importado e serve para só liberar acesso a função um user que estiver logado
# pasamos a url onde é feita o login e a url para ser redirecionado após o login
# o next simplesmente manda para a página que o user tentou acessar sem estar logado, então ele 
# será rediredcionado para o msm local após logar
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    # verificamos se é por método post, se for get vai voltar para página de login, isso é para evitar acessar 
    # a página via link sem passar pelo login
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))
    # também verificamos se o usuário logado é o msm que está tentando acessar
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))
    # por fim realizamos o logtou (cuidado para não colocar o nome da função igual a padrão que causaria erros)
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login'))

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    # Exibimos as receitas não publicadas do usuário no dashboard dele 
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes,
        }
    )

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    #filtramos a receita não publicadas do usuário pelo id
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
        #essa função first é para retornar apenas o primeiro elemento encontrado, pois o filter retorna uma lista 
        # de elementos encontrados. ao invés dessa função, poderiamos usar o get no lugar do filter que retorna só um
        # porém o get gera um erro se não encontrar, isso tornaria o if abaixo obsoleto. Optamos por nós mesmos 
        # conferirmos se o elemento existe
    ).first()
    # se a receita não existir da um 404
    if not recipe:
        raise Http404()
    # instaciamos a classe de forms do authors podendo passar a requisição (caso o filtro acima encontre o elemento)
    # ou None, caso a receita ainda não exista. Depois instaciamos na própria variável acima (do filtro), caso ela exista
    # isso é para atualizar caso já exista ou criar caso não exista.
    form = AuthorRecipeForm(
        data=request.POST or None,
        # para receber uma mídia ou não
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        # Agora, o form é válido e eu posso tentar salvar, fingimos salvar para faze algumas manipulações
        recipe = form.save(commit=False)
        # garantimos que esses campos serão salvos com os dados abaixo como medida de segurança adicional
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form
        }
    )