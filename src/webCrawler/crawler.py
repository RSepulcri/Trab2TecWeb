#código funcionará no google colab

import requests #importa biblioteca de requests get,post
from bs4 import BeautifulSoup #importa bs4 para extrair os dados html e xml
import pandas as pd #importa pd para manipular, organizar e exportar dados coletados em tabelas e salvar como csv
from selenium import webdriver #simulador de navegador
from selenium.webdriver.chrome.service import Service #faz com que o selenium simule um navegador
from selenium.webdriver.chrome.options import Options #//
import time #biblioteca de tempo para trabalhar com sleep(time.sleep(xxx)) e outras coisas
from google.colab import files
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import random #importa modulo de random
import google.generativeai as genai #SDK da Gemini
import ipywidgets as widgets #importa biblioteca para widgets
from IPython.display import display #importa biblioteca para widgets
from google.colab import userdata #importa o módulo que manipula variáveis de enviroment/secrets do colab
#
#credenciais do LambdaTest
username = 'eduardo.evaristo.am'  #username
access_key = 'VZGoC8JtKpO3xrvZTcIOTGaV3iFOP1YD2MnLguzKNGuT8N8QLv'  #access key
#
#configurações do ChromeOptions
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  #inicia o navegador
#
#configurações do navegador
capabilities = {
    'LT:Options': {
        'build': 'Selenium Python Sample',  #nome da sua build
        'name': 'Sample Test',  #nome do seu teste
        'platform': 'Windows 11',  #plataforma do SO
        'browserName': 'Chrome',  #nome do navegador
        'version': 'latest'  #versão do navegador
    }
}

chrome_options.set_capability('LT:Options', capabilities['LT:Options'])
#
#conectando ao LambdaTest
driver = webdriver.Remote(
    command_executor=f'https://{username}:{access_key}@hub.lambdatest.com/wd/hub',
    options=chrome_options
)
#
# Configurações do ChromeOptions - Utilizar este
def config_driver():
  chrome_options = Options()
  chrome_options.add_argument("--start-maximized")  # Inicia o navegador

  # Lista de user-agent strings
  user_agents = [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/94.0",
      # Adicione mais user-agent strings conforme necessário
  ]

  # Definindo um user-agent aleatório
  chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')

  # Configurações do navegador
  capabilities = {
      'LT:Options': {
          'build': 'Selenium Python Sample',  # Nome da sua build
          'name': 'Sample Test',  # Nome do seu teste
          'platform': 'Windows',  # Plataforma do SO
          'browserName': 'Chrome',  # Nome do navegador
          'version': 'latest'  # Versão do navegador
      }
  }

  chrome_options.set_capability('LT:Options', capabilities['LT:Options'])

  # Conectando ao LambdaTest
  driver = webdriver.Remote(
      command_executor=f'https://{username}:{access_key}@hub.lambdatest.com/wd/hub',
      options=chrome_options
  )
  return driver
