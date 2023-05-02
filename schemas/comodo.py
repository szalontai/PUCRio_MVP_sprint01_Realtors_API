from venv import logger
from pydantic import BaseModel
from typing import List
from model.comodo import Comodo


class ComodoSchema(BaseModel):
    """ Define como um novo cômodo deve ser inserido
    """
    id_imovel: int = 0  # Código do imóvel
    id_tipo_comodo: int = 0  # Código do tipo do cômodo
    nome: str = "Quarto"
    quantidade: int = 2
    descricao: str = ""


class ComodoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
        Será feita apenas com base no id do cômodo.
    """
    id: int = 0  # Id do cômodo


class ComodoBuscaByImovelSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
        Será feita apenas com base no id do imóvel.
    """
    id_imovel: int = 0  # Id do imóvel


class ComodoViewSchema(BaseModel):
    """ Define como um cômodo será retornado.
    """
    id: int
    id_imovel: int
    id_tipo_comodo: int
    nome: str
    quantidade: int
    descricao: str


class ListagemComodosSchema(BaseModel):
    """ Define como uma listagem de cômodos será retornada seguindo o schema definido em
        ComodoViewSchema.
    """
    comodo: List[ComodoViewSchema]


class ComodoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int
    id_imovel: int
    id_tipo_comodo: int
    nome: str


def apresenta_comodo(comodo: Comodo, tipo: str):
    """ Retorna uma representação do cômodo.
    """


    if tipo == "P":
        result = {
            "id": comodo.id,
            "imovel": comodo.nome,
            "tipo_comodo": comodo.id_tipo_comodo,
            "nome": comodo.nome,
            "quantidade": comodo.quantidade,
            "descricao": comodo.descricao,
        }
    else:
        result = {
            "id": comodo.Comodo.id,
            "imovel": comodo.Imovel.nome,
            "tipo_comodo": comodo.Tipo_Comodo.descricao,
            "nome": comodo.Comodo.nome,
            "quantidade": comodo.Comodo.quantidade,
            "descricao": comodo.Comodo.descricao,
        }

    return result


def apresenta_comodos(comodos: List[Comodo]):
    """ Retorna uma listagem da representação do cômodo.
    """
    result = []
    for comodo in comodos:
        result.append(
            {
                "id": comodo.Comodo.id,
                "imovel": comodo.Imovel.nome,
                "tipo_comodo": comodo.Tipo_Comodo.descricao,
                "nome": comodo.Comodo.nome,
                "quantidade": comodo.Comodo.quantidade,
                "descricao": comodo.Comodo.descricao,
            }
        )

    return {"comodos": result}

def apresenta_comodos_tot(comodos: List[Comodo]):
    """ Retorna uma listagem da representação do cômodo.
    """
    result = []
    for comodo in comodos:
        
        result.append(
            {
                "id": comodo[0],
                "imovel": comodo[8],
                "tipo_comodo": comodo[22],
                "nome": comodo[3],
                "quantidade": comodo[4],
                "descricao": comodo[5],
                "qtde_filhas": comodo[24],
            }
        )

    return {"comodos": result}
