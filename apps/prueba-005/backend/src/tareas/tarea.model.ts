export interface Tarea {
  id: number;
  titulo: string;
  prioridad: 'alta' | 'media' | 'baja';
  completada: boolean;
}

export type Prioridad = 'alta' | 'media' | 'baja';

export type CrearTareaDto = Omit<Tarea, 'id' | 'completada'>;

export type ActualizarTareaDto = Partial<Omit<Tarea, 'id'>>;