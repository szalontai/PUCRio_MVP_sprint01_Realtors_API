from sqlalchemy import BLOB, Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Imagem(Base):
    __tablename__ = 'imagem'

    id = Column(Integer, primary_key=True)
    local = Column(String(4000))
    photo = Column(BLOB,nullable=False)  
    resume =  Column(BLOB)  
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e um produto.
    # Aqui está sendo definido a coluna 'produto' que vai guardar
    # a referencia ao produto, a chave estrangeira que relaciona
    # um produto ao comentário.
   
    def __init__(self, local:str,photo:BLOB,resume:BLOB, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.local = local
        self.photo = photo
        self.resume = resume
        if data_insercao:
            self.data_insercao = data_insercao
