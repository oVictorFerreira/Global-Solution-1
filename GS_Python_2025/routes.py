# João Victor da Silva Ferreira - RM 560439
# Erick Cardoso - RM 560440
# Davi Daparé - RM 560721

# Este módulo define as rotas da aplicação Flask para gerenciar relatos de enchentes.

# routes.py - Arquivo que define todas as rotas da aplicacao Flask

from flask import request, jsonify, Response         # Funcoes para requisicoes e respostas
from datetime import datetime, timedelta             # Para manipulacao de datas
from models import Session, Relato                   # Importa o modelo e a sessao do banco

# Funcao que registra todas as rotas no app Flask
def register_routes(app):

    # Rota GET para listar apenas relatos aprovados
    @app.route('/relatos', methods=['GET'])
    def listar_relatos():
        session = Session()  # Inicia a sessao com o banco
        relatos = session.query(Relato).filter_by(aprovado=True).all()  # Busca relatos com aprovado=True

        # Prepara os dados como lista de dicionarios
        resposta = [{
            "id": r.id,
            "title": r.title,
            "message": r.message,
            "severity": r.severity,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "neighborhood": r.neighborhood,
            "water_level": r.water_level,
            "affected_people": r.affected_people,
            "rescue_needed": r.rescue_needed,
            "people_trapped": r.people_trapped,
            "access_blocked": r.access_blocked
        } for r in relatos]

        session.close()  # Fecha conexao com o banco
        return jsonify(resposta)  # Retorna os dados em formato JSON

    # Rota POST para criar um novo relato
    @app.route('/relatos', methods=['POST'])
    def criar_relato():
        dados = request.get_json()  # Recebe os dados enviados em JSON
        try:
            # Cria um novo objeto Relato com os dados recebidos
            novo = Relato(
                title=dados.get("title"),
                message=dados.get("message"),
                severity=dados.get("severity"),
                latitude=dados.get("latitude"),
                longitude=dados.get("longitude"),
                neighborhood=dados.get("neighborhood"),
                water_level=dados.get("water_level"),
                affected_people=dados.get("affected_people"),
                rescue_needed=dados.get("rescue_needed"),
                people_trapped=dados.get("people_trapped"),
                access_blocked=dados.get("access_blocked"),
                aprovado=False  # Sempre comecando como nao aprovado
            )
            session = Session()
            session.add(novo)  # Adiciona o relato
            session.commit()   # Salva no banco
            session.close()
            return jsonify({"mensagem": "Relato recebido com sucesso"}), 201
        except Exception as e:
            return jsonify({"erro": f"Erro ao criar relato: {str(e)}"}), 500

    # Rota PUT para aprovar um relato pelo ID
    @app.route('/relatos/<int:relato_id>/aprovar', methods=['PUT'])
    def aprovar_relato(relato_id):
        session = Session()
        relato = session.query(Relato).get(relato_id)  # Busca o relato pelo ID
        if not relato:
            session.close()
            return jsonify({"erro": "Relato nao encontrado"}), 404
        relato.aprovado = True  # Marca como aprovado
        session.commit()
        session.close()
        return jsonify({"mensagem": "Relato aprovado com sucesso"})

    # Rota DELETE para excluir relato pelo ID
    @app.route('/relatos/<int:relato_id>', methods=['DELETE'])
    def deletar_relato(relato_id):
        session = Session()
        relato = session.query(Relato).get(relato_id)
        if not relato:
            session.close()
            return jsonify({"erro": "Relato nao encontrado"}), 404
        session.delete(relato)  # Remove
        session.commit()       # Aplica no banco
        session.close()
        return jsonify({"mensagem": "Relato excluido com sucesso"})

    # Rota GET que exporta os relatos aprovados em .txt (relatos da semana)
    @app.route('/relatos/semana', methods=['GET'])
    def exportar_txt_semana():
        session = Session()
        sete_dias_atras = datetime.now() - timedelta(days=7)  # Calculo de 7 dias atras

        # Busca relatos aprovados (por enquanto nao temos campo data)
        relatos = session.query(Relato).filter(Relato.aprovado == True, Relato.id > 0).all()

        linhas = []  # Armazena as linhas do arquivo
        for r in relatos:
            linhas.append(f"Titulo: {r.title}")
            linhas.append(f"Bairro: {r.neighborhood}")
            linhas.append(f"Gravidade: {r.severity}")
            linhas.append(f"Pessoas Atingidas: {r.affected_people}")
            linhas.append(f"Altura da Agua: {r.water_level} cm")
            linhas.append(f"Resgate Necessario: {'Sim' if r.rescue_needed else 'Nao'}")
            linhas.append("-" * 40)

        session.close()
        txt_content = "\n".join(linhas)  # Junta todas as linhas

        # Retorna como arquivo .txt para download
        return Response(
            txt_content,
            mimetype='text/plain',
            headers={"Content-Disposition": "attachment;filename=relatos_semana.txt"}
        )