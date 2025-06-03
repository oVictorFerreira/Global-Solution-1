import mysql.connector  # Biblioteca para conectar ao MySQL

# Configurações (você pode trocar por leitura de arquivo no futuro)
USUARIO = "seu_usuario"  # Trocar pelo seu usuário do MySQL
SENHA = "sua_senha"  # Trocar pela sua senha do MySQL
HOST = "localhost"  # Endereço do MySQL
BANCO = "ENCHENTES_DB"  # Nome do banco desejado

try:
    # Conecta sem banco específico só para criar, se necessário
    conexao_inicial = mysql.connector.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA
    )
    cursor_inicial = conexao_inicial.cursor()
    cursor_inicial.execute(f"CREATE DATABASE IF NOT EXISTS {BANCO}")  # Cria banco se não existir
    conexao_inicial.close()

    # Conecta agora ao banco definitivo
    conexao = mysql.connector.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA,
        database=BANCO
    )
    cursor = conexao.cursor()

    # Cria a tabela RELATOS se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS RELATOS (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            BAIRRO VARCHAR(100) NOT NULL,
            NIVEL VARCHAR(20) NOT NULL,
            MENSAGEM TEXT NOT NULL,
            DATA DATETIME NOT NULL,
            APROVADO BOOLEAN DEFAULT FALSE
        )
    """)
    conexao.commit()
    print(f"✅ Banco '{BANCO}' e tabela 'RELATOS' prontos para uso.")

except Exception as e:
    print(f"Erro ao configurar banco de dados: {e}")
