from venv import logger
from pydantic import BaseModel
from typing import List
from model.imobiliaria import Imobiliaria


class ImobiliariaSchema(BaseModel):
    """ Define como uma nova imobiliária deve ser inserida
    """
    nome: str = "FANEL"
    razao_social: str = "FANEL IMOBILIARIA LTDA"
    cnpj: str = "43.945.104/0001-81"
    ie: str = ""
    endereco: str = "Rua Regente Leon Kaniefsky, 113"
    complemento: str = ""
    bairro: str = "VILA PROGREDIOR"
    cidade: str = "SAO PAULO"
    uf: str = "SP"
    cep: str = "05617-030"
    ddd: str = "11"
    telefone: str = "3742-6377"
    id_matriz: int = 0  # Se a imobiliária for a matriz


class ImobiliariaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
        Será feita apenas com base no id da imobiliária.
    """
    id: int = 0  # Id da imobiliária


class ImobiliariaViewSchema(BaseModel):
    """ Define como uma imobiliária será retornada.
    """
    id: int
    nome: str
    razao_social: str
    cnpj: str
    ie: str
    endereco: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: str
    ddd: str
    telefone: str
    id_matriz: int


class ListagemImobiliariasSchema(BaseModel):
    """ Define como uma listagem de imobiliárias será retornada seguindo o schema definido em
        ImobiliariaViewSchema.
    """
    imobiliaria: List[ImobiliariaViewSchema]


class ImobiliariaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    id: int
    nome: str
    razao_social: str
    cnpj: str
    ie: str


def apresenta_imobiliaria(imobiliaria: Imobiliaria, tipo:str ):
    """ Retorna uma representação da imobiliária.
    """

    if tipo=="P":
                 result = {
                "id": imobiliaria.id,
                "nome": imobiliaria.nome,
                "razao_social": imobiliaria.razao_social,
                "cnpj": imobiliaria.cnpj,
                "ie": imobiliaria.ie,
                "endereco": imobiliaria.endereco,
                "complemento": imobiliaria.complemento,
                "bairro": imobiliaria.bairro,
                "cidade": imobiliaria.cidade,
                "uf": imobiliaria.uf,
                "cep": imobiliaria.cep,
                "ddd": imobiliaria.ddd,
                "telefone": imobiliaria.telefone,
                "id_matriz": imobiliaria.id_matriz,
            }
    else:
        if imobiliaria[1]:
            result = {
                "id": imobiliaria.Imobiliaria.id,
                "nome": imobiliaria.Imobiliaria.nome,
                "razao_social": imobiliaria.Imobiliaria.razao_social,
                "cnpj": imobiliaria.Imobiliaria.cnpj,
                "ie": imobiliaria.Imobiliaria.ie,
                "endereco": imobiliaria.Imobiliaria.endereco,
                "complemento": imobiliaria.Imobiliaria.complemento,
                "bairro": imobiliaria.Imobiliaria.bairro,
                "cidade": imobiliaria.Imobiliaria.cidade,
                "uf": imobiliaria.Imobiliaria.uf,
                "cep": imobiliaria.Imobiliaria.cep,
                "ddd": imobiliaria.Imobiliaria.ddd,
                "telefone": imobiliaria.Imobiliaria.telefone,
                "matriz": imobiliaria[1].nome,
            }
        else:
            result = {
                "id": imobiliaria.Imobiliaria.id,
                "nome": imobiliaria.Imobiliaria.nome,
                "razao_social": imobiliaria.Imobiliaria.razao_social,
                "cnpj": imobiliaria.Imobiliaria.cnpj,
                "ie": imobiliaria.Imobiliaria.ie,
                "endereco": imobiliaria.Imobiliaria.endereco,
                "complemento": imobiliaria.Imobiliaria.complemento,
                "bairro": imobiliaria.Imobiliaria.bairro,
                "cidade": imobiliaria.Imobiliaria.cidade,
                "uf": imobiliaria.Imobiliaria.uf,
                "cep": imobiliaria.Imobiliaria.cep,
                "ddd": imobiliaria.Imobiliaria.ddd,
                "telefone": imobiliaria.Imobiliaria.telefone,
                "matriz": "",
            }

    return result


def apresenta_imobiliarias(imobiliarias: List[Imobiliaria]):
    """ Retorna uma listagem da representação da imobiliária.
    """
    result = []
    for imobiliaria in imobiliarias:
        
        if imobiliaria[1]:
            result.append(
                {
                    "id": imobiliaria.Imobiliaria.id,
                    "nome": imobiliaria.Imobiliaria.nome,
                    "razao_social": imobiliaria.Imobiliaria.razao_social,
                    "cnpj": imobiliaria.Imobiliaria.cnpj,
                    "ie": imobiliaria.Imobiliaria.ie,
                    "endereco": imobiliaria.Imobiliaria.endereco,
                    "complemento": imobiliaria.Imobiliaria.complemento,
                    "bairro": imobiliaria.Imobiliaria.bairro,
                    "cidade": imobiliaria.Imobiliaria.cidade,
                    "uf": imobiliaria.Imobiliaria.uf,
                    "cep": imobiliaria.Imobiliaria.cep,
                    "ddd": imobiliaria.Imobiliaria.ddd,
                    "telefone": imobiliaria.Imobiliaria.telefone,
                    "matriz": imobiliaria[1].nome,
                }
            )
        else:
            result.append(
                {
                    "id": imobiliaria.Imobiliaria.id,
                    "nome": imobiliaria.Imobiliaria.nome,
                    "razao_social": imobiliaria.Imobiliaria.razao_social,
                    "cnpj": imobiliaria.Imobiliaria.cnpj,
                    "ie": imobiliaria.Imobiliaria.ie,
                    "endereco": imobiliaria.Imobiliaria.endereco,
                    "complemento": imobiliaria.Imobiliaria.complemento,
                    "bairro": imobiliaria.Imobiliaria.bairro,
                    "cidade": imobiliaria.Imobiliaria.cidade,
                    "uf": imobiliaria.Imobiliaria.uf,
                    "cep": imobiliaria.Imobiliaria.cep,
                    "ddd": imobiliaria.Imobiliaria.ddd,
                    "telefone": imobiliaria.Imobiliaria.telefone,
                    "matriz": "",
                }
            )

    return {"imobiliarias": result}


def apresenta_imobiliarias_tot(imobiliarias: List[Imobiliaria]):
    """ Retorna uma listagem da representação da imobiliária.
    """
    result = []
    for imobiliaria in imobiliarias:

        result.append(
                {
                    "id": imobiliaria[0],
                    "nome": imobiliaria[1],
                    "razao_social": imobiliaria[2],
                    "cnpj": imobiliaria[3],
                    "ie": imobiliaria[4],
                    "endereco": imobiliaria[5],
                    "complemento": imobiliaria[6],
                    "bairro": imobiliaria[7],
                    "cidade": imobiliaria[8],
                    "uf": imobiliaria[9],
                    "cep": imobiliaria[10],
                    "ddd": imobiliaria[11],
                    "telefone": imobiliaria[12],
                    "matriz": imobiliaria[16],
                    "qtde_filhas":imobiliaria[30],
                    "qtde_filiais":imobiliaria[31],
                }
            )
    
    return {"imobiliarias": result}