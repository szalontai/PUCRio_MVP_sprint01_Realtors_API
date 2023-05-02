# from ast import List
from venv import logger
from pydantic import BaseModel
from typing import Optional, List
from model.tipo_comodo import Tipo_Comodo


class Tipo_ComodoSchema(BaseModel):
    """ Define como um novo tipo de cômodo deve ser inserido.
    """
    descricao: str = "Quarto"


class Tipo_ComodoBuscaSchema(BaseModel):
     """ Define como deve ser a estrutura que representa a busca.
        Será feita apenas com base no id do tipo do cômodo.
    """
     id: int = 0  # Id do tipo do cômodo

class Tipo_ComodoPostSchema(BaseModel):
    """ Define como um tipo de cômodo será retornado.
    """
    mensagem: str
    id: int
    descricao: str


class Tipo_ComodoViewSchema(BaseModel):
    """ Define como um tipo de cômodo será retornado.
    """
    
    id: int
    descricao: str

class Tipos_ComodosViewSchema(BaseModel):
    """ Define como um tipo de cômodo será retornado.
    """
    id: int
    descricao: str
    qtde:int

class ListagemTipos_ComodoSchema(BaseModel):
    """ Define como uma listagem de tipos de cômodos será retornada seguindo o schema definido em
        Tipos_ComodosViewSchema.
    """
    tipos_comodos: List[Tipos_ComodosViewSchema]


class Tipo_ComodoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    id: int
    descricao: str


def apresenta_tipo_comodo(tipo_Comodo: Tipo_Comodo):
    """ Retorna uma representação do tipo de cômodo.
    """
   
    result = {
            "mensagem":"Item adicionado com sucesso !",
            "id": tipo_Comodo.id,
            "descricao": tipo_Comodo.descricao,
        }
    return result


def mostra_tipo_comodo(tipo_Comodo: Tipo_Comodo):
    """ Retorna uma representação do tipo de cômodo.
    """
   
    result = {
            #"mensagem":"",
            "id": tipo_Comodo.id,
            "descricao": tipo_Comodo.descricao,
        }
    return result

def apresenta_tipos_comodos(tipos_Comodo: List[Tipo_Comodo]):
    """ Retorna uma listagem da representação do tipo de cômodo.
    """
    result = []
    for tipo_comodo in tipos_Comodo:

        result.append(

            {
                "id": tipo_comodo[0].id,
                "descricao": tipo_comodo[0].descricao,
                "qtde": tipo_comodo[1],
            }
        )

    return {"tipos_comodos": result}
