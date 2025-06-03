# João Victor da Silva Ferreira - RM 560439
# Erick Cardoso - RM 560440
# Davi Daparé - RM 560721

# Este módulo define as rotas da aplicação Flask para gerenciar relatos de enchentes.

from flask import request, jsonify                # Para receber dados (request) e responder em JSON
from datetime import datetime                     # Para usar data/hora
import os                                         # Para criar pasta e salvar arquivos
from models import conexao, cursor                # Usa conexão e cursor do banco (importado do models)

# Função que salva os relatos em arquivo diário
def salvar_em_arquivo(bairro, nivel, mensagem):
    try:
        os.makedirs("relatorios", exist_ok=True)  # Cria pasta "relatorios" se ainda não existir
        nome_arquivo = datetime.now().strftime("relatorios/relatorio_%Y-%m-%d.txt")
        with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            arquivo.write(f"Bairro: {bairro}\n")
            arquivo.write(f"Nível: {nivel}\n")
            arquivo.write(f"Mensagem: {mensagem}\n")
            arquivo.write("-" * 40 + "\n")
    except Exception as e:
        print(f"Erro ao salvar em arquivo: {e}")

# Função principal que registra as rotas no app Flask
def configurar_rotas(app):

    # Rota para registrar um novo relato (não aprovado por padrão)
    @app.route("/relato", methods=["POST"])
    def receber_relato():
        try:
            dados = request.get_json()
            bairro = dados.get("bairro")
            nivel = dados.get("nivel")
            mensagem = dados.get("mensagem")
            data = datetime.now()
            cursor.execute(
                "INSERT INTO RELATOS (BAIRRO, NIVEL, MENSAGEM, DATA, APROVADO) VALUES (%s, %s, %s, %s, %s)",
                (bairro, nivel, mensagem, data, False)
            )
            conexao.commit()
            salvar_em_arquivo(bairro, nivel, mensagem)  # Também salva no arquivo diário
            return jsonify({"mensagem": "Relato salvo (aguardando aprovação)."}), 201
        except Exception as e:
            return jsonify({"erro": f"Erro ao salvar relato: {str(e)}"}), 500

    # Rota para listar relatos (com filtro ?aprovado=1 ou não)
    @app.route("/relatos", methods=["GET"])
    def listar_relatos():
        try:
            aprovado = request.args.get("aprovado")
            if aprovado is not None:
                cursor.execute("SELECT * FROM RELATOS WHERE APROVADO = %s", (aprovado,))
            else:
                cursor.execute("SELECT * FROM RELATOS")
            resultados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            dados = [dict(zip(colunas, linha)) for linha in resultados]
            return jsonify(dados)
        except Exception as e:
            return jsonify({"erro": f"Erro ao listar relatos: {str(e)}"}), 500

    # Rota para aprovar relato por ID
    @app.route("/aprovar/<int:id_relato>", methods=["PUT"])
    def aprovar_relato(id_relato):
        try:
            cursor.execute("UPDATE RELATOS SET APROVADO = TRUE WHERE ID = %s", (id_relato,))
            conexao.commit()
            return jsonify({"mensagem": f"Relato {id_relato} aprovado com sucesso."})
        except Exception as e:
            return jsonify({"erro": f"Erro ao aprovar relato: {str(e)}"}), 500

    # Rota para deletar relato por ID
    @app.route("/relato/<int:id_relato>", methods=["DELETE"])
    def deletar_relato(id_relato):
        try:
            cursor.execute("DELETE FROM RELATOS WHERE ID = %s", (id_relato,))
            conexao.commit()
            return jsonify({"mensagem": f"Relato {id_relato} deletado com sucesso."})
        except Exception as e:
            return jsonify({"erro": f"Erro ao deletar relato: {str(e)}"}), 500

    # Rota de login básico para administrador
    @app.route("/login", methods=["POST"])
    def login_admin():
        try:
            dados = request.get_json()
            usuario = dados.get("usuario")
            senha = dados.get("senha")
            if usuario == "admin" and senha == "1234":  # Login fixo para exemplo
                return jsonify({"mensagem": "Login autorizado", "token": "admin123"})
            else:
                return jsonify({"mensagem": "Credenciais inválidas"}), 401
        except Exception as e:
            return jsonify({"erro": f"Erro no login: {str(e)}"}), 500