#
# Três páginas da zapimovieis
urls = {
    "zapimoveis1": "https://www.zapimoveis.com.br/aluguel/imoveis/es+vitoria/?__ab=sup-hl-pl:newC,exp-aa-test:control,super-high:new,off-no-hl:new,pos-zap:new,new-rec:b,ltroffline:control&transacao=aluguel&onde=,Esp%C3%ADrito%20Santo,Vit%C3%B3ria,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVitoria,-20.319664,-40.338475,&pagina=1",
    "zapimoveis2": "https://www.zapimoveis.com.br/aluguel/imoveis/es+vitoria/?__ab=sup-hl-pl:newC,exp-aa-test:control,super-high:new,off-no-hl:new,pos-zap:new,new-rec:b,ltroffline:control&transacao=aluguel&onde=,Esp%C3%ADrito%20Santo,Vit%C3%B3ria,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVitoria,-20.319664,-40.338475,&pagina=2",
    "zapimoveis3": "https://www.zapimoveis.com.br/aluguel/imoveis/es+vitoria/?__ab=sup-hl-pl:newC,exp-aa-test:control,super-high:new,off-no-hl:new,pos-zap:new,new-rec:b,ltroffline:control&transacao=aluguel&onde=,Esp%C3%ADrito%20Santo,Vit%C3%B3ria,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVitoria,-20.319664,-40.338475,&pagina=3"
}
#
#função para buscar informações de um imóvel
def get_imovel_data(url, driver):
    driver.get(url)
    time.sleep(10)  # Aguarde o carregamento da página

    # Aguarda elemento desejado estar presente na página
    target_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "aside.campaign[data-cy='campaign']"))
    )

    #Registra a altura da página
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scrolla até o elememnto desejado
        driver.execute_script("arguments[0].scrollIntoView();", target_element)
        time.sleep(5)  #Aguarda novos anúncios carregarem

        # Checa se a altura da página mudou (novos anúncios foram carregados)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Se altura não mudou, sai do loop
        #Se altura mudou, atualiza a útlima
        last_height = new_height


    #Obtém o html da página
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    #Seleciona div dos resultados
    outer_div = soup.find('div', class_='listing-wrapper__content')

    #Seleciona divs dos anuncios (cards)
    divs = outer_div.find_all("div", {"data-position": True})
    print(divs)


    #Array p/ guardar os dados
    listings = []
    for listing in divs:
        try:
            # Title/Location (Centro, Vitória)
            title = listing.find("h2", {"data-cy": "rp-cardProperty-location-txt"}).get_text(strip=True)

            # Street Address (Rua Henrique Novaes)
            address = listing.find("p", {"data-cy": "rp-cardProperty-street-txt"}).get_text(strip=True)

            # Property Size (32 m²)
            size = listing.find("p", {"data-cy": "rp-cardProperty-propertyArea-txt"}).get_text(strip=True)

            # Bathroom Quantity (1)
            bathroom_quantity = listing.find("p", {"data-cy": "rp-cardProperty-bathroomQuantity-txt"}).get_text(strip=True)

            # Price (R$ 450)
            price = listing.find("div", {"data-cy": "rp-cardProperty-price-txt"}).find("p").get_text(strip=True)

            # Additional Costs (Cond. R$ 300 | IPTU R$ 26)
            additional_costs = listing.find("div", {"data-cy": "rp-cardProperty-price-txt"}).find_all("p")[1].get_text(strip=True)

            listings.append({
                "title": title,
                "address": address,
                "size": size,
                "bathroom_quantity": bathroom_quantity,
                "price": price,
                "additional_costs": additional_costs,
            })
        except AttributeError as e:
            print(f"Erro ao processar um imóvel: {e}")
            continue  # Pular para o próximo listing em caso de erro

    driver.quit()

    # Print the extracted listings (apenas para testes)
    for listing in listings:
        print(listing)
    return listings
#
#função para coletar dados de todas as cidades e sites
def coletar_dados_de_aluguel():
    dados_coletados = []
    driver = config_driver()  # Inicie o driver uma vez

    for site, url in urls.items():
        print(f"Coletando dados de {site}...")
        dados_imoveis = get_imovel_data(url, driver)
        dados_coletados.extend(dados_imoveis)

    driver.quit()  # Feche o driver após a coleta
    return dados_coletados

#
#armazenar dados em um DataFrame e exportar
dados_de_aluguel = coletar_dados_de_aluguel()
df = pd.DataFrame(dados_de_aluguel)
df.to_csv('imoveis_aluguel.csv', index=True, encoding='utf-8')

print("Coleta concluída e dados salvos em imoveis_aluguel.csv")
print(df)
files.download('imoveis_aluguel.csv') #descomentar caso queira baixar o csv
#
#Front-end
api_key = userdata.get('API_KEY_GEMAI')

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Criação de um campo de texto para a pergunta do usuário
pergunta_texto = widgets.Text(
    description='Pergunta:',
    placeholder='Digite sua pergunta aqui...'
)

# Criação de um botão para enviar a pergunta
botao_enviar = widgets.Button(description='Enviar')

# Saída para mostrar a resposta
saida_resposta = widgets.Output()

#Lê arquivo csv
with open('imoveis_aluguel.csv', 'r') as file:
    dados = file.read()

# Função para gerar a resposta quando o botão é clicado
def on_botao_enviar_clicked(b):
    with saida_resposta:
        saida_resposta.clear_output()  # Limpa a saída anterior
        pergunta = pergunta_texto.value
        # Chamando o modelo com a pergunta do usuário e contexto adicional
        response = model.generate_content(f'{pergunta}. {dados}. Considere que o salário mínimo é R$1412 e dê respostas concisas.', generation_config = genai.GenerationConfig(
        temperature=0.1,
    )
)
        print(response.text)

# Conectando a função ao botão
botao_enviar.on_click(on_botao_enviar_clicked)

# Exibindo os widgets
display(pergunta_texto, botao_enviar, saida_resposta)
#
