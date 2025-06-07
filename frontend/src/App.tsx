import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { UsuarioProvider, useUsuario } from "./contexts/UsuarioContext";

import Login from "./Login/page";

import TelaPadrao from "./components/TelaPadrao"; // Importe TelaPadrao

import "./App.css";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Ocorreu um erro:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Algo deu errado.</h1>;
    }
    return this.props.children;
  }
}

const RequireAuth = ({ children }) => {
  const { usuario } = useUsuario();

  if (!usuario) {
    return <Navigate to="/Login" />;
  }

  return children;
};

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <UsuarioProvider>
          <Routes>
            {/* Rotas públicas (sem autenticação) */}
            <Route path="/" element={<Navigate to="/Login" replace />} />
            <Route path="/Login" element={<Login />} />

            {/* Rota protegida que usa TelaPadrao como layout */}
            <Route
              path="/*"
              element={
                //<RequireAuth>
                <TelaPadrao />
                //</RequireAuth>
              }
            />
          </Routes>
        </UsuarioProvider>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
