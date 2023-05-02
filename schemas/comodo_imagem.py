from venv import logger
from flask import jsonify
from pydantic import BaseModel
from typing import List

from sqlalchemy import BLOB
from model.comodo_imagem import Comodo_Imagem


class Comodo_ImagemSchema(BaseModel):
    """ Define como uma nova imagem do cômodo deve ser inserida
    """
    id_comodo: int = 0  # Código do tipo do cômodo
    nome_imagem: str  # imagem do cômodo
    descricao: str  # descrição do cômodo


class Comodo_ImagemBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
        Será feita apenas com base no id da imagem da cômodo.
    """
    id: int = 0  # Id da imagem do cômodo

class Comodo_ImagemByComodoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
        Será feita apenas com base no id da imagem da cômodo.
    """
    id_comodo: int = 0  # Id da imagem do cômodo

class Comodo_ImagemViewSchema(BaseModel):
    """ Define como uma imagem da cômodo será retornada.
    """
    id: int
    comodo: str
    nome_imagem: str
    descricao: str


class ListagemComodos_ImagemSchema(BaseModel):
    """ Define como uma listagem da imagem da cômodo será retornada seguindo o schema definido em
        Comodo_ImagemViewSchema.
    """
    comodo_Imagem: List[Comodo_ImagemViewSchema]


class Comodo_ImagemDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int
    id_comodo: int
    nome_imagem: str
    descricao: str


def apresenta_comodo_imagem(comodo_imagem: Comodo_Imagem, imagem_id: int):
    """ Retorna uma representação da imagem da cômodo.
    """
    result = {}
    if imagem_id != 0:
        result = {
            "id": imagem_id,
            "comodo": comodo_imagem.id_comodo,
            "nome_imagem": comodo_imagem.nome_imagem,
            "descricao": comodo_imagem.descricao,
        }
    else:
        result = {
            "comodo": comodo_imagem.id_comodo,
            "nome_imagem": comodo_imagem.nome_imagem,
            "descricao": comodo_imagem.descricao,
        }

    return result


def apresenta_comodos_imagems(comodos_imagem: List[Comodo_Imagem]):
    """ Retorna uma listagem da representação da imagem da cômodo.
    """

    result = []
    for comodo_imagem in comodos_imagem:
        result.append(
            {
                "id": comodo_imagem["id"],
                "comodo": comodo_imagem["comodo"],
                "nome_imagem": comodo_imagem["nome_imagem"],
                "descricao": comodo_imagem["descricao"],
            }
        )

    return {"imagens": result}
