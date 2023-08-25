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

vw = session.get(Marca, 1)
fiat = session.get(Marca, 2)
gm = session.get(Marca, 3)
# Selecionando uma marca existente no banco de dados e utilizando-a para adicionar um novo carro.

golf = Carro(
    name='Golf',
    content='Golf é um automóvel fabricado pela Volkswagen. Foi lançado no mercado europeu em 1974 e no mercado brasileiro em 1995, quando já estava na sua terceira geração. O Golf é, atualmente, o carro de maior sucesso de vendas na história da Volkswagen, superando até o mítico Volkswagen Fusca, carro que substituiu na Europa a partir da década de 1970.',
    released=1974,
    marca=vw
)

jetta = Carro(
    name='Jetta',
    content='Desde 1999, a Volkswagen comercializa o sedãn médio no Brasil, durante quase todo este período o modelo foi importado do México. A 4ª geração do modelo foi a primeira a chegar, sendo chamada de Volkswagen Bora. O modelo, em versão única de acabamento era equipada com o mesmo motor a gasolina do Golf brasileiro, o EA 113 2.0, que mais tarde, em 2002, passou a equipar também o Polo e o Polo Sedan. O modelo podia vir com câmbio manual de 5 marchas ou automático Tiptronic de 4 marchas.',
    released=1979,
    marca=vw
)

s10 = Carro(
    name='S10',
    content='A S10 é uma picape de porte médio da Chevrolet produzida no Brasil desde 1995 até atualmente. De mecânica relativamente simples, foi campeã de vendas de 1996 até 2005.',
    released=1995,
    marca=gm
)

session.add_all([golf, jetta, s10])
session.flush()
session.commit()
