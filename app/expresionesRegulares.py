import re

def palabrayMayuscula(cadena):
    return bool(re.match(r"[\w\s]+[A-Z]", cadena))

def correoValido(cadena):
    return bool(re.match(r"^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,3})$", cadena))

def tarjetaCredito(cadena):
    return bool(re.match(r"^\d{4}([\ -]?)\d{4}\1\d{4}\1\d{4}$", cadena))
