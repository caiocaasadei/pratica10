import requests
import re
import json

from cargo_routes import rotasCargoPost, rotasCargoGetPutGet, rotasCargoDelete
from login_routes import rotasLoginPost, rotasLoginGetPutGet, rotasLoginDelete
from evento_routes import rotasEventoPost, rotasEventoGetPutGet, rotasEventoDelete

# Cabeçalhos comuns (se necessário token ou content-type)
headers = {
    "Content-Type": "application/json",
}

def perguntar(pergunta):
    while True:  
        resposta = input(f"{pergunta} ").strip().upper()
        if resposta == 'S':
            return True
        elif resposta == 'N':
            return False
        else:
            print("Digite 'S' para Sim ou 'N' para Não.")


def testaRota(rotas, headers=None):
    headers = headers or {}
    for rota in  rotas:
        try:
            method = rota.get("method")
            url = rota.get("url")
            data = rota.get("data")

            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                print(f"🚫 Método {method} não suportado: {url}")
                continue
            
            status = response.status_code
            if status == 200:
                icone = '✅'
            else:
                if status < 499:
                    icone = '👈'
                else: 
                    icone = '❌' 

            print(f"{icone} Método: {method} status {status} url {url}:")
        
            try:
                conteudo = response.json()
                if conteudo == '':
                   continue
                
            except json.JSONDecodeError:
                html = response.text
                # Expressão regular para capturar conteúdo de <div class="plain">...</div>
                match = re.search(r'<div\s+class=["\']plain["\'].*?>(.*?)</div>', html, re.DOTALL)
                print("Conteúdo da resposta bruta (possivelmente HTML):")
                if match:
                    conteudo = match.group(1).strip()
                    print(conteudo)
                else:
                    print(f"⚠️ {response.text}")
                print("-----------------------------------❌")
                continue
            except requests.exceptions.RequestException as err:
                print(f"Erro de conexão: {err}")
                continue
  
            if response.status_code > 200: 
                if type(conteudo) == tuple:
                    resposta, erro = conteudo
                else:
                    resposta = conteudo
                    
                tipo = resposta.get("tipo")
                mensagem = resposta.get("mensagem", "")
                
                print(f"ℹ️ Tipo: {tipo}")
                for linha in mensagem:
                    print(linha)
                
                print(f"-----------------------------------------------------------ℹ️\n")
            else:
                print(f"🔍 Resposta SQL:")
                print(json.dumps(conteudo, indent=2, ensure_ascii=False))
                print(f"Fim Select -----------------------------🔍\n")

        except Exception as e:
            print(f"❌ ERRO ao acessar {url}: {str(e)}")


print("✅ Validando rotas...\n")


if perguntar("Valida endpoints da rota Cargo (S/N)? "):
    testaRota(rotasCargoDelete)
    testaRota(rotasCargoPost)
    testaRota(rotasCargoGetPutGet)

if perguntar("Valida endpoints da rota Login (S/N)? "):
    testaRota(rotasLoginDelete)
    testaRota(rotasLoginPost)
    testaRota(rotasLoginGetPutGet)


if perguntar("Valida endpoints da rota Login (S/N)? "):
    testaRota(rotasEventoDelete)
    testaRota(rotasEventoPost)
    testaRota(rotasEventoGetPutGet)


