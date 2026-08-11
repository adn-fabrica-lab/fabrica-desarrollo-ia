import { Injectable } from '@nestjs/common';
import { Tarea, Prioridad } from './tarea.model';

@Injectable()
export class TareasService {
  private tareas: Tarea[] = [];
  private ultimoId = 0;

  crearTarea(titulo: string, prioridad: Prioridad): Tarea {
    const nuevaTarea: Tarea = {
      id: ++this.ultimoId,
      titulo,
      prioridad,
      completada: false,
    };
    this.tareas.push(nuevaTarea);
    return nuevaTarea;
  }

  listarTareas(prioridad?: Prioridad): Tarea[] {
    if (prioridad) {
      return this.tareas.filter(tarea => tarea.prioridad === prioridad);
    }
    return [...this.tareas];
  }

  completarTarea(id: number): Tarea {
    const tarea = this.tareas.find(t => t.id === id);
    if (!tarea) {
      throw new Error('Tarea no encontrada');
    }
    tarea.completada = true;
    return tarea;
  }

  eliminarTarea(id: number): void {
    const indice = this.tareas.findIndex(t => t.id === id);
    if (indice === -1) {
      throw new Error('Tarea no encontrada');
    }
    this.tareas.splice(indice, 1);
  }
}
