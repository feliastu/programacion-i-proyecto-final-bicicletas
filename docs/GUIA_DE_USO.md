# Guía de uso y preparación de la sustentación

## Ejecutar

Descargar y descomprimir el repositorio. Abrir una terminal en la carpeta de
`main.py` y ejecutar `py main.py` en Windows, o `python3 main.py` en Linux/macOS.
El programa imprime una demostración completa, sin menú ni entrada por teclado.
Cada ejecución vuelve a crear los datos ficticios.

Para repetir las 34 pruebas: `py -m unittest discover -s pruebas -v`.

## Seguir los objetos

Empezar por `crear_datos_demo()`. Un Cliente se entrega al constructor de
Bicicleta; esa misma Bicicleta se entrega a OrdenServicio. La orden crea su
Bitacora internamente. Observar la diferencia entre recibir un objeto existente
y construir una parte propia.

Después leer ServicioMantenimiento: sus atributos comunes son código y observación.
Las clases hijas llaman `super().__init__()` e incorporan sus campos particulares.
Los dos métodos abstractos obligan a cada servicio a describirse y estimar su tiempo.

## Comprender el recorrido polimórfico

En `mostrar_reporte_servicios()` se usa un solo ciclo con las mismas llamadas.
Identificar qué implementación ejecuta cada objeto. Los condicionales internos
que revisan disco, limpieza profunda o tubeless son reglas de cada servicio,
no una selección manual de clases en el reporte.

## Revisar las operaciones y errores

En OrdenServicio, agregar y retirar comienzan comprobando que la orden esté
abierta. El código duplicado se compara antes de agregar. El cierre comprueba que
exista al menos un servicio. Una excepción interrumpe ese método y se captura en
`main.py`; después el programa continúa.

Seguir O01: agrega tres servicios, rechaza un duplicado, retira L01, rechaza S99,
recupera L01 y cierra. La duración total pasa de 99 a 81 y vuelve a 99. La bitácora
incluye solo los movimientos aceptados. Comparar con O02, que inicialmente no
puede cerrarse por estar vacía y luego termina con 81 minutos.

## Preparar la explicación personal

Poder explicar por qué no se crea ServicioMantenimiento directamente, qué
información aporta cada hija y por qué OrdenServicio contiene una Bitacora en
lugar de heredar de ella. Explicar también la diferencia entre una tupla de
referencias y una copia de los objetos, y por qué los rechazos no alteran el estado.

Los tiempos y rangos son decisiones del ejemplo. No certifican la calidad de una
reparación ni reemplazan un procedimiento técnico real. El programa registra
trabajos y su cierre administrativo; no ejecuta intervenciones físicas.

## Entrega

Revisar el documento y ejecutar el proyecto. Pegar el enlace al repositorio del
proyecto final en la plataforma del curso y confirmar el envío allí. El código,
el README, el UML y el documento técnico están dentro del repositorio.
