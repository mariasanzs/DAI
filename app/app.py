#./app/app.py
from flask import ( Flask, url_for, redirect, render_template, session, request, jsonify)
from flask_restful import (Resource, Api, reqparse)
from bson import ObjectId
from pickleshare import *
from model import *
from ordenacionMatrices import *
from cribaEratostenes import *
from fibonacci import *
from balanceoCadenas import *
from expresionesRegulares import *
from svg import *
from pymongo import MongoClient
from random_object_id import generate
import sys

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongo", 27017)
db = client.SampleCollections

app.secret_key = '/r/xd8}q/xde/x13/xe5F0/xe5/x8b/x96A64'
urls = []

def store_visited_urls():
    urls.append(request.path)

@app.route('/')

@app.route('/index')
def index():
    store_visited_urls()
    tam = len(urls)
    return render_template('index.html', url=urls, tam = tam)

class api_restful_1(Resource):
    def get(self):
        lista = []
        movies = db.video_movies.find().sort('year')
        for movie in movies:
            lista.append({
                  'id':    str(movie.get('_id')), # pasa a string el ObjectId
                  'title': movie.get('title'),
                  'year':  movie.get('year'),
                  'imdb':  movie.get('imdb')
                })
        return jsonify(lista)
    def post(self):
        titulo = "No tengo titulo"
        year = "2020"
        imdb = "tt01"
        id = generate()

        if 'title' in request.form:
            titulo = request.form['title']
        if 'year' in request.form:
            year = request.form['year']
        if 'imdb' in request.form:
            imdb = request.form['imdb']

        pelicula = { "_id": ObjectId(id), "title":titulo, "year":year, "imdb":imdb }
        db.video_movies.insert_one(pelicula)
        peliculajson = { "_id": id, "title":titulo, "year":year, "imdb":imdb }
        return jsonify(peliculajson)

api.add_resource(api_restful_1, "/api_restful_1")

class api_restful_2(Resource):
    def get(self, id):
        try:
            movie = db.video_movies.find_one({'_id':ObjectId(id)})
            return jsonify({
                'id':    id,
                'title': movie.get('title'),
                'year':  movie.get('year'),
                'imdb':  movie.get('imdb')
            })
        except:
          return jsonify({'error':'Not found'})

    def put(self, id):
        try:
            movie = db.video_movies.find_one({'_id':ObjectId(id)})

            titulo = movie.get('title')
            year = movie.get('year')
            imdb = movie.get('imdb')

            if 'title' in request.form:
                titulo = request.form['title']
            if 'year' in request.form:
                year = request.form['year']
            if 'imdb' in request.form:
                imdb = request.form['imdb']

            id_update = { "$set": { 'title' : titulo , 'year' : year, 'imdb' : imdb } }
            id_anterior = { '_id' : ObjectId(id) }
            db.video_movies.update_one(id_anterior, id_update)

            movie = db.video_movies.find_one({'_id':ObjectId(id)})
            return jsonify({
                'id':    id,
                'title': movie.get('title'),
                'year':  movie.get('year'),
                'imdb':  movie.get('imdb')
            })
        except:
            return jsonify({'error':'Not found'})

    def delete(self, id):
        try:
            movie = db.video_movies.find_one({'_id':ObjectId(id)})
            id_borrar = { '_id' : ObjectId(id) }
            db.video_movies.delete_one(id_borrar)
            id_borrado = { '_id' : id }
            return jsonify(id_borrado)
        except:
            return jsonify({'error':'Not found'})

api.add_resource(api_restful_2, "/api_restful_2/<string:id>")

