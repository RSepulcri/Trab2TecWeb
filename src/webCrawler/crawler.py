import requests #importa biblioteca de requests get,post
from bs4 import BeautifulSoup #importa bs4 para extrair os dados html e xml
import pandas as pd #importa pd para manipular, organizar e exportar dados coletados em tabelas e salvar como csv
from selenium import webdriver #simulador de navegador
from selenium.webdriver.chrome.service import Service #faz com que o selenium simule um navegador
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time #biblioteca de tempo para trabalhar com sleep(time.sleep(xxx)) e outras coisas
import random #importa modulo de random

#credenciais do LambdaTest
username = 'eduardo.evaristo.am'  #username
access_key = 'VZGoC8JtKpO3xrvZTcIOTGaV3iFOP1YD2MnLguzKNGuT8N8QLv'  #access key


# Configurações do ChromeOptions
def config_driver():
  chrome_options = Options()
  chrome_options.add_argument("--start-maximized")  # Inicia o navegador

  # Lista de user-agent strings para evitar cair no cloudflare
  user_agents = [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/94.0",
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

# Três páginas da zapimoveis
urls = {
    "zapimoveis1": "https://www.zapimoveis.com.br/aluguel/imoveis/es+vitoria/?__ab=sup-hl-pl:newC,exp-aa-test:control,super-high:new,off-no-hl:new,pos-zap:new,new-rec:b,ltroffline:control&transacao=aluguel&onde=,Esp%C3%ADrito%20Santo,Vit%C3%B3ria,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVitoria,-20.319664,-40.338475,&pagina=1",
    "zapimoveis2": "https://www.zapimoveis.com.br/aluguel/imoveis/es+vitoria/?__ab=sup-hl-pl:newC,exp-aa-test:control,super-high:new,off-no-hl:new,pos-zap:new,new-rec:b,ltroffline:control&transacao=aluguel&onde=,Esp%C3%ADrito%20Santo,Vit%C3%B3ria,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVitoria,-20.319664,-40.338475,&pagina=2",
    "zapimoveis3": "https://www.zapimoveis.com.br/aluguel/imoveis/es+vitoria/?__ab=sup-hl-pl:newC,exp-aa-test:control,super-high:new,off-no-hl:new,pos-zap:new,new-rec:b,ltroffline:control&transacao=aluguel&onde=,Esp%C3%ADrito%20Santo,Vit%C3%B3ria,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVitoria,-20.319664,-40.338475,&pagina=3"
}

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

#função para coletar dados de todas as cidades e sites
def coletar_dados_de_aluguel():
    dados_coletados = []

    for site, url in urls.items():
        driver = config_driver()
        print(f"Coletando dados de {site}...")
        dados_imoveis = get_imovel_data(url, driver)
        dados_coletados.extend(dados_imoveis)

    return dados_coletados


#armazenar dados em um DataFrame e exportar
dados_de_aluguel = coletar_dados_de_aluguel()
df = pd.DataFrame(dados_de_aluguel)
df.to_csv('imoveis_aluguel.csv', index=True, encoding='utf-8')

print("Coleta concluída e dados salvos em imoveis_aluguel.csv")
print(df)



