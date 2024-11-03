# Projeto Crawler em Python

Este projeto consiste em uma aplicação de web scraping que coleta informações de imóveis disponíveis para aluguel no site Zap Imóveis. A aplicação também utiliza inteligência artificial através da API Gemini para responder perguntas sobre os dados coletados.

## Pré-requisitos

Antes de executar a aplicação, você precisa configurar uma chave de API no Google Colab. 

### Configurando a Chave da API

1. Abra seu notebook no Google Colab.
2. No menu superior, clique em `Ambiente de Execução` > `Executar tudo`.
3. Execute o seguinte comando para definir sua chave de API:
   ```python
   import google.colab.userdata as userdata
   userdata.set('API_KEY_GEMAI', 'AIzaSyDDhRGiIErRIey3NyP09O')
