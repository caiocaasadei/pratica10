export class Telefone {
  constructor(telefone) {
    this.telefone = telefone;
    if (!this.validarTelefone()) {
      throw new Error(
        "Telefone inválido. Formato: (DDD) 9XXXX-XXXX ou (DDD) XXXX-XXXX"
      );
    }
  }

  validarTelefone() {
    // Valida apenas o formato final completo
    return /^\(\d{2}\)\s?(9\d{4}|\d{4})-\d{4}$/.test(this.telefone);
  }

  getValue() {
    return this.email;
  }
}
