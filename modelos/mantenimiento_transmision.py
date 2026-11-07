"""Servicio especializado en la transmisión por cadena."""

from modelos.servicio_mantenimiento import ServicioMantenimiento
from modelos.validaciones import validar_entero


class MantenimientoTransmision(ServicioMantenimiento):
    def __init__(self, codigo, observacion, velocidades, limpieza_profunda):
        super().__init__(codigo, observacion)
        self.__velocidades = validar_entero(velocidades, "Las velocidades", 1, 30)
        if not isinstance(limpieza_profunda, bool):
            raise ValueError("La limpieza profunda debe indicarse con True o False.")
        self.__limpieza_profunda = limpieza_profunda

    def get_velocidades(self):
        return self.__velocidades

    def get_limpieza_profunda(self):
        return self.__limpieza_profunda

    def describir_trabajo(self):
        limpieza = "profunda" if self.__limpieza_profunda else "básica"
        return (f"Mantenimiento de transmisión de {self.__velocidades} velocidades "
                f"con limpieza {limpieza}. Observación: {self.get_observacion()}")

    def calcular_duracion(self):
        # Regla didáctica: 15 min base, 2 por velocidad y 20 por limpieza profunda.
        adicional = 20 if self.__limpieza_profunda else 0
        return 15 + 2 * self.__velocidades + adicional
