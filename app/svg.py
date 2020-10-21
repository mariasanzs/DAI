import random

def svg():
    formas=['rect','circle','ellipse']
    colores=['burlywood', 'darksalmon', 'lightgreen	', 'lightpink', 'lightblue', 'indianred','rosybrown']

    forma = random.choice(formas)
    color = random.choice(colores)
    cadena = '<svg width=400 height=400>'

    if forma == 'rect':
        x = random.randint(20,100)
        y = random.randint(20,100)
        width = random.randint(100,300)
        height = random.randint(100,300)

        cadena += '<rect x=' + str(x) + ' y=' + str(y)
        cadena += ' width=' + str(width) + ' height=' + str(height) + ' fill=' + color + ' /></svg>'

    elif forma == 'circle':
        cx = random.randint(100,300)
        cy = random.randint(100,300)
        r = random.randint(25,75)

        cadena += '<circle cx=' + str(cx) + ' cy=' + str(cy) + ' r=' + str(r) + ' fill=' + color + ' /></svg>'

    elif forma == 'ellipse':
        cx = random.randint(100,300)
        cy = random.randint(100,300)
        rx = random.randint(25,75)
        ry = random.randint(25,75)

        cadena += '<ellipse cx=' + str(cx) + ' cy=' + str(cy) + ' rx=' + str(rx) + ' ry=' + str(ry) + ' fill=' + color + ' /></svg>'

    return cadena
