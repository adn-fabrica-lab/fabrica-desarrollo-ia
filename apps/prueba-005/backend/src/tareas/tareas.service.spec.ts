import { Test, TestingModule } from '@nestjs/testing';
import { TareasService } from './tareas.service';
import { Prioridad } from './tarea.model';

describe('TareasService', () => {
  let service: TareasService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [TareasService],
    }).compile();

    service = module.get<TareasService>(TareasService);
  });

  it('debería estar definido', () => {
    expect(service).toBeDefined();
  });

  describe('crearTarea', () => {
    it('debería crear una nueva tarea', () => {
      const tarea = service.crearTarea('Test Tarea', 'media');
      expect(tarea).toHaveProperty('id');
      expect(tarea.titulo).toBe('Test Tarea');
      expect(tarea.prioridad).toBe('media');
      expect(tarea.completada).toBe(false);
    });
  });

  describe('listarTareas', () => {
    beforeEach(() => {
      service.crearTarea('Tarea 1', 'alta');
      service.crearTarea('Tarea 2', 'media');
      service.crearTarea('Tarea 3', 'baja');
    });

    it('debería devolver todas las tareas sin filtro', () => {
      const tareas = service.listarTareas();
      expect(tareas.length).toBe(3);
    });

    it('debería filtrar tareas por prioridad', () => {
      const tareas = service.listarTareas('alta');
      expect(tareas.length).toBe(1);
      expect(tareas[0].prioridad).toBe('alta');
    });
  });

  describe('completarTarea', () => {
    it('debería marcar una tarea como completada', () => {
      const tarea = service.crearTarea('Test Tarea', 'media');
      const tareaCompletada = service.completarTarea(tarea.id);
      expect(tareaCompletada.completada).toBe(true);
    });

    it('debería lanzar error si la tarea no existe', () => {
      expect(() => service.completarTarea(999)).toThrowError('Tarea no encontrada');
    });
  });

  describe('eliminarTarea', () => {
    it('debería eliminar una tarea existente', () => {
      const tarea = service.crearTarea('Test Tarea', 'media');
      service.eliminarTarea(tarea.id);
      expect(service.listarTareas().length).toBe(0);
    });

    it('debería lanzar error si la tarea no existe', () => {
      expect(() => service.eliminarTarea(999)).toThrowError('Tarea no encontrada');
    });
  });
});