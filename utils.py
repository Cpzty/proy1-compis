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


def add_concat(expresion):
    for j in range((len(expresion))):
        for i in range(len(expresion)-1):
            if expresion[i] not in ['*', '(', '|', '.'] and expresion[i+1] not in [')', '*', '.']:
                expresion.insert(i+1, '.')

    return expresion

#kleene siempre va aprocesar un caracter o nodo entero...

def move_after_parenthesis(expresion):
    try:
        index_parenthesis = expresion.index('(')
        if index_parenthesis != 0:
            swap_piece = expresion[:index_parenthesis]
            expresion = expresion[index_parenthesis:]
            paright = expresion.index(')')
            for i in range(len(swap_piece)):
                expresion.insert(paright+1+i, swap_piece[i])
    except:
        index_parenthesis == 0
    return (expresion, index_parenthesis)

