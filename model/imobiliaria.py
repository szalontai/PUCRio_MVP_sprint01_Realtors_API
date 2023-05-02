from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Imobiliaria(Base):
    __tablename__ = 'imobiliaria'

    # Definição da tabela imobiliaria.
    # Aqui está sendo definida a tabela imobiliaria, que deverá
    # conter os fornecedores dos produtos a serem listados escolha dos clientes

    id = Column("pk_imobiliaria", Integer, primary_key=True)
    nome = Column(String(20), nullable=False, unique=True)
    razao_social = Column(String(40), nullable=False, unique=True)
    cnpj = Column(String(20), nullable=False, unique=True)
    ie = Column(String(20))
    endereco = Column(String(90))
    complemento = Column(String(15))
    bairro = Column(String(25))
    cidade = Column(String(90))
    uf = Column(String(2))
    cep = Column(String(9))
    ddd = Column(String(2))
    telefone = Column(String(10))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o filial e a matriz.
    # Aqui está sendo definido a coluna 'id_matriz' que vai guardar
    # a referencia à matriz, a chave estrangeira que relaciona
    # uma filial à matriz.
    id_matriz = Column(Integer, ForeignKey(
        "imobiliaria.pk_imobiliaria"), nullable=True)

    # Definição do relacionamento entre o preço e o fornecedor.
    # Essa relação é implicita, não está salva na tabela 'fornecedor',
    # mas aqui estou deixando para SQLAlchemy a responsabilidadeString(10)
    # de reconstruir esse relacionamento.
    #
    imovel = relationship("Imovel")

    # Definição do relacionamento entre a filial e a matriz.
    # Essa relação é implicita, não está salva na tabela 'fornecedor',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    filial = relationship("Imobiliaria")

    def __init__(self, nome: str, razao_social: str, cnpj: str, ie: str, endereco: str, complemento: str,
                 bairro: str, cidade: str, uf: str, cep: str, ddd: str, telefone: str,
                 id_matriz: int, data_insercao: Union[DateTime, None] = None):
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
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.ie = ie
        self.endereco = endereco
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.cep = cep
        self.ddd = ddd
        self.id_matriz = id_matriz
        self.telefone = telefone

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
