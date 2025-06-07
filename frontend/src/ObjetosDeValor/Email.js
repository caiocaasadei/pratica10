export class Email {
  constructor(email) {
    this.email = email;
    if (!this.validarEmail()) {
      throw new Error("Email inválido. Use um formato de email valido");
    }
  }

  validarEmail() {
    // Regex atualizado para aceitar múltiplos subdomínios
    const regex =
      /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$/;
    return regex.test(this.email);
  }

  getValue() {
    return this.email;
  }
}
