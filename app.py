from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User


app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['nombre_usuario']
        password = request.form['contrasenha']

        user = User(0, username, password, "aux@gmail.com")
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña invalida...")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/register_user', methods=['GET','POST'])
def registerUser():
    if request.method == 'POST':
        username = request.form['nombre_usuario']
        email = request.form['correo_electronico']
        password = request.form['contrasenha']

        if username and email and password:
            user = User(0, username, password, email)
            ModelUser.createUser(db, user)
            return redirect(url_for('login'))
        
        return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))





@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/add_content')
def addContent():
    try:
        dataone = addContentOne()
        datatwo = addContentTwo()
    except Exception as ex:
        raise Exception(ex)
    return render_template('home.html', data_simp = dataone, data_comp = datatwo)

def addContentOne():
    try:
        cursor = db.connection.cursor()
        sql = """SELECT * FROM contenidos WHERE tipo='palabra_clave_simple'"""
        cursor.execute(sql)
        myresult = cursor.fetchall()
        insertObject = []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames,record)))
    except Exception as ex:
        raise Exception(ex)
    return insertObject

def addContentTwo():
    try:
        cursor = db.connection.cursor()
        sql = """SELECT * FROM contenidos WHERE tipo='palabra_clave_compue'"""
        cursor.execute(sql)
        myresult = cursor.fetchall()
        insertObject = []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames,record)))
    except Exception as ex:
        raise Exception(ex)
    return insertObject


@app.route('/edit/<string:id>',methods=['POST'])
def edit(id):
    difficult = request.form['grado_dificultad']
    rating = request.form['rating']
    definition = request.form['definicion']

    if difficult and rating and definition:
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE contenidos SET grado_dificultad=%s, rating=%s, definicion=%s 
                WHERE identificador=%s"""
            data = (difficult, rating, definition, id)
            cursor.execute(sql, data)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    return render_template('home.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()