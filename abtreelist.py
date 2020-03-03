class Tree():
    def __init__(self):
        self.nodes = []
        self.count = 0
    def add_entree(self, left, op, right):
        if len(self.nodes) == 0:
            if right != ' ':
                node = [left, op, right]
            else:
                node = [left, op]
            self.nodes.append(node)
        else:
            if left == ' ':
                #node = [self.count, op, right]
                node = [op, right]
            elif right == ' ' and left == ' ':
                #node = [self.count, op]
                node = [op]
            elif right == ' ':
                node = [left, op]
            else:
                node = [left, op, right]
            #self.count += 1
            self.nodes.append(node)
        #op nunca es vacia

    def see_tree(self):
        print(self.nodes)

#sin_tree = Tree()

#sin_tree.add_entree(str(ord('a')), '|', str(ord('b')))
#sin_tree.add_entree(str(ord('a')), '|', str(ord('b')))
#sin_tree.add_entree(str(ord('a')), '|', str(ord('b')))

#sin_tree.see_tree()