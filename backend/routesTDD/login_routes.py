rotasLoginPost = [
    {
        "method": "POST", 
           "url": "http://localhost:5000/api/usuario",   
          "data": {"codUsuarioCPF": "50087622655", 
                   "nomUsuario": "José Antônio",
                   "desEmail": "jose@gmail.com",
                   "idtPapel": "A",
                   "idtAtivo": True
                 }

    },
    {
        "method": "POST", 
           "url": "http://localhost:5000/api/usuario",   
          "data": {"codUsuarioCPF": "", 
                   "nomUsuario": "",
                   "desEmail": "",
                   "idtPapel": "",
                   "idtAtivo": "",
             }
    }
]

rotasLoginGetPutGet = [
    {
        "method": "GET",
           "url": "http://localhost:5000/api/loginAcesso/50087622655"
    },
    {
        "method": "PUT", "url": "http://localhost:5000/api/alterarSenha",
          "data": {"codUsuarioCPF": "50087622654", 
                   "desSenha": "123456"
                  }
    },    
    {
        "method": "POST",
           "url": "http://localhost:5000/api/loginAcesso",
          "data": {"codUsuarioCPF": "50087622654", 
                   "desSenha": "123456"
                  }
    },

    {
        "method": "PUT",
           "url": "http://localhost:5000/api/usuario",
          "data": {"nomUsuario": "José Antônio Alterado",
                   "desEmail": "jose@gmail.com",
                   "idtPapel": "G",
                   "idtAtivo": True,
                   "codUsuarioCPF": "50087622654"
                  }
    },
]

rotasLoginDelete = [
]