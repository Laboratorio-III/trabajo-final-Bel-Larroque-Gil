import sqlite3 as sql
from tareas import Tarea
import datetime

def crearBaseDeDatos(db_file):
    conn = sql.connect(db_file)
    conn.commit()
    conn.close()

def crearTabla():
    conn = sql.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER,
            titulo TEXT,
            descripcion TEXT,
            estado TEXT,
            creada TEXT,
            actualizada TEXT)""")
    conn.commit()
    conn.close()

def agregarFila(tarea:Tarea):
        conn = sql.connect('tareas.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO tareas (id, titulo, descripcion, estado, creada, actualizada)
                          VALUES (?, ?, ?, ?, ?, ?)""", tuple(tarea.values()))
        tarea_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea_id
 
        
def traerTareaDeBDD(id):
    conn = sql.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id=?"
    ,(id,))
    tarea = cursor.fetchone()
    conn.commit()
    conn.close()
    return tarea

def traerTareasDeBDD():
    conn = sql.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas"
    )
    tareas = cursor.fetchall()
    conn.commit()
    conn.close()

    return tareas



def modificarValor(id, estado, actualizada):
    conn = sql.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas SET estado=?, actualizada=? WHERE id=?", (estado, actualizada, id))
    conn.commit()