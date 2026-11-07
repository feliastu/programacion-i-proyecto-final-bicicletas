"""Validaciones compartidas; cada función devuelve el valor aceptado."""


def validar_texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} debe ser un texto no vacío.")
    return valor.strip()


def validar_entero(valor, campo, minimo, maximo):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(f"{campo} debe ser un número entero.")
    if not minimo <= valor <= maximo:
        raise ValueError(f"{campo} debe estar entre {minimo} y {maximo}.")
    return valor


def validar_opcion(valor, campo, opciones):
    texto = validar_texto(valor, campo).lower()
    if texto not in opciones:
        raise ValueError(f"{campo} debe ser una de estas opciones: {', '.join(opciones)}.")
    return texto
