# Encargo prueba-002

- encargo_id: prueba-002
- repositorio: fabrica-prueba-002

## Descripcion

Construir una mini aplicacion de "estado del sistema" con dos partes:

1. Backend NestJS (carpeta backend/) con un endpoint GET /estado que
   responda el JSON {"servicio": "fabrica-prueba-002", "estado": "ok",
   "hora": "<hora actual en formato ISO 8601>"}.
2. Frontend Next.js (carpeta frontend/) con una unica pagina que consulte
   GET /estado del backend y muestre el servicio, el estado y la hora.

## Criterios de aceptacion

- El backend es NestJS con TypeScript y corre en el puerto 3001.
- El backend habilita CORS para que el frontend pueda consultarlo.
- El frontend es Next.js (App Router) con TypeScript y usa la variable de
  entorno NEXT_PUBLIC_API_URL (con default http://localhost:3001) para
  llamar al backend.
- backend/ y frontend/ son proyectos npm independientes: cada uno tiene su
  package.json con script "build" y compila sin errores.
- No se necesita base de datos ni autenticacion.