# para devolver una lista (GET), o añadir (POST)
@app.route('/api/movies', methods=['GET', 'POST'])
def api_1():
    if request.method == 'GET':
        lista = []
        movies = db.video_movies.find().sort('year')
        for movie in movies:
            lista.append({
                  'id':    str(movie.get('_id')), # pasa a string el ObjectId
                  'title': movie.get('title'),
                  'year':  movie.get('year'),
                  'imdb':  movie.get('imdb')
                })
        return jsonify(lista)
    elif request.method == 'POST':
        titulo = "No tengo titulo"
        year = "2020"
        imdb = "tt01"
        id = generate()

        if 'title' in request.form:
            titulo = request.form['title']
        if 'year' in request.form:
            year = request.form['year']
        if 'imdb' in request.form:
            imdb = request.form['imdb']

        pelicula = { "_id": ObjectId(id), "title":titulo, "year":year, "imdb":imdb }
        db.video_movies.insert_one(pelicula)
        peliculajson = { "_id": id, "title":titulo, "year":year, "imdb":imdb }
        return jsonify(peliculajson)

# para devolver una, modificar o borrar
@app.route('/api/movies/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_2(id):
    if request.method == 'GET':
        try:
            movie = db.video_movies.find_one({'_id':ObjectId(id)})
            return jsonify({
                'id':    id,
                'title': movie.get('title'),
                'year':  movie.get('year'),
                'imdb':  movie.get('imdb')
            })
        except:
          return jsonify({'error':'Not found'}), 404
    elif request.method == 'PUT':
        try:
            movie = db.video_movies.find_one({'_id':ObjectId(id)})

            titulo = movie.get('title')
            year = movie.get('year')
            imdb = movie.get('imdb')

            if 'title' in request.form:
                titulo = request.form['title']
            if 'year' in request.form:
                year = request.form['year']
            if 'imdb' in request.form:
                imdb = request.form['imdb']

            id_update = { "$set": { 'title' : titulo , 'year' : year, 'imdb' : imdb } }
            id_anterior = { '_id' : ObjectId(id) }
            db.video_movies.update_one(id_anterior, id_update)

            movie = db.video_movies.find_one({'_id':ObjectId(id)})
            return jsonify({
                'id':    id,
                'title': movie.get('title'),
                'year':  movie.get('year'),
                'imdb':  movie.get('imdb')
            })
        except:
            return jsonify({'error':'Not found'}), 404
    elif request.method == 'DELETE':
        try:
            movie = db.video_movies.find_one({'_id':ObjectId(id)})
            id_borrar = { '_id' : ObjectId(id) }
            db.video_movies.delete_one(id_borrar)
            id_borrado = { '_id' : id }
            return jsonify(id_borrado)
        except:
            return jsonify({'error':'Not found'}), 404

@app.route('/mongoform')
def mongoformulario():
    store_visited_urls()
    tam = len(urls)
    return render_template('lista.html', url=urls, tipo="form", tam = tam, msgerror="", accion="mongo")


@app.route('/mongo', methods=["GET", "POST"])
def mongo():
    store_visited_urls()
    tam = len(urls)
    peliculas = db.video_movies.find()
    parametro = request.form['parametro']
    n_elementos = request.form['n_elementos']

    listaPeliculas = []
    if int(n_elementos) > peliculas.count():
        n_elementos = peliculas.count()
    for pelicula in range(int(n_elementos)):
        app.logger.debug(peliculas[pelicula])
        listaPeliculas.append(peliculas[pelicula])
    return render_template('lista.html', peliculas=listaPeliculas, tipo="list", parametro=parametro, url=urls, tam = tam, accion="baseDatos")

@app.route('/baseDatos', methods=["GET", "POST"])
def basedeDatos():
    store_visited_urls()
    tam = len(urls)
    accion = request.form['accion']
    if accion == "Editar":
        nombre_pelicula = request.form['nombre_']
        year_pelicula = request.form['year_']
        imdb_pelicula = request.form['imdb_']
        type_pelicula = request.form['type_']
        return render_template('lista.html', url=urls, tipo="editar", tam = tam, msgerror="", year_pelicula=year_pelicula ,imdb_pelicula=imdb_pelicula ,type_pelicula=type_pelicula , nombre_pelicula=nombre_pelicula ,accion="baseDatos", boton="editarPelicula")
    elif accion == "anadirPelicula":
        return render_template('lista.html', url=urls, tipo="editar", tam = tam, msgerror="", accion="baseDatos", boton="insertarPelicula")
    elif accion == "insertarPelicula":
        nombre_e_pelicula = request.form['nombre_e']
        year_pelicula = request.form['year_']
        imdb_pelicula = request.form['imdb_']
        type_pelicula = request.form['type_']
        id_editar = { 'title' : nombre_e_pelicula , 'year' : year_pelicula, 'imdb' : imdb_pelicula , 'type' : type_pelicula }
        db.video_movies.insert_one(id_editar)
        return render_template('lista.html', url=urls, tipo="form", tam = tam, msgerror="", accion="mongo" , exito = "si", mensaje="Película Añadida con Éxito")
    elif accion == "Borrar":
        nombre_pelicula = request.form['nombre_']
        id_borrar = { 'title' : nombre_pelicula }
        db.video_movies.delete_one(id_borrar)
        return render_template('lista.html', url=urls, tipo="form", tam = tam, msgerror="", accion="mongo" , exito = "si", mensaje="Película Borrada con Éxito")
    elif accion == "editarPelicula":
        nombre_pelicula = request.form['nombre_']
        nombre_e_pelicula = request.form['nombre_e']
        year_pelicula = request.form['year_']
        imdb_pelicula = request.form['imdb_']
        type_pelicula = request.form['type_']
        id_editar = { "$set": { 'title' : nombre_e_pelicula , 'year' : year_pelicula, 'imdb' : imdb_pelicula , 'type' : type_pelicula } }
        id_anterior = { 'title' : nombre_pelicula }
        db.video_movies.update_one(id_anterior, id_editar)
        return render_template('lista.html', url=urls, tipo="form", tam = tam, msgerror="", accion="mongo" , exito = "si", mensaje="Película Editada con Éxito")
    else:
        return render_template('lista.html', url=urls, tipo="form", tam = tam, msgerror="", accion="mongo" , exito = "no", mensaje="Error realizando esta acción")

@app.route('/signinform')
def signinformulario():
    store_visited_urls()
    tam = len(urls)
    return render_template('signin.html', url=urls, tam = tam, msgerror="", msg="Iniciar sesión", accion="signin", msgBoton="iniciar" )


@app.route('/signin', methods=["GET", "POST"])
def signin():
    store_visited_urls()
    tam = len(urls)
    msgerror=""
    usuario = request.form['usuario']
    password = request.form['password']

    if(loginDB(usuario,password)):
        session['usuario']=usuario
        session['password']=password

        return redirect(url_for('index'))
    else:
        msgerror="Este usuario y/o contraseña no son válidos"

    return render_template('signin.html', url=urls, tam = tam, msgerror=msgerror, msg="Iniciar sesión", accion="signin", msgBoton="iniciar")

@app.route('/registrarseform')
def registrarseformulario():
    store_visited_urls()
    tam = len(urls)
    return render_template('signin.html', url=urls, tam = tam, msgerror="", msg="Regístrate", accion="registrarse", msgBoton="registrarme" )


@app.route('/registrarse', methods=["GET", "POST"])
def registrarse():
    store_visited_urls()
    tam = len(urls)
    msgerror=""
    usuario = request.form['usuario']
    password = request.form['password']

    if(registro(usuario,password)):
        session['usuario']=usuario
        session['password']=password
        return redirect(url_for('index'))
    else:
        msgerror="Este nombre de usuario ya está ocupado"

    return render_template('signin.html', url=urls, tam = tam, msgerror=msgerror, msg="Regístrate", accion="registrarse", msgBoton="registrarme")


@app.route('/signout')
def singnout():
    store_visited_urls()
    tam = len(urls)
    session.pop('usuario',None)
    session.pop('password',None)
    return redirect(url_for('index'))

@app.route('/miperfil')
def vermiperfil():
    store_visited_urls()
    tam = len(urls)
    cadena = '<h1 class="mt-5">DATOS DE MI PERFIL</h1><h2 class="lead">Nombre de usuario: '
    cadena += str(session['usuario'])
    cadena += '</h2>'
    cadena += '<h2 class="lead" type="password">Contraseña Encriptada: '
    for i in range(len(session['password'])):
        cadena += '*'
    cadena += '</h2>'
    return render_template('ejercicio.html', title='vermiperfil', url=urls, tam = tam , cadena=cadena)

@app.route('/editarperfilform')
def editarperfilformulario():
    store_visited_urls()
    tam = len(urls)
    return render_template('signin.html', url=urls, tam = tam, msgerror="", msg="Editar mi perfil", accion="editarperfil", msgBoton="Editar" )


@app.route('/editarperfil', methods=["GET", "POST"])
def editarperfil():
    store_visited_urls()
    tam = len(urls)
    msgerror=""
    usuario = session['usuario']
    usuarioNuevo = request.form['usuario']
    password = request.form['password']

    if(editUsuario(usuarioNuevo, usuario ,password)):
        session['usuario']=usuarioNuevo
        session['password']=password
        return redirect(url_for('index'))
    else:
        msgerror="Este nombre de usuario ya está ocupado"

    return render_template('signin.html', url=urls, tam = tam, msgerror=msgerror, msg="Editar mi perfil", accion="editarperfil", msgBoton="Editar")

@app.route('/ordena/<lista>')
def ordena(lista):
   list = lista.split(',')
   cadena = '<h1 class="mt-5">Compara tiempos entre BURBUJA e INSERCCIÓN</h1>'
   app.logger.debug(list)
   t_inicio = time.time()
   ordenacionBurbuja(list);
   t_final = time.time()
   tiempo = str(t_final-t_inicio)
   cadena += '<h2 class="lead">La ordenación burbuja ha tardado: ' + tiempo + ' segundos</h2>'

   list2 = lista.split(',')
   t_inicio = time.time()
   inserccion(list2);
   t_final = time.time()
   tiempo = str(t_final-t_inicio)

   cadena += '<h2 class="lead">La ordenación inserccion ha tardado: ' + tiempo + ' segundos</h2>'
   return cadena

@app.route('/ejer1-ordena')
def mostrarordena():
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='ordena' , url=urls, tam = tam, cadena='', datos='ejerOrdena')


