
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


