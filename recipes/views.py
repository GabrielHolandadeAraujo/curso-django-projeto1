import os
from django.db.models import F, Q, Value
from django.db.models.functions import Concat
from django.http.response import Http404
from django.views.generic import DetailView, ListView
from recipes.models import Recipe
from utils.pagination import make_pagination
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models.aggregates import Count

# Aqui estamos definindo a qtd de itens por página usando a constante em .env
# Caso o valor da 'PER_PAGE' não seja encontrado, o valor padrão será 6
PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def theory(request, *args, **kwargs):
    # recipes = Recipe.objects.values('id', 'title')
    # try:
    #     recipes = Recipe.objects.get(pk=10000)
    # except ObjectDoesNotExist:
    #     recipes = None
    # recipes = Recipe.objects.filter(
    #     Q(
    #         Q(title__icontains='da',
    #           id__gt=2,
    #           is_published=True,) |
    #         Q(
    #             id__gt=1000
    #         )
    #     )
    # )[:10]
    #     id=F('author__id'),
    # ).order_by('-id', 'title')[:1]
    # recipes = Recipe.objects \
    #     .values('id', 'title', 'author__username')[:10]
    # recipes = Recipe.objects.values('id', 'title')[:5]
    recipes = Recipe.objects.all().annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')'),
        )
    )
    number_of_recipes = recipes.aggregate(number=Count('id'))

    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['number']
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context
    )

# o ListView é uma CBV do Django para tratar de listas e já tem várias funções prontas como uma paginação
# Como a pagina home é uma lista de receitas, podemos usar essa cbv para lá.
class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'
    # pra tratar de exibir só os filtradso precisamos mexer na queryset e pora isso temos que reescrecer a função
    # get_queryset do django filtrando os publicados e retornando a variável que criamos no filtro
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        return qs
    # Como fizemos um paginação própria, temos que defini-la com uma função que usará a função que criamos para
    # fazer a paginaçãp e atualizar na home.

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_object, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {'recipes': page_object, 'pagination_range': pagination_range}
        )
        return ctx
    
class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - Category | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        if not search_term:
            raise Http404()
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx

    # Abrir tela de emojis é WINDOWS + . (ponto)

# o Detailview requer poucas coisas, baiscamente só precisaremos mexer no contexto
class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })

        return ctx
    
class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        # o model_to_dict transforma um modelo em um dicionário com os dados do modelo
        recipe_dict = model_to_dict(recipe)
        # estamos adicionando a data de criação e atualização no dicionário
        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)
        # precisamos verificar se o modelo tem imagem, se tiver temos que fazer uma operação
        if recipe_dict.get('cover'):
            # invés da imagem, passamos a url. Para passar a url completa precisamos pegar a url absoluta 
            # e untar com a url do dicionário fatiada, pois uma barra seria duplicada. A barra é o primeiro 
            # elemento da segunda string então podemos fatiar apenas ela.
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            # se não tiver img passamos apenas uma string vazia
            recipe_dict['cover'] = ''
        # removemos do dicionário as informações de dados html
        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']
        # por fim damos a resposta em json passando o dicionário e o safe
        return JsonResponse(
            recipe_dict,
            safe=False,
        )

    # INFORMAÇÕES:
    # O - no id serve para inverter a ordem, o Q coloca os termos entre parênteses
    # O | (pipe) serve para substituir a busca do AND para OR
    # o varaivel__icontains serve para buscar algo que contenha, exemplo: bolo acha bolo de cenoura
    # o i de icontains serve para ignorar caixa alta ou baixa na busca, sem o i ele considera   
    # o messages precisa ser importado e serve para flash messages com alertas como success, error e warning
    # messages.error(request, 'Epa, você foi pesquisar algo que eu vi.')
    # messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')
    # messages.info(request, 'Epa, você foi pesquisar algo que eu vi.')
