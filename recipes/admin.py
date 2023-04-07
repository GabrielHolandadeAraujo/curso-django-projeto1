from django.contrib import admin

# Register your models here.

from .models import Category, Recipe

#Primeira forma de importar a tabela é fazer a função e usar o comando admin.site.registrer pasando a tabela importada e a função criada
class CategoryAdmin(admin.ModelAdmin):
    ...

#Outra maneira é colocando um decorator com @admin.registrer passando a função importada como parâmetro e criar a função
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # aqui é onde configuramos a área administrativa do django, as alterações são feitas no admim de cada app
    # o list_display recebe uma lista com todas os campos que estarão visiveis na área de admim (o padrão é só id)
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    # o list_display_links recebe uma lista de todos os campos que serão links para o post (o padrão é só id)
    list_display_links = 'title', 'created_at',
    # o search_fields recebe uma lista dos  campos que poderão ser buscados no admim
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps',
    # o list_filter recebe uma lista com os campos para filtro na area admim que serão exibidos num meno a direita
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html',
    # o list_per_page recebe a quantidade de posts que serão exibidos por página
    list_per_page = 10
    # o list_editable é uma opção de marcar ou desmarcar um determinado campo, muito util para posts publiucados ou não
    list_editable = 'is_published',
    # o ordereing recebe uma lista para ordenar as receitas, por padrão é por id e ordem crescente, mas é melhor colcoar em ordem decrescente
    ordering = '-id',
    # o prepopulated_fields recebe um dicionário para autocompletar alguns campos com base em outros, por exemplo a 
    # slug, que já autocompleta da maneira correta colcoando os traços, eliminando caracteres especiasi e caixa alta
    prepopulated_fields = {
        "slug": ('title',)
    }

admin.site.register(Category, CategoryAdmin)
