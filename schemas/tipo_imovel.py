# from ast import List
from venv import logger
from pydantic import BaseModel
from typing import Optional, List
from model.tipo_imovel import Tipo_Imovel


class Tipo_ImovelSchema(BaseModel):
    """ Define como um novo tipo de imóvel deve ser inserido.
    """
    descricao: str = "Residencial"


class Tipo_ImovelBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
        Será feita apenas com base no id do tipo de imóvel.
    """
    id: int = 0  # Id do tipo do imóvel

class Tipo_ImovelViewSchema(BaseModel):
    """ Define como um tipo de imóvel será retornado.
    """
    id: int
    descricao: str

class Tipos_ImoveisViewSchema(BaseModel):
    """ Define como um tipo de imóvel será retornado.
    """
    id: int
    descricao: str
    qtde: int


class ListagemTipos_ImovelSchema(BaseModel):
    """ Define como uma listagem de tipos de imóvel será retornada seguindo o schema definido em
        Tipo_ImovelViewSchema.
    """
    tipos_imoveis: List[Tipos_ImoveisViewSchema]




class Tipo_ImovelDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    id: int
    descricao: str


def apresenta_tipo_imovel(tipo_Imovel: Tipo_Imovel):
    """ Retorna uma representação do tipo de imóvel.
    """
    result = {
            "id": tipo_Imovel.id,
            "descricao": tipo_Imovel.descricao,
        }
    return result


def apresenta_tipos_imoveis(tipos_Imovel: List[Tipo_Imovel]):
    """ Retorna uma listagem da representação do tipo de imóvel.
    """
    result = []
    for tipo_imovel in tipos_Imovel:

        result.append(

            {
                "id": tipo_imovel[0].id,
                "descricao": tipo_imovel[0].descricao,
                "qtde": tipo_imovel[1],
            }
        )

    return {"tipos_imoveis": result}
