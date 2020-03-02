import utils as ut
import abtreelist as ltree
expresion = "(a.b)*c*"
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
expresion, return_to_original = ut.move_after_parenthesis(expresion)
expresion = ut.add_concat(expresion)
print(expresion)
#print(expresion)
syn_tree = ltree.Tree()
while len(expresion) > 0 or len(outp) > 1:
    if len(outp) > 0:
        print(outp)
        for indx, item in enumerate(outp):
            #concat is last case
            if item == '.':
                #or and kleene should not be present
                if '|' and '*' not in outp:
                    if len(syn_tree.nodes) == 0:
                        syn_tree.add_entree(outp[indx-1], '.', outp[indx+1])
                        #outp[indx-1] = syn_tree.count
                        for i in range(3):
                            del outp[indx-1]
                    else:
                        print("yo", outp)
                        syn_tree.add_entree(' ', '.', outp[1])
                        for i in range(2):
                            del outp[0]
            #kleene first case
            elif item == '*':
                syn_tree.add_entree(' ', '*', outp[indx-1])
                for i in range(2):
                    del outp[0]



    else:
        print("send to outp")
        if expresion[0] == '*':
            syn_tree.add_entree(' ', '*', ' ')
            del expresion[0]
        if '(' in expresion:

            #guardar index de parentesis para pushear de regreso
            indexar_parentesis = expresion.index('(')

            outp = outp + expresion[expresion.index('(') + 1:expresion.index(')')]
            #print(outp)
            expresion = expresion[:expresion.index('(')] + expresion[expresion.index(')') + 1:]
            print(expresion)
        else:
            outp = expresion[:]
            expresion.clear()

        #print(expresion)
    #break
print("finish, expression", expresion)
print("finish outp", outp)
syn_tree.see_tree()
if return_to_original > 0:
    for i in range(return_to_original):
        syn_tree.nodes[i], syn_tree.nodes[i+1] = syn_tree.nodes[i+1], syn_tree.nodes[i]
        syn_tree.nodes[i].reverse()
syn_tree.see_tree()