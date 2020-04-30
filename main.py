import Afn
import dfa
from copy import deepcopy, copy
import  Tokens
from time import sleep
#TOKENIZE CLASS
tokenize = Tokens.Tokens()

def process_tokens(token_list):
        for substring in token_list:
            token_list[token_list.index(substring)] = substring.split('=')
        for sublist in token_list:
                for substring in sublist:
                    if 'EXCEPT' in substring:
                        inmediate_process = deepcopy(substring)
                        inmediate_process = inmediate_process.split()

                        tokenize.tokens_excepto.append([sublist[0], inmediate_process[inmediate_process.index('EXCEPT')+1].lower()])

                        destroy = deepcopy(inmediate_process)
                        destroy = destroy[:destroy.index('EXCEPT')]
                        token_list[token_list.index(sublist)] = [token_list[token_list.index(sublist)][0], destroy[0]]
        return token_list

def quitar_caracteres_inecesarios(lista):
    lista = [str.rstrip(x, '\n') for x in lista]
    lista = [str.rstrip(x, '.') for x in lista]

    return lista

def process_keywords(key_list):
    for substring in key_list:
        key_list[key_list.index(substring)] = substring.split('=')
    return key_list

def further_slicing(lista):
    # break appart list in half to have definitions on one side
    lista = [x.split('=') for x in lista]
    for sublist in lista:
        for indx, texto in enumerate(sublist):
            if '+' in list(texto):
                cut_again = list(texto)
                cut_again = [cut_again[:cut_again.index('+')], cut_again[cut_again.index('+') + 1:]]
                flat_list = []
                for i in range(len(cut_again)):
                    str1 = ""
                    cut_again[i] = [x for x in cut_again[i] if x != ' ']
                    cut_again[i] = str1.join(cut_again[i])
                    flat_list.append(cut_again[i])
                flat_list.insert(0, sublist[0])
                lista[lista.index(sublist)] = flat_list
            if ' ' in list(texto):
                str2 = ""
                more_empty_spaces = list(texto)
                more_empty_spaces = [x for x in more_empty_spaces if x != ' ']
                more_empty_spaces = str2.join(more_empty_spaces)
                sublist[indx] = more_empty_spaces
    return lista

scanner_file = open('Aritmetica.txt', 'r')
#scanner_file = open('DoubleAritmetica.txt', 'r')
#scanner_file = open('HexNumber.txt', 'r')
lines = scanner_file.readlines()
scanner_file.close()
#index
#print(lines)
index_characters = lines.index("CHARACTERS\n") + 1
index_keywords = lines.index("KEYWORDS\n")
index_tokens = lines.index("TOKENS\n")
index_productions = lines.index("PRODUCTIONS\n")
#slice
characters_slice = lines[index_characters:index_keywords]
characters_slice = quitar_caracteres_inecesarios(characters_slice)
keywords_slice = lines[index_keywords+1:index_tokens]
keywords_slice = quitar_caracteres_inecesarios(keywords_slice)
tokens_slice = lines[index_tokens+1:index_productions]
tokens_slice = quitar_caracteres_inecesarios(tokens_slice)
#productions_slice = lines[index_productions+1:]

characters_slice = further_slicing(characters_slice)
keywords_slice = process_keywords(keywords_slice)
tokens_slice = process_tokens(tokens_slice)
            #sublist[indx] = [sublist[0], ]
#print(characters_slice)
#print(keywords_slice)
#print(tokens_slice)
#clean empties from all 3
characters_slice = [x for x in characters_slice if x!= ['']]
keywords_slice = [x for x in keywords_slice if x!= ['']]
tokens_slice = [x for x in tokens_slice if x!= ['']]

#print(characters_slice)

for indx1, sublist in enumerate(characters_slice):
    for indx2, subtext in enumerate(sublist):
        if '+' in subtext:
            redo = deepcopy(subtext.split('+'))
            characters_slice[indx1][indx2] = redo[0]
            characters_slice[indx1].append(redo[1])


for i in range(len(characters_slice)):
    if len(characters_slice[i]) == 2:
        my_node = tokenize.create_node()
        my_node.data = characters_slice[i][0]
        my_node.content = [characters_slice[i][1]]
        tokenize.characters.append(my_node)
    else:
        for j in range(len(characters_slice[i])):
            for nod in tokenize.characters:
                if nod.data == characters_slice[i][j]:
                    characters_slice[i][j] = nod.content[0]

#print(characters_slice)

#now add the ones with len > 2
for i in range(len(characters_slice)):
    if len(characters_slice[i]) == 3:
        my_node = tokenize.create_node()
        my_node.data = characters_slice[i][0]

        for j in range(1, len(characters_slice[i])-1):
            characters_slice[i][j] = characters_slice[i][j].replace('"', '')
            characters_slice[i][j] = characters_slice[i][j].replace('"', '')
            characters_slice[i][j+1] = characters_slice[i][j+1].replace('"', '')
            characters_slice[i][j+1] = characters_slice[i][j+1].replace('"', '')
            cerberus = [list1+list2 for list1 in characters_slice[i][j] for list2 in characters_slice[i][j+1]]

        my_node.content = deepcopy(cerberus)
        tokenize.characters.append(my_node)
    elif len(characters_slice[i]) >= 4:
        my_node = tokenize.create_node()
        my_node.data = characters_slice[i][0]
        my_node.content = [''.join(characters_slice[i][1:])]
        tokenize.characters.append(my_node)
#tokenize.characters = tokenize.characters[0].replace("'", '')
#tokenize.see_nodes(tokenize.characters)
for nod in tokenize.characters:
    if len(nod.content) ==1:
        fix_doubles = list(nod.content[0])
        for item in fix_doubles:
            if item == '"' or item == '.':
                fix_doubles.remove(item)
            if ord(item) == 34:
                fix_doubles.remove(item)
        nod.content = [''.join(fix_doubles)]

#tokenize.see_nodes(tokenize.characters)
#tokenize.see_nodes(tokenize.keywords)
for sublist in keywords_slice:
    tokenize.keywords[keywords_slice[keywords_slice.index(sublist)][0]] = keywords_slice[keywords_slice.index(sublist)][1]
for key in tokenize.keywords.keys():
    clean_strings = tokenize.keywords.get(key, '')
    if clean_strings[0] == '"' and clean_strings[-1] == '"' :
        clean_strings = clean_strings[1:-1]
        tokenize.keywords[key] = clean_strings

for indx, sublist in enumerate(tokens_slice):
    my_node = tokenize.create_node()
    my_node.data = sublist[0]
    for indx2, substring in enumerate(sublist):
        if '}' in substring:
            repeat = deepcopy(substring[substring.index('{')+1:substring.index('}')])
            substring = substring[:substring.index('{')] + ' ' + repeat + '* '  + substring[substring.index('}')+1:]
            substring = substring.replace('{', '')
            substring = substring.replace('}', '*')
            substring = substring.replace('"', '')
            substring = substring.replace('.', '')

    my_node.content = substring
    tokenize.tokens.append(my_node)



for indx, sublist in enumerate(tokenize.tokens_excepto):
    for indx2, nod in enumerate(tokenize.tokens):
        if nod.data == sublist[0]:
            nod.exceptions = sublist[1:]
#checkpoint1
#tokenize.see_nodes(tokenize.characters)
#replace tokens for their true contenttokenize.see_nodes(tokenize.characters)
for toke1 in tokenize.tokens:
    for toke2 in tokenize.characters:
        my_text = toke1.content.split()
      #  print(my_text)
        for each_word in my_text:
            if toke2.data == each_word:
                if len(toke2.content) == 1:
                    toke1.content = toke1.content.replace(toke2.data, toke2.content[0])

                else:
                    create_strim = ' '.join([str(elem) for elem in toke2.content])
                    create_strim = create_strim.replace(' ', '')
                    toke1.content = toke1.content.replace(toke2.data, create_strim)
                    toke1.content = toke1.content.replace('"', '')
            elif toke2.data in each_word:
                if each_word[each_word.index(toke2.data)-1] == '|':
                    toke1.content = toke1.content.replace(toke2.data, toke2.content[0])

#print('characters: ', characters_slice)
#print('keywords: ', keywords_slice)
#print('tokens: ', tokens_slice)
#tokenize.see_nodes(tokenize.tokens)

#experiment 1
no_determinista = Afn.NFA()

for nod in tokenize.tokens:
    current_nod = nod.content.strip()
    current_nod = current_nod.split(' ')
    #new_tokens = []
    for i in range(1, len(current_nod)):
        if current_nod[0] in current_nod[i]:
            current_nod[i] = [current_nod[0]] + current_nod[i].split(current_nod[0])

            #current_nod[i] = current_nod[i][1].remove('')
        else:
            current_nod[i] = list(current_nod[i])
    current_nod[0] = [current_nod[0]]
    current_nod[0].append('.')
    current_nod[1].remove('')
    if '|' in current_nod[1][1]:
        current_nod[1] = [current_nod[1][0]] + ['|'] + [current_nod[1][1][1:]]
    if len(current_nod[1]) > 2:
        if '*' in current_nod[1][2]:
            current_nod[1] = [current_nod[1][0]] + [current_nod[1][1]] + [current_nod[1][2][:-1]]
            current_nod.append(['*'])
    print('nod_token: ',current_nod[1])
    nod.content = current_nod
tokenize.see_nodes(tokenize.tokens)
 #   new_tokens += current_nod
#print('new_tokens: ', new_tokens)
#for i in range(len(new_tokens)):

    #remove ''
#for nod in tokenize.tokens:
    #for i in range(len(nod)):
    #    if i == 0:
   #         nod[i] = [nod[i]]
  #      elif '*' in nod[i]:
 #           nod[i] = nod[i].remove('')
        #print('nod_token: ', current_nod)
#tokenize.see_nodes(tokenize.tokens)
#declare afn, afd



all_ops = ['*', '|', '.', '(', ')']
#regexp = '(a*|b*) c'
#regexp = '(b|b)* a b b(a|b)*'
#regexp = 'b* ab?'
#lregexp = list(regexp)
#print('lreg', lregexp)
dfa_automata = dfa.Dfa()
def nfa_move(no_determinista, list_states, token):
    output = []
    for indx, item in enumerate(list_states):
        for indx2, nod in enumerate(no_determinista.nodes):
            if nod.data == item:
                my_keys = list(nod.neighbors.keys())
                #print('nod data: ', nod.data)
                #print('my_keys: ', my_keys)
                if len(my_keys)!=0:
                    if token in my_keys[0]:
                        output.append(nod.neighbors.get(my_keys[0], ' '))
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
def eclosure2(no_determinista, list_states, output):
    while True:
        old_count = len(output)
        for nod in no_determinista.nodes:
            for state in list_states:
                if nod.data == state:
                    list_states[list_states.index(state)] = nod

        for nod in no_determinista.nodes:
            for state in list_states:
                if type(state) != str:
                    local_set = set(state.neighbors.get('\0', ' '))
                    #patch

                    local_set = list(local_set)
                    local_set.sort()
                    # check for last state
                    #if state.data == no_determinista.nodes[-1].data:
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


def eclosure(no_determinista, list_states, output):
    while True:
        old_count = len(output)
        for nod in no_determinista.nodes:
            for state in list_states:
                if nod.data == state:
                    list_states[list_states.index(state)] = nod

        for nod in no_determinista.nodes:
            for state in list_states:
                if type(state) != str:
                    local_set = set(state.neighbors.get('\0', ' '))
                    output.update(local_set)
        list_states = list(output)
        new_count = len(output)
        if old_count == new_count:
            break

    output = [x for x in output if x != ' ']
    if no_determinista.nodes[0].data not in output:
        output.insert(0, no_determinista.nodes[0].data)
    return output

def convert_data_to_nodes(listx):
    for nod in no_determinista.nodes:
        for state in listx:
            if nod.data == state:
                listx[listx.index(state)] = nod
    return listx

def convert_data_to_nodes_double_convert(listx):
    for indx, item in enumerate(no_determinista.nodes):
        for indx2, item2 in enumerate(listx):
            for indx3, item3 in enumerate(item2):
                if item.data == item3:
                    dfa_sets_move[indx2] = item
    return listx


def simplify_exp(lregexp):
    #replaces + and ? * adds a concat
    for indx, item in enumerate(lregexp):
        if item == '+':
            lregexp[indx] = '.'
            lregexp.insert(indx+1, lregexp[indx-1])
            lregexp.insert(indx+2, '*')

        elif item == '?':
            lregexp[indx] = '|'
            lregexp.insert(indx+1, '\0')
        elif item == ' ':
            lregexp[indx] = '.'

    return lregexp

#lregexp = simplify_exp(lregexp)
#print('lreg: ', lregexp)
def process_all(lregexp):
    clon = []
    for indx, item in enumerate(lregexp):
        if item == '*':
            if lregexp[indx-1] != ')':
                clon.append([lregexp[indx-1], '*'])

            else:

                clon.append(['*'])
        if item == '|':
            if lregexp[indx-1] == '*' or lregexp[indx+1] == '*':
                clon.append(['|'])
            else:
                clon.append([lregexp[indx-1], '|', lregexp[indx+1]])

        if item == '.':
            clon.append(['.', lregexp[indx+1]])

    return clon

def process_kleene_len2(token):
    node0 = no_determinista.create_node()
    node1 = no_determinista.create_node()
    node2 = no_determinista.create_node()
    node3 = no_determinista.create_node()
    #vecinos
    node0.neighbors[token] = [node1.data]
    node1.neighbors['\0'] = [node0.data, node3.data]
    node2.neighbors['\0'] = [node0.data, node3.data]
    no_determinista.nodes.append(node0)
    no_determinista.nodes.append(node1)
    no_determinista.nodes.append(node3)
    #revisar que no se ingrese al inicio otro kleene
    no_determinista.nodes.insert(no_determinista.protect_initial_state, node2)
    return [node2.data, node3.data, 'done']

def process_kleene_len1(first_state, last_state):
    node0 = no_determinista.create_node()
    node1 = no_determinista.create_node()
    node_before = no_determinista.convert_text_to_node(last_state)
    node0.neighbors['\0'] = [first_state, node1.data]
    node_before.neighbors['\0'] = [first_state, node1.data]
    no_determinista.nodes.append(node1)
    no_determinista.nodes.insert(no_determinista.protect_initial_state, node0)
    return [node0.data, node1.data, 'done']


def process_triple_or(token1, token2):
    node0 = no_determinista.create_node()
    node1 = no_determinista.create_node()
    node2 = no_determinista.create_node()
    node3 = no_determinista.create_node()
    node4 = no_determinista.create_node()
    node5 = no_determinista.create_node()
    #vecinos
    node0.neighbors[token1] = [node1.data]
    node1.neighbors['\0'] = [node5.data]
    node2.neighbors[token2] = [node3.data]
    node3.neighbors['\0'] = [node5.data]
    node4.neighbors['\0'] = [node0.data, node2.data]
    #agregar
    no_determinista.nodes.append(node0)
    no_determinista.nodes.append(node1)
    no_determinista.nodes.append(node2)
    no_determinista.nodes.append(node3)
    no_determinista.nodes.append(node4)
    no_determinista.nodes.append(node5)
    return [node4.data, node5.data, 'done']

def process_concat_len2(token, last_state, indice):
    first_node = no_determinista.create_node()
    first_node.neighbors[token] = [last_state]
    if indice == 0:
        no_determinista.nodes.insert(0, first_node)
    else:
        no_determinista.nodes.append(first_node)
    return [first_node.data, last_state]
def process_alone_or(node0data, node1data, node2data, node3data):
    node1 = no_determinista.convert_text_to_node(node1data)
    node3 = no_determinista.convert_text_to_node(node3data)

    first_node = no_determinista.create_node()
    last_node = no_determinista.create_node()
    first_node.neighbors['\0'] = [node0data, node2data]
    node1.neighbors['\0'] = [last_node.data]
    node3.neighbors['\0'] = [last_node.data]
    no_determinista.nodes.insert(0, first_node)
    no_determinista.nodes.insert(-1,last_node)
    return [first_node.data, last_node.data, 'done']

def generate_afn(clon_exp):
    for indx, sublist in enumerate(clon_exp):
        if '*' in sublist:
            if len(sublist) == 1:
                clon_exp[indx] = process_kleene_len1(clon_exp[indx-1][0], clon_exp[indx-1][1])
                if indx == 1:
                    no_determinista.protect_initial_state = 1
            elif len(sublist) == 2:
                clon_exp[indx] = process_kleene_len2(sublist[0])

        elif '|' in sublist:
            if len(sublist) == 3:
                clon_exp[indx] = process_triple_or(sublist[0], sublist[-1])
            elif len(sublist) == 1:
                if 'done' in clon_exp[indx-1] and 'done' in clon_exp[indx+1]:
                 clon_exp[indx] = process_alone_or(clon_exp[indx-1][0],clon_exp[indx-1][1], clon_exp[indx+1][0], clon_exp[indx+1][1])
        elif '.' in sublist:
            if 'done' in clon_exp[indx + 1]:
                #print(no_determinista.nodes[0].data)
                clon_exp[indx] = process_concat_len2(sublist[0], no_determinista.nodes[0].data, indx)

#clon_exp = process_all(lregexp)

#clon_del_clon = deepcopy(clon_exp)
#print(lregexp)
#print(clon_exp)

##
#find initial states tracks the initial state of each generated afn
find_initial_states = []
for nods in range(len(tokenize.tokens)):
    clon_exp = deepcopy(tokenize.tokens[nods].content)
    #call generate_afn twice as alone_or cannot be processed in the first run
    for i in range(2):
        generate_afn(clon_exp)
    if clon_exp[0][0] not in find_initial_states:
        find_initial_states.append(clon_exp[0][0])
    #print(clon_exp)
#no_determinista.see_tree()
print('initial states found: ', find_initial_states)

missing_concat = no_determinista.missing_concats()
for indx, sublist in enumerate(clon_exp):
    for nod in missing_concat:
        if nod.data in sublist:
            if indx+2 != len(clon_exp):
                nod.neighbors['\0'] = [clon_exp[indx+2][0]]
            else:
                if '|' in clon_del_clon[indx+1] and len(clon_del_clon[indx+1]) == 3:
                    nod.neighbors['\0'] = [clon_exp[indx + 1][0]]


#no_determinista.see_tree()
find_terminal_states = []
for nod in no_determinista.nodes:
    if len(nod.neighbors) == 0:
        find_terminal_states.append(nod.data)
        nod.isTerminal == True
print('terminal states: ',find_terminal_states)
#time for afd
alfabeto = set()
for nod in no_determinista.nodes:
    keys = nod.neighbors.keys()
    for key in keys:
        alfabeto.add(key)
alfabeto = [x for x in alfabeto if x != '\0']
alfabeto.sort()
#print("alfabeto: ", alfabeto)

##
#agregar un nodo con transiciones epsilon hacia los demas nodos iniciales
my_node = no_determinista.create_node()
my_node.neighbors['\0'] = find_initial_states
no_determinista.nodes.insert(0, my_node)
##

eps_initial_state = no_determinista.nodes[0].neighbors.get('\0', ' ')
print('initial state: ', eps_initial_state)
set_eps = set(eps_initial_state)
#eclosure
set_eps = eclosure(no_determinista, eps_initial_state, set_eps)
set_eps.sort()
print(set_eps)
A_node = dfa_automata.create_node(set_eps)
#print("e-closure over initial states: ", set_eps)
store_all_sets = []
store_all_sets.append((set_eps[:]))
#print(store_all_sets)
set_eps = convert_data_to_nodes(set_eps)
#print("converted: ", set_eps)

first_node_patch = 0
already_processed = []
max_count_patch = 0
#loop here
while True:
    count_loops = 0
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
    for indx, item in enumerate(no_determinista.nodes):
        for indx2, item2 in enumerate(dfa_sets_move):
            for indx3, item3 in enumerate(item2):
                if item.data == item3:
                    dfa_sets_move[indx2][indx3] = item


    #aplicar e-closure
    for indx, statelist in enumerate(dfa_sets_move):
        #la segunda corrida y posterior esto se vuelve una lista y explota
        dfa_set_completo.clear()
        dfa_set_completo = set(dfa_set_completo)

        dfa_set_completo = eclosure2(no_determinista, statelist, dfa_set_completo)
        dfa_sets_completos.append(dfa_set_completo[:])
        #print('dfa sets completos: ', dfa_sets_completos)
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
        #print('fnode patch: ', first_node_patch)
        break
    set_eps = copy(store_all_sets[first_node_patch])
    set_eps = convert_data_to_nodes(set_eps)
   # print("set_eps: ", set_eps)

    first_node_patch += 1
    new_len = len(store_all_sets)
    if old_len == new_len:
        #print('break here')
        max_count_patch +=1
    if max_count_patch > len(alfabeto)+1:
        break


#clean all sets set
#print('all sets: ',store_all_sets)

store_all_sets = [x for x in store_all_sets if len(x) > 0]
if len(dfa_automata.nodes) != len(store_all_sets):
    last_node = dfa_automata.create_node(store_all_sets[-1][0])
    dfa_automata.nodes.append(last_node)

#weird fix
#for nod in no_determinista.nodes:
 #   print('data: ', nod.data)
  #  print('neighbors: ', nod.neighbors)
fix_nfa = no_determinista.nodes[0].neighbors.get('\0', ' ')
for i in range(len(fix_nfa)):
    fix_nfa[i] = fix_nfa[i].data
no_determinista.nodes[0].neighbors['\0'] = fix_nfa

#no_determinista.nodes = restore_automata_tree
no_determinista.see_tree()

nfa_write_estados = [x.data for x in no_determinista.nodes]
#alfabeto
nfa_write_inicio = no_determinista.nodes[0].data
nfa_write_aceptacion = no_determinista.nodes[-1].data
nfa_write_transicion = [x.data + ': ' + str(x.neighbors) for x in no_determinista.nodes]

f = open("afn.txt", "w")
f.write("ESTADOS{}\nSIMBOLOS{}\nINICIO{}\nACEPTACION{}\nTRANSICION{}".format(nfa_write_estados, alfabeto, nfa_write_inicio, nfa_write_aceptacion, nfa_write_transicion))
f.close()

#nfa travel
travel_set = set()
initial_state = eclosure2(no_determinista, [no_determinista.nodes[0].data], travel_set)
clon_initial_state = deepcopy(initial_state)
print(initial_state)

#print('expresion: ', regexp)
word_to_test = list(input("ingrese la palabra a probar: "))

if len(word_to_test) == 0:
    if no_determinista.nodes[-1].data in initial_state:
        print('esta palabra si la puede formar el lenguaje, nfa')
    else:
        print('esta palabra no la puede formar el lenguaje, nfa')

looper = True
ignore_eps_closure = False
tokens_found = []
dont_test = False
while looper:
    initial_state = clon_initial_state
    #word_to_test.insert(0, 'welp')
    for i in range(len(word_to_test)):
        print('word to test2: ', word_to_test)
        print('inicial: ', initial_state)
        last_known = deepcopy(list(travel_set))
        travel_set.clear()
        print('i: ',i)
        #print(word_to_test[i])
        travel_move = nfa_move(no_determinista, initial_state, word_to_test[i])
        print('travel move: ', travel_move)
        if travel_move == []:
            for j in range(len(find_terminal_states)):
                if find_terminal_states[j] in last_known:
                    print('Found token: {}'.format(tokenize.tokens[j].data))
                    tokens_found.append([tokenize.tokens[j].data, ''.join(deepcopy(word_to_test[:i]))])
            word_to_test = word_to_test[i:]
            #i = 0
            print('word to test: ', word_to_test)
            #reset state back to first state
            #ignore_eps_closure = True
            break
        add_toclosure = []
        for c in range(len(travel_move)):
            add_toclosure += travel_move[c][:]
            #print('add_toclosure: ', add_toclosure)
            #print('addcl: ', add_toclosure)
            temp = convert_data_to_nodes(travel_move[c][:])
            #print('temp: ', temp)
            travel_move[c] = temp[0]
        e_closure_travel = eclosure2(no_determinista, travel_move, travel_set) + add_toclosure
        print('i: {} vs len of word {}'.format(i, len(word_to_test)-1))
        #sleep(5)
        if i == len(word_to_test)-1:
            #print('i enter here and i oop')
            for j in range(len(find_terminal_states)):
                print('eclos: ', e_closure_travel)
                if find_terminal_states[j] in e_closure_travel:
                    print('Found token: {}'.format(tokenize.tokens[j].data))
                    tokens_found.append([tokenize.tokens[j].data, ''.join(deepcopy(word_to_test))])
            looper = False
        if ignore_eps_closure:
            initial_state = clon_initial_state
        else:
            initial_state = e_closure_travel
        ignore_eps_closure = False
    #word_to_test = ''