@app.route('/ejerOrdena', methods=["GET", "POST"])
def imprimirordena():
     cadena = ordena(request.args.get('datos'))
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='ordena', url=urls, tam = tam , cadena=cadena, datos='')

@app.route('/criba/<maximo>')
def cribaEratostenes(maximo):
    max = int(maximo)
    app.logger.debug(max)
    cadena = '<h1>LISTADO DE PRIMOS</h1><h2>'
    cadena += criba(max)
    cadena = cadena[:-2]
    cadena += '</h2>'
    return cadena

@app.route('/ejer2-criba')
def mostrarcriba():
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='Criba' , cadena='', url=urls, tam = tam, datos='ejerCriba')


@app.route('/ejerCriba', methods=["GET", "POST"])
def imprimircriba():
     cadena = cribaEratostenes(request.args.get('datos'))
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='Criba', url=urls, tam = tam , cadena=cadena, datos='')


@app.route('/fibonacci')
def fibonacci():
    num = obtenerNumeroFichero()
    escribirFichero(num)
    app.logger.debug(num)
    cadena = '<h1 class="mt-5">SUCESIÓN DE FIBONACCI</h1><h2 class="lead">'
    cadena += str(fib(num))
    cadena += '</h2>'
    return cadena

@app.route('/ejer3-fibonnaci/')
def imprimirfibonacci():
    cadena = fibonacci()
    store_visited_urls()
    tam = len(urls)
    return render_template('ejercicio.html', title='fibonnaci', url=urls, tam = tam , cadena=cadena)

