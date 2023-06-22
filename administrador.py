from tareas import Tarea
from connectionbdd import agregarFila, crearBaseDeDatos, crearTabla, traerTareaDeBDD, traerTareasDeBDD, modificarValor
import sqlite3 as sql
from fastapi import FastAPI
from fastapi import HTTPException, status
from datetime import datetime
from pydantic import BaseModel
from tkinter import messagebox
import tkinter.messagebox as messagebox
import datetime
import tkinter as tk
import requests
from flask import Response

class administradorDeTarea:
    def __init__(self, db_file:str):
        self.db = sql.connect(db_file)
        
    def agregar_tarea(self, tarea: Tarea) -> int:
        tarea_dic = tarea.tarea_dict()
        conn = sql.connect('tareas.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO tareas (id, titulo, descripcion, estado, creada, actualizada)
                        VALUES (?, ?, ?, ?, ?, ?)""", tuple(tarea_dic.values()))
        tarea_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea_id

    def traer_tarea(self, tarea_id: int) -> Tarea:
        tarea=traerTareaDeBDD(tarea_id)
        if tarea:
            return Tarea(*tarea)
        else:
            return None
        
    def id_repetido(self, id):
        conexion = sql.connect('tareas.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        ids = resultado[0]
        conexion.close()
        return ids

    def traer_todas_tareas(self):
        conn = sql.connect('tareas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas")
        tareas = cursor.fetchall()
        conn.close()
        todas_tareas = ""
        for tarea in tareas:
            tarea = Tarea(*tarea)
            todas_tareas += f"ID: {tarea.id}\nTítulo: {tarea.titulo}\nDescripción: {tarea.descripcion}\nEstado: {tarea.estado}\n\n"
        return todas_tareas
    
    def actualizar_estado_tarea(self, tarea_id: int, estado: str, actualizada:str):
        conn = sql.connect('tareas.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET estado=?, actualizada=? WHERE id=?", (estado, actualizada, tarea_id))
        conn.commit()
        conn.close()


    def eliminar_tarea(self, tarea_id: int):
        if tarea_id is None:
            raise ValueError("El ID de la tarea no puede ser nulo")

        conn = sql.connect('tareas.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM tareas WHERE id=?", (tarea_id,))
        tarea = cursor.fetchone()

        if tarea:
            tarea_eliminada_id = tarea[0]
            cursor.execute("DELETE FROM tareas WHERE id=?", (tarea_id,))
            conn.commit()
            conn.close()
            return tarea_eliminada_id
        else:
            conn.close()
            raise HTTPException(status_code=404, detail="No se encontró la tarea")
        