from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password

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
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')
        # add_attr(self.fields['username'], 'css', 'a-css-class')

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=4, max_length=150,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.',
    )

    # Aqui é uma alteração diferente, estamos alterando diretamente um campo, primeiro defindo como campo de 
    # caracteres e colocando o required para True (pode omitir, pois True é padrão), 
    # dessa forma o campo é obrigaório, se estivesse falso o campo seria opcional (como um complemento de um endereço)
    password = forms.CharField(
        # required=True, (omitido)
        # Aqui estamos alterando os atributos do campo com o widget, esse tipo de alteração é 
        # uma sobrescrita, pois algumas coisas já haviam sido definidos na classe meta abaixo, 
        # alterar por sobrescrita pode gerar confusões, principalmente se o campo em questão for usado 
        # em várias partes do código 
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        # podemos adicionar validores para os campos, como no caso da função de senha forte, 
        # para isso é só colocar todos os validadores dentro da lista de validators no final do campo
        validators=[strong_password],
        label='Password'
    )
    #aqui estamos gerando um campo novo a partir da sobrescrita de password para ser usado como método 
    # de segurança para comparar as senhas que devem ser iguais 
    password2 = forms.CharField(
        required=True,
        # widget = forms.PasswordInput(attrs={
        #     'placeholder': 'Repeat your password'
        # })    
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages={
            'required': 'Please, repeat your password'
        },
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

        # para mostrar os campos no form da pra dizer quais campos são exibidos, como no field acima, outra
        # opção é o exclude abaixo onde vc iforma quais campos não aparecem
        # exclude = ['first_name']

        # a label será o nome dos campos, aqui definimos como cada campo será mostrado ao user
        # labels = {
        #     'username': 'Username',
        # }
        # os help_texts são as mensagens que ajudam o user a preencehr o campo, como uma dica de como preencher
        # help_texts = {
        #     'email': 'The e-mail must be valid.',
        # }
        # as error_messages são as mensagens de erro, caso o user preencha errado um campo, podemos informar um 
        # erro, é necessário colocar o campo: e abrier chaves conm códigos específicos para o erro em questão, 
        # por exemplo o required é quanto um campo é obrigatório, invalid seria algo como digitar um email sem um @, etc
        # error_messages = {
        #     'username': {
        #         'required': 'This field must not be empty',
        #     } 
        # }
        # as widgets serevem para configurar os campos, podemos por exemplo, definir atributos através do forms 
        # o TextInput é para textos, podemos usar o attrs para definir um placeholder ou até mesmo uma classe css 
        # e sim, é basicamente manipular html direto pelo django.  
        # widgets= {
        #     'first_name': forms.TextInput(attrs={
        #         'placeholder': 'Type your username here',
        #         'class': 'input text-input'
        #     }),
        #     # já o de PassWordInput é específico para senhas, ao usar isso ele vai automaticamente colocar 
        #     # a senha escondinda com o padrão de pontinhos e também podemos definir attrs
        #     'password': forms.PasswordInput(attrs={
        #         'placeholder': 'Type your password here'
        #     })
        # }

    # a função clean é prórpia do Django e deve ser usada com _algumCampo, nos exemplos abaixo tem passsword 
    # e first_name. é possivel pegar os dados brutos dos campos com self.data ou tratados pelo django com 
    # self.cleaned_data e pegar o campos específico com o get
    # def clean_password(self):
    #     data = self.cleaned_data.get('password')
    #     # podemos impedir uma string em específica entrar no campo, como no caso de atenção levantado um erro 
    #     # de validação com o ValidationError (precisa ser importado). Detro da validação você pode colocar uma 
    #     # mensagem e usar o %(var)s e depois definr a var no params, para especificar o termo que não vai entrar.
    #     # também tem que clocar o código do erro como invalid, max_lenth ou required.
    #     if 'atenção' in data:
    #         raise ValidationError(
    #             'Não digite %(pipoca)s no campo password',
    #             code='invalid',
    #             params={'pipoca': '"atenção'}
    #         )
    #     return data
    
    # def clean_first_name(self):
    #     data = self.cleaned_data.get('first_name')

    #     if 'John Doe' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo first name',
    #             code='invalid',
    #             params={'value': '"John Doe"'}
    #         )

    #     return data
    
    # o clean sem definir nenhum campo especifico é uma função de validação do form inteiro e pode 
    # ser usado para validar mais de um campo ao msm tempo, como no caso de senhas iguais 
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email

    def clean(self):
        # podemos acessar a classe pai com super e depois com .clean() para pegar todos os forms, 
        cleaned_data = super().clean()
        # depois é só pegar os especificos com o get
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        # aqui estamos jogando o erro para uma variável e depois levantamos o erro nos campos desejados passando 
        # a variável
        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
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