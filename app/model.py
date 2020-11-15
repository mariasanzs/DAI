from pickleshare import *
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph


def loginDB(usuario, password):
    db = PickleShareDB('./usuarios.dat')
    comprobado = False
    if usuario in db and checkph(db[usuario].get('password'), password) :
        comprobado = True
    return comprobado

def editUsuario(usuarioNuevo, usuario, passwordNuevo):
    db = PickleShareDB('./usuarios.dat')

    if(usuarioNuevo not in db ):
        del db[usuario]
        registro(usuarioNuevo,passwordNuevo)
        editado = True
    else:
        editado = False
    return editado

def registro(usuario,password):
    db = PickleShareDB('./usuarios.dat')

    if(usuario not in db):
        contra = genph(password)
        db[usuario] = dict()
        db[usuario]['password'] = contra
        db[usuario] = db[usuario]
        registrado = True
    else:
        registrado = False
    return registrado
