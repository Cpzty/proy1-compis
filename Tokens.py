class Node():
    def __init__(self):
        self.data = ''
        self.content = []
        self.exceptions = []

class Tokens:
    def __init__(self):
        self.characters = []
        self.keywords = {}
        self.tokens = []
        self.productions = []
        self.tokens_excepto = []
    def create_node(self):
        my_node = Node()
        return my_node

    def see_nodes(self, what_list):
        if what_list != self.keywords:
            for nod in what_list:
                print('name: ', nod.data)
                print('content: ', nod.content)
                print('exceptions: ', nod.exceptions)
        else:
            print(what_list)



