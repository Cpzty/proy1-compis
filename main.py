import utils as ut
import abtreelist as ltree
expresion = "(aa)b"
outp = []

#should receive from outp only if expression is not empty
#save index of (
indexar_parentesis = 0
#convertir expresion a lista
expresion = list(expresion)

#primero cambiar ? y +
expresion = ut.op_opcional(expresion)
expresion = ut.op_positivo(expresion)
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
                    if len(outp) > 2:
                        syn_tree.add_entree(outp[indx-1], '.', outp[indx+1])
                        #outp[indx-1] = syn_tree.count
                        for i in range(3):
                            del outp[indx-1]
                    else:
                        syn_tree.add_entree(' ', '.', outp[indx+1])
                        for i in range(2):
                            del outp[indx]



    else:
        print("send to outp")
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