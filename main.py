import utils as ut
import abtreelist as ltree
import Afn
import dfa
import string
all_letters = string.ascii_uppercase
universal_dfa_count = 0
def convert_data_to_nodes(listx):
    for nod in non_automata.nodes:
        for state in listx:
            if nod.data == state:
                listx[listx.index(state)] = nod
    return listx

def kleen_1char():
    my_node = non_automata.create_node()
    next_node = non_automata.create_node()
    my_node.neighbors[lista[indx + 1]] = [next_node.data]
    # to grow list...
    # some_data = my_node.neighbors.get(lista[indx+1], "")
    # some_data.append('some other node')
    # my_node.neighbors[lista[indx+1]] = some_data
    non_automata.nodes.append(my_node)
    non_automata.nodes.append(next_node)
    # insert to the beginning
    first_node = non_automata.create_node()
    last_node = non_automata.create_node()
    # connect to my_node via epsilon and last node
    first_node.neighbors['\0'] = [my_node.data, last_node.data]
    non_automata.nodes.insert(0, first_node)
    non_automata.nodes.append(last_node)
    # next_node now has epsilon towards my_node and last node
    next_node.neighbors['\0'] = [my_node.data, last_node.data]
    print("nodes: ", non_automata.nodes)
expresion = "(a*|b*)c"
outp = []

#should receive from outp only if expression is not empty
#save index of (
indexar_parentesis = -2
#convertir expresion a lista
expresion = list(expresion)

#primero cambiar ? y +
expresion = ut.op_opcional(expresion)
expresion = ut.op_positivo(expresion)
#move stuff after parenthesis
#expresion, return_to_original = ut.move_after_parenthesis(expresion)
expresion = ut.add_concat(expresion)
#print(expresion)

#create tree afn and other stuff
syn_tree = ltree.Tree()
non_automata = Afn.NFA()

while len(expresion) > 0 or len(outp) > 1:
    if len(outp) > 0:
        for indx, item in enumerate(outp):
            #concat is last case
            if item == '.':
                #or and kleene should not be present
                if '|' and '*' not in outp:
                    if len(outp) >= 3:
                            print(outp)
                            temp = outp[:]
                            if temp[indx-1] == '.':
                                syn_tree.add_entree(' ', '.', temp[indx + 1])
                            else:
                                syn_tree.add_entree(temp[indx-1], '.', temp[indx+1])

                            syn_tree.see_tree()
                            for i in range(3):
                                del outp[0]
                            print("t1", outp)
                    else:

                        syn_tree.add_entree(outp[indx-1], '.', ' ')
                        # outp[indx-1] = syn_tree.count
                        for i in range(2):
                            del outp[0]
                        print("t2", outp)

                    #else:
                     #   print("yo", outp)
                      #  syn_tree.add_entree(' ', '.', outp[1])
                       # for i in range(2):
                        #    del outp[0]
            #kleene first case
            elif item == '*':
                #send concat first
                if len(outp) == 4 and outp[1] == '.':
                    syn_tree.add_entree(' ', '.', outp[0])
                    for i in range(2):
                        del outp[0]
                elif len(outp) == 5 and outp[2] == '|':
                    syn_tree.add_entree(' ', outp[1], outp[0])
                    syn_tree.add_entree(' ', outp[2], ' ')
                    for i in range(3):
                        del outp[0]
                syn_tree.add_entree(' ', '*', outp[-2])
                print("outp", outp)
                for i in range(2):
                    del outp[-1]
                print("outp", outp)
            #or case
            elif item == '|':
                if '*' not in outp:
                    print("im here")
                    #possible lengths 3,2
                    if len(outp) >= 3:
                        syn_tree.add_entree(outp[indx-1], '|', outp[indx+1])
                        for i in range(3):
                            del outp[0]
                    else:
                        #standarize to save all as | token
                        if outp[0] != '|':
                            outp[0], outp[1] = outp[1], outp[0]
                        syn_tree.add_entree(' ', '|', outp[1])
                        for i in range(2):
                            del outp[0]





    else:
        print("send to outp")
        if expresion[0] == '*':
            syn_tree.add_entree(' ', '*', ' ')
            del expresion[0]
        if '(' in expresion:
            if expresion[0] != '(':
                outp = expresion[:expresion.index('(')]
                expresion = expresion[expresion.index('('):]
                continue

            #guardar index de parentesis para pushear de regreso
            indexar_parentesis = expresion.index('(')
            outp = outp + expresion[expresion.index('(') + 1:expresion.index(')')]
            #print(outp)
            expresion = expresion[:expresion.index('(')] + expresion[expresion.index(')') + 1:]
            #print(expresion)
        else:
            outp = expresion[:]
            expresion.clear()

        #print(expresion)
    #break
