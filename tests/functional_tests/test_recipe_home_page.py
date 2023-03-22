import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser

# estqmos herdando de StaticLiveServerTestCase para carregar o css da página, se não fosse necessário os 
# arquivos estáticos poderimos herdar de LiveServerTestCase que é mais leve, mas não carrega css na pag
class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    # o seconds=5 define um tempo padrão de 5 segundos, mas pode ser mudado no parâmetro da função
    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_the_test(self):
        # primeiro sempre confguramos o navegador
        browser = make_chrome_browser()
        # depois passamos o link do site, podemos usar o live_server_url pois o StaticLiveServerTestCase sobe
        # um servidor para testarmos
        browser.get(self.live_server_url)
        self.sleep(2)
        # podemos buscar qualquer elemento no site procurando pelo By.(o que buscar), pode ser nome de tag, classe, 
        # id... e depois passamos o que estamos buscando, nesse caso o conteúdo do body
        body = browser.find_element(By.TAG_NAME, 'body')
        # depois verificamos se a menssaem está dentro do texto contido no conteúdo da tag body
        self.assertIn('No recipes found here 🥲', body.text)
        # por fim sempre fechamos o navegador
        browser.quit()
