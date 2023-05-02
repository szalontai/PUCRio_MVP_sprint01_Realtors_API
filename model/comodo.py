from sqlalchemy import BLOB, Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Comodo(Base):
    __tablename__ = 'comodo'

    # Definição da tabela imobiliaria.
    # Aqui está sendo definida a tabela imobiliaria, que deverá
    # conter os fornecedores dos produtos a serem listados escolha dos clientes

    id = Column("pk_comodo", Integer, primary_key=True)
   
    # Definição do relacionamento entre o imobiliaria e uma atividade.
    # Aqui está sendo definido a coluna 'id_atividade' que vai guardar
    # a referencia à atividade, a chave estrangeira que relaciona
    # um imobiliaria à atividade.
    id_imovel = Column(Integer, ForeignKey(
        "imovel.pk_imovel"), nullable=False)

    # Definição do relacionamento entre o imobiliaria e uma atividade.
    # Aqui está sendo definido a coluna 'id_atividade' que vai guardar
    # a referencia à atividade, a chave estrangeira que relaciona
    # um imobiliaria à atividade.
    id_tipo_comodo = Column(Integer, ForeignKey(
        "tipo_comodo.pk_tipo_comodo"), nullable=False)
    
    nome = Column(String(20), nullable=False)
    quantidade = Column(Integer)
    descricao =  Column(String(4000))  
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o preço e o fornecedor.
    # Essa relação é implicita, não está salva na tabela 'fornecedor',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comodo = relationship("Comodo_Imagem")


    def __init__(self, nome: str, quantidade: int,  descricao: str,id_imovel:int,
                 id_tipo_comodo:int, data_insercao: Union[DateTime, None] = None):
        """
        Cria um Imobiliaria

        Arguments:
            nome: nome da imobiliaria
            razao_social: razão social da imobiliaria
            cnpj: cnpj da imobiliaria
            ie: inscrição estadual da imobiliaria
            endereco: endereco da imobiliaria
            complemento: complemento da imobiliaria
            bairro: bairro da imobiliaria
            cidade: cidade da imobiliaria
            uf: unidade da federação da imobiliaria
            cep: cep da imobiliaria
            ddd: ddd da imobiliaria
            telefone: telefone da imobiliaria
            id_atividade: código do ramo de atividade da imobiliaria, associado à tabela atividade
            id_matriz: se houver valor, indica o codigo da matriz no qual esse fornecedor faz parte
            data_insercao: data de quando o fornecedor foi inserido à base
        """
        self.nome = nome
        self.quantidade = quantidade
        self.descricao = descricao
        self.id_imovel = id_imovel
        self.id_tipo_comodo = id_tipo_comodo
         
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao