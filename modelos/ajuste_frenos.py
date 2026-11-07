"""Servicio especializado en frenos de rin o disco."""

from modelos.servicio_mantenimiento import ServicioMantenimiento
from modelos.validaciones import validar_entero, validar_opcion


class AjusteFrenos(ServicioMantenimiento):
    def __init__(self, codigo, observacion, tipo_freno, ruedas):
        super().__init__(codigo, observacion)
        self.__tipo_freno = validar_opcion(tipo_freno, "El tipo de freno", ("rin", "disco"))
        self.__ruedas = validar_entero(ruedas, "La cantidad de ruedas", 1, 2)

    def get_tipo_freno(self):
        return self.__tipo_freno

    def get_ruedas(self):
        return self.__ruedas

    def describir_trabajo(self):
        return (f"Ajuste de frenos de {self.__tipo_freno} en {self.__ruedas} rueda(s). "
                f"Observación: {self.get_observacion()}")

    def calcular_duracion(self):
        # Regla didáctica: 12 min por rueda y 8 min adicionales si usa disco.
        adicional = 8 if self.__tipo_freno == "disco" else 0
        return 12 * self.__ruedas + adicional
