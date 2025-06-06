# Import das classes do SQLAlchemy para manipular o banco de dados
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define a URL de conexão com o banco PostgreSQL
DATABASE_URL = 'postgresql://postgres:joao@localhost:5432/ALAGANAO_DB'

# Cria uma base de modelo (classe base para tabelas)
Base = declarative_base()

# Cria o mecanismo de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões para interagir com o banco
Session = sessionmaker(bind=engine)

# Define o modelo da tabela 'relatos'
class Relato(Base):
    __tablename__ = 'relatos'  # Nome da tabela no banco

    # Define as colunas da tabela
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)         # Título do relato
    message = Column(String, nullable=False)       # Descrição do ocorrido
    severity = Column(String, nullable=False)      # Nível de gravidade (leve, moderado, severo)
    latitude = Column(Float, nullable=False)       # Coordenada geográfica
    longitude = Column(Float, nullable=False)      # Coordenada geográfica
    neighborhood = Column(String, nullable=False)  # Bairro
    water_level = Column(Float)                    # Altura da água (opcional)
    affected_people = Column(Integer)              # Quantidade de pessoas afetadas
    rescue_needed = Column(Boolean, default=False) # Se é necessário resgate
    people_trapped = Column(Integer, default=0)    # Pessoas presas no local
    access_blocked = Column(Boolean, default=False)# Acesso bloqueado
    images = Column(String)                        # Imagem opcional
    aprovado = Column(Boolean, default=False)      # Se o relato foi aprovado por um moderador

# Cria fisicamente a tabela no banco, se ainda não existir
Base.metadata.create_all(engine)
