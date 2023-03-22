from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# primeiro passamos o caminho do projeto, podemos pegar o caminho do aquivo com Path(__file__), preccisa importar o path
# porém, precisamos do caminho do projeto, para isso usamos .parent que pega o caminho da pasta mãe.
# Como o arquivo está dentro de uma sub-pasta (bin) precisamos usar o .parent 2 vezes para pegar o caminho do projeto 
ROOT_PATH = Path(__file__).parent.parent
# aqui é o nome do arquivo, se tiver no nome alguma extensão como por exemplo: arquivo.exe, precisamos botar 
# exatatamente igual com o .exe para funcionar
CHROMEDRIVER_NAME = 'chromedriver'
# Depois passamos o caminho do arquivo, podemos usar as variáveis já usadas para montar o caminho
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

# uma função para abir o Chrome e fazer algo, passamos um options com o * de args que nos permite passar 
# uma tupla de argumentos.
def make_chrome_browser(*options):
    # pegamos as opções do Chrome, tem que importar o webdriver
    chrome_options = webdriver.ChromeOptions()
    #se tiver argumetos no options, passamos pela tupla com um for e adcionamos as opções
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    # depois definimos o serviço a ser executado pegando o caminho do arquivo
    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    # depois passamos o serviço e as opções para o navegador e retornamos a variável para acessar as funções 
    # a partir dela
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser

if __name__ == '__main__':
    #chamamos a função passando o --headless que serve para fazer o serviço em segundo plano, ou seja, 
    # sem abrir o navegador. Se não passar esse argumento ele mostra tudo abrindo o navegador e fazendo o serviço
    browser = make_chrome_browser('--headless')
    # passamos o site a ser assesado com o get, isso vai abrir o navegador
    browser.get('http://www.udemy.com/')
    # um pequeno delay de 5 segundos (tem que importar)
    sleep(5)
    # por fim fechamos o navegador
    browser.quit