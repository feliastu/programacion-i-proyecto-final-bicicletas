"""Demostración integrada del proyecto final. Ejecutar: python main.py."""

from excepciones import (
    OrdenCerradaError, OrdenSinServiciosError,
    ServicioDuplicadoError, ServicioNoEncontradoError,
)
from modelos.ajuste_frenos import AjusteFrenos
from modelos.bicicleta import Bicicleta
from modelos.cliente import Cliente
from modelos.mantenimiento_transmision import MantenimientoTransmision
from modelos.orden_servicio import OrdenServicio
from modelos.reparacion_llanta import ReparacionLlanta
from modelos.servicio_mantenimiento import ServicioMantenimiento


def crear_datos_demo():
    """Crea 14 objetos: 2 clientes, 2 bicicletas, 6 servicios, 2 órdenes y 2 bitácoras."""
    clientes = [Cliente("C01", "Ana Torres", "000-000-0001"),
                Cliente("C02", "Luis Rojas", "000-000-0002")]
    bicicletas = [Bicicleta("B01", "Marca A", "Urbana", clientes[0]),
                  Bicicleta("B02", "Marca B", "Montaña", clientes[1])]
    # La única colección de demostración polimórfica mezcla los tres tipos.
    servicios = [
        AjusteFrenos("F01", "Ajuste de ambas ruedas", "disco", 2),
        MantenimientoTransmision("T01", "Limpieza general", 7, True),
        ReparacionLlanta("L01", "Llanta trasera", "camara", 1),
        AjusteFrenos("F02", "Ajuste de rueda delantera", "rin", 1),
        MantenimientoTransmision("T02", "Mantenimiento periódico", 9, False),
        ReparacionLlanta("L02", "Llanta delantera", "tubeless", 2),
    ]
    ordenes = [OrdenServicio("O01", bicicletas[0]), OrdenServicio("O02", bicicletas[1])]
    return clientes, bicicletas, servicios, ordenes


def mostrar_reporte_servicios(servicios):
    """Un ciclo, dos métodos sobrescritos y ninguna selección manual por tipo."""
    for servicio in servicios:
        print(servicio.mostrar_identificacion())
        print(servicio.describir_trabajo())
        print("Tiempo estimado:", servicio.calcular_duracion(), "minutos\n")


def main():
    print("TALLER DE BICICLETAS - ÓRDENES DE MANTENIMIENTO")
    print("Datos ficticios. Los tiempos son supuestos didácticos, no estándares técnicos.\n")
    clientes, bicicletas, servicios, ordenes = crear_datos_demo()
    print("1. OBJETOS Y ENCAPSULAMIENTO")
    print(clientes[0].mostrar_informacion())
    clientes[0].actualizar_contacto("Ana María Torres", "000-000-0010")
    print("Contacto actualizado:", clientes[0].mostrar_informacion())
    print("Referencia compartida:", bicicletas[0].mostrar_informacion())
    try:
        clientes[0].actualizar_contacto("Nombre que no se debe guardar", " ")
    except ValueError as error:
        print("CONTROLADO - ValueError:", error)
    print("CONTINÚA: contacto conservado:", clientes[0].mostrar_informacion())

    print("\n2. ABSTRACCIÓN")
    try:
        ServicioMantenimiento("S00", "Servicio sin especialidad")
    except TypeError:
        print("CONTROLADO - TypeError: ServicioMantenimiento es abstracto.")
    print("CONTINÚA: se utilizan los tres servicios especializados.")

    print("\n3. REPORTE POLIMÓRFICO\n")
    mostrar_reporte_servicios(servicios)

    print("4. ÓRDENES Y EXCEPCIONES PERSONALIZADAS")
    primera, segunda = ordenes
    primera.agregar_servicio(servicios[0])
    primera.agregar_servicio(servicios[1])
    primera.agregar_servicio(servicios[2])
    print("ALTA CORRECTA: tres servicios en O01.")
    print(primera.mostrar_informacion())

    try:
        primera.agregar_servicio(servicios[0])
    except ServicioDuplicadoError as error:
        print("CONTROLADO - ServicioDuplicadoError:", error)
    print("CONTINÚA: O01 conserva", len(primera.get_servicios()), "servicios.")

    retirado = primera.retirar_servicio("L01")
    print("RETIRO CORRECTO:", retirado.get_codigo(), "| Total:",
          primera.calcular_duracion_total(), "minutos.")
    try:
        primera.retirar_servicio("S99")
    except ServicioNoEncontradoError as error:
        print("CONTROLADO - ServicioNoEncontradoError:", error)
    print("CONTINÚA: se incorpora nuevamente el servicio L01.")
    primera.agregar_servicio(retirado)

    try:
        segunda.cerrar()
    except OrdenSinServiciosError as error:
        print("CONTROLADO - OrdenSinServiciosError:", error)
    print("CONTINÚA: O02 sigue", segunda.get_estado(), "y puede recibir servicios.")
    segunda.agregar_servicio(servicios[3])
    segunda.agregar_servicio(servicios[4])
    segunda.agregar_servicio(servicios[5])

    primera.cerrar()
    print("CIERRE CORRECTO: O01.")
    try:
        primera.agregar_servicio(servicios[3])
    except OrdenCerradaError as error:
        print("CONTROLADO - OrdenCerradaError:", error)
    print("CONTINÚA: O01 se consulta aunque ya no admite cambios.")
    segunda.cerrar()

    print("\n5. CONSULTA FINAL Y COMPOSICIÓN")
    for orden in ordenes:
        print(orden.mostrar_informacion())
        print(orden.mostrar_bitacora(), "\n")
    print("FIN: ambas órdenes cerradas y todos los errores previstos controlados.")
    return ordenes


if __name__ == "__main__":
    main()
