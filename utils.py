def op_opcional(expresion):
    for i in range(len(expresion)):
        if expresion[i] == '?':
            expresion[i] = '|'
            #insert no longer requires checking for last position
            # try:
            #     expresion.insert(i+1, '0')
            # except:
            #     expresion.append('0')
            expresion.insert(i + 1, '\0')

    return expresion

def op_positivo(expresion):
    for i in range(len(expresion)):
        if expresion[i] == '+':
            #repetir = expresion[i - 1] + '*'
            expresion[i] = expresion[i - 1]
            expresion.insert(i, '.')
            expresion.insert(i + 2, '*')
    return expresion

#kleene siempre va aprocesar un caracter o nodo entero...