@app.route('/balanceo')
def balanceo():
    cadena = '<h1 class="mt-5">Balanceo de Cadenas</h1>'
    cadena += '<h2 class="lead">Generando cadena aleatoria ...</h2>'
    list = generarCadenaAleatoria()
    print(list)
    app.logger.debug(list)
    cadena += '<h2 class="lead">' + list + '</h2>'
    cadena += '<h2 class="lead">' + comprobarBalanceo(list) + '</h2>'
    return cadena

@app.route('/ejer4-balanceo/')
def imprimirbalanceo():
    cadena = balanceo()
    store_visited_urls()
    tam = len(urls)
    return render_template('ejercicio.html', title='balanceo' , cadena=cadena, url=urls, tam = tam)

@app.route('/palabra+mayuscula/<cadena>')
def palabraMayuscula(cadena):
    print(cadena)
    msg = '<h1>' + cadena + '</h1>'
    app.logger.debug(cadena)
    if palabrayMayuscula(cadena):
        msg += "<h2>palabra aceptada</h2>"
    else:
        msg += "<h2>palabra no válida</h2>"
    return msg

@app.route('/ejer5-palabra+mayuscula')
def mostrarpalabraM():
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='Palabra+Mayúscula' , cadena='', url=urls, tam = tam, datos='ejerPalabra')


