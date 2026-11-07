# Órdenes de mantenimiento de bicicletas

Proyecto final de **Programación I**, Universidad de Manizales.

**Estudiante responsable:** Hernan Felipe Astudillo Peña (`feliastu`).

**Modalidad:** individual. **Actividad:** colaborativa 3.

**Repositorio:** https://github.com/feliastu/programacion-i-proyecto-final-bicicletas

El sistema registra bicicletas y sus propietarios, reúne los servicios de cada
orden, calcula la duración estimada y conserva una bitácora. Controla duplicados,
retiros inexistentes y cierres inválidos. El contexto es un taller de mantenimiento;
no administra ventas, inventario comercial, bibliotecas ni información académica.

## Ejecución

Requiere **Python 3.10 o superior** y solo utiliza su biblioteca estándar.
Descargar el proyecto con **Code > Download ZIP**, descomprimirlo y abrir una
terminal en la carpeta que contiene `main.py`. En Windows:

```powershell
py main.py
py -m unittest discover -s pruebas -v
```

En Linux o macOS, usar `python3` en lugar de `py`. No se instala nada con `pip`.
La demostración es automática, no solicita datos por teclado y no necesita internet.
El resultado comprobado es **34 pruebas, OK**, con Python 3.12.14.

## Qué demuestra el programa

`main.py` crea **14 objetos**: dos clientes, dos bicicletas, seis servicios,
dos órdenes y dos bitácoras construidas dentro de las órdenes. Actualiza un
contacto, rechaza un contacto inválido y comprueba la prohibición de instanciar
el servicio abstracto. Después muestra los seis servicios mediante un solo ciclo.

La demostración añade y retira servicios, controla las cuatro excepciones del
taller y continúa después de cada captura. Termina con las dos órdenes cerradas:
O01 conserva tres servicios y 99 minutos estimados; O02, tres servicios y 81 minutos.
La bitácora de O01 contiene siete movimientos y la de O02 contiene cinco.

## Requisitos y ubicación

| Requisito | Implementación |
| --- | --- |
| Al menos seis clases concretas | Siete: Cliente, Bicicleta, AjusteFrenos, MantenimientoTransmision, ReparacionLlanta, OrdenServicio y Bitacora |
| Una clase abstracta | ServicioMantenimiento, con dos métodos abstractos |
| Tres especializaciones | AjusteFrenos, MantenimientoTransmision y ReparacionLlanta |
| Encapsulamiento | Atributos privados, consultas y operaciones con validación |
| Dos métodos sobrescritos | describir_trabajo() y calcular_duracion() en las tres hijas |
| Polimorfismo | mostrar_reporte_servicios() recorre la lista heterogénea sin condicionales por tipo |
| Relaciones entre objetos | Bicicleta–Cliente, OrdenServicio–Bicicleta y OrdenServicio–ServicioMantenimiento |
| Composición | Cada OrdenServicio crea y administra su Bitacora |
| Excepciones propias | Cuatro clases específicas en excepciones.py |
| Objetos y ejecución integrada | 14 objetos y casos normales y excepcionales en main.py |
| UML | docs/UML.md, vistas SVG/PNG y fuentes DOT/Mermaid |
| Documento técnico | docs/Decisiones_Diseno_AC3.pdf y .docx; versión Markdown disponible |

## Organización

- `main.py`: datos ficticios, reporte polimórfico y demostración completa.
- `modelos/`: una clase por archivo y funciones comunes en `validaciones.py`.
- `excepciones.py`: base ErrorTaller y cuatro excepciones del dominio.
- `pruebas/test_taller.py`: 34 pruebas de comportamiento e integración.
- `docs/`: diseño, UML, instrucciones, matriz de pruebas y salidas reales.

## Decisiones del modelo

`ServicioMantenimiento` es abstracta porque no existe una duración ni una descripción
única para un trabajo sin especialidad. Los tres servicios reutilizan código,
observación y `mostrar_identificacion()`, e implementan los dos métodos abstractos
con sus propios datos. Un ajuste de frenos **es un** servicio de mantenimiento.

El reporte no selecciona por tipo:

