from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="",  
    database="atividade_python"
)

# Página inicial
@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categoria")
    categorias = cursor.fetchall()
    return render_template('index.html', categorias=categorias)

# Ver categoria
@app.route('/categoria/<int:id>')
def view_cat(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categoria WHERE id = %s", (id,))
    categoria = cursor.fetchone()
    return render_template('view_cat.html', categoria=categoria)

# Adicionar categoria
@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        cursor = db.cursor()
        cursor.execute("INSERT INTO categoria (nome, descricao) VALUES (%s, %s)", (nome, descricao))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_cat.html')

# Editar categoria
@app.route('/edit_cat/<int:id>', methods=['GET', 'POST'])
def edit_cat(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        cursor.execute("UPDATE categoria SET nome = %s, descricao = %s WHERE id = %s", (nome, descricao, id))
        db.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM categoria WHERE id = %s", (id,))
    categoria = cursor.fetchone()
    return render_template('edit_cat.html', categoria=categoria)

# Deletar categoria
@app.route('/delete_cat/<int:id>')
def delete_cat(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM categoria WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
