import string
import random

def generarCadenaAleatoria():
    string.letters='[]'
    list = ""
    num_aleatorio = random.randint(2,8)
    for i in range (num_aleatorio):
        list += str(random.choice(string.letters))
    return list

def comprobarBalanceo(cadena):
    p = ""
    balanceo = True
    i = 0
    while i < len(cadena) and balanceo:
        corchete = cadena[i]
        if corchete == '[':
            p += '['
        else:
            if len(p) is 0:
                balanceo = False
            else:
                p = p[:-1]

        i += 1

    if balanceo and len(p) is 0:
        solucion = "Esta cadena está balanceada"
    else:
        solucion = "Esta cadena NO está balanceada"
    return solucion

list = generarCadenaAleatoria()
print(list)
print(comprobarBalanceo(list))
