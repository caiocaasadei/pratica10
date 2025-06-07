import { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";
import baseUrl from "../Api";

interface Evento {
  codEvento: number;
  nomEvento: string;
}

type OutletContextType = {
  exibirMensagem: (obj: MensagemObj) => void;
};

type MensagemObj = {
  tipo: "ERRO" | "AVISO" | "SUCESSO";
  mensagem: string[];
};

export default function ListaEvento() {
  const [eventos, setEventos] = useState<Evento[]>([]);
  const [eventoEditando, setEventoEditando] = useState<Evento | null>(null);
  const [modoEdicao, setModoEdicao] = useState(false);
  const outletContext = useOutletContext<OutletContextType | null>();
  const exibirMensagem =
    outletContext?.exibirMensagem ??
    ((obj: MensagemObj) => alert(obj.mensagem.join("\n")));

  useEffect(() => {
    buscarEventos();
  }, []);

  const buscarEventos = async () => {
    try {
      const res = await fetch(`${baseUrl}/api/evento`);
      if (!res.ok) {
        const msg = await res.json();
        exibirMensagem(msg);
        return;
      }
      const data = await res.json();
      setEventos(data);
    } catch (error) {
      exibirMensagem({
        tipo: "ERRO",
        mensagem: [`Erro inesperado ao consultar o evento: ${error}`],
      });
    }
  };

  const buscarEventoPorId = async (codEvento: number) => {
    try {
      const res = await fetch(`${baseUrl}/api/obterEventoPorId/${codEvento}`);

      if (!res.ok) {
        const msg = await res.json();
        exibirMensagem(msg);
        return;
      }
      const data = await res.json();
      if (data && data.length > 0) {
        setEventoEditando(data[0]);
        setModoEdicao(true);
      }
    } catch (error) {
      exibirMensagem({
        tipo: "ERRO",
        mensagem: [`Erro inesperado ao salvar o evento: ${error}`],
      });
    }
  };

  const salvarEvento = async () => {
    if (!eventoEditando) return;

    const metodo = modoEdicao ? "PUT" : "POST";

    try {
      const res = await fetch(`${baseUrl}/api/evento`, {
        method: metodo,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(eventoEditando),
      });

      if (!res.ok) {
        const msg = await res.json();
        exibirMensagem(msg);
        return;
      }
      const resposta = await res.json();
      if (resposta.tipo !== "SUCESSO") {
        return;
      }
      exibirMensagem(resposta);
    } catch (error) {
      exibirMensagem({
        tipo: "ERRO",
        mensagem: [`Erro inesperado ao salvar o evento: ${error}`],
      });
    } finally {
      await buscarEventos();
      setEventoEditando(null);
      setModoEdicao(false);
    }
  };

  const excluirEvento = async (codEvento: number) => {
    const confirmado = confirm("Deseja realmente excluir este evento?");
    if (!confirmado) return;

    try {
      const res = await fetch(`${baseUrl}/api/evento/${codEvento}`, {
        method: "DELETE",
      });

      if (!res.ok) {
        const msg = await res.json();
        exibirMensagem(msg);
        return;
      }

      await buscarEventos();
    } catch (error) {
      exibirMensagem({
        tipo: "ERRO",
        mensagem: [`Erro inesperado ao excluir o evento: ${error}`],
      });
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Lista de Eventos</h2>

      <table className="w-full border-collapse border border-gray-400">
        <thead>
          <tr className="bg-gray-200">
            <th className="border border-gray-400 px-4 py-2">Nome do Evento</th>
            <th className="border border-gray-400 px-4 py-2">Ações</th>
          </tr>
        </thead>
        <tbody>
          {eventos.map((evento) => (
            <tr key={evento.codEvento} className="border border-gray-400">
              <td className="border border-gray-400 px-4 py-2">{evento.nomEvento}</td>
              <td className="border border-gray-400 px-4 py-2">
                <button
                  className="mr-2 text-blue-500"
                  onClick={() => buscarEventoPorId(evento.codEvento)}
                >
                  ✏️
                </button>
                <button
                  className="text-red-500"
                  onClick={() => excluirEvento(evento.codEvento)}
                >
                  🗑️
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button
        className="mt-4 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        onClick={() => {
          setEventoEditando({
            codEvento: 0,
            nomEvento: "",
          });
          setModoEdicao(false);
        }}
      >
        ➕ Inserir Novo Evento
      </button>

      {eventoEditando && (
        <div className="mt-6 p-4 border border-gray-400 rounded">
          <h3 className="text-lg font-semibold mb-2">
            {modoEdicao ? "Editar Evento" : "Novo Evento"}
          </h3>

          <label className="block mb-2">
            Nome do Evento:
            <input
              type="text"
              className="w-full p-2 border border-gray-400 rounded"
              value={eventoEditando.nomEvento}
              onChange={(e) =>
                setEventoEditando({
                  ...eventoEditando,
                  nomEvento: e.target.value,
                })
              }
            />
          </label>

          <div className="mt-4 flex justify-center space-x-4">
            <button
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              onClick={() => {
                setEventoEditando(null);
                setModoEdicao(false);
              }}
            >
              ❌ Cancelar
            </button>
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              onClick={salvarEvento}
            >
              💾 Salvar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
