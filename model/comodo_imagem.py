from sqlalchemy import BLOB, Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comodo_Imagem(Base):
    __tablename__ = 'comodo_imagem'

    id = Column("pk_comodo_imagem", Integer, primary_key=True)

    # Definição do relacionamento entre o imobiliaria e uma atividade.
    # Aqui está sendo definido a coluna 'id_atividade' que vai guardar
    # a referencia à atividade, a chave estrangeira que relaciona
    # um imobiliaria à atividade.
    id_comodo = Column(Integer, ForeignKey(
        "comodo.pk_comodo"), nullable=False)

    imagem = Column(BLOB,nullable=False)  
    nome_imagem = Column(String(4000))  
    descricao =  Column(BLOB)  
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e um produto.
    # Aqui está sendo definido a coluna 'produto' que vai guardar
    # a referencia ao produto, a chave estrangeira que relaciona
    # um produto ao comentário.
   
    def __init__(self,id_comodo:int, imagem:BLOB,nome_imagem:str, 
                 descricao:BLOB, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.id_comodo = id_comodo
        self.imagem = imagem
        self.nome_imagem = nome_imagem
        self.descricao = descricao
        if data_insercao:
            self.data_insercao = data_insercao
