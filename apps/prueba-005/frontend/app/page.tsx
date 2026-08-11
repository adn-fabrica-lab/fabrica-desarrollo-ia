'use client';

import { useState, useEffect } from 'react';

export default function Page() {
  const [tareas, setTareas] = useState<Array<{id: number, titulo: string, prioridad: string, completada: boolean}>>([]);
  const [filtro, setFiltro] = useState<string>('todas');
  const [nuevaTarea, setNuevaTarea] = useState<string>('');
  const [prioridadNuevaTarea, setPrioridadNuevaTarea] = useState<string>('media');

  useEffect(() => {
    cargarTareas();
  }, []);

  const cargarTareas = async () => {
    try {
      const url = filtro === 'todas' 
        ? `${process.env.NEXT_PUBLIC_API_URL}/tareas` 
        : `${process.env.NEXT_PUBLIC_API_URL}/tareas?prioridad=${filtro}`;
      
      const res = await fetch(url);
      const data = await res.json();
      setTareas(data);
    } catch (error) {
      console.error('Error cargando tareas:', error);
    }
  };

  const crearTarea = async () => {
    if (!nuevaTarea.trim()) return;
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tareas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          titulo: nuevaTarea,
          prioridad: prioridadNuevaTarea,
          completada: false
        })
      });
      
      const tareaCreada = await res.json();
      setTareas([...tareas, tareaCreada]);
      setNuevaTarea('');
    } catch (error) {
      console.error('Error creando tarea:', error);
    }
  };

  const completarTarea = async (id: number) => {
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tareas/${id}/completar`, {
        method: 'PATCH'
      });
      
      setTareas(tareas.map(t => 
        t.id === id ? { ...t, completada: true } : t
      ));
    } catch (error) {
      console.error('Error completando tarea:', error);
    }
  };

  const eliminarTarea = async (id: number) => {
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tareas/${id}`, {
        method: 'DELETE'
      });
      
      setTareas(tareas.filter(t => t.id !== id));
    } catch (error) {
      console.error('Error eliminando tarea:', error);
    }
  };

  const filtrarTareas = (filtroSeleccionado: string) => {
    setFiltro(filtroSeleccionado);
    cargarTareas();
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Lista de Tareas</h1>
      
      <div className="mb-6 bg-white p-4 rounded shadow">
        <div className="flex mb-4">
          <input
            type="text"
            value={nuevaTarea}
            onChange={(e) => setNuevaTarea(e.target.value)}
            placeholder="Nueva tarea"
            className="flex-grow p-2 border rounded-l"
          />
          <select
            value={prioridadNuevaTarea}
            onChange={(e) => setPrioridadNuevaTarea(e.target.value)}
            className="border-t border-b border-r p-2"
          >
            <option value="alta">Alta</option>
            <option value="media">Media</option>
            <option value="baja">Baja</option>
          </select>
          <button 
            onClick={crearTarea}
            className="bg-blue-500 text-white p-2 rounded-r hover:bg-blue-600"
          >
            Agregar
          </button>
        </div>
        
        <div className="flex justify-between items-center">
          <div className="flex space-x-2">
            <button 
              onClick={() => filtrarTareas('todas')}
              className={`px-3 py-1 rounded ${filtro === 'todas' ? 'bg-gray-200' : 'bg-gray-100'}`}
            >
              Todas
            </button>
            <button 
              onClick={() => filtrarTareas('alta')}
              className={`px-3 py-1 rounded ${filtro === 'alta' ? 'bg-gray-200' : 'bg-gray-100'}`}
            >
              Alta
            </button>
            <button 
              onClick={() => filtrarTareas('media')}
              className={`px-3 py-1 rounded ${filtro === 'media' ? 'bg-gray-200' : 'bg-gray-100'}`}
            >
              Media
            </button>
            <button 
              onClick={() => filtrarTareas('baja')}
              className={`px-3 py-1 rounded ${filtro === 'baja' ? 'bg-gray-200' : 'bg-gray-100'}`}
            >
              Baja
            </button>
          </div>
        </div>
      </div>
      
      <ul className="space-y-2">
        {tareas.map((tarea) => (
          <li 
            key={tarea.id} 
            className={`bg-white p-3 rounded shadow flex justify-between items-center ${tarea.completada ? 'opacity-70' : ''}`}
          >
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={tarea.completada}
                onChange={() => completarTarea(tarea.id)}
                className="mr-3"
              />
              <span className={`${tarea.completada ? 'line-through' : ''}`}>
                {tarea.titulo}
              </span>
              <span className={`ml-2 px-2 py-1 text-xs rounded-full ${
                tarea.prioridad === 'alta' ? 'bg-red-100 text-red-800' :
                tarea.prioridad === 'media' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {tarea.prioridad}
              </span>
            </div>
            <button 
              onClick={() => eliminarTarea(tarea.id)}
              className="text-red-500 hover:text-red-700"
            >
              Eliminar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}