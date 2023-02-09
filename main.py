class Node:
    def __init__(self, val, leftPtr, rightPtr):
        self.val = val
        self.leftPtr = leftPtr
        self.rightPtr = rightPtr

class Parser:
    def __init__(self, string):
        self.string = string
        self.currentPosition = 0

    def GetCurrentCharacter(self):
        if self.currentPosition >= len(self.string):
            return None
        else:
            return self.string[self.currentPosition]

    def unary(self):
        if self.GetCurrentCharacter() == "(":
            self.currentPosition += 1
            newNode = self.Parser()
            if self.GetCurrentCharacter() == ")":
                return newNode
            else:    
                raise Exception("Missing closing bracket")
        currentNumber = ""
        while self.GetCurrentCharacter() in ["1","2","3",
                "4","5","6",
                "7","8","9",
                "0"]:
            currentNumber += self.string[self.currentPosition]
            self.currentPosition += 1
        number = int(currentNumber)
        return Node(number,None,None)




    def term(self):
        currentTree = self.unary()

        while self.GetCurrentCharacter() in ["1","2","3",
            "4","5","6",
            "7","8","9",
            "0","(","*"]:
            self.currentPosition += 1
            nextUnary = self.unary()
            currentTree = Node("*",currentTree,nextUnary)
        
        return currentTree
                

    def division(self):
        currentTree = self.term()
        while self.GetCurrentCharacter() == "/":
            self.currentPosition += 1
            nextTerm = self.term()
            currentTree = Node("/",currentTree,nextTerm)

        return currentTree

    def additive(self):
        currentTree = self.division()
        while self.GetCurrentCharacter() in ["+","-"]:
            currentOperation = self.string[self.currentPosition]
            self.currentPosition += 1
            nextDivision = self.division()
            currentTree = Node(currentOperation,currentTree,nextDivision)
        return currentTree

    def Parser(self):
        return self.additive()

coolParser = Parser("(1+2)")
coolParser.Parser()
print("gdilsfhuudf")