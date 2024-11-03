import google.generativeai as genai #SDK da Gemini
import ipywidgets as widgets #importa biblioteca para widgets
from IPython.display import display #importa biblioteca para widgets
from dotenv import load_dotenv
import os

#Front-end - Funciona apenas no Colab! Não funcionará no terminal.

#Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv('API_KEY_GEMAI')

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