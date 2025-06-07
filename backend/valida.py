# Valida
import enum
from flask import jsonify


class Tipo(enum.Enum):
    SUCESSO = 0
    AVISO = 1
    ERRO = 2
       
class Valida:
    def __init__(self):
        self.mensagem = []

    def temMensagem(self):
        return len(self.mensagem) > 0

    def getMensagens(self):
        msg = {"tipo": "AVISO", 
               "mensagem": self.mensagem}
        
        return jsonify(msg), 400
    
    def CPF(self, codCPF):
        if codCPF is None:
            self.mensagem.append("Código do CPF não pode ser nulo!")
        else:
            if not (isinstance(codCPF, str)):
                self.mensagem.append(f"CPF tipo {type(codCPF)} inválido: valor não é uma string!")
            else:
                cpf = codCPF.strip()
                if len(cpf) != 11:
                    self.mensagem.append("Quantidade de dígitos do CPF diferente de 11!")
                else:
                    if not cpf.isdigit():
                        self.mensagem.append("CPF possui caracteres não numéricos!")
        
    def desSenha(self, desSenha):
        if len(desSenha) <= 4:
            self.mensagem.append("A senha tem de ter pelo menos 4 caracteres!")
        else:
            tamanho = len(desSenha)
            if tamanho < 4 or tamanho > 12:
                self.mensagem.append("Senha deve ter entre 4 a 12 digitos!")
 

    def nomUsuario(self, nomUsuario):
        if nomUsuario is None:
            self.mensagem.append("Nome do usuário não pode ser nulo!")
        else:
            tamanho = len(nomUsuario)
            if tamanho <= 0 or tamanho > 50:
                self.mensagem.append("Nome do usuário é obrigatório e pode ter até 50 caracteres!")
        
    def desEmail(self, desEmail):
        if desEmail is None:
            self.mensagem.append("E-mail do usuário não pode ser nulo!")
        else:
            tamanho = len(desEmail)
            if tamanho <= 0 or tamanho > 50:
                self.mensagem.append('E-mail do usuario é obrigatório e pode ter até 50 caracteres!')
        
    def idtPapel(self, idtPapel):
        if idtPapel is None:
            self.mensagem.append('Papel do usuário não pode ser nulo!')
        else:
            if idtPapel not in ['A', 'F', 'G']:
                self.mensagem.append(f'Papel de usuário {idtPapel} inválido!')

    def idtAtivo(self, idtAtivo):
        if idtAtivo is None:
            self.mensagem.append('Idt Ativo não pode ser nulo!')
        

    def codCargo(self, codCargo):
        if codCargo is None:
            self.mensagem.append("Código do cargo não pode ser nulo!")
        else:
            try:
                codCargo = int(codCargo)
            except:
                self.mensagem.append('Código do cargo não é numérico!')

    def nomCargo(self, nomCargo):
        if nomCargo is None:
            self.mensagem.append("Nome do cargo não pode ser nulo!")
        else:
            tamanho = len(nomCargo)
            if tamanho <= 0 or tamanho > 50:
                self.mensagem.append('Nome do cargo é obrigatório e pode ter até 30 caracteres!')


                
    def codEvento(self, codEvento):
        if codEvento is None:
            self.mensagem.append("Código do evento não pode ser nulo!")
        else:
            try:
                codEvento = int(codEvento)
            except:
                self.mensagem.append('Código do evento não é numérico!')

    def nomEvento(self, nomEvento):
        if nomEvento is None:
            self.mensagem.append("Nome do evento não pode ser nulo!")
        else:
            tamanho = len(nomEvento)
            if tamanho <= 0 or tamanho > 50:
                self.mensagem.append('Nome do evento é obrigatório e pode ter até 30 caracteres!')
