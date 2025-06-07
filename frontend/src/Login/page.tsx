import { useState, useEffect } from "react";
import TelaSemMenu from "../components/TelaSemMenu";
import { Eye, EyeOff } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useUsuario } from "../contexts/UsuarioContext";
import baseUrl from "../Api";

interface UsuarioLogado {
  cpf: string;
  nome: string;
  perfil: string;
  senha: string;
  idtTemSenha: boolean;
}
export default function Login() {
  const [cpf, setCpf] = useState("");
  const [usuarioValido, setUsuarioValido] = useState<UsuarioLogado | null>(
    null
  );
  const [senha, setSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");
  const [senhaVisivel, setSenhaVisivel] = useState(false);
  const [erro, setErro] = useState("");
  const toggleSenhaVisivel = () => setSenhaVisivel((prev) => !prev);
  const { setUsuario, limparUsuario } = useUsuario();

  const navigate = useNavigate();

  useEffect(() => {
    // Resetar usuário ao entrar na tela
    limparUsuario();
  }, []);
  const direcionarCadastro = () => {
    /*
    navigate("/<RotaDeCadastro>")
    ;*/
  };

  const verificarCpf = async (e: React.FormEvent) => {
    e.preventDefault();

    const cpfLimpo = cpf.replace(/\D/g, "");

    try {
      const response = await fetch(`${baseUrl}/api/loginAcesso/${cpfLimpo}`, {
        method: "GET",
      });

      if (!response.ok) {
        const errorData = await response.json();
        const mensagemBackend = errorData?.mensagem || "Erro na requisição";
        throw new Error(mensagemBackend);
      }

      const resultado = await response.json();

      setUsuarioValido({
        cpf: cpfLimpo,
        nome: "",
        perfil: "",
        senha: "",
        idtTemSenha: resultado?.idtTemSenha ?? true,
      });
      setErro("");
    } catch (err: any) {
      console.error("Erro ao verificar CPF:", err);
      setErro(err.message || "Erro ao verificar CPF.");
      setUsuarioValido(null);
    }
  };

  const verificarSenha = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!usuarioValido?.cpf) {
      setErro("Nenhum usuário validado. Por favor, verifique o CPF.");
      return;
    }

    const cpfLimpo = usuarioValido.cpf;

    // Caso 1: idtTemSenha === false → criar nova senha
    if (!usuarioValido.idtTemSenha) {
      if (senha.length < 4 || confirmarSenha.length < 4) {
        setErro("A senha deve ter no mínimo 4 caracteres.");
        return;
      }

      if (senha !== confirmarSenha) {
        setErro("As senhas digitadas não coincidem.");
        return;
      }

      try {
        const response = await fetch(`${baseUrl}/api/alterarSenha`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            codUsuarioCPF: cpfLimpo,
            desSenha: senha,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData?.mensagem || "Erro ao salvar senha.");
        }

        const resultado = await response.json();
        if (resultado?.sucesso) {
          alert("Senha cadastrada com sucesso!");
          setErro(""); // Limpa qualquer erro anterior em caso de sucesso
        } else {
          setErro(resultado?.mensagem || "Falha ao cadastrar senha.");
        }
      } catch (error: any) {
        console.error("Erro ao cadastrar senha:", error);
        setErro(error.message || "Erro ao cadastrar senha.");
      }
    }

    // Caso 2: idtTemSenha === true → login com senha existente
    try {
      const response = await fetch(`${baseUrl}/api/loginAcesso`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          codUsuarioCPF: cpfLimpo,
          desSenha: senha,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData?.mensagem || "Erro ao autenticar.");
      }

      const resultado = await response.json();

      if (resultado?.length > 0) {
        const usuario = resultado[0];

        setErro("");
        setUsuario(
          usuario.codUsuarioCPF || "",
          usuario.nomUsuario || "",
          usuario.idtPapel || ""
        );

        if (usuario.idtPapel) {
          console.log("Chamando telaPadrao");
          navigate("/TelaPadrao");
        } else {
          setErro(resultado?.mensagem || "Nenhum papel atribuido ao usuario");
        }
      } else {
        setErro(resultado?.mensagem || "Falha ao autenticar.");
      }
    } catch (error: any) {
      setErro(error.message || "Erro ao verificar senha.");
    }
  };

  return (
    <TelaSemMenu titulo="Login">
      <div className="flex flex-col items-center justify-center w-full h-full gap-6">
        <div className="bg-white p-10 rounded-2xl shadow-lg w-full max-w-md">
          <h2 className="text-2xl font-semibold text-center mb-6">
            Acessar Sistema
          </h2>
          {!usuarioValido && (
            <form className="flex flex-col gap-4" onSubmit={verificarCpf}>
              <input
                type="text"
                placeholder="CPF"
                value={cpf}
                onChange={(e) => setCpf(e.target.value)}
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {erro && <p className="text-red-600 text-sm">{erro}</p>}
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition duration-200"
              >
                Avançar
              </button>
            </form>
          )}
          {usuarioValido && (
            <form className="flex flex-col gap-4" onSubmit={verificarSenha}>
              <div className="text-center text-gray-700">
                <span className="text-sm">Usuário:</span>
                <p className="text-lg font-semibold">{usuarioValido.nome}</p>
              </div>

              {!usuarioValido.idtTemSenha ? (
                <>
                  <div className="relative">
                    <input
                      type={senhaVisivel ? "text" : "password"}
                      placeholder="Criar senha"
                      value={senha}
                      onChange={(e) => setSenha(e.target.value)}
                      className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                      type="button"
                      onClick={toggleSenhaVisivel}
                      className="absolute right-3 top-2.5 text-gray-500"
                    >
                      {senhaVisivel ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                  <div className="relative">
                    <input
                      type={senhaVisivel ? "text" : "password"}
                      placeholder="Confirmar senha"
                      value={confirmarSenha}
                      onChange={(e) => setConfirmarSenha(e.target.value)}
                      className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                      type="button"
                      onClick={toggleSenhaVisivel}
                      className="absolute right-3 top-2.5 text-gray-500"
                    >
                      {senhaVisivel ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                </>
              ) : (
                <div className="relative">
                  <input
                    type={senhaVisivel ? "text" : "password"}
                    placeholder="Senha"
                    value={senha}
                    onChange={(e) => setSenha(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    type="button"
                    onClick={toggleSenhaVisivel}
                    className="absolute right-3 top-2.5 text-gray-500"
                  >
                    {senhaVisivel ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
              )}
              {erro && <p className="text-red-600 text-sm">{erro}</p>}
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition duration-200"
              >
                Entrar
              </button>
            </form>
          )}

          <div className="mt-6 flex flex-col items-center gap-2">
            <button
              onClick={direcionarCadastro}
              className="text-blue-600 hover:underline text-sm"
            >
              Cadastra
            </button>
          </div>
        </div>
      </div>
    </TelaSemMenu>
  );
}