```python
for servicio in servicios:
    print(servicio.mostrar_identificacion())
    print(servicio.describir_trabajo())
    print("Tiempo estimado:", servicio.calcular_duracion(), "minutos\n")
```

Los condicionales de cada servicio aplican sus reglas internas; los controles
`isinstance()` validan asociaciones, no deciden qué método ejecutar en el reporte.

La orden **tiene una** bitácora creada en su constructor. Esta relación es
composición porque la orden organiza y administra ese registro propio. Heredar
de Bitacora expresaría incorrectamente que una orden es un registro de movimientos.
Los clientes, bicicletas y servicios llegan como objetos existentes y se asocian.

Los códigos y la configuración de cada servicio no tienen setters. Las listas
internas se consultan mediante tuplas; esto protege las colecciones y mantiene las
referencias a sus objetos. `actualizar_contacto()` valida ambos valores antes de
asignar. La duración total se calcula desde los servicios, sin un contador duplicado.

## Reglas de duración

Son **supuestos didácticos**, no tiempos profesionales ni instrucciones de reparación.

| Servicio | Regla en minutos | Datos aceptados |
| --- | --- | --- |
| AjusteFrenos | 12 por rueda, más 8 si es de disco | Tipo rin/disco; 1 o 2 ruedas |
| MantenimientoTransmision | 15 base, más 2 por velocidad y 20 si la limpieza es profunda | 1 a 30 velocidades; indicador True/False |
| ReparacionLlanta | 10 base, más 8 por pinchazo y 10 si es tubeless | Sistema camara/tubeless; 1 a 3 pinchazos |

Se rechazan textos vacíos, valores fuera de rango y booleanos cuando se requieren
cantidades enteras. Las opciones se normalizan a minúsculas. Los códigos conservan
mayúsculas/minúsculas y se comparan tras eliminar espacios externos.

## Excepciones

| Clase | Dónde se lanza | Situación |
| --- | --- | --- |
| ServicioDuplicadoError | agregar_servicio() | Código ya presente en esa orden |
| ServicioNoEncontradoError | retirar_servicio() | Código ausente de esa orden |
| OrdenSinServiciosError | cerrar() | Orden abierta sin servicios |
| OrdenCerradaError | verificar_abierta(), invocado antes de agregar, retirar o cerrar | Orden ya cerrada |

Las cuatro heredan de ErrorTaller y esta de Exception. El programa principal
captura cada clase, muestra el motivo y continúa. Una operación rechazada no
modifica los servicios, el estado, la duración ni los movimientos registrados.

## Documentación y entrega

- [Documento de diseño en PDF](docs/Decisiones_Diseno_AC3.pdf).
- [Documento editable en Word](docs/Decisiones_Diseno_AC3.docx).
- [Lectura del diseño en GitHub](docs/DECISIONES_DISENO_AC3.md).
- [Diagrama UML y explicación de sus relaciones](docs/UML.md).
- [Pruebas y resultados](docs/PRUEBAS.md).
- [Guía para ejecutar y explicar el proyecto](docs/GUIA_DE_USO.md).
- [Aporte individual y asistencia utilizada](docs/APORTE_INDIVIDUAL.md).

El enlace de este repositorio es el entregable solicitado. Se identifica la versión
final con `Entrega_AC3` como ayuda de trazabilidad; el enunciado de AC3 no exige un
nombre específico para una etiqueta. AC1 y AC2 permanecen en su repositorio anterior.

## Alcance y asistencia

Los datos se recrean en memoria al ejecutar. El cierre es administrativo: no
certifica una reparación física. No se gestionan pagos, repuestos, agenda, usuarios,
persistencia ni unicidad global de códigos. La bitácora registra operaciones
aceptadas en orden; no es una auditoría inalterable ni incluye fechas.

Se utilizó ChatGPT para analizar requisitos, desarrollar el código, preparar y
ejecutar pruebas, generar el UML y elaborar la documentación. El documento técnico
explica las propuestas descartadas y el proceso de verificación. La revisión,
comprensión y sustentación personal corresponden al estudiante responsable.
