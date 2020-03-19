import utils as ut
import abtreelist as ltree
import Afn
import dfa
import string
from copy import copy, deepcopy
import directdfa

all_letters = string.ascii_uppercase
small_letters = [x for x in string.ascii_lowercase]
universal_dfa_count = 0

def triple_or():
    first_nodeA = non_automata.create_node()
    last_nodeA = non_automata.create_node()
    first_nodeB = non_automata.create_node()
    last_nodeB = non_automata.create_node()
    first_nodeC = non_automata.create_node()
    last_nodeC = non_automata.create_node()
    first_nodeA.neighbors[lista[0]] = [last_nodeA.data]
    first_nodeB.neighbors[lista[-1]] = [last_nodeB.data]
    first_nodeC.neighbors['\0'] = [first_nodeA.data, first_nodeB.data]
    last_nodeA.neighbors['\0'] = [last_nodeC.data]
    last_nodeB.neighbors['\0'] = [last_nodeC.data]
    non_automata.nodes.append(first_nodeC)
    non_automata.nodes.append(first_nodeA)
    non_automata.nodes.append(last_nodeA)
    non_automata.nodes.append(first_nodeB)
    non_automata.nodes.append(last_nodeB)
    non_automata.nodes.append(last_nodeC)
    syn_tree.nodes[syn_tree.nodes.index(lista)] = [first_nodeC.data, last_nodeC.data, 'done']


def nfa_move(non_automata, list_states, token):
    output = []
    for indx, item in enumerate(list_states):
        for indx2, nod in enumerate(non_automata.nodes):
            if nod.data == item:
                output.append(nod.neighbors.get(token, ' '))
    #clean empty returns
    output = [x for x in output if x!= ' ']
    return output

def fnullable(element):
    if element == '*':
        return True
    elif element not in ['*', '|', '.']:
        return False

def subset_move(subset):
    dfa_set = set()
    dfa_sets_move = []
    for letra in alfabeto:
        dfa_set.clear()
        for estado in subset:
            local_dfa_set = estado.neighbors.get(letra, ' ')
            dfa_set.update(local_dfa_set)
        dfa_set = {x for x in dfa_set if x != ' '}
        # dfa_sets_move.append([letra] + list(dfa_set))
        dfa_sets_move.append(list(dfa_set))
    return dfa_sets_move

#esta version hace una correccion al original
def eclosure2(non_automata, list_states, output):
    while True:
        old_count = len(output)
        for nod in non_automata.nodes:
            for state in list_states:
                if nod.data == state:
                    list_states[list_states.index(state)] = nod

        for nod in non_automata.nodes:
            for state in list_states:
                if type(state) != str:
                    local_set = set(state.neighbors.get('\0', ' '))
                    #patch

                    local_set = list(local_set)
                    local_set.sort()
                    # check for last state
                    #if state.data == non_automata.nodes[-1].data:
                        #local_set.append(state.data)
                    local_set = set(local_set)
                #print("local set: ", local_set)
                    output.update(local_set)
        list_states = list(output)
        new_count = len(output)
        if old_count == new_count:
            break

    output = [x for x in output if x != ' ']

    return output


def eclosure(non_automata, list_states, output):
    while True:
        old_count = len(output)
        for nod in non_automata.nodes:
            for state in list_states:
                if nod.data == state:
                    list_states[list_states.index(state)] = nod

        for nod in non_automata.nodes:
            for state in list_states:
                if type(state) != str:
                    local_set = set(state.neighbors.get('\0', ' '))
                    output.update(local_set)
        list_states = list(output)
        new_count = len(output)
        if old_count == new_count:
            break

    output = [x for x in output if x != ' ']
    if non_automata.nodes[0].data not in output:
        output.insert(0, non_automata.nodes[0].data)
    return output

def convert_data_to_nodes(listx):
    for nod in non_automata.nodes:
        for state in listx:
            if nod.data == state:
                listx[listx.index(state)] = nod
    return listx

def convert_data_to_nodes_double_convert(listx):
    for indx, item in enumerate(non_automata.nodes):
        for indx2, item2 in enumerate(listx):
            for indx3, item3 in enumerate(item2):
                if item.data == item3:
                    dfa_sets_move[indx2] = item
    return listx


def kleen_1char():
    my_node = non_automata.create_node()
    next_node = non_automata.create_node()
    if '*' == lista[-1]:
        wolfx = lista[0]
    else:
        wolfx = lista[-1]
    my_node.neighbors[wolfx] = [next_node.data]
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
    first_node.neighbors['\0'] = [copy(my_node.data), copy(last_node.data)]
    non_automata.nodes.insert(0, first_node)
    non_automata.nodes.append(last_node)
    # next_node now has epsilon towards my_node and last node
    next_node.neighbors['\0'] = [deepcopy(my_node.data), copy(last_node.data)]
    print('last node:', last_node.data)
#expresion = "(a*|b*)c"
#expresion = '(a|b)'
#expresion = "b+abc+"
expresion = input('ingrese la expresion: ')
outp = []

clone_expresion = copy(expresion)
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
print('op concat',expresion)


#create tree afn and other stuff
syn_tree = ltree.Tree()
non_automata = Afn.NFA()
dfa_automata = dfa.Dfa()
#skip processing and write directly
if '(' not in expresion:
    for indx, item in enumerate(expresion):
        if item == '.':
            syn_tree.add_entree(expresion[indx-1], '.', expresion[indx+1])
        elif item == '*':
            syn_tree.add_entree(' ', '*', ' ')
        elif item == '|':
            if expresion[indx+1] not in ['-', '*', '|', '.'] and expresion[indx-1] != '-':
                syn_tree.add_entree(expresion[indx-1], '|', expresion[indx+1])
                if expresion[indx+1] not in ['*', '|', '.']:
                    expresion[indx+1] = '-'
            else:
                if expresion[indx-1] == '-':
                    syn_tree.add_entree(' ', '|', expresion[indx+1])
    expresion.clear()


#clean the tree a bit
for indx, sublist in enumerate(syn_tree.nodes):
    if ['*'] == sublist and indx+1 != len(syn_tree.nodes):
        syn_tree.nodes.insert(indx+1, ['.'])

    elif '.' in sublist and len(sublist)>1:
        if '.' in syn_tree.nodes[indx+1] and len(syn_tree.nodes[indx+1]) == 3 :
            syn_tree.nodes[indx+1].pop(0)
        elif '|' in syn_tree.nodes[indx+1]:
            if syn_tree.nodes[indx][-1] == syn_tree.nodes[indx+1][0]:
                syn_tree.nodes[indx].pop(-1)
    elif ' ' in sublist:
        sublist[sublist.index(' ')] = clone_expresion[sublist.index(' ')]



while len(expresion) > 0 or len(outp) > 1:
    if len(outp) > 0:
        for indx, item in enumerate(outp):
            #concat is last case
            if item == '.':
                #or and kleene should not be present
                    if len(outp) >= 3:
                            #print(outp)
                            temp = outp[:]
                            if temp[indx-1] == '.':
                                syn_tree.add_entree(' ', '.', temp[indx + 1])
                            else:
                                syn_tree.add_entree(temp[indx-1], '.', temp[indx+1])

                            syn_tree.see_tree()
                            for i in range(3):
                                del outp[0]
                            #print("t1", outp)
                    else:

                        syn_tree.add_entree(outp[indx-1], '.', ' ')
                        # outp[indx-1] = syn_tree.count
                        for i in range(2):
                            del outp[0]
                        #print("t2", outp)

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
           #     print("outp", outp)
                for i in range(2):
                    del outp[-1]
         #       print("outp", outp)
            #or case
            elif item == '|':
          #          print("im here")
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
        #print("send to outp")
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
#print("finish, expression", expresion)
#print("finish outp", outp)
if (len(outp) == 1):
    syn_tree.add_entree(' ', '.', outp[0])
#syn_tree.see_tree()
print('le tree')
syn_tree.see_tree()
#create NFA
clone_tree = syn_tree.nodes[:]
#print("clone tree: ", clone_tree)
while len(syn_tree.nodes) > 0:
    #process kleenes that are alone first
    for lista in syn_tree.nodes:
        for indx, item in enumerate(lista):
            if item == '*' and len(lista) == 2:
               # print("process alone kleene")
                kleen_1char()
                syn_tree.nodes[syn_tree.nodes.index(lista)] = [non_automata.nodes[0].data , non_automata.nodes[-1].data, 'done']
            elif item == '*' and len(lista) == 1:
                #syn_tree.see_tree()
                first_node = non_automata.create_node()
                last_node = non_automata.create_node()
                first_node.neighbors['\0'] = [syn_tree.nodes[syn_tree.nodes.index(lista)-1][0], last_node.data]
                for nod in non_automata.nodes:
                    if nod.data == syn_tree.nodes[syn_tree.nodes.index(lista)-1][1]:
                        nod.neighbors['\0'] = [[syn_tree.nodes.index(lista)-1][0] ,last_node.data]
                non_automata.nodes.insert(0, first_node)
                non_automata.nodes.append(last_node)
                syn_tree.nodes[syn_tree.nodes.index(lista)] = [deepcopy(first_node.data), deepcopy(last_node.data), 'done']

                print(syn_tree.nodes)
            elif item == '|' and len(lista) == 1:
                #print("im here")
                if 'done' in syn_tree.nodes[syn_tree.nodes.index(lista)-1] and 'done' in syn_tree.nodes[syn_tree.nodes.index(lista)+1]:
                    first_node = non_automata.create_node()
                    first_node.neighbors['\0'] = [copy(syn_tree.nodes[syn_tree.nodes.index(lista)-1] [0]), copy(syn_tree.nodes[syn_tree.nodes.index(lista)+1] [0])]
                    last_node = non_automata.create_node()
                    non_automata.nodes.insert(0, first_node)
                    non_automata.nodes.append(last_node)
                    for nod in non_automata.nodes:
                        if nod.data == syn_tree.nodes[syn_tree.nodes.index(lista)-1][1] or nod.data ==syn_tree.nodes[syn_tree.nodes.index(lista)+1][1]:
                            nod.neighbors['\0'] = [last_node.data]
                    syn_tree.nodes[syn_tree.nodes.index(lista)] = ["done"]
                else:
                   pass

            #or for 3 case
            elif item == '|' and len(lista) == 3:
                triple_or()
            elif item == '|' and len(lista) == 2:
                first_nodeA = non_automata.create_node()
                last_nodeA = non_automata.create_node()
                first_nodeA.neighbors[syn_tree.nodes[syn_tree.nodes.index(lista)][1]] = [last_nodeA.data]
                last_nodeB = non_automata.create_node()
                last_nodeA.neighbors['\0'] = [last_nodeB.data]
                non_automata.nodes.append(first_nodeA)
                non_automata.nodes.append(last_nodeA)
                first_nodeB = non_automata.create_node()
                first_nodeB.neighbors['\0'] = [syn_tree.nodes[syn_tree.nodes.index(lista)-1][0], first_nodeA.data]
                non_automata.nodes.insert(0, first_nodeB)
                non_automata.nodes.append(last_nodeB)
                for nod in non_automata.nodes:
                    if nod.data == syn_tree.nodes[syn_tree.nodes.index(lista)-1][1]:
                        nod.neighbors['\0'] = [last_nodeB.data]
                syn_tree.nodes[syn_tree.nodes.index(lista)] = [first_nodeB.data, last_nodeB.data, 'done']
            #concat case
            elif item == '.':
                #print(syn_tree.nodes)
                if len(lista) == 2:
                    should_process = True
                    for i in range(syn_tree.nodes.index(lista)):
                        if 'done' not in syn_tree.nodes[i]:
                            should_process = False
                    if should_process == True:
                        if syn_tree.nodes.index(lista) != 0:
                            last_node = non_automata.create_node()
                            non_automata.nodes[-1].neighbors[lista[0]] = [last_node.data]
                            #concat not present in next node so reference must be made
                            if syn_tree.nodes.index(lista) +1 != len(syn_tree.nodes):
                                if '|' in syn_tree.nodes[syn_tree.nodes.index(lista)+1] and len(syn_tree.nodes[syn_tree.nodes.index(lista)+1]) == 3:
                                    welp = int(last_node.data[1]) + 5
                                    ghost_ref = 'q' + str(welp)
                                    last_node.neighbors['\0'] = [ghost_ref]
                        non_automata.nodes.append(last_node)
                        syn_tree.nodes[syn_tree.nodes.index(lista)] = [last_node.data, 'done']

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

