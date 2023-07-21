from interfaz import VentanaPrincipal
from administrador import administradorTarea
from api import User
from basededatos import crearTabla, crearDB
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from administrador import administradorTarea
from tareas import Tarea
from datetime import datetime, timedelta
from uvicorn import Config, Server
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api import app
import threading

app
def iniciar_ventana():
    ventana = VentanaPrincipal()
    ventana.mainloop()

def iniciar_servidor():
    config = Config(app="main:app", host="0.0.0.0", port=8000, reload=True)
    server = Server(config)
    server.run()

if __name__ == "__main__":
    ventana_thread = threading.Thread(target=iniciar_ventana)
    servidor_thread = threading.Thread(target=iniciar_servidor)

    servidor_thread.start()
    ventana_thread.start()
#    administrador = administradorTarea('admintareas.db')
#    usuario = User(username="pato", password="pato23", ultimoAcesso=None)
#    miembro = administrador.buscarUser(usuario.username)
#    print(miembro[0])
