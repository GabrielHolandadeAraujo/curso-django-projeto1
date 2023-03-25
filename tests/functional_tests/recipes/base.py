import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_chrome_browser

# estqmos herdando de StaticLiveServerTestCase para carregar o css da página, se não fosse necessário os
# arquivos estáticos poderimos herdar de LiveServerTestCase que é mais leve, mas não carrega css na pag
class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    # Estamos abrindo o acesso ao drive aqui para não precisar abrir nos testes
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()
    # estamos fechando o navegador após todos os testes

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    # o seconds=5 define um tempo padrão de 5 segundos, mas pode ser mudado no parâmetro da função

    def sleep(self, seconds=5):
        time.sleep(seconds)
