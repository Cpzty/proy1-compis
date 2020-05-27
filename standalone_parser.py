from copy import deepcopy
class ariParser():
    def __init__(self):
        self.parse_list = []
        self.start_pos = 0
    def expr(self):
        self.stat()
    
    def stat(self):
        value = self.Expression()
        print('final val: ',value)
    
    def plus_min(self):
        
        if self.start_pos < len(self.parse_list):
            if self.parse_list[self.start_pos] == '+' or self.parse_list[self.start_pos] == '-':
                self.start_pos += 1
                #print('plusmindebug: ', self.parse_list[self.start_pos-1])
                return deepcopy(self.parse_list[self.start_pos-1])
            return None
    
    def muldiv(self):
        
        if self.start_pos < len(self.parse_list):
            if self.parse_list[self.start_pos] == '*' or self.parse_list[self.start_pos] == '/':
                self.start_pos += 1
               # print('muldivdebug: ', self.parse_list[self.start_pos - 1])
                return deepcopy(self.parse_list[self.start_pos - 1])
            return None
    
    
    
    def Expression(self):
        result1 = self.Term()
        while True:
            op = self.plus_min()
            if op is None:
                break
    
            result2 = self.Term()
            if op == '+':
                result1 += result2
            else:
                result1 -= result2
        result = result1
        return result
    
    def Term(self):
        result1 = self.Factor()
        #print('res1: ',result1)
        while True:
            op = self.muldiv()
            if op is None:
                break
    
            result2 = self.Factor()
            if op == '*':
                result1 *= result2
            else:
                result1 /= result2
        result = result1
        return result
    
    def matchparentesis(self):
        
        if self.parse_list[self.start_pos] == '(':
            self.start_pos += 1
            return deepcopy(self.parse_list[self.start_pos - 1])
        return None
    
    
    def Factor(self):
        
        par = self.matchparentesis()
        if par != None:
            value = self.Expression()
            self.start_pos += 1
    
            return value
        return self.Number()
    
    def Number(self):
        
        try:
            #print('numdebug', self.parse_list[self.start_pos])
            value = int(self.parse_list[self.start_pos])
            self.start_pos += 1
            return value
        except:
            return None


class ariDoubleParser():
    def __init__(self):
        self.parse_list = []
        self.start_pos = 0

    def expr(self):
        self.stat()

    def stat(self):
        value = self.Expression()
        print('final val: ', round(value,4))

    def plus_min(self):

        if self.start_pos < len(self.parse_list):
            if self.parse_list[self.start_pos] == '+' or self.parse_list[self.start_pos] == '-':
                self.start_pos += 1
                # print('plusmindebug: ', self.parse_list[self.start_pos-1])
                return deepcopy(self.parse_list[self.start_pos - 1])
            return None

    def muldiv(self):

        if self.start_pos < len(self.parse_list):
            if self.parse_list[self.start_pos] == '*' or self.parse_list[self.start_pos] == '/':
                self.start_pos += 1
                # print('muldivdebug: ', self.parse_list[self.start_pos - 1])
                return deepcopy(self.parse_list[self.start_pos - 1])
            return None

    def Expression(self):
        result1 = self.Term()
        while True:
            op = self.plus_min()
            if op is None:
                break

            result2 = self.Term()
            if op == '+':
                result1 += result2
            else:
                result1 -= result2
        result = result1
        return result

    def Term(self):
        result1 = self.Factor()
        # print('res1: ',result1)
        while True:
            op = self.muldiv()
            if op is None:
                break

            result2 = self.Factor()
            if op == '*':
                result1 *= result2
            else:
                result1 /= result2
        result = result1
        return result

    def matchparentesis(self):

        if self.parse_list[self.start_pos] == '(':
            self.start_pos += 1
            return deepcopy(self.parse_list[self.start_pos - 1])
        return None

    def Factor(self):

        par = self.matchparentesis()
        if par != None:
            value = self.Expression()
            self.start_pos += 1

            return value
        return self.Float_number()

    def Float_number(self):

        try:
            # print('numdebug', self.parse_list[self.start_pos])
            value = float(self.parse_list[self.start_pos])
            self.start_pos += 1
            return value
        except:
            return None


class hexParser():
    def __init__(self):
        self.parse_list = []
        self.start_pos = 0

    def expr(self):
        self.stat()

    def stat(self):
        value = self.Expression()
        print('final val: ', value)

    def plus_min(self):

        if self.start_pos < len(self.parse_list):
            if self.parse_list[self.start_pos] == '+' or self.parse_list[self.start_pos] == '-':
                self.start_pos += 1
                # print('plusmindebug: ', self.parse_list[self.start_pos-1])
                return deepcopy(self.parse_list[self.start_pos - 1])
            return None

    def muldiv(self):

        if self.start_pos < len(self.parse_list):
            if self.parse_list[self.start_pos] == '*' or self.parse_list[self.start_pos] == '/':
                self.start_pos += 1
                # print('muldivdebug: ', self.parse_list[self.start_pos - 1])
                return deepcopy(self.parse_list[self.start_pos - 1])
            return None

    def Expression(self):
        result1 = self.Term()
        while True:
            op = self.plus_min()
            if op is None:
                break

            result2 = self.Term()
            if op == '+':
                result1 += result2
            else:
                result1 -= result2
        result = result1
        return result

    def Term(self):
        result1 = self.Factor()
        # print('res1: ',result1)
        while True:
            op = self.muldiv()
            if op is None:
                break

            result2 = self.Factor()
            if op == '*':
                result1 *= result2
            else:
                result1 /= result2
        result = result1
        return result

    def matchparentesis(self):

        if self.parse_list[self.start_pos] == '(':
            self.start_pos += 1
            return deepcopy(self.parse_list[self.start_pos - 1])
        return None

    def Factor(self):

        par = self.matchparentesis()
        if par != None:
            value = self.Expression()
            self.start_pos += 1

            return value
        return self.Number()

    def Number(self):

        try:
            # print('numdebug', self.parse_list[self.start_pos])
            value = int(self.parse_list[self.start_pos], 16)
            self.start_pos += 1
            return value
        except:
            return None