if len(clone_tree) == 2:
    count_kleenes = 0
    for i in range(len(clone_tree)):
        if '*' in clone_tree[i]:
            count_kleenes += 1
    if count_kleenes == 2:
        non_automata.nodes[-2].neighbors['\0'] = ['q0', 'q5']
print('broken references in tree')
#non_automata.see_tree()
restore_automata_tree = deepcopy(non_automata.nodes)

#time for afd
alfabeto = set()
for nod in non_automata.nodes:
    keys = nod.neighbors.keys()
    for key in keys:
        alfabeto.add(key)
alfabeto = [x for x in alfabeto if x != '\0']
alfabeto.sort()
#print("alfabeto: ", alfabeto)

eps_initial_state = non_automata.nodes[0].neighbors.get('\0', ' ')
#print(eps_initial_state)
set_eps = set(eps_initial_state)
#eclosure
set_eps = eclosure(non_automata, eps_initial_state, set_eps)
set_eps.sort()
A_node = dfa_automata.create_node(set_eps)
#print("e-closure over initial states: ", set_eps)
store_all_sets = []
store_all_sets.append((set_eps[:]))
#print(store_all_sets)
set_eps = convert_data_to_nodes(set_eps)
#print("converted: ", set_eps)

first_node_patch = 0
already_processed = []
#max_count_patch = 0
#loop here
while True:
    #print("set eps: ", set_eps)
    old_len = len(store_all_sets)
    dfa_sets_move = subset_move(set_eps)
   # print("dfa sets move: ", dfa_sets_move)
    clone_dfa_sets_move = []
    for i in range(len(dfa_sets_move)):
        clone_dfa_sets_move.append(dfa_sets_move[i][:])
 #   print("dfa sets move: ", clone_dfa_sets_move)
    dfa_set_completo = set()
    dfa_sets_completos = []
    #create new sets from making gets
    for indx, item in enumerate(non_automata.nodes):
        for indx2, item2 in enumerate(dfa_sets_move):
            for indx3, item3 in enumerate(item2):
                if item.data == item3:
                    dfa_sets_move[indx2][indx3] = item


    #aplicar e-closure
    for indx, statelist in enumerate(dfa_sets_move):
        #la segunda corrida y posterior esto se vuelve una lista y explota
        dfa_set_completo.clear()
        dfa_set_completo = set(dfa_set_completo)

        dfa_set_completo = eclosure2(non_automata, statelist, dfa_set_completo)
        dfa_sets_completos.append(dfa_set_completo[:])

    for i in range(len(dfa_sets_completos)):
        dfa_sets_completos[i] += clone_dfa_sets_move[i]
        dfa_sets_completos[i].sort()
    #print("full sets: ", dfa_sets_completos)

    if first_node_patch == 0:
        for i in range(len(dfa_sets_completos)):
            A_node.neighbors[alfabeto[i]] = copy(dfa_sets_completos[i])
        dfa_automata.nodes.append(A_node)
        first_node_patch = 1

        set_eps = copy(dfa_sets_completos[0])
        set_eps = convert_data_to_nodes(set_eps)
  #      print("set_eps: ", set_eps)


    else:
        recursive_patch = False
        for i in range(len(dfa_sets_completos)):
            if dfa_sets_completos[i] not in already_processed:
                if recursive_patch == False:
                    new_set = dfa_automata.create_node(copy(dfa_sets_completos[i]))

                    recursive_patch = True
        for i in range(len(dfa_sets_completos)):
            new_set.neighbors[alfabeto[i]] = copy(dfa_sets_completos[i])
        dfa_automata.nodes.append(new_set)

    for i in range(len(dfa_sets_completos)):
        if dfa_sets_completos[i] not in store_all_sets:

            store_all_sets.append(copy(dfa_sets_completos[i]))
    if first_node_patch >= len(store_all_sets):
        break
    set_eps = copy(store_all_sets[first_node_patch])
    set_eps = convert_data_to_nodes(set_eps)
   # print("set_eps: ", set_eps)

    first_node_patch += 1
    new_len = len(store_all_sets)
    if old_len == new_len:
  #      max_count_patch +=1
 #   if max_count_patch > len(alfabeto)+1:
        break