print("finish, expression", expresion)
print("finish outp", outp)
if (len(outp) == 1):
    syn_tree.add_entree(' ', '.', outp[0])
syn_tree.see_tree()

#create NFA
clone_tree = syn_tree.nodes[:]
print("clone tree: ", clone_tree)
while len(syn_tree.nodes) > 0:
    #process kleenes that are alone first
    for lista in syn_tree.nodes:
        for indx, item in enumerate(lista):
            if item == '*' and len(lista) == 2:
                print("process alone kleene")
                kleen_1char()
                syn_tree.nodes[syn_tree.nodes.index(lista)] = [non_automata.nodes[0].data , non_automata.nodes[-1].data, 'done']
                print(syn_tree.nodes)
            elif item == '|' and len(lista) == 1:
                print("im here")
                if 'done' in syn_tree.nodes[syn_tree.nodes.index(lista)-1] and 'done' in syn_tree.nodes[syn_tree.nodes.index(lista)+1]:
                    print("dawg")
                    first_node = non_automata.create_node()
                    first_node.neighbors['\0'] = [syn_tree.nodes[syn_tree.nodes.index(lista)-1] [0], syn_tree.nodes[syn_tree.nodes.index(lista)+1] [0]]
                    last_node = non_automata.create_node()
                    non_automata.nodes.insert(0, first_node)
                    non_automata.nodes.append(last_node)
                    for nod in non_automata.nodes:
                        if nod.data == syn_tree.nodes[syn_tree.nodes.index(lista)-1][1] or nod.data ==syn_tree.nodes[syn_tree.nodes.index(lista)+1][1]:
                            nod.neighbors['\0'] = [last_node.data]
                    syn_tree.nodes[syn_tree.nodes.index(lista)] = ["done"]
                else:
                    print("hey there")
            #concat case
            elif item == '.':
                print(syn_tree.nodes)
                if len(lista) == 2:
                    should_process = True
                    for i in range(syn_tree.nodes.index(lista)):
                        if 'done' not in syn_tree.nodes[i]:
                            should_process = False
                    if should_process == True:
                        if syn_tree.nodes.index(lista) != 0:
                            last_node = non_automata.create_node()
                            non_automata.nodes[-1].neighbors[lista[0]] = [last_node.data]
                            syn_tree.nodes[syn_tree.nodes.index(lista)] = [last_node.data, 'done']
                            non_automata.nodes.append(last_node)
                    else:
                        continue
            elif 'done' in lista:
                count = 0
                for listx in syn_tree.nodes:
                    for itemx in listx:
                        if itemx == 'done':
                            count += 1
                if count == len(syn_tree.nodes):
                    #clear list causing a break
                    #print("making sure this broke loop")
                    syn_tree.nodes.clear()
                else:
                    continue
    #break



for nod in non_automata.nodes:
    print(nod.data, nod.neighbors)

#time for afd
alfabeto = set()
for nod in non_automata.nodes:
    keys = nod.neighbors.keys()
    for key in keys:
        alfabeto.add(key)
alfabeto = [x for x in alfabeto if x != '\0']
alfabeto.sort()
print("alfabeto: ", alfabeto)

eps_initial_state = non_automata.nodes[0].neighbors.get('\0', ' ')
print(eps_initial_state)
set_eps = set(eps_initial_state)
for i in range(20):

    for nod in non_automata.nodes:
        for state in eps_initial_state:
            if nod.data == state:
                print(state)
                eps_initial_state[eps_initial_state.index(state)] = nod

    for nod in non_automata.nodes:
        for state in eps_initial_state:
            if type(state) != str:
                local_set = set(state.neighbors.get('\0', ' '))
            #print("local set: ", local_set)
                set_eps.update(local_set)
    eps_initial_state = list(set_eps)

set_eps = {x for x in set_eps if x != ' '}
print("e-closure over initial state: ", set_eps)



