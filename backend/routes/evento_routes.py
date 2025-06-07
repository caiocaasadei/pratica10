from flask import Blueprint, request
from db import Db, Mode
from valida import Valida
import util

evento_bp = Blueprint("evento_bp", __name__)

# Gera resposta padronizada
def geraResposta(eventos):
    if not isinstance(eventos, list):
        return eventos

    if not eventos:
        return []  # Agora retorna lista vazia ao invés de aviso

    evento_formatado = []
    for evento in eventos:
        evento_formatado.append({
            "codEvento": evento[0],
            "nomEvento": evento[1]
        })

    return evento_formatado

# Lista todos os eventos
@evento_bp.route("/evento", methods=["GET"])
def get_evento():
    sql = """
        SELECT codEvento,
               nomEvento
          FROM Evento
    """
    try:
        db = Db()
        eventos = db.execSql(sql, None, Mode.SELECT)
    except Exception as e:
        return db.getErro(e)

    return geraResposta(eventos)

# Retorna um evento específico por ID
@evento_bp.route("/obterEventoPorId/<int:codEvento>", methods=["GET"])
def obter_eventoPorId(codEvento):
    valida = Valida()
    valida.codEvento(codEvento)
    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        SELECT codEvento,
               nomEvento 
          FROM Evento
         WHERE codEvento = %s
    """
    params = (codEvento,)

    db = Db()
    try:
        eventos = db.execSql(sql, params, Mode.SELECT)
    except Exception as e:
        return db.getErro(e)

    return geraResposta(eventos)

# Adiciona um novo evento
@evento_bp.route('/evento', methods=['POST'])
def add_evento():
    data = request.json
    nomEvento = data.get('nomEvento')

    valida = Valida()
    valida.nomEvento(nomEvento)

    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        INSERT INTO Evento (nomEvento)
        VALUES (%s)
    """
    params = (nomEvento,)

    db = Db()
    try:
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro(e)

# Atualiza um evento existente
@evento_bp.route('/evento', methods=['PUT'])
def update_evento():
    data = request.json
    codEvento = data.get('codEvento')
    nomEvento = data.get('nomEvento')

    valida = Valida()
    valida.codEvento(codEvento)
    valida.nomEvento(nomEvento)

    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        UPDATE Evento
           SET nomEvento = %s
         WHERE codEvento = %s
    """
    params = (nomEvento, codEvento)

    try:
        db = Db()
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro(e)

# Deleta um evento
@evento_bp.route("/evento/<int:codEvento>", methods=["DELETE"])
def deletar_evento(codEvento):
    valida = Valida()
    valida.codEvento(codEvento)

    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        DELETE FROM Evento 
         WHERE codEvento = %s
    """
    params = (codEvento,)

    try:
        db = Db()
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro(e)