@app.route('/ejerPalabra', methods=["GET", "POST"])
def imprimirpalabraM():
     cadena = palabraMayuscula(request.args.get('datos'))
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='Palabra+Mayúscula' , cadena=cadena, datos='', url=urls, tam = tam)

@app.route('/correo/<cadena>')
def correoElectronicoValido(cadena):
    print(cadena)
    msg = '<h1 class="mt-5">' + cadena + '</h1>'
    app.logger.debug(cadena)
    if correoValido(cadena):
        msg += '<h2 class="list-group-item">Correo aceptado</h2>'
    else:
        msg += '<h2 class="list-group-item">Este correo electrónico no es correcto</h2>'
    return msg

@app.route('/ejer6-correo')
def mostrarcorreo():
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='Correo' , cadena='', datos='ejerCorreo', url=urls, tam = tam)


@app.route('/ejerCorreo', methods=["GET", "POST"])
def imprimircorreo():
     cadena = correoElectronicoValido(request.args.get('datos'))
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='Correo' , cadena=cadena, datos='', url=urls, tam = tam)

@app.route('/tarjetaCredito/<cadena>')
def tarjeraCreditoAceptada(cadena):
    print(cadena)
    msg = '<h1 class="mt-5">' + cadena + '</h1>'
    app.logger.debug(cadena)
    if tarjetaCredito(cadena):
        msg += '<h2 class="list-group-item" >Tarjeta de crédito aceptada</h2>'
    else:
        msg += '<h2>Este tarjeta de crédito no es correcta</h2>'
    return msg

@app.route('/ejer7-tarjetaCredito')
def mostrartarjeta():
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='TarjetaCredito' , cadena='', datos='ejerTarjeta' , url=urls, tam = tam)


@app.route('/ejerTarjeta', methods=["GET", "POST"])
def imprimirtarjeta():
     cadena = tarjeraCreditoAceptada(request.args.get('datos'))
     store_visited_urls()
     tam = len(urls)
     return render_template('ejercicio.html', title='TarjetaCredito' , cadena=cadena, datos='', url=urls, tam = tam)


@app.route('/svg/')
def random_svg():
    cadena = svg()
    return cadena

@app.route('/ejer8-svg/')
def imprimirsvg():
    cadena = random_svg()
    store_visited_urls()
    tam = len(urls)
    return render_template('ejercicio.html', title='svg' , cadena=cadena, url=urls, tam = tam)

@app.errorhandler(404)
def page_not_found(error):
    return "Oops, algo ha salido mal :(", 404
