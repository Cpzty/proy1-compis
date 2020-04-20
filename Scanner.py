import  Tokens
from copy import deepcopy

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
#print(characters_slice)
#print(keywords_slice)
#print(tokens_slice)
#clean empties from all 3
characters_slice = [x for x in characters_slice if x!= ['']]
keywords_slice = [x for x in keywords_slice if x!= ['']]
tokens_slice = [x for x in tokens_slice if x!= ['']]

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

tokenize.see_nodes(tokenize.characters)
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
    my_node.content = substring
    tokenize.tokens.append(my_node)

for indx, sublist in enumerate(tokenize.tokens_excepto):
    for indx2, nod in enumerate(tokenize.tokens):
        if nod.data == sublist[0]:
            nod.exceptions = sublist[1:]
#checkpoint1
#tokenize.see_nodes(tokenize.tokens)
#replace tokens for their true contenttokenize.see_nodes(tokenize.characters)
for toke1 in tokenize.tokens:
    for toke2 in tokenize.characters:
        my_text = toke1.content.split()
       # print(my_text)
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
                    print(toke1.content)
tokenize.see_nodes(tokenize.tokens)
#experiment 1
experiment1 = tokenize.tokens[0].content.strip()
#print(experiment1.split(' '))
