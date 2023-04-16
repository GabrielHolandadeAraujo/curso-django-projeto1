import os
from django.db.models import Q
from django.http.response import Http404
from django.views.generic import DetailView, ListView
from recipes.models import Recipe
from utils.pagination import make_pagination

# Aqui estamos definindo a qtd de itens por página usando a constante em .env
# Caso o valor da 'PER_PAGE' não seja encontrado, o valor padrão será 6
PER_PAGE = int(os.environ.get('PER_PAGE', 6))

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

    # INFORMAÇÕES:
    # O - no id serve para inverter a ordem, o Q coloca os termos entre parênteses
    # O | (pipe) serve para substituir a busca do AND para OR
    # o varaivel__icontains serve para buscar algo que contenha, exemplo: bolo acha bolo de cenoura
    # o i de icontains serve para ignorar caixa alta ou baixa na busca, sem o i ele considera   
    # o messages precisa ser importado e serve para flash messages com alertas como success, error e warning
    # messages.error(request, 'Epa, você foi pesquisar algo que eu vi.')
    # messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')
    # messages.info(request, 'Epa, você foi pesquisar algo que eu vi.')
