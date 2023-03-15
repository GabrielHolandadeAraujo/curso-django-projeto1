from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# É interessante criar um arquivo forms.py para controlar os formulários, nele precisa criar uma classe que
# herda de forms.ModelForm pq ele é atrlado ao model do User que foi importado
# Dentro dela é importante uma classe meta que serve para passar metadados do formulário para o django

# essa funçãop serve para adicionar atributos aos campos. Primeiro acessamos o atributo que queremos 
# add via get e caso não tenha nada, setamos um valor em branco. Após isso adicionamos o novo valor e usamos o stip para remover possíveis espaços em branco no inicio e fim da String 
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

# essa uma função para facilitar colocar um placeholder, passamos o campo e o nome do placeholder para 
# add, usamos a função anterior para alterar o valor do placeholder no campo escolhido
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

class RegisterForm(forms.ModelForm):    
    # essa função init é um padrão de projeto chamado construtor (builder) e serve para permitir a 
    # classe de iniciar seus atributos, já *args e **kwargs Servem para que você possa passar quantos parâmetros quiser, sendo eles de posição ou de keyword. Dessa forma o Python vai entender que naquele local você vai passar um ou mais argumentos para a sua função. O args passamos valores como em uma lista e no kwars passams um dicionário com as chaves e os valores
    def __init__(self, *args, **kwargs):
        # O super() é utilizado entre heranças de classes, ele nos proporciona extender/subscrever métodos de uma super classe (classe pai) para uma sub classe (classe filha), atrávez dele definimos um novo comportamento para um determinado método construido na classe pai e herdado pela classe filha.
        # O super nos permite fazer as sobrescritas abaixo
        super().__init__(*args, **kwargs)
        # Aqui estamos usando a função para adicionar alguns placeholders, essa forma é mais 
        # correta, pois estamos alterando o campo definido no meta
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Yugi')
        add_placeholder(self.fields['last_name'], 'Ex.: Moto')

    # Aqui é uma alteração diferente, estamos alterando diretamente um campo, primeiro defindo como campo de 
    # caracteres e colocando o required para True, dessa forma o campo é obrigaório, se estivesse falso o 
    # campo seria opcional (como um complemento de um endereço)
    password = forms.CharField(
        required=True,
        # Aqui estamos alterando os atributos do campo com o widget, esse tipo de alteração é 
        # uma sobrescrita, pois algumas coisas já haviam sido definidos na classe meta abaixo, 
        # alterar por sobrescrita pode gerar confusões, principalmente se o campo em questão for usado 
        # em várias partes do código 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text= (
            'Password must  have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characteres.'
        )
    )
    #aqui estamos gerando um campo novo a partir da sobrescrita de password para ser usado como método 
    # de segurança para comparar as senhas que devem ser iguais 
    password2 = forms.CharField(
        required = True,
        widget = forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model = User
        # nos fields podemos passar quais campos usar (os msm do model User), para passar tudo usamos __all__
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        # para mostrar os campos nor form da pra dizer quais campos são exibidos, como no field acima, outra
        # opção é o exclude abaixo onde vc iforma quais campos não aparecem
        # exclude = ['first_name']

        # a label será o nome dos campos, aqui definimos como cada campo será mostrado ao user
        label = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',                      
        }
        # os help_texts são as mensagens que ajudam o user a preencehr o campo, como uma dica de como preencher
        help_texts = {
            'email': 'The email must be valid.',
        }
        # as error_messages são as mensagens de erro, caso o user preencha errado um campo, podemos informar um 
        # erro, é necessário colocar o campo: e abrier chaves conm códigos específicos para o erro em questão, 
        # por exemplo o required é quanto um campo é obrigatório, invalid seria algo como digitar um email sem um @, etc
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            } 
        }
        # as widgets serevem para configurar os campos, podemos por exemplo, definir atributos através do forms 
        # o TextInput é para textos, podemos usar o attrs para definir um placeholder ou até mesmo uma classe css 
        # e sim, é basicamente manipular html direto pelo django.  
        widgets= {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
                'class': 'input text-input'
            }),
            # já o de PassWordInput é específico para senhas, ao usar isso ele vai automaticamente colocar 
            # a senha escondinda com o padrão de pontinhos e também podemos definir attrs
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    # a função clean é prórpia do Django e deve ser usada com _algumCampo, nos exemplos abaixo tem passsword 
    # e first_name. é possivel pegar os dados brutos dos campos com self.data ou tratados pelo django com 
    # self.cleaned_data e pegar o campos específico com o get
    def clean_password(self):
        data = self.cleaned_data.get('password')
        # podemos impedir uma string em específica entrar no campo, como no caso de atenção levantado um erro 
        # de validação com o ValidationError (precisa ser importado). Detro da validação você pode colocar uma 
        # mensagem e usar o %(var)s e depois definr a var no params, para especificar o termo que não vai entrar.
        # também tem que clocar o código do erro como invalid, max_lenth ou required.
        if 'atenção' in data:
            rasie ValidationError(
                'Não digite %(pipoca)s no campo password',
                code='invalid'
                params={'pipoca': '"atenção'}
            )
        return data
    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': '"John Doe"'}
            )

        return data
    
    # o clean sem definir nenhum campo especifico é uma função de validação do form inteiro e pode 
    # ser usado para validar mais de um campo ao msm tempo, como no caso de senhas iguais 
    def clean(self):
        # podemos acessar a classe pai com super e depois com .clean() para pegar todos os forms, 
        cleaned_data = super().clean()
        # depois é só pegar os especificos com o get
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password')
        # aqui estamos jogando o erro para uma variável e depois levantamos o erro nos campos desejados passando 
        # a variável
        if password != password2:
            password_confirmation_error = ValidationError(
                'Password e and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                # podemos passa um dicionário com as chaves dos campos e valores dos erros
                'password': password_confirmation_error,
                # e podemos passar uma lista de erros no valor da chave
                'password2': [
                    password_confirmation_error,
                ],
            })