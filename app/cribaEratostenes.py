
#max = int(input("Introduzca hasta que número quieres buscar primos: "))
def criba(max):
    numeros = set ()
    primos = ''

    for i in range(2,max):
        if i not in numeros:
            primos += str(i) + ' , '
            numeros.update(range(i*i, max, i))

    return primos

def imprimirLista(primos):
    print("LISTADO DE PRIMOS:\n")
    for i in range(len(primos)):
        print(primos[i], ' ')
    print('\n')
