"""Bicicleta relacionada con un propietario ya creado."""

from modelos.cliente import Cliente
from modelos.validaciones import validar_texto


class Bicicleta:
    def __init__(self, codigo, marca, modelo, propietario):
        self.__codigo = validar_texto(codigo, "El código de la bicicleta")
        self.__marca = validar_texto(marca, "La marca")
        self.__modelo = validar_texto(modelo, "El modelo")
        if not isinstance(propietario, Cliente):
            raise ValueError("El propietario debe ser un objeto Cliente.")
        self.__propietario = propietario

    def get_codigo(self):
        return self.__codigo

    def get_marca(self):
        return self.__marca

    def get_modelo(self):
        return self.__modelo

    def get_propietario(self):
        return self.__propietario

    def mostrar_informacion(self):
        return (f"{self.__codigo} - {self.__marca} {self.__modelo} | "
                f"Propietario: {self.__propietario.get_nombre()}")
