class Node():
    def __init__(self):
        self.data = ''
        self.neighbors = {}
class NFA():
    def __init__(self):
        self.nodes = []
        self.current_node = 0

    def create_node(self):
        some_node = Node()
        some_node.data = 'q' + str(self.current_node)
        self.current_node += 1
        return some_node

    def see_tree(self):
        for nod in self.nodes:
            print('data: ', nod.data)
            print('neighbors: ', nod.neighbors)







