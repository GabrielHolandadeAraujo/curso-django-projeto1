import os

from django.contrib import messages
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe
from utils.pagination import make_pagination

# Aqui estamos definindo a qtd de itens por página usando a constante em .env
# Caso o valor da 'PER_PAGE' não seja encontrado, o valor padrão será 6
PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    # Abrir tela de emojis é WINDOWS + . (ponto)
    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    # o strip tira os espaços em branco antes e depois da string
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    # O - no id serve para inverter a ordem, o Q coloca os termos entre parênteses
    # O | (pipe) serve para substituir a busca do AND para OR
    # o varaivel__icontains serve para buscar algo que contenha, exemplo: bolo acha bolo de cenoura
    # o i de icontains serve para ignorar caixa alta ou baixa na busca, sem o i ele considera   
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    # o messages precisa ser importado e serve para flash messages com alertas como success, error e warning
    # messages.error(request, 'Epa, você foi pesquisar algo que eu vi.')
    # messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')
    # messages.info(request, 'Epa, você foi pesquisar algo que eu vi.')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