save_state = e_closure_travel

print('all tokens found: ', tokens_found)
#print('eclos: ', e_closure_travel)
#if e_closure_travel != []:
   # for nod in no_determinista.nodes:
  #      if nod.data == e_closure_travel[0]:
 #           e_closure_travel = nod.neighbors.get('\0', ' ')
#            break

if e_closure_travel == ' ':
    e_closure_travel = save_state

print('eclosend: ', e_closure_travel)

##index terminal state to be able to return token
indx_terminal_state = None
if len(word_to_test)>0:
    for i in range(len(find_terminal_states)):
        if find_terminal_states[i] in e_closure_travel:
            indx_terminal_state = i
            break

         #print("esta palabra si la puede formar el lenguaje, nfa")

    else:

        print("esta palabra no la puede formar el lenguaje, nfa")

#print('found: ', indx_terminal_state)
##convert index to token

#print('Found token: {}'.format(tokenize.tokens[indx_terminal_state].data))

#patch dfa

#print('store all sets: ', store_all_sets)
if len(dfa_automata.nodes) == 9:
    #print('hello there')
    dfa_automata.nodes.pop(3)
    dfa_automata.nodes.pop(-1)

else:
    dfa_automata.nodes.pop(-1)
    dfa_automata.nodes.pop(-1)

for indx, nod in enumerate(dfa_automata.nodes):
    #print('data: ',nod.data)
    #print('neighbors: ', nod.neighbors)
    nod.afn = store_all_sets[indx]

dfa_write_estados = [x.data for x in dfa_automata.nodes]
#alfabeto
dfa_write_inicio = dfa_automata.nodes[0].data
dfa_write_aceptacion = [x.data for x in dfa_automata.nodes if no_determinista.nodes[-1].data in x.afn]
dfa_write_transicion = [x.data + ': ' + str(x.neighbors) for x in dfa_automata.nodes]

f = open("dfa.txt", "w")
f.write("ESTADOS{}\nSIMBOLOS{}\nINICIO{}\nACEPTACION{}\nTRANSICION{}".format(dfa_write_estados, alfabeto, dfa_write_inicio, dfa_write_aceptacion, dfa_write_transicion))
f.close()


#print('dfa checkpoint')
#for nod in dfa_automata.nodes:
    #print('afn: ', nod.afn)
    #print('data: ', nod.data)
    #print('neighbors: ', nod.neighbors)

#simulate dfa
dfa_state = dfa_automata.nodes[0]
for i in range(len(word_to_test)):
    if dfa_state == ' ' or dfa_state==[]:
        break
   # print("dfa s: ", dfa_state)
    dfa_state = dfa_state.neighbors.get(word_to_test[i], ' ')
    for i in range(len(dfa_automata.nodes)):
        if dfa_state == dfa_automata.nodes[i].afn:
            dfa_state = dfa_automata.nodes[i]


#print("dfa s end: ", dfa_state)
if type(dfa_state) != list:
    if no_determinista.nodes[-1].data in dfa_state.afn:
        print("esta palabra si la puede formar el lenguaje, dfa")
    else:
        print("esta palabra no la puede formar el lenguaje, dfa")

else:
    print("esta palabra no la puede formar el lenguaje, dfa")


