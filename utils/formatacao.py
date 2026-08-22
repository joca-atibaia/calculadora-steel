"""
Funções de formatação da Calculadora Steel Framing.
"""


def moeda(valor: float) -> str:
    """Formata um número como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def numero(valor: float, casas: int = 2) -> str:
    """Formata números usando vírgula como separador decimal."""
    return f"{valor:.{casas}f}".replace(".", ",")


def quantidade(valor: float, casas: int = 2) -> str:
    """Formata quantidades de materiais."""
    return numero(valor, casas)
