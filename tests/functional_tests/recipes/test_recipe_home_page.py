import pytest
from selenium.webdriver.common.by import By
from unittest.mock import patch
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
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
