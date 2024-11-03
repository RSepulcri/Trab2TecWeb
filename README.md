# Projeto Crawler em Python

Este projeto consiste em uma aplicação de web scraping que coleta informações de imóveis disponíveis para aluguel no site Zap Imóveis. A aplicação também utiliza inteligência artificial através da API Gemini para responder perguntas sobre os dados coletados.

## Pré-requisitos

- **Possuir uma conta Google**
- **Acessar o Google Colab**  
    link: [https://colab.google/](https://colab.research.google.com/drive/1huAnkuhvSEa-oIfiFmi2vpJ1yA1Cb2wT?usp=sharing)

### Configurando Inteligencia Artificial GemIA
- **Passo 1**  ![Passo 1](/src/img/1.png)  
- **Passo 2**  ![Passo 2](/src/img/11.png)  
- **Passo 3**  ![Passo 3](/src/img/111.png)  
- **Passo 4**  ![Passo 4](/src/img/1111.png)  



#### Configurando a Chave da API

1. Abra seu notebook no Google Colab.
2. No menu superior, clique em `Ambiente de Execução` > `Executar tudo`.
3. Execute o seguinte comando para definir sua chave de API:
   ```python
   import google.colab.userdata as userdata
   userdata.set('API_KEY_GEMAI', 'AIzaSyDDhRGiIErRIey3NyP09O')
