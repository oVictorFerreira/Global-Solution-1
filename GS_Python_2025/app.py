# João Victor da Silva Ferreira - RM 560439
# Erick Cardoso - RM 560440
# Davi Daparé - RM 560721

# Projeto: Sistema de Monitoramento de Enchentes
# Descrição: Este é o arquivo principal da aplicação Flask que conecta ao banco de dados MySQL e inicia o servidor.

# Importa as bibliotecas necessárias
from flask import Flask, request, jsonify          # Flask para criar servidor web e lidar com requisições JSON
import mysql.connector                             # Biblioteca para conectar com o MySQL

# Inicializa a aplicação Flask
app = Flask(__name__)

# ---------------- CONEXÃO COM BANCO DE DADOS ----------------
try:
    # Tenta conectar ao banco MySQL
    conexao = mysql.connector.connect(
        host="localhost",                          # Endereço do servidor MySQL
        user="seu_usuario",                        # Nome de usuário do MySQL (troque pelo seu)
        password="sua_senha",                      # Senha do MySQL (troque pela sua)
        database="ENCHENTES_DB"                    # Nome do banco de dados usado
    )
    cursor = conexao.cursor()                      # Cria cursor para executar comandos SQL
except Exception as e:
    # Caso ocorra erro na conexão, imprime no terminal
    print(f"Erro ao conectar ao banco de dados: {e}")

# ---------------- INICIA APLICAÇÃO ----------------
if __name__ == "__main__":
    app.run(debug=True)                                # Inicia o servidor Flask em modo debug
