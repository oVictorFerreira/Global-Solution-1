# João Victor da Silva Ferreira - RM 560439
# Erick Cardoso - RM 560440
# Davi Daparé - RM 560721

# Projeto: Sistema de Monitoramento de Enchentes - AlagaNão!
# Descrição: Este é o arquivo principal da aplicação Flask que conecta ao banco de dados SQL e inicia o servidor.

# app.py - Arquivo principal da aplicação Flask

# Importação da classe Flask para criar a aplicação web
# Importação de render_template para renderizar arquivos HTML dentro da pasta templates
from flask import Flask, render_template

# Importação do CORS para permitir acesso da API por qualquer origem (frontend em React, etc.)
from flask_cors import CORS

# Inicializa a aplicação Flask, apontando a pasta templates como local dos HTMLs
app = Flask(
    __name__,                      # Nome do aplicativo
    template_folder='templates',  # Pasta onde estão os arquivos .html
    static_folder='static'        # Pasta onde estão os arquivos .css e .jsx
)

# Ativa o suporte a CORS na aplicação para evitar erros de "Cross-Origin Request"
CORS(app)

# Rota principal '/' que renderiza a página index.html (frontend)
@app.route('/')
def index():
    # Renderiza o arquivo HTML templates/index.html (com React dentro)
    return render_template('index.html')

# Executa a aplicação em modo debug (com recarregamento automático)
if __name__ == '__main__':
    # Roda o servidor Flask na porta padrão (5000), com debug ativado
    app.run(debug=True)
