# Taller Arquitectura Monolítica

Integrantes: Marlon Delgado, Edward Fonseca

Este repositorio resuelve el taller práctico comparando un monolito altamente acoplado y uno modularizado.

## Estructura del Repositorio

- `version_1_acoplado/`
  - Contiene el script `main.py`, un sistema funcional pero con alto nivel de acoplamiento. La lógica de usuarios, pedidos y pagos está completamente entrelazada. Modifica estructuras de datos de otras partes directa e indebidamente.

- `version_2_modular/`
  - Contiene la refactorización arquitectónica.
  - Dividido en dominios: `users`, `orders` y `payments`.
  - Cada dominio tiene su propia lógica de servicio (reglas de negocio) y repositorio (manejo de datos).
  - Interactúan exclusivamente por medio de interfaces definidas en los servicios.

- `Documento_Tecnico.md`
  - Incluye el análisis, identificación de acoplamiento y respuestas teóricas a las exigencias del taller.

## Ejecución

El código fue escrito empleando Python, utilizando estructuras de datos en memoria para mantener el foco en el acoplamiento arquitectónico en lugar de en la gestión de una base de datos externa.

**Prueba Versión 1 (Acoplada):**
```bash
python version_1_acoplado/main.py
```

**Prueba Versión 2 (Modular):**
```bash
python version_2_modular/main.py
```

Al observarlos, ambos producirán el mismo resultado (lógica idéntica), pero la diferencia radica en la organización interna y la mantenibilidad.
