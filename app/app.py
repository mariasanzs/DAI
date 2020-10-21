#./app/app.py
from flask import ( Flask, url_for, redirect)
from ordenacionMatrices import *
from cribaEratostenes import *
from fibonacci import *
from balanceoCadenas import *
from expresionesRegulares import *
from svg import *
import sys


app = Flask(__name__)

@app.route('/')
def index():
   return '<h2>Para acceder al indice puedes: </h2><h2>Hacer click en <a href="./static"> Directorio /static</a></h2><h2>O escribir tras la url /static </h2>'

@app.route('/static')
def indice():
    return redirect(url_for('static', filename='index.html'))

@app.route('/hello')
def hello_world():
   return 'Hello, world!'

@app.route('/user/<usuario>')
def hola(usuario):
    return 'Hola ' + usuario + '! 😊'

@app.route('/ordena')
def ordenanone():
    return '<h2>Debes poner tras ordena una lista de vectores</h2><h2>Ejemplo: http://localhost:5000/ordena/5,2,7,3</h2>'

@app.route('/ordena/<lista>')
def ordena(lista):
   list = lista.split(',')
   cadena = '<h1>Compara tiempos entre BURBUJA e INSERCCIÓN</h1>'
   app.logger.debug(list)
   t_inicio = time.time()
   ordenacionBurbuja(list);
   t_final = time.time()
   tiempo = str(t_final-t_inicio)
   cadena += '<h2>La ordenación burbuja ha tardado: ' + tiempo + ' segundos</h2>'

   list2 = lista.split(',')
   t_inicio = time.time()
   inserccion(list2);
   t_final = time.time()
   tiempo = str(t_final-t_inicio)

   cadena += '<h2>La ordenación inserccion ha tardado: ' + tiempo + ' segundos</h2>'
   return cadena

@app.route('/criba')
def cribanone():
    return '<h2>Debes poner tras criba el número hasta el que quieres calcular primas</h2><h2>Ejemplo: http://localhost:5000/criba/46</h2>'

@app.route('/criba/<maximo>')
def cribaEratostenes(maximo):
    max = int(maximo)
    app.logger.debug(max)
    cadena = '<h1>LISTADO DE PRIMOS</h1><h2>'
    cadena += criba(max)
    cadena = cadena[:-2]
    cadena += '</h2>'
    return cadena

@app.route('/fibonacci/')
def fibonacci():
    num = obtenerNumeroFichero()
    escribirFichero(num)
    app.logger.debug(num)
    cadena = '<h1>SUCESIÓN DE FIBONACCI</h1><h2>'
    cadena += str(fib(num))
    cadena += '</h2>'
    return cadena

@app.route('/balanceo/')
def balanceo():
    cadena = '<h2>Generando cadena aleatoria ...</h2>'
    list = generarCadenaAleatoria()
    print(list)
    app.logger.debug(list)
    cadena += '<h2>' + list + '</h2>'
    cadena += '<h2>' + comprobarBalanceo(list) + '</h2>'
    return cadena


@app.route('/palabra+mayuscula/')
def palabranone():
    return '<h2>Debes poner tras palabra+mayuscula/ la cadena que desees comprobar</h2><h2>Ejemplo: http://localhost:5000/palabra+mayuscula/maria S</h2>'

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

@app.route('/correo/')
def correoanone():
    return '<h2>Debes poner tras correo/ la cadena que desees comprobar</h2><h2>Ejemplo: http://localhost:5000/correo/maria@correo.ugr.es</h2>'

@app.route('/correo/<cadena>')
def correoElectronicoValido(cadena):
    print(cadena)
    msg = '<h1>' + cadena + '</h1>'
    app.logger.debug(cadena)
    if correoValido(cadena):
        msg += "<h2>Correo aceptado</h2>"
    else:
        msg += "<h2>Este correo electrónico no es correcto</h2>"
    return msg

@app.route('/tarjetaCredito/')
def tarjetanone():
    return '<h2>Debes poner tras tarjetaCredito/ la cadena que desees comprobar</h2><h2>Ejemplo: http://localhost:5000/tarjetaCredito/1234-5678-9012-3456</h2>'

@app.route('/tarjetaCredito/<cadena>')
def tarjeraCreditoAceptada(cadena):
    print(cadena)
    msg = '<h1>' + cadena + '</h1>'
    app.logger.debug(cadena)
    if tarjetaCredito(cadena):
        msg += "<h2>Tarjeta de crédito aceptada</h2>"
    else:
        msg += "<h2>Este tarjeta de crédito no es correcta</h2>"
    return msg

@app.route('/svg/')
def random_svg():
    cadena = svg()
    return cadena

@app.errorhandler(404)
def page_not_found(error):
    return "Oops, algo ha salido mal :(", 404

with app.test_request_context():
    url_for('static', filename='index.html')
