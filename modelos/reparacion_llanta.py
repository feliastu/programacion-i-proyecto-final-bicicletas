"""Servicio especializado en pinchazos de una llanta."""

from modelos.servicio_mantenimiento import ServicioMantenimiento
from modelos.validaciones import validar_entero, validar_opcion


class ReparacionLlanta(ServicioMantenimiento):
    def __init__(self, codigo, observacion, sistema, pinchazos):
        super().__init__(codigo, observacion)
        self.__sistema = validar_opcion(sistema, "El sistema de la llanta", ("camara", "tubeless"))
        self.__pinchazos = validar_entero(pinchazos, "Los pinchazos", 1, 3)

    def get_sistema(self):
        return self.__sistema

    def get_pinchazos(self):
        return self.__pinchazos

    def describir_trabajo(self):
        return (f"Reparación de {self.__pinchazos} pinchazo(s) en llanta "
                f"con sistema {self.__sistema}. Observación: {self.get_observacion()}")

    def calcular_duracion(self):
        # Regla didáctica: 10 min base, 8 por pinchazo y 10 adicionales para tubeless.
        adicional = 10 if self.__sistema == "tubeless" else 0
        return 10 + 8 * self.__pinchazos + adicional
