import string
all_letters = [x for x in string.ascii_uppercase]

class Node:
    def __init__(self):
        self.data = ''
        self.neighbors = {}


class Dfa:
    def __init__(self):
        self.nodes = []
        self.current_node = 0
        self.afn = None
    def create_node(self, afn):
        some_node = Node()
        some_node.data = all_letters[self.current_node]
        self.current_node += 1
        some_node.afn = afn
        return some_node
