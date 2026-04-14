# Documento Técnico: Análisis de Monolitos

## Parte 2 - Identificación de problemas (Basado en la Versión 1)

**1. ¿Dónde hay alto acoplamiento?**
Se puede identificar un acoplamiento patológico y de control en casi todos los puntos de integración:
- **Compartición de Datos Globales:** Ambos módulos (`crear_pedido` y `procesar_pago`) leen y modifican la base de datos `db` directamente (rompiendo el encapsulamiento).
- **Control Directo:** `crear_pedido` sabe que los usuarios son un diccionario con las llaves `id` y `activo`, por ende depende de su estructura interna.
- **Acoplamiento de Contenido:** `procesar_pago` directamente restringe el dinero modificando la entrada del diccionario `usuario["balance"] -= ...` en vez de pedirle al módulo de usuarios que realice la transacción, y modifica el pedido a mano (`pedido["estado"] = "PAGADO"`).

**2. ¿Qué ocurre si cambia la lógica de pagos?**
Si la lógica de pagos requiere de una pasarela externa o de congelar el saldo antes de aprobarlo:
- Se tendría que modificar la macrofunción `procesar_pago`, lo que incrementa el riesgo de romper la lógica de búsquedas o modificación de pedidos.
- Si el método decide reintentar asíncronamente, los estados de pedido (`PAGADO`, `RECHAZADO`) deberán actualizarse en múltiples lugares, lo que genera un código difícil de mantener y propenso a errores.

**3. ¿Qué tan fácil es modificar el sistema?**
Es sumamente difícil y restrictivo. Cambiar el tipo de dato subyacente (ej: de un diccionario en memoria a una base MySQL o MongoDB) implicaría reestructurar por completo la aplicación y reescribir todas las búsquedas. Cualquier otro cambio en la estructura de los datos de `usuarios` afectará directamente la creación de pedidos.

**4. ¿Qué partes representan el mayor riesgo de cambio?**
Las reglas de validación ligadas a la modificación de estructuras de datos simultáneamente. En `procesar_pago`, si ocurre un error inesperado entre el descuento al usuario y el registro del pago, el usuario pierde dinero pero el sistema podría presentar una falla grave y no marcar el pedido como pagado.

---

## Parte 3 - Transformación a monolito modular (Basado en la Versión 2)

**Decisiones de Diseño**
1. **Patrón Servicio-Repositorio:** Para aislar la infraestructura de los datos (las listas en memoria), se asignaron Repositorios. Si en el futuro se quiere una Base de Datos real, solo modificamos los Repositorios, nunca la lógica de negocio.
2. **Inyección de Dependencias:** El `PaymentService` y `OrderService` reciben la interfaz (`UserService` y los repositorios necesarios) a través de su constructor, invirtiendo la dependencia e impulsando arquitecturas más abstractas.

**Mejoras Logradas**
- Alta Cohesión: La lógica contable del saldo está centralizada en `UserService.process_transaction()`. Los demás servicios simplemente delegan la responsabilidad mediante llamadas, desconociendo cómo se gestiona internamente el descuento.
- Encapsulamiento Fuerte: Por ejemplo, los repositorios ahora devuelven copias `dict(u)` en lugar del tipo de referencia, por lo tanto si un servicio sin permisos modifica un dict, la base de datos no es mutada accidentalmente.

**Trade-offs (Desventajas) Introducidas**
- **Mayor Verbocidad y Boilerplate:** Es necesario definir clases adicionales, constructores e instancias. Esto demanda más tiempo de desarrollo inicial en comparación con un script único altamente acoplado.
- **Llamadas Adicionales:** Pasamos de validaciones condicionales directas a un flujo que atraviesa capas de Control -> Servicio -> Repositorio, añadiendo complejidad al seguimiento del código.

---

## Pregunta Obligatoria

**¿Su solución realmente reduce el acoplamiento o solo reorganiza el código?**

*La solución efectivamente reduce el acoplamiento.* No consiste únicamente en una reorganización de variables en distintos archivos, sino que **se restringe radicalmente la visibilidad que cada módulo tiene sobre los datos de los demás**.
En la Versión 1, el módulo de pagos conocía exactamente cómo se estructuraba el registro de un usuario (y sus tipos de datos, llaves e iteraciones directas). En la Versión 2, el módulo de pagos **ignora por completo** cómo el módulo de usuarios gestiona los saldos o si usa listas o SQL; solo conoce su firma `process_transaction()`. Esta es una verdadera reducción de acoplamiento.
