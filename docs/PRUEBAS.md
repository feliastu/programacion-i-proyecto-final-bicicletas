# Pruebas del proyecto final

Verificación realizada el **7 de noviembre de 2026**, con Python 3.12.14:
**34 pruebas correctas** y ejecución completa de `main.py`.

| Caso | Resultado observado |
| --- | --- |
| Servicio abstracto o subclase incompleta | TypeError; no se crea una instancia incompleta |
| Seis servicios de tres clases | Descripciones y tiempos distintos: 32, 49, 18, 12, 33 y 36 minutos |
| Contacto válido e inválido | Actualización conjunta; ante error, ambos datos anteriores se conservan |
| Relaciones entre objetos | Se mantienen las referencias; un cambio de nombre se observa en la bicicleta |
| Orden nueva | Abierta, sin servicios, cero minutos y un movimiento de apertura |
| Añadir tres servicios a O01 | Tres objetos originales, 99 minutos y altas registradas |
| Duplicar un código | ServicioDuplicadoError, sin cambios en lista, duración o bitácora |
| Retirar L01 de O01 | Devuelve el objeto; el total pasa de 99 a 81 minutos |
| Retirar S99 | ServicioNoEncontradoError; después puede añadirse L01 de nuevo |
| Cerrar O02 vacía | OrdenSinServiciosError; continúa abierta y acepta servicios |
| Cerrar una orden con servicios | Estado cerrado y registro de cierre |
| Agregar, retirar o cerrar otra vez una orden cerrada | OrdenCerradaError y estado conservado |
| Consultar servicios y movimientos | Tuplas; modificar una copia no altera las colecciones internas |
| Dos órdenes | Bitácoras y listas independientes |
| Nuevo tipo de servicio en una prueba | El mismo reporte lo procesa sin cambiar su ciclo |
| Ejecución completa | Seis errores previstos capturados, seis continuaciones y dos órdenes cerradas |

Los seis errores de la demostración comprenden cuatro excepciones personalizadas,
un ValueError por contacto inválido y un TypeError por la clase abstracta.

Se probaron también límites, textos vacíos, tipos incorrectos y booleanos usados
como cantidades. Los rechazos verifican el estado posterior, no solamente que
aparezca una excepción.

## Repetir la comprobación

```powershell
py main.py
py -m unittest discover -s pruebas -v
```

En Linux o macOS usar `python3`. Evidencias guardadas:
[demostración](salida_demostracion.txt) y [suite](resultado_pruebas.txt).

La ejecución final deja O01 con tres servicios, 99 minutos y siete movimientos;
O02 con tres servicios, 81 minutos y cinco movimientos. Los tiempos obedecen a
las reglas didácticas descritas en el README.
