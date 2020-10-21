import time
import random

def ordenacionBurbuja(list):
    for i in range(len(list)):
        for j in range(len(list)-1-i):
            if list[j] > list[j+1]:
                aux = list[j+1]
                list[j] = list[j+1]
                list[j+1] = aux

def inserccion(list):
    for i in range(len(list)):
        val = list[i]
        j = i

        while j > 0 and list[j-1] > val:
            list[j] = list[j-1]
            j -= 1

        list[j] = val

list = []
for i in range (8):
    num_aleatorio = random.randint(0,15)
    list.append(num_aleatorio)

t_inicio = time.time()
ordenacionBurbuja(list);
t_final = time.time()

print("la ordenación burbuja ha tardado ", t_final-t_inicio," segundos")
list2 = []
for i in range (8):
    num_aleatorio = random.randint(0,15)
    list2.append(num_aleatorio)

t_inicio = time.time()
inserccion(list2);
t_final = time.time()

print("la ordenación inserccion ha tardado ", t_final-t_inicio," segundos")
