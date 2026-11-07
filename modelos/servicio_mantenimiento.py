"""Contrato común de los trabajos; las duraciones son supuestos del ejemplo."""

from abc import ABC, abstractmethod

from modelos.validaciones import validar_texto


class ServicioMantenimiento(ABC):
    def __init__(self, codigo, observacion):
        self.__codigo = validar_texto(codigo, "El código del servicio")
        self.__observacion = validar_texto(observacion, "La observación")

    def get_codigo(self):
        return self.__codigo

    def get_observacion(self):
        return self.__observacion

    def mostrar_identificacion(self):
        return f"{self.__codigo} | {self.__observacion}"

    @abstractmethod
    def describir_trabajo(self):
        """Devuelve la descripción particular del servicio."""

    @abstractmethod
    def calcular_duracion(self):
        """Devuelve los minutos estimados para este servicio."""
