class Node():
    def __init__(self):
        self.data = ''
        self.neighbors = {}
        self.isTerminal = False
class NFA():
    def __init__(self):
        self.nodes = []
        self.current_node = 0
        self.protect_initial_state = 0
    def create_node(self):
        some_node = Node()
        some_node.data = 'q' + str(self.current_node)
        self.current_node += 1
        return some_node

    def see_tree(self):
        for nod in self.nodes:
            print('data: ', nod.data)
            print('neighbors: ', nod.neighbors)

    def convert_text_to_node(self, text):
        for nod in self.nodes:
            if text == nod.data:
                return nod

    def missing_concats(self):
        all_missing = []
        for nod in self.nodes:
            if nod.data != self.nodes[-1].data:
                if not bool(nod.neighbors):
                    all_missing.append(nod)
        return all_missing







