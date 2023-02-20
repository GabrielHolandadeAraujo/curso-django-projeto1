from django.contrib import admin

# Register your models here.

from .models import Category, Recipe

#Primeira forma de importar a tabela é fazer a função e usar o comando admin.site.registrer pasando a tabela importada e a função criada
class CategoryAdmin(admin.ModelAdmin):
    ...

#Outra maneira é colocando um decorator com @admin.registrer passando a função importada como parâmetro e criar a função
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...

admin.site.register(Category, CategoryAdmin)
