from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\ALAIN\Documents\rubrica\TasksDB.accdb;')

def obtener_datos():
    cursor = conn.cursor()

    query = 'SELECT * FROM Tareas'

    cursor.execute(query)
    data = cursor.fetchall()
    print(data)
        
    return data
@app.route('/')
def index():
    data = obtener_datos() 
    return render_template('index.html', data=data)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        estado = request.form['estado']

        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tareas (descripcion, estado) VALUES (?, ?)", (descripcion, estado))
        conn.commit()
        return redirect(url_for('index'))
    
    return render_template('agregar.html')

@app.route('/marcador/<int:id>', methods=['POST','GET'])
def marcador(id):
    cursor = conn.cursor()
    cursor.execute("UPDATE Tareas SET estado = 'Completada' WHERE id = ?", (id))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/eliminar_tarea/<int:id>', methods=['POST','GET'])
def eliminar_tarea(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tareas WHERE id = ?", (id))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)