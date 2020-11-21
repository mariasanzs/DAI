#./app/app.py
from flask import ( Flask, url_for, redirect, render_template, session, request)
from pickleshare import *
from model import *
from ordenacionMatrices import *
from cribaEratostenes import *
from fibonacci import *
from balanceoCadenas import *
from expresionesRegulares import *
from svg import *
from pymongo import MongoClient
import sys

client = MongoClient("mongo", 27017)
db = client.SampleCollections

app = Flask(__name__)
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

@app.route('/mongoform')
def mongoformulario():
    store_visited_urls()
    tam = len(urls)
    return render_template('lista.html', url=urls, tipo="form", tam = tam, msgerror="", accion="mongo" )


@app.route('/mongo', methods=["GET", "POST"])
def mongo():
    store_visited_urls()
    tam = len(urls)
    peliculas = db.video_movies.find()

    parametro = request.form['parametro']
    n_elementos = request.form['n_elementos']

    listaPeliculas = []
    for pelicula in range(int(n_elementos)):
        app.logger.debug(peliculas[pelicula])
        listaPeliculas.append(peliculas[pelicula])
    return render_template('lista.html', peliculas=listaPeliculas,  parametro=parametro, url=urls, tam = tam)


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
