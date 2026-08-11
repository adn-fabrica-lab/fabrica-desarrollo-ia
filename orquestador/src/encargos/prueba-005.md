# Encargo prueba-005

- encargo_id: prueba-005
- repositorio: fabrica-prueba-005

## Descripcion

Construir una aplicacion de "lista de tareas" con dos partes:

1. Backend NestJS (carpeta backend/) con un modulo de tareas:
   - GET /tareas: lista las tareas; acepta el filtro opcional
     ?prioridad=alta|media|baja.
   - POST /tareas: crea una tarea con {"titulo": "...", "prioridad": "media"};
     responde la tarea creada {"id": 1, "titulo": "...",
     "prioridad": "media", "completada": false}.
   - PATCH /tareas/:id/completar: marca la tarea como completada.
   - DELETE /tareas/:id: elimina la tarea.
   - Almacenamiento en memoria, sin base de datos.
2. Frontend Next.js (carpeta frontend/) con una unica pagina que lista las
   tareas (mostrando su prioridad y si estan completadas), permite crearlas,
   marcarlas como completadas, eliminarlas y filtrarlas por prioridad.

## Criterios de aceptacion

- El backend es NestJS con TypeScript, corre en el puerto 3001 y habilita
  CORS.
- La logica de tareas vive en un servicio separado del controlador.
- El servicio de tareas tiene pruebas unitarias con Jest (archivo .spec.ts)
  que cubren crear, listar (con y sin filtro), completar y eliminar;
  "npm test" pasa sin fallos.
- El package.json del backend define la configuracion de jest con
  "rootDir": "src" y transformacion con ts-jest.
- En el backend usar exactamente estas versiones (verificadas en la Fase 4):
  "@types/node": "^20.11.0", "@types/express": "^4.17.21",
  "jest": "^29.7.0", "@nestjs/schematics": "^10.1.0".
- El frontend es Next.js (App Router) con TypeScript y usa la variable de
  entorno NEXT_PUBLIC_API_URL (con default http://localhost:3001).
- El plan y el codigo del frontend DEBEN incluir frontend/app/layout.tsx
  (root layout que exporta un componente con <html> y <body>): sin ese
  archivo, "next build" falla.
- backend/ y frontend/ son proyectos npm independientes: cada uno tiene su
  package.json con script "build" y compila sin errores.
- El frontend NO define script "lint" (el lint queda fuera de este encargo).
- Usar solo versiones de dependencias publicadas y estables en package.json.
- No se necesita base de datos ni autenticacion.
