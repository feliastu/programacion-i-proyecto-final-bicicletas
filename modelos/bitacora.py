"""Secuencia de movimientos de una orden; no es un registro de auditoría seguro."""

from modelos.validaciones import validar_texto


class Bitacora:
    def __init__(self, codigo_orden):
        self.__codigo_orden = validar_texto(codigo_orden, "El código de la orden")
        self.__movimientos = []

    def registrar(self, descripcion):
        texto = validar_texto(descripcion, "La descripción del movimiento")
        self.__movimientos.append(texto)

    def consultar(self):
        """Una tupla de textos no permite modificar la lista interna."""
        return tuple(self.__movimientos)

    def mostrar_informacion(self):
        lineas = [f"Bitácora de {self.__codigo_orden}"]
        for numero, descripcion in enumerate(self.__movimientos, start=1):
            lineas.append(f"{numero}. {descripcion}")
        return "\n".join(lineas)
