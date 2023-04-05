from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AuthorsRegisterTest(AuthorsBaseTest):
    # procuramos pelo placeholder, aqui usamos o prórpio form (form.find_element pq estamos com o campo selecionado)

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )
    # aqui é para preencher os dados dos campos para testar a resposta a requisição
    def fill_form_dummy_data(self, form):
        # buscamos todos os campos pois são input
        fields = form.find_elements(By.TAG_NAME, 'input')

        # preenchemos todos os campos com 20 espaços em bnanco
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def test_empty_first_name_error_message(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)
        # preenchemos o email separadamente pois ele precisa ter um formato específico para validar
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        first_name_field = self.get_by_placeholder(form, 'Ex.: John')
        first_name_field.send_keys(' ')
        first_name_field.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.assertIn('Write your first name', form.text)