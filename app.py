from sqlalchemy import ForeignKey, create_engine
# 'ForeingKey' estabelece o relacionamento entre duas tabelas / 'create_engine' serve para o ORM se comunicar com um banco de dados através de um URL.
from sqlalchemy.engine import URL
# 'URL' representa um link para se conectar com o banco de dados.
from sqlalchemy import Column, Integer, String, DateTime, Text
# 'Column, Integer, String e Text' são classes que indetificam os tipos de cada dado que podem preencher a tabela / 'DateTime' é uma classe para definir o horário de alguma ação.
from sqlalchemy.orm import declarative_base
# A função 'declarative_base' é a base de todas as classes que geram as classes do Python mapeadas em tabelas do banco de dados.
from datetime import datetime
# 'datetime' é uma classe que serve para manipular datas e horas.
from sqlalchemy.orm import relationship, backref
# 'relationship' é uma função que estabelece relacionamento entre classes / 'backref' é um parâmetro que serve para relacionar tabelas através de uma nova referência.
from sqlalchemy.orm import sessionmaker
# 'sessionmaker' é uma classe usada para criar as configurações de uma sessão que pode ser usada em todo o aplicativo sem a necessidade de repetição.

url = "sqlite:///database.db"
# Criando uma URL.
engine = create_engine(url)
# Criando uma ligação do ORM com o banco de dados através da URL definida.
connection = engine.connect()
# Conectando o ORM com o banco de dados.
Session = sessionmaker(bind=engine)
# Criando sessão através da engine definida.
session = Session()
# Iniciando sessão.

Base = declarative_base()
# Criando uma classe base para as outras classes que serão geradas posteriormente.


class Carro(Base):
    __tablename__ = 'carros'

    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now,
                        onupdate=datetime.now)
    content = Column(Text)
    released = Column(Integer())
    marca_id = Column(Integer(), ForeignKey('marcas.id'))


class Marca(Base):
    __tablename__ = 'marcas'

    id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    country = Column(String(100))
    contact = Column(String(25))
    joined = Column(DateTime(), default=datetime.now)

    cars = relationship('Carro', backref='marca')


Base.metadata.create_all(engine)

vw = Marca(
    name="Volkswagen",
    country="Alemanha",
    contact="0800 019 5775"
)

fiat = Marca(
    name="Fiat",
    country="Itália",
    contact="0800 707 1000"
)

gm = Marca(
    name="Chevrolet",
    country="Estados Unidos",
    contact="0800 702 4200"
)

carro1 = Carro(
    name="Gol",
    content="Lançado em 1980, o Gol é considerado um dos maiores sucessos da Volkswagen do Brasil de todos os tempos. É também o primeiro e único carro produzido no Brasil a ultrapassar a marca de 5 milhões de unidades produzidas até hoje, tornando-se, em fevereiro de 2009, o primeiro e único a superar o Fusca em vendas. Nos mais de 40 anos de produção, teve mais de 8,5 milhões de unidades produzidas, sendo o carro mais vendido da história do Brasil.",
    released=1980,
    marca=vw
)

carro2 = Carro(
    name="Uno",
    content="O Uno é um automóvel compacto fabricado pela Fiat, lançado na Europa em 1983. Foi lançado no Brasil no ano seguinte, e sua nova geração (projetada no Brasil) só foi lançada em 2010, direcionada aos países da América Latina. A versão antiga foi produzida até dezembro de 2013 sendo vendida como Fiat Mille nome adotado inicialmente em 1990, quando adotou um motor com menos de 1 000 cc no Brasil. O nome é uma referência ao número um em italiano.",
    released=1983,
    marca=fiat
)

carro3 = Carro(
    name="Onix",
    content="O Onix é um automóvel hatchback, sedan e notchback, produzido pela Chevrolet; desenvolvido e fabricado pela General Motors do Brasil. Em 2013, foi apresentado no salão de São Paulo, sendo uma das atrações da Chevrolet. Lançado com a missão de substituir o Celta, (posteriormente substituiu o Chevrolet Sonic e o Chevrolet Agile) o Onix é baseado na arquitetura global de veículos pequenos da General Motors.",
    released=2013,
    marca=gm
)

session.add_all([vw, fiat, gm, carro1, carro2, carro3])
session.flush()
session.commit()
