from django.urls import resolve, reverse
from recipes import views
from unittest.mock import patch

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Check if one recipe exists
        self.assertIn(
            '<h1>No recipes found here 🥲</h1>',
            response.content.decode('utf-8')
        )
    
    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)
        # Esse patch precisa ser importado e pode ser usado da forma abaixo ou com o decorator
        # O path basicamente serve para alterar o valor de uma variável para um fim (no caso o teste)
        # e após isso retorna com o valor original, no exemplo estamos mudando o valor de PER_PAGE para 3 durante 
        # o teste, isso é fundamental em variáveis que afetam o teste
        with patch('recipes.views.PER_PAGE', new=3):
            # o reverse renderiza uma url do projeto
            response = self.client.get(reverse('recipes:home'))
            # o context é uma variável gerada pelo reverse e ela captura muitas informações da página, para 
            # entender melhor é recomendável fazer um break point logo abaixo dele e debugar para ver o valor 
            # de context, cada um dos valores pode ser assessado como um índice da maneira abaixo            
            recipes = response.context['recipes']
            # a função paginator retorna já captura a paginação da tela
            paginator = recipes.paginator
            # a função num_pages retorna o valor de itens na página
            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)