from basededatos import crearDB, crearTabla
from interfaz import VentanaPrincipal
from administrador import administradorTarea
from tareas import Tarea
from fastapi import FastAPI
from pydantic import BaseModel
from administrador import administradorTarea
from tareas import Tarea
from basededatos import crearDB, crearTabla
from fastapi import FastAPI, HTTPException, status
import datetime
import tkinter as tk
from tkinter import messagebox
import requests
class tareaApi(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    creada: str | None
    actualizada: str | None

app = FastAPI()

administrador = administradorTarea('tareas.db')
@app.post('/tarea')
def insertar_tarea(tarea:tareaApi):
    tarea_dict = dict(tarea)
    tarea_objeto = Tarea(**tarea_dict)
    if administrador.buscar_id_repetido(tarea_objeto.id):
        raise HTTPException(status_code=409, detail="Error: El ID de la tarea ya está repetido.")
    
    try:
        administrador.agregar_tarea(tarea_objeto)
        return tarea_objeto
    except Exception as e:
        raise HTTPException(status_code=422, detail="Error al insertar la tarea: " + str(e))

@app.delete("/tarea/{id}")
def eliminar_tarea_endpoint(id: int):
    
    if id is None:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Se requiere un ID de tarea")

    tarea_id = administrador.eliminar_tarea(id)

    if tarea_id is not None:
        return {"mensaje": f"Tarea con ID {tarea_id} eliminada"}
    else:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")

@app.put('/tarea/{id}/{estado}')
def actualizarestado_api(id:int, estado:str):
    tarea_actual = administrador.traer_tarea(id)
    if tarea_actual:
        tarea_actual.estado = estado
        tarea_actual.actualizada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        administrador.actualizar_estado_tarea(tarea_actual.id, tarea_actual.estado, tarea_actual.actualizada)
        return {"mensaje": f"Tarea con id {id} actualizada"}
    else:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")

@app.get('/tarea/{id}')
def traertarea_api(id: int):
    tarea = administrador.traer_tarea(id)
    
    if tarea:
        return tarea
    else:
         raise HTTPException(status_code=404, detail="No se encontró la tarea con ese id")
# from fastapi import FastAPI

# app = FastAPI()
if __name__ == "__main__":
    crearDB('tareas.db')
    crearTabla()
    ventana = VentanaPrincipal()
    ventana.mainloop()
    # administrador.buscar_id_repetido(1)