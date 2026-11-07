"""Orden que reúne servicios de una bicicleta y crea su propia bitácora."""

from excepciones import (
    OrdenCerradaError, OrdenSinServiciosError,
    ServicioDuplicadoError, ServicioNoEncontradoError,
)
from modelos.bicicleta import Bicicleta
from modelos.bitacora import Bitacora
from modelos.servicio_mantenimiento import ServicioMantenimiento
from modelos.validaciones import validar_texto


class OrdenServicio:
    def __init__(self, codigo, bicicleta):
        self.__codigo = validar_texto(codigo, "El código de la orden")
        if not isinstance(bicicleta, Bicicleta):
            raise ValueError("La orden debe recibir un objeto Bicicleta.")
        self.__bicicleta = bicicleta
        self.__servicios = []
        self.__estado = "abierta"
        self.__bitacora = Bitacora(self.__codigo)
        self.__bitacora.registrar("Orden abierta.")

    def get_codigo(self):
        return self.__codigo

    def get_bicicleta(self):
        return self.__bicicleta

    def get_estado(self):
        return self.__estado

    def get_servicios(self):
        return tuple(self.__servicios)

    def consultar_movimientos(self):
        return self.__bitacora.consultar()

    def mostrar_bitacora(self):
        return self.__bitacora.mostrar_informacion()

    def __verificar_abierta(self):
        if self.__estado == "cerrada":
            raise OrdenCerradaError(f"La orden {self.__codigo} está cerrada y no admite cambios.")

    def agregar_servicio(self, servicio):
        self.__verificar_abierta()
        if not isinstance(servicio, ServicioMantenimiento):
            raise ValueError("Debe agregar un objeto ServicioMantenimiento concreto.")
        for existente in self.__servicios:
            if existente.get_codigo() == servicio.get_codigo():
                raise ServicioDuplicadoError(
                    f"El servicio {servicio.get_codigo()} ya está en la orden {self.__codigo}."
                )
        self.__servicios.append(servicio)
        self.__bitacora.registrar(f"Servicio agregado: {servicio.get_codigo()}.")

    def retirar_servicio(self, codigo_servicio):
        self.__verificar_abierta()
        codigo = validar_texto(codigo_servicio, "El código del servicio")
        for servicio in self.__servicios:
            if servicio.get_codigo() == codigo:
                self.__servicios.remove(servicio)
                self.__bitacora.registrar(f"Servicio retirado: {codigo}.")
                return servicio
        raise ServicioNoEncontradoError(
            f"El servicio {codigo} no pertenece a la orden {self.__codigo}."
        )

    def calcular_duracion_total(self):
        return sum(servicio.calcular_duracion() for servicio in self.__servicios)

    def cerrar(self):
        """Cierra administrativamente la orden; no ejecuta una reparación física."""
        self.__verificar_abierta()
        if not self.__servicios:
            raise OrdenSinServiciosError(f"La orden {self.__codigo} no tiene servicios para cerrar.")
        self.__estado = "cerrada"
        self.__bitacora.registrar("Orden cerrada.")

    def mostrar_informacion(self):
        return (f"Orden {self.__codigo} | Estado: {self.__estado}\n"
                f"Bicicleta: {self.__bicicleta.mostrar_informacion()}\n"
                f"Servicios: {len(self.__servicios)} | "
                f"Duración estimada: {self.calcular_duracion_total()} minutos")
