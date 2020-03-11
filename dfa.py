import string
all_letters = string.ascii_uppercase
class Dfa_node():
    def __init__(self):
        self.data = ''
        self.transitions = {}
        self.count = 0
    def create_all_transitions(self, alphabet):
        for token in alphabet:
            self.transitions[token] = ' '



