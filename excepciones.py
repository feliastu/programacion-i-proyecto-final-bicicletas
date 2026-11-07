"""Situaciones propias de la gestión de órdenes del taller."""


class ErrorTaller(Exception):
    """Base común de los errores del dominio."""


class ServicioDuplicadoError(ErrorTaller):
    """La orden ya contiene un servicio con el mismo código."""


class ServicioNoEncontradoError(ErrorTaller):
    """Se intenta retirar un servicio que no pertenece a la orden."""


class OrdenSinServiciosError(ErrorTaller):
    """Una orden vacía no puede cerrarse."""


class OrdenCerradaError(ErrorTaller):
    """Una orden cerrada no admite cambios ni un segundo cierre."""
