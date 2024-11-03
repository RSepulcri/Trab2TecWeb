# Projeto Crawler em Python

Este projeto consiste em uma aplicação de web scraping que coleta informações de imóveis disponíveis para aluguel no site Zap Imóveis. A aplicação também utiliza inteligência artificial através da API Gemini para responder perguntas sobre os dados coletados.

## Pré-requisitos

- **Possuir uma conta Google**
- **Acessar o Google Colab**  
  link: [https://colab.google/](https://colab.research.google.com/drive/1huAnkuhvSEa-oIfiFmi2vpJ1yA1Cb2wT?usp=sharing)

## Configurando Inteligencia Artificial GemIA

### Passo 1 - Clique na chave no canto esquerdo

![Passo 1](/src/img/1.png)

### Passo 2 - Clique em adicionar novo segredo

![Passo 2](/src/img/11.png)

### Passo 3 - Insira: nome "API_KEY_GEMAI", valor "AIzaSyDDhRGiIErRIey3NyP09O-IYyu6P9EzETM" e ative a checkbox

![Passo 3](/src/img/111.png)

### Passo 4 - Feche a aba de configuração de segredos

![Passo 4](/src/img/1111.png)

Pronto, agora a parte de inteligencia artificial está configurada!

#### Configurando a Chave da API

1. Abra seu notebook no Google Colab.
2. No menu superior, clique em `Ambiente de Execução` > `Executar tudo`.
3. Execute o seguinte comando para definir sua chave de API:
   ```python
   import google.colab.userdata as userdata
   userdata.set('API_KEY_GEMAI', 'AIzaSyDDhRGiIErRIey3NyP09O')
   ```

## Rodar localmente

### Passo 1 - Clone o repositório no local desejado e acesse-o

![Passo 1](/src/img/3.png)

### Passo 2 - Acesse a branch 'local'

![Passo 2](/src/img/33.png)

### Passo 3 - Crie um ambiente virtual e acesse-o

![Passo 2](/src/img/333.png)

### Passo 4 - Cole o conteúdo de requirements no terminal e execute

![Passo 3](/src/img/3333.png)

### Passo 5 - Execute o crawler e aguarde a criação do arquivo .csv

![Passo 4](/src/img/33333.png)
![Passo 4](/src/img/333333.png)
