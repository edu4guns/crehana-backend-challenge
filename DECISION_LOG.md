DECISION_LOG

Durante el desarrollo del ejercicio intenté mantener un balance entre claridad, pragmatismo y tiempo disponible (4–6 horas).
Estas son algunas decisiones técnicas relevantes y el razonamiento detrás de ellas.

## Arquitectura del proyecto

Decidí separar el proyecto en capas (`domain`, `application`, `infrastructure`, `api`). He trabajado con este tipo de estructura antes y suele funcionar bien cuando el proyecto empieza a crecer, porque evita que la lógica de negocio quede mezclada con el framework o con el ORM.

También consideré hacer algo más simple (por ejemplo dejar todo en routers de FastAPI), que probablemente habría sido más rápido para este ejercicio. Aun así preferí mantener una separación mínima para que la lógica sea más fácil de testear y evolucionar.

## Base de datos

Opté por PostgreSQL para la aplicación y SQLite en memoria para los tests.

En mi experiencia Postgres es una base muy estable y común en entornos productivos, por lo que me pareció una buena opción para simular un entorno más realista. Para los tests preferí SQLite porque permite ejecutar todo muy rápido sin depender de levantar servicios externos.

También consideré usar solo SQLite para simplificar aún más el entorno, pero preferí mantener Postgres para la ejecución normal del proyecto.

## ORM

Elegí SQLAlchemy (versión 2.x). Es una herramienta con la que he trabajado bastante y me resulta cómoda para modelar entidades y consultas sin perder demasiado control sobre lo que ocurre en la base de datos.

Existen ORMs más “automáticos” o frameworks que abstraen más cosas, pero en general SQLAlchemy sigue siendo una opción bastante estándar en proyectos Python.

## Modelado del dominio

Separé los modelos de dominio de los schemas de la API (Pydantic). Esto agrega un poco más de código, pero ayuda a mantener claro qué pertenece al dominio y qué es solo un contrato de entrada/salida de la API.

En proyectos pequeños muchas veces se mezclan ambos modelos, pero cuando el sistema crece esa separación suele ayudar bastante.

## Estados y prioridades

Utilicé enums para estados de tarea y prioridad. En mi experiencia esto evita errores comunes de strings y hace que el dominio sea más explícito.

## `completion_percentage`

El porcentaje de completitud de una lista no se guarda en la base de datos; se calcula cuando se consulta la lista.

Lo pensé como un dato derivado y preferí no persistirlo para evitar inconsistencias si el estado de las tareas cambia.

## Autenticación

Agregué autenticación básica con JWT como funcionalidad extra. El objetivo era demostrar cómo proteger endpoints y manejar login de usuarios.

No implementé refresh tokens ni roles para mantener el alcance acotado al tiempo del ejercicio.

## Notificaciones

Cuando se asigna una tarea a un usuario se simula el envío de una notificación usando `BackgroundTasks` de FastAPI.

La idea fue mostrar cómo desacoplar este tipo de trabajo del request HTTP sin introducir infraestructura adicional (colas de mensajes o servicios de correo).

En un sistema real probablemente lo movería a una cola o a un sistema de eventos.

## Testing

Intenté cubrir principalmente la lógica de servicios y algunos flujos principales de la API.

El objetivo fue mantener una cobertura razonable (en torno al 75% que plantea el enunciado) sin dedicar demasiado tiempo a cubrir todos los edge cases posibles.

## Docker

Incluí Docker y docker-compose para que el proyecto se pueda levantar fácilmente sin instalar dependencias localmente.

La configuración es bastante simple y está pensada más para facilitar la evaluación del ejercicio que para un despliegue productivo.

## Qué mejoraría con más tiempo

Si este proyecto evolucionara más allá del ejercicio probablemente agregaría:

- migraciones con Alembic
- validaciones de negocio más estrictas
- logging más estructurado
- mejores políticas de seguridad para autenticación
