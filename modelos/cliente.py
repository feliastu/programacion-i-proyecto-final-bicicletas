"""Datos de contacto del propietario de una bicicleta."""

from modelos.validaciones import validar_texto


class Cliente:
    def __init__(self, codigo, nombre, telefono):
        self.__codigo = validar_texto(codigo, "El código del cliente")
        self.actualizar_contacto(nombre, telefono)

    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_telefono(self):
        return self.__telefono

    def actualizar_contacto(self, nombre, telefono):
        """Valida ambos datos antes de reemplazar cualquiera de ellos."""
        nuevo_nombre = validar_texto(nombre, "El nombre")
        nuevo_telefono = validar_texto(telefono, "El teléfono")
        self.__nombre = nuevo_nombre
        self.__telefono = nuevo_telefono

    def mostrar_informacion(self):
        return f"{self.__codigo} - {self.__nombre} | Teléfono: {self.__telefono}"