#clean all sets set
store_all_sets = [x for x in store_all_sets if len(x) > 0]
#print(store_all_sets)
if len(dfa_automata.nodes) != len(store_all_sets):
    last_node = dfa_automata.create_node(store_all_sets[-1][0])
    dfa_automata.nodes.append(last_node)

#weird fix
#for nod in non_automata.nodes:
 #   print('data: ', nod.data)
  #  print('neighbors: ', nod.neighbors)
fix_nfa = non_automata.nodes[0].neighbors.get('\0', ' ')
for i in range(len(fix_nfa)):
    fix_nfa[i] = fix_nfa[i].data
non_automata.nodes[0].neighbors['\0'] = fix_nfa

non_automata.nodes = restore_automata_tree
non_automata.see_tree()

nfa_write_estados = [x.data for x in non_automata.nodes]
#alfabeto
nfa_write_inicio = non_automata.nodes[0].data
nfa_write_aceptacion = non_automata.nodes[-1].data
nfa_write_transicion = [x.data + ': ' + str(x.neighbors) for x in non_automata.nodes]

f = open("afn.txt", "w")
f.write("ESTADOS{}\nSIMBOLOS{}\nINICIO{}\nACEPTACION{}\nTRANSICION{}".format(nfa_write_estados, alfabeto, nfa_write_inicio, nfa_write_aceptacion, nfa_write_transicion))
f.close()

#nfa travel
travel_set = set()
initial_state = eclosure2(non_automata, [non_automata.nodes[0].data], travel_set)
print(initial_state)

print('expresion: ', clone_expresion)
word_to_test = list(input("ingrese la palabra a probar: "))

if len(word_to_test) == 0:
    if non_automata.nodes[-1].data in initial_state:
        print('esta palabra si la puede formar el lenguaje, nfa')
    else:
        print('esta palabra no la puede formar el lenguaje, nfa')

for i in range(len(word_to_test)):
    travel_set.clear()
    travel_move = nfa_move(non_automata, initial_state, word_to_test[i])
    add_toclosure = []
    for i in range(len(travel_move)):
        add_toclosure += travel_move[i][:]
        temp = convert_data_to_nodes(travel_move[i])
        travel_move[i] = temp[i]
    e_closure_travel = eclosure2(non_automata, travel_move, travel_set) + add_toclosure
    initial_state = e_closure_travel

if len(word_to_test)>0:
    print(e_closure_travel)
    if non_automata.nodes[-1].data in e_closure_travel:
        print("esta palabra si la puede formar el lenguaje, nfa")
    else:
        print("esta palabra no la puede formar el lenguaje, nfa")



#patch dfa

for indx, nod in enumerate(dfa_automata.nodes):
    nod.afn = store_all_sets[indx]

dfa_write_estados = [x.data for x in dfa_automata.nodes]
#alfabeto
dfa_write_inicio = dfa_automata.nodes[0].data
dfa_write_aceptacion = [x.data for x in dfa_automata.nodes if non_automata.nodes[-1].data in x.afn]
dfa_write_transicion = [x.data + ': ' + str(x.neighbors) for x in dfa_automata.nodes]

f = open("dfa.txt", "w")
f.write("ESTADOS{}\nSIMBOLOS{}\nINICIO{}\nACEPTACION{}\nTRANSICION{}".format(dfa_write_estados, alfabeto, dfa_write_inicio, dfa_write_aceptacion, dfa_write_transicion))
f.close()


#simulate dfa
dfa_state = dfa_automata.nodes[0]
for i in range(len(word_to_test)):
    if dfa_state == ' ' or dfa_state==[]:
        break
    #print("dfa s: ", dfa_state)
    dfa_state = dfa_state.neighbors.get(word_to_test[i], ' ')
    for i in range(len(dfa_automata.nodes)):
        if dfa_state == dfa_automata.nodes[i].afn:
            dfa_state = dfa_automata.nodes[i]

if type(dfa_state) != list:
    if non_automata.nodes[-1].data in dfa_state.afn:
        print("esta palabra si la puede formar el lenguaje, dfa")
    else:
        print("esta palabra no la puede formar el lenguaje, dfa")

else:
    print("esta palabra no la puede formar el lenguaje, dfa")


