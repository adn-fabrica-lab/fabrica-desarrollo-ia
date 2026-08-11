# Encargo prueba-003

- encargo_id: prueba-003
- repositorio: fabrica-prueba-003

## Descripcion

Construir una mini aplicacion de "registro de tareas" con dos partes:

1. Backend NestJS (carpeta backend/) con un modulo de tareas:
   - GET /tareas: lista las tareas (almacenadas en memoria, sin base de datos).
   - POST /tareas: crea una tarea con {"titulo": "..."}; responde la tarea
     creada {"id": 1, "titulo": "...", "completada": false}.
   - PATCH /tareas/:id/completar: marca la tarea como completada.
   - GET /tareas/resumen: responde {"total": n, "completadas": n,
     "pendientes": n}.
2. Frontend Next.js (carpeta frontend/) con una unica pagina que:
   - Lista las tareas y muestra el resumen.
   - Permite crear una tarea con un formulario simple.
   - Permite marcar una tarea como completada con un boton.

## Criterios de aceptacion

- El backend es NestJS con TypeScript, corre en el puerto 3001 y habilita
  CORS.
- La logica de tareas vive en un servicio separado del controlador.
- El servicio de tareas tiene pruebas unitarias con Jest (archivo .spec.ts)
  que cubren crear, completar y el resumen; "npm test" pasa sin fallos.
- El frontend es Next.js (App Router) con TypeScript y usa la variable de
  entorno NEXT_PUBLIC_API_URL (con default http://localhost:3001).
- backend/ y frontend/ son proyectos npm independientes: cada uno tiene su
  package.json con script "build" y compila sin errores.
- Usar solo versiones de dependencias publicadas y estables en package.json.
- No se necesita base de datos ni autenticacion.
