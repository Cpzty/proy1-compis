class Tree():
    def __init__(self):
        self.nodes = {}
        self.count = 1
    def add_entree(self, left, op, right):
        if left != ' ':
            self.nodes[self.count] = left
            self.count += 1
        if right != ' ':
            self.nodes[self.count] = right
            self.count += 1
        #op nunca es vacia
        self.nodes[self.count] = op

    def see_tree(self):
        print(self.nodes)

sin_tree = Tree()

sin_tree.add_entree(ord('a'), '|', ord('b'))
sin_tree.see_tree()