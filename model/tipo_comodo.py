from sqlalchemy import Column, String, Integer, DateTime, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Tipo_Comodo(Base):
    __tablename__ = 'tipo_comodo'
   
    # Definição da tabela lista.
    # Aqui está sendo definida a tabela lista, que deverá
    # conter os nomes dos tipos de listas que os clientes podem fazer
    # É uma tabela auxiliar
   
    id = Column("pk_tipo_comodo", Integer, primary_key=True)
    descricao = Column(String(40),unique=True,nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o atividade e a forncedor.
    # Essa relação é implicita, não está salva na tabela 'atividade',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comodo = relationship("Comodo")
   
    def __init__(self, descricao:str,data_insercao:Union[DateTime, None] = None):
        """
        Cria um tipo de comodo

        Arguments:
            descricao: descricao do tipo de comodo
            data_insercao: data de quando o tipo de comodo foi inserido à base
        """
        self.descricao = descricao
        
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
