from authors.forms import RegisterForm
from django.test import TestCase
from parameterized import parameterized

# para criar testes unitários precisamos de uma classe, nesse caso para os testes unitários de registro 
# de authors. A classe precisa herdar de TestCase (existem outras opçãoes) que tem que ser importada 
# após isso fazemos todas as funções de tests dentro da classe
class AuthorRegisterFormUnitTest(TestCase):
    # o parameterized permite testar várias coisas de uma vez, ele precisa ser importado.
    # Basicamente usamos ele como decoretor com o nome dele.expand (adicionando com @ antes da função que vai usar).
    # podemos passar uma lista de parâmetros, onde em cada parênteses teremos o nome da variável (campo no caso) 
    # e o valor (placeholder no caso), ele joga cada um dos valores dentro da função para não precisar 
    # fazer uma função para cada valor
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: Yugi'),
        ('last_name', 'Ex.: Moto'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        # precisamos importar oq será testado, e adicionar a função a uma variável para manipulá-la
        form = RegisterForm()
        # estamos acessando o index de placeholder usando o form no index do campo
        current_placeholder = form[field].field.widget.attrs['placeholder']
        # aqui que o parameterized brilha. ele vai jogar o primeiro valor na current_placeholder 
        # (o placeholder que acabamos de buscar) e o segundo no placeholder que passamos por parãnmetro para comparar
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', (
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.')),
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        # esse teste é igual o anterior, porém podemos acessar os help_text pela forma padrão do django abaixo
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)