from datetime import datetime

from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect, request, send_file
from urllib.parse import unquote
from sqlalchemy import func, select
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError


# from sqlalchemy.sql import alias
from model import Session
from logger import logger
from model.tipo_imovel import Tipo_Imovel
from schemas import *
from flask_cors import CORS
from werkzeug.utils import secure_filename
from termcolor import colored

import os.path as path
import model
import sqlite3


info = Info(title="Realtors", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
app.debug = True

# tratamento da pasta para upload
upload_folder = path.join('images', 'uploads')
app.config['UPLOAD'] = upload_folder


# request.json = True
""" import os

appdev = Flask(__name__)
IS_DEV = appdev.env == 'development'  # FLASK_ENV env. variable


##if __name__ == '__main__':
# guaranteed to not be run on a production server
assert os.path.exists('.env')  # for other environment variables...
os.environ['FLASK_ENV'] = 'development'  # HARD CODE since default is production
appdev.run(debug=True) """

# definindo tags

home_tag = Tag(name="Realtors",
               description="Documentação da APi do Realtors")

imagem_tag = Tag(name="Imagens",
                      description="Adição, visualização e remoção da imagem de um cômodo à base")

comodo_tag = Tag(name="Cômodos", 
                      description="Adição, visualização e remoção de um cômodo à base")
imobiliaria_tag = Tag(
    name="Imobiliárias", description="Adição, visualização e remoção de uma imobiliária à base")

imovel_tag = Tag(
    name="Imóveis", description="Adição, visualização e remoção de um imóvel à base")

tipo_imovel_tag = Tag(name="Tipos de imóveis",
                      description="Adição, visualização e remoção de um tipo de imóvel à base")

tipo_comodo_tag = Tag(name="Tipos de cômodos",
                      description="Adição, visualização e remoção de um tipo de cômodo à base")


# atividade_tag = Tag(name="Ramos de Atividades",
#                     description="Adição, visualização e remoção de um ramo de atividade à base")
# fornecedor_tag = Tag(name="Fornecedores",
#                      description="Adição, visualização e remoção de um fornecedor à base")
# produto_tag = Tag(
#     name="Produtos", description="Adição, visualização e remoção de um produto à base")
# preco_tag = Tag(
#     name="Preços", description="Adição, visualização e remoção dos preços à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger, tela do swagger com a documentação do Realtors.
    """
    return redirect('/openapi/swagger')


##############################################################################################
# Tratamento dos imagens dos cômodos
##############################################################################################


@app.post('/imagem', tags=[imagem_tag],
          responses={"200": Comodo_ImagemViewSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def add_imagem():
    """Adiciona uma nova imagem do cômodo à base de dados.

    Retorna uma representação da imagem do cômodo.
    """

    logger.debug(
        colored(f"Adicionando a imagem do cômodo.", 'blue', attrs=['dark']))

    # criando conexão com a base
    sqliteConnection = sqlite3.connect(model.db_name)
    cursor = sqliteConnection.cursor()

    try:

        logger.debug(colored(
            f"Carregou a pasta '{upload_folder}' para upload.", 'blue', attrs=['dark']))

        # tratamento da imagem
        file = request.files['imagem']

        logger.debug(colored(
            f"Carregou a descrição '{file}'.", 'blue', attrs=['dark']))

        logger.debug(colored(
            f"Carregou o arquivo '{file}'.", 'blue', attrs=['dark']))

        filename = secure_filename(file.filename)

        logger.debug(colored(
            f"Carregou o filename '{filename}'.", 'blue', attrs=['dark']))

        file.save(path.join(app.config['UPLOAD'], filename))

        logger.debug(colored(
            f"Salvou o aquivo .", 'blue', attrs=['dark']))

        imagem = path.join(app.config['UPLOAD'], filename)

        logger.debug(
            colored(f"Adicionando a imagem : '{imagem}'", 'blue', attrs=['dark']))

        # carga dos demais campos
        id_comodo = request.form['id_comodo']

        logger.debug(colored(
            f"Carregou o comodo '{id_comodo}'.", 'blue', attrs=['dark']))

        descricao = request.form['descricao']

        logger.debug(colored(
            f"Carregou a descrição '{descricao}'.", 'blue', attrs=['dark']))

        # Convertendo a imagem para o formato binário(BLOB)
        imagemBLOB = convertToBinaryData(imagem)

        comodo_imagem = Comodo_Imagem(
            id_comodo=id_comodo,
            imagem=imagemBLOB,
            nome_imagem=imagem,
            descricao=descricao)

        # Convertendo os dados no formato de tuple
        data_tuple = (id_comodo, imagemBLOB, imagem,
                      descricao,  datetime.now())

        sqlite_insert_blob_query = """ INSERT INTO comodo_imagem
                                        (id_comodo,imagem,nome_imagem,descricao,data_insercao) 
                                        VALUES ( ?, ? ,? , ?, ?)
                                    """

        # adicionando a imagem
        cursor.execute(sqlite_insert_blob_query, data_tuple)

        # efetivando o camando de adição da imagem
        sqliteConnection.commit()

    except IntegrityError as e:
        # como a duplicidade do id_imovel e do id_tipo_comodo é a provável razão do IntegrityError
        error_msg = "Imagem já salva na base :/"
        logger.warning(colored(
            f"Erro ao adicionar a imagem : '{filename}', {error_msg}", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível salvar nova imagem :/"
        logger.warning(colored(
            f"Erro ao adicionar a imagem ", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400

    finally:

        cursor.close()

        logger.debug(
            colored(f"Adicionado a imagem : '{imagem}'", 'green', attrs=['bold']))
        return apresenta_comodo_imagem(comodo_imagem, 0), 200


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


@app.get('/retornar_imagem', tags=[imagem_tag],
         responses={"200": Comodo_ImagemViewSchema, "404": ErrorSchema})
def retornar_imagem(query: Comodo_ImagemBuscaSchema):
    """Faz a busca pela imagem do cômodo a partir do id da imagem.

    Retorna uma representação da imagem do cômodo.
    """
    imagem_id: int = int(query.id)

    # criando conexão com a base
    sqliteConnection = sqlite3.connect(model.db_name)
    cursor = sqliteConnection.cursor()

    try:

        logger.debug(
            colored(f"Coletando dados sobre a imagem do cômodo de id# {imagem_id}", 'blue', attrs=['dark']))

        cursor.execute(
            'SELECT nome_imagem FROM comodo_imagem WHERE pk_comodo_imagem = ?', (imagem_id,))
        imagem_bytes = cursor.fetchone()[0]

        logger.debug(
            colored(f"Enviando a imagem do cômodo de id # {imagem_id}", 'green', attrs=['bold']))

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível retornar a imagem :/"
        logger.warning(colored(
            f"Erro ao retornar a imagem ", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400

    finally:

        cursor.close()
        return send_file(imagem_bytes, mimetype='image/jpeg'), 200


# @app.get('/imagem', tags=[imagem_tag],
#          responses={"200": Comodo_ImagemViewSchema, "404": ErrorSchema})
# def get_imagem(query: Comodo_ImagemBuscaSchema):
#     """Faz a busca pela imagem do cômodo a partir do id da imagem.

#     Retorna uma representação da imagem do cômodo.
#     """
#     imagem_id: int = int(query.id)

#     logger.debug(
#         colored(f"Coletando dados sobre a imagem do cômodo", 'blue', attrs=['dark']))

#     # criando conexão com a base
#     sqliteConnection = sqlite3.connect(model.db_name)
#     cursor = sqliteConnection.cursor()

#     try:
#         sql_fetch_blob_query = """SELECT  comodo_imagem.pk_comodo_imagem as Id,
#                                             comodo.nome as comodo,
#                                             comodo_imagem.imagem,
#                                             comodo_imagem.nome_imagem,
#                                             comodo_imagem.descricao
#                                     from comodo_imagem 
#                                     inner join comodo on comodo_imagem.id_comodo = comodo.pk_comodo
#                                     where pk_comodo_imagem = ?"""
#         cursor.execute(sql_fetch_blob_query, (imagem_id,))

#         record = cursor.fetchall()

#     except Exception as e:
#         # caso um erro fora do previsto ocorra
#         error_msg = "Não foi possível retornar a imagem :/"
#         logger.warning(colored(
#             f"Erro ao retornar a imagem ", 'red', attrs=['bold']))
#         return {"mensagem": error_msg}, 400

#     finally:

#         cursor.close()

#         if record:

#             record[0][1]
#             comodo_imagem = Comodo_Imagem(
#                 id_comodo=record[0][1],
#                 imagem=record[0][2],
#                 nome_imagem=record[0][3],
#                 descricao=record[0][4]
#             )

#             logger.debug(
#                 colored(f"Imagem do cômodo encontrada : '{comodo_imagem.nome_imagem}'", 'green', attrs=['bold']))
#             # retorna a representação do cômodo
#             return apresenta_comodo_imagem(comodo_imagem, imagem_id), 200

#         else:

#             # se o cômodo não foi encontrado
#             error_msg = "Imagem do cômodo não encontrada na base :/"
#             logger.warning(colored(
#                 f"Erro ao buscar a imagem do cômodo de id #'{imagem_id}'. {error_msg}", 'red', attrs=['bold']))
#             return {"mensagem": error_msg}, 404


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


@app.get('/imagens', tags=[imagem_tag],
         responses={"200": ListagemComodos_ImagemSchema, "404": ErrorSchema})
def get_imagens():
    """Faz a busca por todas as imagens dos cômodos cadastradas.

    Retorna uma listagem da representação das imagens dos cômodos.
    """
    logger.debug(colored(f"Coletando imagens", 'blue', attrs=['dark']))
    # # criando conexão com a base
    # session = Session()
    # # fazendo a busca
    # imagens = session.query(Comodo_Imagem).all()

    sqliteConnection = sqlite3.connect(model.db_name)
    cursor = sqliteConnection.cursor()

    # comodo_imagem :Comodo_Imagem
    try:

        sql_fetch_blob_query = """  SELECT  comodo_imagem.pk_comodo_imagem as Id,
                                            comodo.nome as comodo,
                                            comodo_imagem.imagem,
                                            comodo_imagem.nome_imagem,
                                            comodo_imagem.descricao
                                    from comodo_imagem 
                                    inner join comodo on comodo_imagem.id_comodo = comodo.pk_comodo """
        cursor.execute(sql_fetch_blob_query, ())
        imagens = cursor.fetchall()

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível retornar a imagem :/"
        logger.warning(colored(
            f"Erro ao retornar a imagem ", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400

    finally:

        cursor.close()

        if imagens:

            imagens_adicionadas: Comodo_Imagem = []

            for form in imagens:

                imagem_adicionada: Comodo_Imagem = {}

                imagem_adicionada["id"] = form[0]
                imagem_adicionada["comodo"] = form[1]
                imagem_adicionada["imagem"] = form[2]
                imagem_adicionada["nome_imagem"] = form[3]
                imagem_adicionada["descricao"] = form[4]

                imagens_adicionadas.append(imagem_adicionada)

            logger.debug(colored(f"%d imagens encontradas" %
                                 len(imagens_adicionadas), 'green', attrs=['bold']))
            # retorna a representação do cômodo
            # print(comodos)
            return apresenta_comodos_imagems(imagens_adicionadas), 200

        else:
            # se não há comodos cadastrados
            return {"imagens": []}, 200


@app.get('/imagensByComodo', tags=[imagem_tag],
         responses={"200": ListagemComodos_ImagemSchema, "404": ErrorSchema})
def get_imagensByComodo(query: Comodo_ImagemByComodoBuscaSchema):
    """Faz a busca por todas as imagens pelo id do cômodo.

    Retorna uma listagem da representação das imagens dos cômodos.
    """
    comodo_id = query.id_comodo

    logger.debug(colored(f"Coletando imagens", 'blue', attrs=['dark']))
    # # criando conexão com a base
    # session = Session()
    # # fazendo a busca
    # imagens = session.query(Comodo_Imagem).all()

    sqliteConnection = sqlite3.connect(model.db_name)
    cursor = sqliteConnection.cursor()

    try:

        sql_fetch_blob_query = """  SELECT  comodo_imagem.pk_comodo_imagem as Id,
                                            comodo.nome as comodo,
                                            comodo_imagem.imagem,
                                            comodo_imagem.nome_imagem,
                                            comodo_imagem.descricao
                                    from comodo_imagem 
                                    inner join comodo on comodo_imagem.id_comodo = comodo.pk_comodo
                                    where  comodo_imagem.id_comodo = ?"""
        cursor.execute(sql_fetch_blob_query, (comodo_id,))
        imagens = cursor.fetchall()

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível retornar a imagem :/"
        logger.warning(colored(
            f"Erro ao retornar a imagem ", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400

    finally:

        cursor.close()

        if imagens:

            imagens_adicionadas: Comodo_Imagem = []

            for form in imagens:

                imagem_adicionada: Comodo_Imagem = {}

                imagem_adicionada["id"] = form[0]
                imagem_adicionada["comodo"] = form[1]
                imagem_adicionada["imagem"] = form[2]
                imagem_adicionada["nome_imagem"] = form[3]
                imagem_adicionada["descricao"] = form[4]

                imagens_adicionadas.append(imagem_adicionada)

            logger.debug(colored(f"%d imagens encontradas" %
                                 len(imagens_adicionadas), 'green', attrs=['bold']))
            # retorna a representação do cômodo
            # print(comodos)
            return apresenta_comodos_imagems(imagens_adicionadas), 200

        else:
            # se não há comodos cadastrados
            return {"imagens": []}, 200


@app.delete('/imagem', tags=[imagem_tag],
            responses={"200": Comodo_ImagemDelSchema, "404": ErrorSchema})
def del_imagem(query: Comodo_ImagemBuscaSchema):
    """Deleta uma imagem do cômodo a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    _imagem = query.id

    logger.debug(
        colored(f"Deletando dados da imagem do cômodo de id #{_imagem}", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    # imagem: Comodo = session.query(Comodo_Imagem).filter(
    #     Comodo_Imagem.id == _imagem).count()

    imagem = session.query(Comodo_Imagem).filter(
        Comodo_Imagem.id == _imagem).count()

    if imagem:

        # criando conexão com a base
        sqliteConnection = sqlite3.connect(model.db_name)
        cursor = sqliteConnection.cursor()

        try:

            # Deleting single record now
            sql_delete_query = """DELETE from comodo_imagem where pk_comodo_imagem = ?"""
            count = cursor.execute(sql_delete_query, (_imagem,))
            sqliteConnection.commit()

        except Exception as e:
            # caso um erro fora do previsto ocorra
            error_msg = "Não foi possível apagar a imagem :/"
            logger.warning(colored(
                f"Erro ao apagar a imagem ", 'red', attrs=['bold']))
            return {"mensagem": error_msg}, 400

        finally:

            cursor.close()

            if count:

                # retorna a representação da mensagem de confirmação
                logger.debug(
                    colored(f"Deletada imagem do cômodo de id #{_imagem}", 'green', attrs=['bold']))

                return {
                    "mensagem": "Imagem do cômodo removida",
                    "id": _imagem,
                }
            else:

                # avisa se der erro ao deletar o cômodo
                error_msg = "Erro ao deletar a imagem do cômodo :/"
                logger.warning(colored(
                    f"Erro ao deletar a imagem do cômodo de id #'{_imagem}'", 'red', attrs=['bold']))
                return {"mensagem": error_msg}, 404

    else:
        # se o cômodo não foi encontrado
        error_msg = "Imagem do cômodo não encontrada na base :/"
        logger.warning(colored(
            f"Imagem do cômodo não encontrada na base", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404


##############################################################################################
# Tratamento do cômodo
##############################################################################################


@app.post('/comodo', tags=[comodo_tag],
          responses={"200": ComodoViewSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def add_comodo(form: ComodoSchema):
    """Adiciona um novo cômodo à base de dados.

    Retorna uma representação do cômodo.
    """
    _comodo = form.nome.strip()
    comodo = Comodo(
        id_imovel=form.id_imovel,
        id_tipo_comodo=form.id_tipo_comodo,
        nome=form.nome.upper(),
        quantidade=form.quantidade,
        descricao=form.descricao)

    logger.debug(
        colored(f"Adicionando o cômodo de nome: '{_comodo}'", 'blue', attrs=['dark']))

    try:

        # criando conexão com a base
        session = Session()
        # adicionando comodo
        session.add(comodo)

        # efetivando o camando de adição de novo item na tabela
        session.commit()
        comodo_id = comodo.id

        comodo = session.execute(select(Comodo, Imovel, Tipo_Comodo).join(Imovel).join(Tipo_Comodo).filter(
            Comodo.id == comodo_id)).first()

        logger.debug(
            colored(f"Adicionado o cômodo de nome: '{_comodo}'", 'green', attrs=['bold']))
        return apresenta_comodo(comodo, "G"), 200

    except IntegrityError as e:
        # como a duplicidade do id_imovel e do id_tipo_comodo é a provável razão do IntegrityError
        error_msg = "Cômodo de mesmo id_imovel e  id_tipo_comodo já salvo na base :/"
        logger.warning(colored(
            f"Erro ao adicionar o cômodo '{_comodo}', {error_msg}", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(colored(
            f"Erro ao adicionar o cômodo '{_comodo}'", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400


@app.get('/comodo', tags=[comodo_tag],
         responses={"200": ComodoViewSchema, "404": ErrorSchema})
def get_comodo(query: ComodoBuscaSchema):
    """Faz a busca por um cômodo a partir do id do cômodo.

    Retorna uma representação do cômodo.
    """
    comodo_id: str = query.id

    logger.debug(
        colored(f"Coletando dados sobre o cômodo", 'blue', attrs=['dark']))
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    comodo = session.execute(select(Comodo, Imovel, Tipo_Comodo).join(Imovel).join(Tipo_Comodo).filter(
        Comodo.id == comodo_id)).first()

    if not comodo:
        # se o cômodo não foi encontrado
        error_msg = "Cômodo não encontrado na base :/"
        logger.warning(colored(
            f"Erro ao buscar cômodo de id #'{comodo_id}', {error_msg}", 'blue', attrs=['dark']))
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(
            colored(f"Cômodo encontrado: '{comodo.Comodo.nome}'", 'green', attrs=['bold']))
        # retorna a representação do cômodo
        return apresenta_comodo(comodo, "G"), 200


@app.get('/comodos', tags=[comodo_tag],
         responses={"200": ListagemComodosSchema, "404": ErrorSchema})
def get_comodos():
    """Faz a busca por todos os cômodos cadastrados.

    Retorna uma listagem da representação dos cômodos.
    """
    logger.debug(colored(f"Coletando cômodos", 'blue', attrs=['dark']))
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    # comodos = session.query(Comodo).all()

    comodos = session.execute(
        select(Comodo, Imovel, Tipo_Comodo).join(Imovel).join(Tipo_Comodo))

    if not comodos:
        # se não há comodos cadastrados
        return {"Cômodos": []}, 200
    else:
        logger.debug(colored(f"Cômodos encontrados", 'green', attrs=['bold']))
        # retorna a representação do cômodo
        # print(comodos)
        return apresenta_comodos(comodos), 200


@app.get('/comodosByImovel', tags=[comodo_tag],
         responses={"200": ListagemComodosSchema, "404": ErrorSchema})
def get_comodosByimovel(query: ComodoBuscaByImovelSchema):
    """Faz a busca por todos os cômodos pelo id imóvel.

    Retorna uma listagem da representação dos cômodos.
    """

    id_imovel: str = query.id_imovel

    logger.debug(
        colored(f"Coletando cômodos", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    # fazendo a busca

    # Faz a contagem de imagens por cômodos
    stmt = select(
        Comodo_Imagem.id_comodo, func.count('*').label('id_comodo_count')
    ).group_by(Comodo_Imagem.id_comodo).subquery()

    smtp0 = select(Comodo, Imovel, Tipo_Comodo).join(Imovel).join(
        Tipo_Comodo).filter(Comodo.id_imovel == id_imovel).subquery()

    # Join entre cursor dos imoveis e a contagem de comodos
    comodos = session.query(smtp0, stmt.c.id_comodo_count).outerjoin(
        stmt, smtp0.c.pk_comodo == stmt.c.id_comodo).order_by(smtp0.c.pk_comodo)

    count: int = 0

    for u in comodos:
        count = count+1

    if not comodos:
        # se não há comodos cadastrados
        return {"comodos": []}, 200
    else:
        logger.debug(colored(f"%d cômodos encontrados" %
                     count, 'green', attrs=['bold']))
        # retorna a representação do cômodo
        # print(comodos)
        return apresenta_comodos_tot(comodos), 200


@app.delete('/comodo', tags=[comodo_tag],
            responses={"200": ComodoDelSchema, "404": ErrorSchema})
def del_comodo(query: ComodoBuscaSchema):
    """Deleta um cômodo a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    _comodo = query.id

    logger.debug(
        colored(f"Deletando dados do cômodo de id #{_comodo}", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    comodo: Comodo = session.query(Comodo).filter(Comodo.id == _comodo).first()

    if comodo:

        # print(str(comodo_id))
        # fazendo a remoção
        count = session.query(Comodo).filter(
            Comodo.id == _comodo).delete()
        session.commit()

        if count:

            # retorna a representação da mensagem de confirmação
            logger.debug(
                colored(f"Deletado o cômodo de id #{_comodo}", 'green', attrs=['bold']))

            return {
                "mensagem": "Cômodo removido",
                "id": _comodo,
                "id_imovel": comodo.id_imovel,
                "id_tipo_comodo": comodo.id_tipo_comodo,
                "nome": comodo.nome,
            }
        else:

            # avisa se der erro ao deletar o cômodo
            error_msg = "Erro ao deletar cômodo :/"
            logger.warning(colored(
                f"Erro ao deletar o cômodo de id #'{_comodo}'", 'red', attrs=['bold']))
            return {"mensagem": error_msg}, 404

    else:
        # se o cômodo não foi encontrado
        error_msg = "Cômodo não encontrado na base :/"
        logger.warning(colored(
            f"Cômodo não encontrado na base", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404


##############################################################################################
# Tratamento do imóvel
##############################################################################################


@app.post('/imovel', tags=[imovel_tag],
          responses={"200": ImovelViewSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def add_imovel(form: ImovelSchema):
    """Adiciona um novo imóvel à base de dados.

    Retorna uma representação do imóvel.
    """
    _imovel = form.nome.strip()
    imovel = Imovel(
        nome=form.nome.upper(),
        endereco=form.endereco.upper(),
        complemento=form.complemento,
        bairro=form.bairro,
        cidade=form.cidade,
        uf=form.uf,
        cep=form.cep,
        ddd=form.ddd,
        telefone=form.telefone,
        descricao=form.descricao,
        id_tipo_imovel=form.id_tipo_imovel,
        id_imobiliaria=form.id_imobiliaria
    )

    logger.debug(colored(
        f"Adicionando o imóvel de nome: '{_imovel}'", 'blue', attrs=['dark']))

    try:

        # criando conexão com a base
        session = Session()
        # adicionando imovel
        session.add(imovel)

        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(colored(
            f"Adicionado o imóvel de nome: '{_imovel}'", 'green', attrs=['bold']))
        return apresenta_imovel(imovel, "P"), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Imovel de mesmo nome ja salvo na base :/"
        logger.warning(colored(
            f"Erro ao adicionar o imóvel '{_imovel}', {error_msg}", 'red', attrs=['bold']))
        # return {"mensagem": error_msg}, 409
        return error_msg, 409

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(colored(
            f"Erro ao adicionar o imóvel '{_imovel}'. {e}", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400


@app.get('/imovel', tags=[imovel_tag],
         responses={"200": ImovelViewSchema, "404": ErrorSchema})
def get_imovel(query: ImovelBuscaSchema):
    """Faz a busca por um imóvel a partir do id do imóvel,

    Retorna uma representação do imóvel.
    """
    imovel_id: str = query.id

    logger.debug(
        colored(f"Coletando dados sobre o imóvel", 'blue', attrs=['dark']))
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    # imovel = session.query(Imovel).filter(Imovel.id == imovel_id).first()
    imovel = session.execute(
        select(Imovel, Tipo_Imovel, Imobiliaria).join(Tipo_Imovel).join(Imobiliaria).filter(
            Imovel.id == imovel_id)).first()

    if not imovel:
        # se o imóvel não foi encontrado
        error_msg = "Imóvel não encontrado na base :/"
        logger.warning(colored(
            f"Erro ao buscar imóvel de id #'{imovel_id}', '{error_msg}'", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(
            colored(f"Imóvel encontrado: '{imovel.Imovel.nome}'", 'green', attrs=['bold']))
        # retorna a representação do imóvel
        return apresenta_imovel(imovel, "G"), 200


@app.get('/imoveis', tags=[imovel_tag],
         responses={"200": ListagemImoveisSchema, "404": ErrorSchema})
def get_imoveis():
    """Faz a busca por todos os imóveis cadastrados.

    Retorna uma listagem da representação dos imóveis.
    """
    logger.debug(
        colored(f"Coletando imóveis", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()

    # Faz a contagem de cômodos por imóveis
    stmt = select(
        Comodo.id_imovel, func.count('*').label('id_imovel_count')
    ).group_by(Comodo.id_imovel).subquery()

    smtp0 = select(Imovel, Tipo_Imovel, Imobiliaria).join(
        Tipo_Imovel).join(Imobiliaria).subquery()

    # Join entre cursor dos imoveis e a contagem de comodos
    imoveis = session.query(smtp0, stmt.c.id_imovel_count).outerjoin(
        stmt, smtp0.c.pk_imovel == stmt.c.id_imovel).order_by(smtp0.c.pk_imovel)

    count: int = 0

    for u in imoveis:
        count = count+1

    if not imoveis:
        # se não há unidades cadastrados
        return {"imoveis": []}, 200
    else:

        logger.debug(colored(f"%d imóveis encontrados" %
                     count, 'green', attrs=['bold']))
        # retorna a representação da imobiliária
        return apresenta_imoveis_tot(imoveis), 200


@app.get('/imoveisByImobiliaria', tags=[imovel_tag],
         responses={"200": ListagemImoveisSchema, "404": ErrorSchema})
def get_imoveisByImobiliaria(query: ImovelBuscaByImobiliariaSchema):
    """Faz a busca por todos os imóveis pelo id da imobiliária.

    Retorna uma listagem da representação dos imóveis.
    """

    id_imobiliaria: str = query.id_imobiliaria

    logger.debug(
        colored(f"Coletando imóveis", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    # imoveis = session.execute(
    #      select(Imovel, Tipo_Imovel, Imobiliaria).join(Tipo_Imovel).join(Imobiliaria).filter(Imovel.id_imobiliaria == id_imobiliaria))

    # Faz a contagem de cômodos por imóveis
    stmt = select(
        Comodo.id_imovel, func.count('*').label('id_imovel_count')
    ).group_by(Comodo.id_imovel).subquery()

    smtp0 = select(Imovel, Tipo_Imovel, Imobiliaria).join(Tipo_Imovel).join(
        Imobiliaria).filter(Imovel.id_imobiliaria == id_imobiliaria).subquery()

    # Join entre cursor dos imoveis e a contagem de comodos
    imoveis = session.query(smtp0, stmt.c.id_imovel_count).outerjoin(
        stmt, smtp0.c.pk_imovel == stmt.c.id_imovel).order_by(smtp0.c.pk_imovel)

    count: int = 0

    for u in imoveis:
        count = count+1

    if not imoveis:
        # se não há unidades cadastrados
        return {"imoveis": []}, 200
    else:

        logger.debug(colored(f"%d imóveis encontrados" %
                     count, 'green', attrs=['bold']))
        # retorna a representação da imobiliária
        return apresenta_imoveis_tot(imoveis), 200


@app.delete('/imovel', tags=[imovel_tag],
            responses={"200": ImovelDelSchema, "404": ErrorSchema})
def del_imovel(query: ImovelBuscaSchema):
    """Deleta um imóvel a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    _imovel = query.id

    logger.debug(colored(
        f"Deletando dados do imóvel de id #{_imovel}", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    imovel: Imovel = session.query(Imovel).filter(
        Imovel.id == _imovel).first()

    if imovel:

        # print(str(imovel_id))
        # fazendo a remoção
        count = session.query(Imovel).filter(
            Imovel.id == _imovel).delete()
        session.commit()

        if count:

            # retorna a representação da mensagem de confirmação
            logger.debug(
                colored(f"Deletado o imóvel de id #{_imovel}", 'green', attrs=['bold']))

            return {
                "mensagem": "Imóvel removido",
                "id": _imovel,
                "nome": imovel.nome,
                "endereco": imovel.endereco
            }
        else:

            # avisa se der erro ao deletar o imóvel
            error_msg = "Erro ao deletar o imóvel :/"
            logger.warning(
                colored(f"Erro ao deletar o imóvel #'{_imovel}'", 'red', attrs=['bold']))
            return {"mensagem": error_msg}, 404

    else:
        # se o imóvel não foi encontrado
        error_msg = "Imóvel não encontrado na base :/"
        logger.warning(
            colored(f"Imóvel não encontrado na base", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404


##############################################################################################
# Tratamento da imobiliária
##############################################################################################


@app.post('/imobiliaria', tags=[imobiliaria_tag],
          responses={"200": ImobiliariaViewSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def add_imobiliaria(form: ImobiliariaSchema):
    """Adiciona uma nova imobiliária à base de dados.

    Retorna uma representação da imobiliária.
    """
    _imobiliaria = form.nome.strip()
    imobiliaria = Imobiliaria(
        nome=form.nome.upper(),
        razao_social=form.razao_social.upper(),
        cnpj=form.cnpj,
        ie=form.ie,
        endereco=form.endereco,
        complemento=form.complemento,
        bairro=form.bairro,
        cidade=form.cidade,
        uf=form.uf,
        cep=form.cep,
        ddd=form.ddd,
        telefone=form.telefone,
        id_matriz=form.id_matriz)

    logger.debug(colored(
        f"Adicionando a imobiliária de nome: '{_imobiliaria}', Id_matriz {form.id_matriz}", 'blue', attrs=['dark']))

    try:

        # criando conexão com a base
        session = Session()
        # adicionando imobiliaria
        session.add(imobiliaria)

        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(colored(
            f"Adicionada a imobiliária de nome: '{_imobiliaria}'", 'green', attrs=['bold']))
        return apresenta_imobiliaria(imobiliaria, "P"), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Imobiliária de mesmo nome já salva na base :/"
        logger.warning(colored(
            f"Erro ao adicionar a imobiliária '{_imobiliaria}'. '{error_msg}'", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(colored(
            f"Erro ao adicionar a imobiliária '{_imobiliaria}'. {e}", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400


@app.get('/imobiliaria', tags=[imobiliaria_tag],
         responses={"200": ImobiliariaViewSchema, "404": ErrorSchema})
def get_imobiliaria(query: ImobiliariaBuscaSchema):
    """Faz a busca por uma imobiliária a partir do id informado.

    Retorna uma representação da imobiliária.
    """
    imobiliaria_id: str = query.id

    logger.debug(
        colored(f"Coletando dados sobre a imobiliária", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    # fazendo a busca

    Matriz = aliased(Imobiliaria)
    sele = select(Imobiliaria, Matriz).join(
        Matriz, Matriz.id == Imobiliaria.id_matriz, isouter=True).filter(
        Imobiliaria.id == imobiliaria_id)

    imobiliaria = session.execute(sele).first()

    # imobiliaria = session.query(Imobiliaria).filter(
    #     Imobiliaria.id == imobiliaria_id).first()

    if not imobiliaria:
        # se o imobiliária não foi encontrado
        error_msg = "Imobiliária não encontrada na base :/"
        logger.warning(colored(
            f"Erro ao buscar imobiliária de id #'{imobiliaria_id}', '{error_msg}'", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(colored(
            f"Imobiliária encontrada: '{imobiliaria.Imobiliaria.nome}'", 'green', attrs=['bold']))
        # retorna a representação do imobiliária
        return apresenta_imobiliaria(imobiliaria, "G"), 200


@app.get('/imobiliarias', tags=[imobiliaria_tag],
         responses={"200": ListagemImobiliariasSchema, "404": ErrorSchema})
def get_imobiliarias():
    """Faz a busca por todas os imobiliárias cadastradas.

    Retorna uma listagem da representação das imobiliárias.
    """
    logger.debug(
        colored(f"Coletando imobiliárias", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()

    # Cria um alias para as imobiliarias que são matriz
    Matriz = aliased(Imobiliaria)

    # O cursor com left join entre a imobiliaria e a matriz
    stmt0 = session.query(Imobiliaria, Matriz).join(
        Matriz, Matriz.id == Imobiliaria.id_matriz, isouter=True).subquery()

    # Faz a contagem de filiais por imobiliaria
    stmtf = session.query(
        Matriz.id_matriz, func.count('*').label('id_matriz_count')
    ).group_by(Matriz.id_matriz).where(Matriz.id_matriz != 0).subquery()

    # Faz a contagem de imóveis por imobiliaria
    stmt = session.query(
        Imovel.id_imobiliaria, func.count('*').label('id_imobiliaria_count')
    ).group_by(Imovel.id_imobiliaria).subquery()

    # Join entre cursor das imobiliarias, contagem de imóveis e contagem de filiais
    imobiliarias = session.query(stmt0,
                                 stmt.c.id_imobiliaria_count,
                                 stmtf.c.id_matriz_count
                                 ).outerjoin(
        stmt, stmt0.c.pk_imobiliaria == stmt.c.id_imobiliaria
    ).outerjoin(
        stmtf, stmt0.c.pk_imobiliaria == stmtf.c.id_matriz
    ).order_by(stmt0.c.pk_imobiliaria)

    count: int = 0

    for u in imobiliarias:
        count = count+1

    if not imobiliarias:
        # se não há unidades cadastrados
        return {"Imobiliárias": []}, 200
    else:
        logger.debug(colored(f"%d imobiliárias encontradas" %
                             count, 'green', attrs=['bold']))

        # retorna a representação da imobiliária
        # print(imobiliarias)
        return apresenta_imobiliarias_tot(imobiliarias), 200
        # return apresenta_imobiliarias(imobiliarias), 200


@app.delete('/imobiliaria', tags=[imobiliaria_tag],
            responses={"200": ImobiliariaDelSchema, "404": ErrorSchema})
def del_imobiliaria(query: ImobiliariaBuscaSchema):
    """Deleta uma imobiliária a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    _imobiliaria = query.id

    logger.debug(colored(
        f"Deletando dados da imobiliária de id #{_imobiliaria}", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    imobiliaria: Imobiliaria = session.query(Imobiliaria).filter(
        Imobiliaria.id == _imobiliaria).first()

    if imobiliaria:

        # print(str(imovel_id))
        # fazendo a remoção
        count = session.query(Imobiliaria).filter(
            Imobiliaria.id == _imobiliaria).delete()
        session.commit()

        if count:

            # retorna a representação da mensagem de confirmação
            logger.debug(
                colored(f"Deletado a imobiliária de id #{_imobiliaria}", 'blue', attrs=['dark']))

            # se o(s) comentário(s) não foi(ram) encontrado(s)
            return {
                "mensagem": "Imobiliária removida",
                "id": _imobiliaria,
                "nome": imobiliaria.nome,
                "razao_social": imobiliaria.razao_social,
                "cnpj": imobiliaria.cnpj,
                "ie": imobiliaria.ie
            }
        else:

            # avisa se der erro ao deletar a imobiliária
            error_msg = "Erro ao deletar a imobiliária :/"
            logger.warning(
                colored(f"Erro ao deletar a imobiliária #'{_imobiliaria}'", 'red', attrs=['bold']))
            return {"mensagem": error_msg}, 404

    else:
        # se a imobiliária não foi encontrada
        error_msg = "Imobiliária não encontrada na base :/"
        logger.warning(
            colored(f"Imobiliária não encontrada na base", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404


##############################################################################################
# Tratamento do tipo de imóvel
##############################################################################################


@app.post('/tipo_imovel', tags=[tipo_imovel_tag],
          responses={"200": Tipo_ImovelViewSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def add_tipo_imovel(form: Tipo_ImovelSchema):
    """Adiciona um novo tipo de imóvel à base de dados.

    Retorna uma representação do tipo de imóvel.
    """
    _imovel = form.descricao.strip()
    imovel = Tipo_Imovel(descricao=form.descricao.upper())

    logger.debug(colored(
        f"Adicionando o tipo de imóvel de descrição: '{_imovel}'", 'blue', attrs=['dark']))

    try:

        # criando conexão com a base
        session = Session()
        # adicionando o tipo de imóvel
        session.add(imovel)

        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(colored(
            f"Adicionado o tipo de imóvel de descrição: '{_imovel}'", 'green', attrs=['bold']))
        return apresenta_tipo_imovel(imovel), 200

    except IntegrityError as e:
        # como a duplicidade da descrição é a provável razão do IntegrityError
        error_msg = "Tipo de imóvel de mesma descrição já salvo na base :/"
        logger.warning(colored(
            f"Erro ao adicionar o tipo de imóvel '{_imovel}'. '{error_msg}'", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(colored(
            f"Erro ao adicionar o tipo de imóvel '{_imovel}'. {e}", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400


@app.get('/tipo_imovel', tags=[tipo_imovel_tag],
         responses={"200": Tipo_ImovelViewSchema, "404": ErrorSchema})
def get_tipo_imovel(query: Tipo_ImovelBuscaSchema):
    """Faz a busca por um tipo de imóvel a partir do id informado.

    Retorna uma representação do tipo de imóvel.
    """
    tipo_imovel_id: str = query.id

    logger.debug(
        colored(f"Coletando dados sobre o tipo de imóvel", 'blue', attrs=['dark']))
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    imovel = session.query(Tipo_Imovel).filter(
        Tipo_Imovel.id == tipo_imovel_id).first()

    if not imovel:
        # se o tipo de imóvel não foi encontrado
        error_msg = "Tipo de imóvel não encontrado na base :/"
        logger.warning(colored(
            f"Erro ao buscar tipo de imóvel de id #'{tipo_imovel_id}', '{error_msg}'", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(colored(
            f"Tipo de imóvel encontrado: '{imovel.descricao}'", 'green', attrs=['bold']))

        # retorna a representação do tipo de imóvel
        return apresenta_tipo_imovel(imovel), 200


@app.get('/tipos_imoveis', tags=[tipo_imovel_tag],
         responses={"200": ListagemTipos_ImovelSchema, "404": ErrorSchema})
def get_tipos_imoveis():
    """Faz a busca por todos os tipos de imóveis cadastrados.

    Retorna uma listagem da representação dos tipos de imóveis.
    """
    logger.debug(
        colored(f"Coletando tipos de imóveis", 'blue', attrs=['dark']))
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    # Faz a contagem de imóveis por tipos de imóveis
    stmt = select(
        Imovel.id_tipo_imovel, func.count('*').label('id_tipo_imovel_count')
    ).group_by(Imovel.id_tipo_imovel).subquery()

    # Faz um left join com tabela de contagem dos moveis
    imoveis = session.query(Tipo_Imovel, stmt.c.id_tipo_imovel_count).outerjoin(
        stmt, Tipo_Imovel.id == stmt.c.id_tipo_imovel).order_by(Tipo_Imovel.id)

    count: int = 0

    for u in imoveis:
        count = count+1

    if not imoveis:
        # se não há unidades cadastrados
        return {"Tipos de imóveis": []}, 200
    else:
        logger.debug(colored(f"%d tipos de imóveis encontrados" %
                     count, 'green', attrs=['bold']))
        # retorna a representação da imóvel
        # print(imoveis)
        return apresenta_tipos_imoveis(imoveis), 200


@app.delete('/tipo_imovel', tags=[tipo_imovel_tag],
            responses={"200": Tipo_ImovelDelSchema, "404": ErrorSchema})
def del_tipo_imovel(query: Tipo_ImovelBuscaSchema):
    """Deleta um tipo de imóvel a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    _imovel = query.id
    logger.debug(colored(
        f"Deletando dados do tipo de imóvel de id #{_imovel}", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    imovel: Tipo_Imovel = session.query(Tipo_Imovel).filter(
        Tipo_Imovel.id == _imovel).first()

    if imovel:

        # print(str(imovel_id))
        # fazendo a remoção
        count = session.query(Tipo_Imovel).filter(
            Tipo_Imovel.id == _imovel).delete()
        session.commit()

        if count:

            # retorna a representação da mensagem de confirmação
            logger.debug(
                colored(f"Deletado o tipo de imóvel de id #{_imovel}", 'green', attrs=['bold']))

            return {
                "mensagem": "Tipo de imóvel removido",
                "id": _imovel,
                "descrição": imovel.descricao
            }
        else:

            # avisa se der erro ao deletar o tipo de imóvel
            error_msg = "Erro ao deletar o tipo de imóvel :/"
            logger.warning(
                colored(f"Erro ao deletar o tipo de imóvel #'{_imovel}'", 'red', attrs=['bold']))
            return {"mensagem": error_msg}, 404

    else:
        # se o tipo de imóvel não foi encontrado
        error_msg = "Tipo de imóvel não encontrado na base :/"
        logger.warning(
            colored(f"Tipo de imóvel não encontrado na base", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404


##############################################################################################
# Tratamento do tipo de cômodo
##############################################################################################


@app.post('/tipo_comodo', tags=[tipo_comodo_tag],
          responses={"200": Tipo_ComodoPostSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def add_tipo_comodo(form: Tipo_ComodoSchema):
    """Adiciona um novo tipo de cômodo à base de dados.

    Retorna uma representação do tipo de cômodo.
    """
    _comodo = form.descricao.strip()
    comodo = Tipo_Comodo(descricao=form.descricao.upper())

    logger.debug(colored(
        f"Adicionando o tipo de cômodo de descrição: '{_comodo}'", 'blue', attrs=['dark']))

    try:

        # criando conexão com a base
        session = Session()

        # adicionando o tipo de cômodo
        session.add(comodo)

        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(colored(
            f"Adicionado o tipo de cômodo de descrição: '{_comodo}'", 'green', attrs=['bold']))
        return apresenta_tipo_comodo(comodo), 200

    except IntegrityError as e:
        # como a duplicidade da descrição é a provável razão do IntegrityError
        error_msg = "Tipo de cômodo de mesma descrição já salvo na base :/"
        logger.warning(colored(
            f"Erro ao adicionar o tipo de cômodo '{_comodo}'. '{error_msg}'", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto ocorra
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(colored(
            f"Erro ao adicionar o tipo de cômodo '{_comodo}'. {e}", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 400


@app.get('/tipo_comodo', tags=[tipo_comodo_tag],
         responses={"200": Tipo_ComodoViewSchema, "404": ErrorSchema})
def get_tipo_comodo(query: Tipo_ComodoBuscaSchema):
    """Faz a busca por um tipo de cômodo a partir do id informado.

    Retorna uma representação do tipo de cômodo.
    """
    tipo_comodo_id: str = query.id

    logger.debug(
        colored(f"Coletando dados sobre o tipo de cômodo", 'blue', attrs=['dark']))
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    comodo = session.query(Tipo_Comodo).filter(
        Tipo_Comodo.id == tipo_comodo_id).first()

    if not comodo:
        # se o tipo de cômodo não foi encontrado
        error_msg = "Tipo de cômodo não encontrado na base :/"
        logger.warning(colored(
            f"Erro ao buscar tipo de cômodo de id #'{tipo_comodo_id}', '{error_msg}'", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(colored(
            f"Tipo de cômodo encontrado: '{comodo.descricao}'", 'green', attrs=['bold']))
        # retorna a representação do tipo de cômodo
        return mostra_tipo_comodo(comodo), 200


@app.get('/tipos_comodos', tags=[tipo_comodo_tag],
         responses={"200": ListagemTipos_ComodoSchema, "404": ErrorSchema})
def get_tipos_comodos():
    """Faz a busca por todos os tipos de cômodos cadastrados.

    Retorna uma listagem da representação dos tipos de cômodos.
    """
    logger.debug(
        colored(f"Coletando tipos de cômodos", 'blue', attrs=['dark']))
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    # Faz a contagem de cômodos por tipos de cômodos
    stmt = select(
        Comodo.id_tipo_comodo, func.count('*').label('id_tipo_comodo_count')
    ).group_by(Comodo.id_tipo_comodo).subquery()

    # Faz um left join com tabela de contagem dos comodos
    comodos = session.query(Tipo_Comodo, stmt.c.id_tipo_comodo_count).outerjoin(
        stmt, Tipo_Comodo.id == stmt.c.id_tipo_comodo).order_by(Tipo_Comodo.id)

    count: int = 0

    for u in comodos:
        count = count+1

    if not comodos:
        # se não há unidades cadastrados
        return {"Tipos cômodos": []}, 200
    else:
        logger.debug(colored(f"%d tipos de cômodos encontrados" %
                     count, 'green', attrs=['bold']))
        # retorna a representação da cômodo
        # print(comodos)
        return apresenta_tipos_comodos(comodos), 200


@app.delete('/tipo_comodo', tags=[tipo_comodo_tag],
            responses={"200": Tipo_ComodoDelSchema, "404": ErrorSchema})
def del_tipo_comodo(query: Tipo_ComodoBuscaSchema):
    """Deleta um tipo de cômodo a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    _comodo = query.id

    logger.debug(colored(
        f"Deletando dados do tipo de cômodo de id #{_comodo}", 'blue', attrs=['dark']))

    # criando conexão com a base
    session = Session()
    comodo: Tipo_Comodo = session.query(Tipo_Comodo).filter(
        Tipo_Comodo.id == _comodo).first()

    if comodo:

        # print(str(comodo_id))
        # fazendo a remoção
        count = session.query(Tipo_Comodo).filter(
            Tipo_Comodo.id == _comodo).delete()
        session.commit()

        if count:

            # retorna a representação da mensagem de confirmação
            logger.debug(
                colored(f"Deletado o tipo de cômodo de id #{_comodo}", 'green', attrs=['bold']))

            return {
                "mensagem": "Tipo de cômodo removido",
                "id": _comodo,
                "descrição": comodo.descricao
            }
        else:

            # avisa se der erro ao deletar o tipo de cômodo
            error_msg = "Erro ao deletar o tipo de cômodo :/"
            logger.warning(
                colored(f"Erro ao deletar o tipo de cômodo #'{_comodo}'", 'red', attrs=['bold']))
            return {"mensagem": error_msg}, 404

    else:
        # se o tipo de cômodo não foi encontrado
        error_msg = "Tipo de cômodo não encontrado na base :/"
        logger.warning(
            colored(f"Tipo de cômodo não encontrado na base", 'red', attrs=['bold']))
        return {"mensagem": error_msg}, 404
