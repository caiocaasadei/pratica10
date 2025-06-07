# routes/cargo_routes.py
from flask import Blueprint, request
from db import Db, Mode

from valida import Valida
import util

cargo_bp = Blueprint("cargo_bp", __name__)

def geraResposta(cargos):
    if not isinstance(cargos, list):
        return cargos
    
    if not cargos:
        return util.formataAviso("Cargo não encontrado")

    cargo_formatado = []
    for cargo in cargos: 
        cargo_formatado.append({
            "codCargo": cargo[0],
            "nomCargo": cargo[1]
        })

    return cargo_formatado

@cargo_bp.route("/cargo", methods=["GET"])
def get_cargo():
    sql = """
        SELECT codCargo,
               nomCargo
          FROM Cargo
        """
    
    try:
        db = Db()
        cargos = db.execSql(sql, None, Mode.SELECT)
    except Exception as e:
        return db.getErro(e)

    return geraResposta(cargos)


# Rota para obter um cargo específico
@cargo_bp.route("/obterCargoPorId/<int:codCargo>", methods=["GET"])
def obter_cargoPorId(codCargo):
    valida = Valida()
    valida.codCargo(codCargo)
    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        SELECT codCargo,
               nomCargo 
          FROM Cargo
         WHERE codCargo = %s
    """
    params = (codCargo,)
    
    db = Db()
    try:   
        cargos = db.execSql(sql, params, Mode.SELECT)
    except Exception as e:
        return db.getErro(e)
    
    return geraResposta(cargos)

# Rota para adicionar um cargo
@cargo_bp.route('/cargo', methods=['POST'])
def add_cargo():
    data = request.json
         
    nomCargo = data.get('nomCargo')

    valida = Valida()
    valida.nomCargo(nomCargo)
  
    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        INSERT INTO Cargo
          (nomCargo)
            VALUES (%s)
    """
    params = (nomCargo,)
    
    db = Db()
    try: 
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro(e)

    
@cargo_bp.route('/cargo', methods=['PUT'])
def update_cargo():
    data = request.json  

    codCargo = data.get('codCargo')
    nomCargo = data.get('nomCargo')

    valida = Valida()
    valida.codCargo(codCargo)
    valida.nomCargo(nomCargo)

    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        UPDATE Cargo
           SET nomCargo = %s
         WHERE codCargo = %s
        """
    params = (nomCargo, codCargo,)
        
    try:
        db = Db()
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro(e)

@cargo_bp.route("/cargo/<int:codCargo>", methods=["DELETE"])
def deletar_cargo(codCargo):
    valida = Valida()
    valida.codCargo(codCargo)
    
    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        DELETE FROM Cargo 
         WHERE codCargo = %s
    """
    params = (codCargo,)

    try:  
        db = Db()  
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro(e)

