# routes/login_routes.py
from flask import Blueprint, request
from db import Db, Mode
from valida import Valida
import util

import bcrypt

# Definindo o blueprint
login_bp = Blueprint("login_bp", __name__)


#Validar login (CPF) de acesso do usuario
@login_bp.route("/loginAcesso/<codUsuarioCPF>", methods=["GET"])
def get_loginAcesso(codUsuarioCPF):
    valida = Valida()
    valida.CPF(codUsuarioCPF)
    if valida.temMensagem():
        return valida.getMensagens()
        
    sql = """
        SELECT desSenha,
               idtAtivo
          FROM Usuario
         WHERE codUsuarioCPF = %s
    """
    params = (codUsuarioCPF,)

    db = Db()
    try:
        usuarios = db.execSql(sql, params, Mode.SELECT)
    except Exception as e:
        return db.getErro(e)
        
    if len(usuarios) == 0:
        return util.formataAviso("Usuario não encontrado!")
    
    usuario = usuarios[0]
    desSenha = usuario[0]
    idtAtivo = usuario[1]
    
    if not idtAtivo:
        return util.formataAviso("Usuario não está ativo!")
    
    idtTemSenha = desSenha is not None

    return {"idtTemSenha": idtTemSenha}
  

#Validar senha de acesso do usuario
@login_bp.route("/loginAcesso", methods=["POST"])
def post_login_acesso():
    data = request.json
    codUsuarioCPF = data.get("codUsuarioCPF")
    desSenhaInfo = data.get("desSenha")
    
    valida = Valida()
    valida.CPF(codUsuarioCPF)
    valida.desSenha(desSenhaInfo)
    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        SELECT nomUsuario,
               desSenha,
               idtPapel,
               idtAtivo
          FROM Usuario
         WHERE codUsuarioCPF = %s
    """
    params = (codUsuarioCPF,)
    db = Db()
    try:
        resultado = db.execSql(sql, params, Mode.SELECT)
    except Exception as e:
        return db.getErro(e)

    if not resultado: 
        return util.formataAviso("Usuario não encontrado!")
    usuario = resultado[0]
    
    nomUsuario = usuario[0]
    desSenha = usuario[1]
    idtPapel = usuario[2]
    idtAtivo = usuario[3]
        
    if not idtAtivo:
        return util.formataAviso("Usuario não está ativo!")
        
    if desSenha is not None: 
        # converte string do banco para bytes
        if not bcrypt.checkpw(desSenhaInfo.encode('utf-8'), desSenha.encode('utf-8')):
            return util.formataAviso("Usuário ou senha inválidos!")

    usuario_formatado = []
    usuario_formatado.append({
        "codUsuarioCPF" : codUsuarioCPF,
        "nomUsuario": nomUsuario,
        "idtPapel": idtPapel,
    })

    return usuario_formatado


# Rota para registrar usuário. A senha é informada somente 1o acesso.
@login_bp.route("/usuario", methods=["POST"])
def post_usuario():
    data = request.json
    codUsuarioCPF = data.get('codUsuarioCPF')
    nomUsuario    = data.get('nomUsuario')
    desEmail      = data.get('desEmail')
    idtPapel      = data.get('idtPapel')
    idtAtivo      = data.get('idtAtivo')
    
    
    valida = Valida()
    valida.CPF(codUsuarioCPF)
    valida.nomUsuario(nomUsuario)
    valida.desEmail(desEmail)
    valida.idtPapel(idtPapel)
           
    if valida.temMensagem():
        return valida.getMensagens()

    sql = """
        INSERT INTO Usuario 
           (codUsuarioCPF, nomUsuario, desEmail,
            idtPapel, idtAtivo )
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (codUsuarioCPF, nomUsuario, desEmail, idtPapel, idtAtivo,)

    try: 
        db = Db() 
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro(e)

# Rota para alterar usuário
@login_bp.route("/usuario", methods=["PUT"])
def put_usuario():
    data = request.json
    codUsuarioCPF    = data.get('codUsuarioCPF')
    nomUsuario       = data.get('nomUsuario')
    desEmail         = data.get('desEmail')
    idtPapel         = data.get('idtPapel')  
    idtAtivo         = data.get('idtAtivo')

    valida = Valida()
    valida.CPF(codUsuarioCPF)
    valida.nomUsuario(nomUsuario)
    valida.desEmail(desEmail)
    valida.idtPapel(idtPapel)
    valida.idtAtivo(idtAtivo)
    if valida.temMensagem():
        return valida.getMensagens()
    
    sql = """
        UPDATE Usuario 
           SET nomUsuario = %s,
               desEmail = %s,
               idtPapel = %s,
               idtAtivo = %s
         WHERE codUsuarioCPF = %s
    """
    params = (nomUsuario, desEmail, idtPapel, idtAtivo, codUsuarioCPF,)

    db = Db()
    try:
        resposta = db.execSql(sql, params, )
        if resposta != '':
            return resposta
        
        return util.formataAviso('Usuário alterado com sucesso')
    except Exception as e:
        return db.getErro(e)

         
# Rota para alterar a senha
@login_bp.route("/alterarSenha", methods=["PUT"])
def put_alterarSenha():
    data = request.json
    codUsuarioCPF = data.get('codUsuarioCPF')
    desSenha      = data.get('desSenha')
 
    valida = Valida()
    valida.CPF(codUsuarioCPF)
    valida.desSenha(desSenha)
    if valida.temMensagem():
        return valida.getMensagens()
       
    # Gerar hash da senha
    desSenhaCripto = bcrypt.hashpw(desSenha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    sql = """
        UPDATE Usuario 
           SET desSenha = %s
         WHERE codUsuarioCPF = %s
    """
    params = (desSenhaCripto, codUsuarioCPF,)
    try:
        db = Db()
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro(e)
    