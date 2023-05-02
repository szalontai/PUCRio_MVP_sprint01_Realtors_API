from venv import logger
from pydantic import BaseModel
from typing import List
from model.imovel import Imovel


class ImovelSchema(BaseModel):
    """ Define como um novo imóvel deve ser inserido
    """
    nome: str = "Apartamento 2 dormitórios"
    endereco: str = "Rua Regente Leon Kaniefsky, 113"
    complemento: str = ""
    bairro: str = "VILA PROGREDIOR"
    cidade: str = "SAO PAULO"
    uf: str = "SP"
    cep: str = "05617-030"
    ddd: int = 11
    telefone: str = "3742-6377"
    descricao: str = ""
    id_tipo_imovel: int = 0  # Código do tipo do imóvel
    id_imobiliaria: int = 0  # Código da imobiliaria


class ImovelBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
        Será feita apenas com base no id do imóvel.
    """
    id: int = 0  # Id do imóvel


class ImovelBuscaByImobiliariaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
        Será feita apenas com base no id do imóvel.
    """
    id_imobiliaria: int = 0  # Id do imóvel



class ImovelViewSchema(BaseModel):
    """ Define como um imóvel será retornado.
    """
    id: int
    nome: str 
    endereco: str 
    complemento: str 
    bairro: str 
    cidade: str 
    uf: str 
    cep: str 
    ddd: int 
    telefone: str 
    descricao: str 
    id_tipo_imovel: int
    id_imobiliaria: int



class ListagemImoveisSchema(BaseModel):
    """ Define como uma listagem de imóveis será retornada seguindo o schema definido em
        ImovelViewSchema.
    """
    imovel: List[ImovelViewSchema]


class ImovelDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    id: int
    nome: str
    endereco: str 

def apresenta_imovel(imovel: Imovel,tipo : str):
    """ Retorna uma representação do imóvel.
    """
    
    if tipo=="P":
        result = {
            "id": imovel.id,
            "nome": imovel.nome,
            "endereco": imovel.endereco,
            "complemento": imovel.complemento,
            "bairro": imovel.bairro,
            "cidade": imovel.cidade,
            "uf": imovel.uf,
            "cep": imovel.cep,
            "ddd": imovel.ddd,
            "telefone": imovel.telefone,
            "descricao": imovel.descricao,
            "id_tipo_imovel": imovel.id_tipo_imovel,
            "id_imobiliaria": imovel.id_imobiliaria,
        }        
    else:
        result = {
            "id": imovel.Imovel.id,
            "nome": imovel.Imovel.nome,
            "endereco": imovel.Imovel.endereco,
            "complemento": imovel.Imovel.complemento,
            "bairro": imovel.Imovel.bairro,
            "cidade": imovel.Imovel.cidade,
            "uf": imovel.Imovel.uf,
            "cep": imovel.Imovel.cep,
            "ddd": imovel.Imovel.ddd,
            "telefone": imovel.Imovel.telefone,
            "descricao": imovel.Imovel.descricao,
            "tipo_imovel": imovel.Tipo_Imovel.descricao,
            "imobiliaria": imovel.Imobiliaria.nome,
        }
        
    return result


def apresenta_imoveis(imoveis: List[Imovel]):
    """ Retorna uma listagem da representação do imóvel.
    """
    result = []
    for imovel in imoveis:

        result.append(
            {
                "id": imovel.Imovel.id,
                "nome": imovel.Imovel.nome,
                "endereco": imovel.Imovel.endereco,
                "complemento": imovel.Imovel.complemento,
                "bairro": imovel.Imovel.bairro,
                "cidade": imovel.Imovel.cidade,
                "uf": imovel.Imovel.uf,
                "cep": imovel.Imovel.cep,
                "ddd": imovel.Imovel.ddd,
                "telefone": imovel.Imovel.telefone,
                "descricao": imovel.Imovel.descricao,
                "tipo_imovel": imovel.Tipo_Imovel.descricao,
                "imobiliaria": imovel.Imobiliaria.nome,

            }
        )

    return {"imoveis": result}

def apresenta_imoveis_tot(imoveis: List[Imovel]):
    """ Retorna uma listagem da representação do imóvel.
    """
    result = []
    for imovel in imoveis:
        
        result.append(
            {
                "id": imovel[0],
                "nome": imovel[1],
                "endereco": imovel[2],
                "complemento": imovel[3],
                "bairro": imovel[4],
                "cidade": imovel[5],
                "uf": imovel[6],
                "cep": imovel[7],
                "ddd": imovel[8],
                "telefone": imovel[9],
                "descricao": imovel[10],
                "imovel": imovel[15],
                "imobiliaria":imovel[18],
                "qtde_filhas":imovel[32],

            }
        )

    return {"imoveis": result}
