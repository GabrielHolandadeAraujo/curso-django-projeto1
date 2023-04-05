import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    # estamos definindo a quantidade de receitas por página
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        # Passamos o link do site, podemos usar o live_server_url pois o StaticLiveServerTestCase sobe
        # um servidor para testarmos
        self.browser.get(self.live_server_url)
        # podemos buscar qualquer elemento no site procurando pelo By.(o que buscar), pode ser nome de tag, classe,
        # id... e depois passamos o que estamos buscando, nesse caso o conteúdo do body
        body = self.browser.find_element(By.TAG_NAME, 'body')
        # depois verificamos se a menssaem está dentro do texto contido no conteúdo da tag body
        self.assertIn('No recipes found here 🥲', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        # criamos n receitas (o padrão é 10)
        recipes = self.make_recipe_in_batch()
        # definimos o título esperado para procurar um elemento na tela
        title_needed = 'This is what I need'
        # definimos que a primiera receita terá o título esperado e salvamos no bd do Django
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            # esse termo permite capturar um input com o placeholder em questão
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Clica neste input e digita o termo de busca
        # para encontrar a receita o título desejado
        # o send_keys permite digitar qualquer coisa que passarmos por parâmetro
        search_input.send_keys(title_needed)
        # o Keys precisa ser importado e serve para digitar teclas específicas do teclado como ENTER, ALT, ESC...
        search_input.send_keys(Keys.ENTER)

        # O usuário vê o que estava procurando na página
        self.assertIn(
            title_needed,
            # procuramos o título esperado pelo conteúdo da classe abaixo
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
