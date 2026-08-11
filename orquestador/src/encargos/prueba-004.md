# Encargo prueba-004

- encargo_id: prueba-004
- repositorio: fabrica-prueba-004

## Descripcion

Construir una mini aplicacion de "notas rapidas" con dos partes:

1. Backend NestJS (carpeta backend/) con un modulo de notas:
   - GET /notas: lista las notas (almacenadas en memoria, sin base de datos).
   - POST /notas: crea una nota con {"texto": "..."}; responde la nota
     creada {"id": 1, "texto": "..."}.
   - DELETE /notas/:id: elimina la nota.
2. Frontend Next.js (carpeta frontend/) con una unica pagina que lista,
   crea y elimina notas.

## Criterios de aceptacion

- El backend es NestJS con TypeScript, corre en el puerto 3001 y habilita
  CORS.
- La logica de notas vive en un servicio separado del controlador.
- El servicio de notas tiene pruebas unitarias con Jest (archivo .spec.ts)
  que cubren crear, listar y eliminar; "npm test" pasa sin fallos.
- El package.json del backend define la configuracion de jest con
  "rootDir": "src" y transformacion con ts-jest (sin ese bloque, jest no
  entiende TypeScript y las pruebas fallan).
- El frontend es Next.js (App Router) con TypeScript y usa la variable de
  entorno NEXT_PUBLIC_API_URL (con default http://localhost:3001).
- backend/ y frontend/ son proyectos npm independientes: cada uno tiene su
  package.json con script "build" y compila sin errores.
- El frontend NO define script "lint" (el lint queda fuera de este encargo).
- Usar solo versiones de dependencias publicadas y estables en package.json.
- No se necesita base de datos ni autenticacion.
- backend/package.json debe fijar en devDependencies exactamente estas versiones:
  "@types/node": "^20.11.0", "@types/express": "^4.17.21",
  "jest": "^29.7.0", "@nestjs/schematics": "^10.1.0".
- IMPORTANTE: el objeto "scripts" de frontend/package.json no debe contener
  la clave "lint" bajo ninguna circunstancia, ni siquiera si la plantilla
  base la incluye por defecto.

## Requisitos tecnicos adicionales (aprendidos de pruebas anteriores)

- El modulo de notas del backend debe llamarse "notes" en ingles unicamente (notes.controller.ts, notes.service.ts, notes.module.ts, notes.service.spec.ts dentro de backend/src/notes). No crear ningun archivo ni carpeta en espanol como "notas".
- El frontend con Next.js App Router debe incluir frontend/app/layout.tsx ademas de frontend/app/page.tsx.
- En backend/package.json usar exactamente estas versiones compatibles de NestJS 10:
  dependencies: "@nestjs/common": "^10.3.0", "@nestjs/core": "^10.3.0", "@nestjs/platform-express": "^10.3.0", "reflect-metadata": "^0.2.0", "rxjs": "^7.8.1"
  devDependencies: "@nestjs/cli": "^10.3.0", "@nestjs/schematics": "^10.1.0", "@nestjs/testing": "^10.3.0", "@types/express": "^4.17.21", "@types/jest": "^29.5.11", "@types/node": "^20.11.0", "jest": "^29.7.0", "ts-jest": "^29.1.1", "typescript": "^5.3.3"
