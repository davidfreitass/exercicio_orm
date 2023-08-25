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

print('-' * 50)
print('Os carros presentes no sistema que são da marca Volkswagen: ')
for carros_vw in session.query(Carro).filter(Carro.marca_id == 1):
    print(carros_vw.name)

print('-' * 50)
print('Os carros presentes no sistema na ordem do mais novo ao mais antigo: ')
for carros_novos in session.query(Carro).order_by(Carro.released.desc()):
    print(f'{carros_novos.name} - {carros_novos.released}')

print('-' * 50)
