import { Controller, Get, Post, Body, Patch, Param, Delete, Query, HttpException, HttpStatus } from '@nestjs/common';
import { TareasService } from './tareas.service';
import { Tarea, Prioridad, CrearTareaDto } from './tarea.model';

@Controller('tareas')
export class TareasController {
  constructor(private readonly tareasService: TareasService) {}

  @Get()
  getTareas(@Query('prioridad') prioridad?: Prioridad): Tarea[] {
    return this.tareasService.listarTareas(prioridad);
  }

  @Post()
  crearTarea(@Body() crearTareaDto: CrearTareaDto): Tarea {
    return this.tareasService.crearTarea(
      crearTareaDto.titulo,
      crearTareaDto.prioridad
    );
  }

  @Patch(':id/completar')
  completarTarea(@Param('id') id: string): Tarea {
    const idNum = parseInt(id);
    try {
      return this.tareasService.completarTarea(idNum);
    } catch (error) {
      throw new HttpException('Tarea no encontrada', HttpStatus.NOT_FOUND);
    }
  }

  @Delete(':id')
  eliminarTarea(@Param('id') id: string): void {
    const idNum = parseInt(id);
    try {
      this.tareasService.eliminarTarea(idNum);
    } catch (error) {
      throw new HttpException('Tarea no encontrada', HttpStatus.NOT_FOUND);
    }
  }
}
