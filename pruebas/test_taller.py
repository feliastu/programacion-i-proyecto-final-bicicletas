"""Verifica reglas del dominio, referencias, abstracción y continuidad."""

from contextlib import redirect_stdout
from io import StringIO
import unittest

from excepciones import (
    ErrorTaller, OrdenCerradaError, OrdenSinServiciosError,
    ServicioDuplicadoError, ServicioNoEncontradoError,
)
from main import crear_datos_demo, main, mostrar_reporte_servicios
from modelos.ajuste_frenos import AjusteFrenos
from modelos.bicicleta import Bicicleta
from modelos.bitacora import Bitacora
from modelos.cliente import Cliente
from modelos.mantenimiento_transmision import MantenimientoTransmision
from modelos.orden_servicio import OrdenServicio
from modelos.reparacion_llanta import ReparacionLlanta
from modelos.servicio_mantenimiento import ServicioMantenimiento


class PruebasTaller(unittest.TestCase):
    def setUp(self):
        self.clientes, self.bicicletas, self.servicios, self.ordenes = crear_datos_demo()
        self.orden = self.ordenes[0]

    def test_no_se_puede_crear_el_servicio_abstracto(self):
        with self.assertRaises(TypeError):
            ServicioMantenimiento("S", "Sin especialidad")

    def test_una_subclase_incompleta_tampoco_se_instancia(self):
        class ServicioIncompleto(ServicioMantenimiento):
            def describir_trabajo(self):
                return "Falta la duración"
        with self.assertRaises(TypeError):
            ServicioIncompleto("S", "Sin duración")

    def test_reporte_admite_otro_servicio_sin_modificarse(self):
        class LimpiezaCuadro(ServicioMantenimiento):
            def describir_trabajo(self):
                return "Limpieza del cuadro"
            def calcular_duracion(self):
                return 9
        salida = StringIO()
        with redirect_stdout(salida):
            mostrar_reporte_servicios(self.servicios + [LimpiezaCuadro("X", "Prueba")])
        self.assertIn("Limpieza del cuadro", salida.getvalue())
        self.assertIn("Tiempo estimado: 9 minutos", salida.getvalue())
        self.assertEqual(salida.getvalue().count("Tiempo estimado:"), 7)

    def test_subclases_reutilizan_codigo_observacion_e_identificacion(self):
        for servicio in self.servicios:
            with self.subTest(codigo=servicio.get_codigo()):
                self.assertIsInstance(servicio, ServicioMantenimiento)
                self.assertIn(servicio.get_codigo(), servicio.mostrar_identificacion())
                self.assertIn(servicio.get_observacion(), servicio.mostrar_identificacion())

    def test_frenos_tiene_descripcion_y_tiempo_segun_sus_datos(self):
        casos = [("rin", 1, 12), ("rin", 2, 24), ("disco", 1, 20), ("disco", 2, 32)]
        for tipo, ruedas, tiempo in casos:
            with self.subTest(tipo=tipo, ruedas=ruedas):
                s = AjusteFrenos("F", "Ajuste", tipo, ruedas)
                self.assertEqual(s.calcular_duracion(), tiempo)
                self.assertIn(tipo, s.describir_trabajo())
                self.assertIn(str(ruedas), s.describir_trabajo())

    def test_transmision_distingue_limpieza_y_velocidades(self):
        basica = MantenimientoTransmision("T1", "Cadena", 7, False)
        profunda = MantenimientoTransmision("T2", "Cadena", 7, True)
        self.assertEqual(basica.calcular_duracion(), 29)
        self.assertEqual(profunda.calcular_duracion(), 49)
        self.assertIn("básica", basica.describir_trabajo())
        self.assertIn("profunda", profunda.describir_trabajo())
        self.assertEqual(MantenimientoTransmision("T3", "Límite", 30, False).calcular_duracion(), 75)

    def test_llanta_distingue_sistema_y_pinchazos(self):
        self.assertEqual(ReparacionLlanta("L1", "Trasera", "camara", 1).calcular_duracion(), 18)
        self.assertEqual(ReparacionLlanta("L2", "Delantera", "tubeless", 2).calcular_duracion(), 36)
        self.assertIn("3 pinchazo(s)", ReparacionLlanta("L3", "Prueba", "camara", 3).describir_trabajo())

    def test_frenos_rechaza_tipo_y_cantidad_invalidos(self):
        for ruedas in (0, 3, True, 1.5, "2"):
            with self.subTest(ruedas=ruedas), self.assertRaises(ValueError):
                AjusteFrenos("F", "Prueba", "rin", ruedas)
        with self.assertRaises(ValueError):
            AjusteFrenos("F", "Prueba", "desconocido", 1)

    def test_transmision_rechaza_velocidades_y_bandera_invalidas(self):
        for velocidades in (0, 31, False, 7.0, "7"):
            with self.subTest(velocidades=velocidades), self.assertRaises(ValueError):
                MantenimientoTransmision("T", "Prueba", velocidades, True)
        for bandera in (0, 1, "sí", None):
            with self.subTest(bandera=bandera), self.assertRaises(ValueError):
                MantenimientoTransmision("T", "Prueba", 7, bandera)

    def test_llanta_rechaza_sistema_y_pinchazos_invalidos(self):
        for pinchazos in (0, 4, True, 2.5, None):
            with self.subTest(pinchazos=pinchazos), self.assertRaises(ValueError):
                ReparacionLlanta("L", "Prueba", "camara", pinchazos)
        with self.assertRaises(ValueError):
            ReparacionLlanta("L", "Prueba", "otro", 1)

    def test_servicios_rechazan_codigo_u_observacion_vacios(self):
        for codigo, observacion in [("", "Prueba"), ("F", " "), (None, "Prueba")]:
            with self.subTest(codigo=codigo), self.assertRaises(ValueError):
                AjusteFrenos(codigo, observacion, "rin", 1)

    def test_normalizacion_de_textos_y_opciones(self):
        servicio = AjusteFrenos(" F01 ", " Prueba ", " DISCO ", 2)
        self.assertEqual(servicio.get_codigo(), "F01")
        self.assertEqual(servicio.get_observacion(), "Prueba")
        self.assertEqual(servicio.get_tipo_freno(), "disco")

    def test_contacto_valido_actualiza_ambos_datos(self):
        cliente = self.clientes[0]
        cliente.actualizar_contacto(" Ana María ", " 000-001 ")
        self.assertEqual((cliente.get_nombre(), cliente.get_telefono()), ("Ana María", "000-001"))

    def test_contacto_invalido_conserva_ambos_datos(self):
        cliente = self.clientes[0]
        anterior = (cliente.get_nombre(), cliente.get_telefono())
        for nombre, telefono in [("Nuevo", ""), (" ", "000"), (None, "000")]:
            with self.subTest(nombre=nombre), self.assertRaises(ValueError):
                cliente.actualizar_contacto(nombre, telefono)
            self.assertEqual((cliente.get_nombre(), cliente.get_telefono()), anterior)

    def test_bicicleta_conserva_el_objeto_propietario(self):
        self.assertIs(self.bicicletas[0].get_propietario(), self.clientes[0])
        self.clientes[0].actualizar_contacto("Nuevo nombre", "000")
        self.assertIn("Nuevo nombre", self.bicicletas[0].mostrar_informacion())

    def test_asociaciones_rechazan_textos_en_lugar_de_objetos(self):
        with self.assertRaises(ValueError):
            Bicicleta("B", "Marca", "Modelo", "C01")
        with self.assertRaises(ValueError):
            OrdenServicio("O", "B01")

    def test_constructores_rechazan_datos_vacios(self):
        with self.assertRaises(ValueError):
            Cliente("", "Ana", "000")
        with self.assertRaises(ValueError):
            Bicicleta("B", " ", "Modelo", self.clientes[0])
        with self.assertRaises(ValueError):
            OrdenServicio(" ", self.bicicletas[0])
        with self.assertRaises(ValueError):
            Bitacora("")

    def test_orden_inicia_abierta_vacia_y_con_bitacora(self):
        self.assertEqual(self.orden.get_estado(), "abierta")
        self.assertEqual(self.orden.get_servicios(), ())
        self.assertEqual(self.orden.calcular_duracion_total(), 0)
        self.assertEqual(self.orden.consultar_movimientos(), ("Orden abierta.",))
        self.assertIs(self.orden.get_bicicleta(), self.bicicletas[0])

    def test_agregar_conserva_los_objetos_y_suma_sus_duraciones(self):
        for servicio in self.servicios[:3]:
            self.orden.agregar_servicio(servicio)
        self.assertIs(self.orden.get_servicios()[0], self.servicios[0])
        self.assertEqual(self.orden.calcular_duracion_total(), 99)
        self.assertEqual(len(self.orden.consultar_movimientos()), 4)

    def test_duplicado_no_cambia_servicios_tiempo_ni_bitacora(self):
        self.orden.agregar_servicio(self.servicios[0])
        anterior = (self.orden.get_servicios(), self.orden.consultar_movimientos())
        with self.assertRaises(ServicioDuplicadoError):
            self.orden.agregar_servicio(self.servicios[0])
        self.assertEqual((self.orden.get_servicios(), self.orden.consultar_movimientos()), anterior)
        self.assertEqual(self.orden.calcular_duracion_total(), 32)

    def test_duplicado_se_detecta_por_codigo_aunque_sea_otro_objeto(self):
        self.orden.agregar_servicio(self.servicios[0])
        with self.assertRaises(ServicioDuplicadoError):
            self.orden.agregar_servicio(ReparacionLlanta("F01", "Otro objeto", "camara", 1))

    def test_no_se_agregan_objetos_ajenos_al_dominio(self):
        for invalido in ("F01", self.clientes[0], None):
            with self.subTest(valor=invalido), self.assertRaises(ValueError):
                self.orden.agregar_servicio(invalido)
        self.assertEqual(self.orden.get_servicios(), ())
        self.assertEqual(len(self.orden.consultar_movimientos()), 1)

    def test_retiro_devuelve_objeto_recalcula_tiempo_y_registra(self):
        self.orden.agregar_servicio(self.servicios[0])
        self.orden.agregar_servicio(self.servicios[1])
        self.assertIs(self.orden.retirar_servicio(" F01 "), self.servicios[0])
        self.assertEqual(self.orden.calcular_duracion_total(), 49)
        self.assertEqual(self.orden.consultar_movimientos()[-1], "Servicio retirado: F01.")

    def test_retiro_inexistente_conserva_estado_y_permite_otra_operacion(self):
        anterior = self.orden.consultar_movimientos()
        with self.assertRaises(ServicioNoEncontradoError):
            self.orden.retirar_servicio("S99")
        self.assertEqual(self.orden.consultar_movimientos(), anterior)
        self.orden.agregar_servicio(self.servicios[0])
        self.assertEqual(len(self.orden.get_servicios()), 1)

    def test_retirar_codigo_vacio_no_modifica_la_orden(self):
        with self.assertRaises(ValueError):
            self.orden.retirar_servicio(" ")
        self.assertEqual(self.orden.get_servicios(), ())
        self.assertEqual(len(self.orden.consultar_movimientos()), 1)

    def test_servicio_retirado_puede_agregarse_nuevamente(self):
        self.orden.agregar_servicio(self.servicios[0])
        retirado = self.orden.retirar_servicio("F01")
        self.orden.agregar_servicio(retirado)
        self.assertEqual(len(self.orden.get_servicios()), 1)

    def test_cierre_vacio_no_cambia_estado_y_permite_recuperacion(self):
        with self.assertRaises(OrdenSinServiciosError):
            self.orden.cerrar()
        self.assertEqual(self.orden.get_estado(), "abierta")
        self.assertEqual(len(self.orden.consultar_movimientos()), 1)
        self.orden.agregar_servicio(self.servicios[0])
        self.orden.cerrar()
        self.assertEqual(self.orden.get_estado(), "cerrada")

    def test_cierre_valido_conserva_servicios_y_registra_cierre(self):
        self.orden.agregar_servicio(self.servicios[0])
        self.orden.cerrar()
        self.assertEqual(self.orden.get_estado(), "cerrada")
        self.assertEqual(self.orden.calcular_duracion_total(), 32)
        self.assertEqual(self.orden.consultar_movimientos()[-1], "Orden cerrada.")

    def test_cerrada_rechaza_alta_retiro_y_segundo_cierre_sin_cambios(self):
        self.orden.agregar_servicio(self.servicios[0])
        self.orden.cerrar()
        anterior = (self.orden.get_servicios(), self.orden.consultar_movimientos())
        operaciones = [lambda: self.orden.agregar_servicio(self.servicios[1]),
                       lambda: self.orden.retirar_servicio("F01"), self.orden.cerrar]
        for operacion in operaciones:
            with self.assertRaises(OrdenCerradaError):
                operacion()
            self.assertEqual((self.orden.get_servicios(), self.orden.consultar_movimientos()), anterior)

    def test_consultas_no_exponen_listas_modificables(self):
        self.orden.agregar_servicio(self.servicios[0])
        copia = list(self.orden.get_servicios())
        copia.clear()
        movimientos = list(self.orden.consultar_movimientos())
        movimientos.clear()
        self.assertEqual(len(self.orden.get_servicios()), 1)
        self.assertEqual(len(self.orden.consultar_movimientos()), 2)

    def test_bitacoras_y_colecciones_son_independientes_por_orden(self):
        self.orden.agregar_servicio(self.servicios[0])
        segunda = self.ordenes[1]
        self.assertEqual(segunda.get_servicios(), ())
        self.assertEqual(segunda.consultar_movimientos(), ("Orden abierta.",))
        self.assertIn("O01", self.orden.mostrar_bitacora())
        self.assertIn("O02", segunda.mostrar_bitacora())

    def test_bitacora_valida_movimientos_y_mantiene_orden(self):
        bitacora = Bitacora("O")
        bitacora.registrar(" Primero ")
        with self.assertRaises(ValueError):
            bitacora.registrar(" ")
        bitacora.registrar("Segundo")
        self.assertEqual(bitacora.consultar(), ("Primero", "Segundo"))
        self.assertIn("2. Segundo", bitacora.mostrar_informacion())

    def test_cada_error_tiene_una_clase_propia(self):
        clases = {ServicioDuplicadoError, ServicioNoEncontradoError,
                  OrdenSinServiciosError, OrdenCerradaError}
        self.assertEqual(len(clases), 4)
        for clase in clases:
            self.assertTrue(issubclass(clase, ErrorTaller))

    def test_main_controla_errores_y_finaliza_con_dos_ordenes(self):
        salida = StringIO()
        with redirect_stdout(salida):
            ordenes = main()
        texto = salida.getvalue()
        for nombre in ("ServicioDuplicadoError", "ServicioNoEncontradoError",
                       "OrdenSinServiciosError", "OrdenCerradaError"):
            self.assertIn("CONTROLADO - " + nombre, texto)
        self.assertEqual(texto.count("CONTINÚA:"), 6)
        self.assertEqual(texto.count("Tiempo estimado:"), 6)
        self.assertIn("FIN: ambas órdenes cerradas", texto)
        self.assertEqual([o.get_estado() for o in ordenes], ["cerrada", "cerrada"])
        self.assertEqual([o.calcular_duracion_total() for o in ordenes], [99, 81])


if __name__ == "__main__":
    unittest.main()
