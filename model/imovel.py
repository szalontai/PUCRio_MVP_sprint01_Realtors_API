from sqlalchemy import BLOB, Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Imovel(Base):
    __tablename__ = 'imovel'

    # Definição da tabela imobiliaria.
    # Aqui está sendo definida a tabela imobiliaria, que deverá
    # conter os fornecedores dos produtos a serem listados escolha dos clientes

    id = Column("pk_imovel", Integer, primary_key=True)
    nome = Column(String(20), nullable=False)
    endereco = Column(String(90))
    complemento = Column(String(15))
    bairro = Column(String(25))
    cidade = Column(String(90))
    uf = Column(String(2))
    cep = Column(String(9))
    ddd = Column(Integer)
    telefone = Column(String(10))
    descricao =  Column(String(4000))  

    # Definição do relacionamento entre o imobiliaria e uma atividade.
    # Aqui está sendo definido a coluna 'id_atividade' que vai guardar
    # a referencia à atividade, a chave estrangeira que relaciona
    # um imobiliaria à atividade.
    id_tipo_imovel = Column(Integer, ForeignKey(
        "tipo_imovel.pk_tipo_imovel"), nullable=False)

    # Definição do relacionamento entre o imobiliaria e uma atividade.
    # Aqui está sendo definido a coluna 'id_atividade' que vai guardar
    # a referencia à atividade, a chave estrangeira que relaciona
    # um imobiliaria à atividade.
    id_imobiliaria = Column(Integer, ForeignKey(
        "imobiliaria.pk_imobiliaria"), nullable=False)
    
     # Definição do relacionamento entre o preço e o fornecedor.
    # Essa relação é implicita, não está salva na tabela 'fornecedor',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comodo = relationship("Comodo")


    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, endereco: str, complemento: str,
                 bairro: str, cidade: str, uf: str, cep: str, ddd: int, telefone: str,
                 descricao: str,id_tipo_imovel:int, id_imobiliaria:int, 
                 data_insercao: Union[DateTime, None] = None):
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
        self.endereco = endereco
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.cep = cep
        self.ddd = ddd
        self.telefone = telefone
        self.descricao = descricao
        self.id_tipo_imovel = id_tipo_imovel
        self.id_imobiliaria = id_imobiliaria
         
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao