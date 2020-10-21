def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)

def obtenerNumeroFichero():
    n = open("entero.txt", "r")
    numero = int(n.read())
    n.close()
    return numero

def escribirFichero(numero):
    salida = open("sucesionFibonacci_entero.txt", "w")
    salida.write('SUCESIÓN DE FIBONACCI: \n')
    salida.write(str(fib(numero)))
    salida.write('\n')
    salida.close()
