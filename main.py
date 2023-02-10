#expression     → additive
#additive       → division (("+" | "-") division)*
#division       → term ("/" term)*
#term           → index ("*"? index)*
#index          → unary ("^" unary)*
#negate         → "-"* unary
#unary          → NUMBER | VARIABLE | "(" expression ")"

class Node:
    def __init__(self, val, leftPtr, rightPtr):
        self.val = val
        self.leftPtr = leftPtr
        self.rightPtr = rightPtr

class Lexer:
    ["x" , "(" , "1231" , "+" , "pi" , ")"]
    def __init__(self,string):
        self.string = string
        self.currentPosition = 0
        self.list = []
        self.temporaryPosition = 0
        self.currentChar = ""
        self.Iterate()

    def Iterate(self):
        for i in range(0,len(self.string)):
            if self.currentPosition >= len(self.string):
                break
            self.currentChar = self.string[self.currentPosition].lower()
            if self.currentChar == "+":
                self.AddToken("+")
            elif self.currentChar == "*":
                self.AddToken("*")
            elif self.currentChar == "-":
                self.AddToken("-")
            elif self.currentChar == "/":
                self.AddToken("/")
            elif self.currentChar == "^":
                self.AddToken("^")
            elif self.currentChar == "(":
                self.AddToken("(")
            elif self.currentChar == ")":
                self.AddToken(")")
            elif self.currentChar == "p":
                self.HandleP()
            elif self.currentChar == "c":
                self.HandleC()
            elif self.currentChar == "s":
                self.HandleS()
            elif self.currentChar == "t":
                self.HandleT()
            else:
                self.HandleElse()
            self.currentPosition += 1
            

    def AddToken(self,token):
        self.list.append(token)

    def PeekAhead(self,count):
        if self.currentPosition + count <= len(self.string):
            return self.string[self.currentPosition + count]
        else:
            return chr(0) 

    def HandleP(self):
        if self.PeekAhead(1) == "i":
            self.AddToken("pi")
            self.currentPosition += 1
        if self.PeekAhead(1) == "s" and self.PeekAhead(2) == "i":
            self.AddToken("psi")
            self.currentPosition += 2
    
    def HandleC(self):
        if self.PeekAhead(1) == "o" and self.PeekAhead(2) == "s":
            self.AddToken("cos")
            self.currentPosition += 2

    def HandleS(self):
        if self.PeekAhead(1) == "i" and self.PeekAhead(2) == "n":
            self.AddToken("sin")
            self.currentPosition += 2
    
    def HandleT(self):
        if self.PeekAhead(1) == "a" and self.PeekAhead(2) == "n":
            self.AddToken("tan")
            self.currentPosition += 2

    def HandleElse(self):
        outputToken = self.currentChar
        i = 1
        while ord(self.PeekAhead(i).lower()) <= 57 and ord(self.PeekAhead(i).lower()) >= 48:
            outputToken = outputToken + self.PeekAhead(i)
            i += 1
        self.AddToken(outputToken)
        self.currentPosition += i - 1

class Parser:
    def __init__(self, string):
        self.string = string
        self.currentPosition = 0

    def GetCurrentCharacter(self):
        if self.currentPosition >= len(self.string):
            return chr(0)
        else:
            return self.string[self.currentPosition]

    def unary(self):
        
        if self.GetCurrentCharacter() == "(":
            self.currentPosition += 1
            newNode = self.Parser()
            if self.GetCurrentCharacter() == ")":
                self.currentPosition += 1
                return newNode
            else:    
                raise Exception("Missing closing bracket")
        currentNumber = ""
        if self.GetCurrentCharacter() in ["1","2","3",
                "4","5","6",
                "7","8","9",
                "0"]:
            while self.GetCurrentCharacter() in ["1","2","3",
                "4","5","6",
                "7","8","9",
                "0"]:
                currentNumber += self.string[self.currentPosition]
                self.currentPosition += 1
        elif self.GetCurrentCharacter().lower() in list(map(chr, range(97, 123))):
            currentNumber += self.GetCurrentCharacter()
            self.currentPosition += 1
            
        
        #number = int(currentNumber)
        return Node(currentNumber,None,None)

    def negate(self):
        negateCount = 0
        tempPosition = self.currentPosition
        while self.GetCurrentCharacter() == "-":
            negateCount += 1
            self.currentPosition += 1
        currentTree = self.unary()
        if negateCount % 2 == 1:
            currentTree = Node("*",Node(-1,None,None),currentTree)
        return currentTree

    def index(self):
        currentTree = self.negate()
        while self.GetCurrentCharacter() == "^":
            self.currentPosition += 1
            nextTerm = self.negate()
            currentTree = Node("^",currentTree,nextTerm)

        return currentTree


    def term(self):
        currentTree = self.index()

        while self.GetCurrentCharacter() in ["1","2","3",
            "4","5","6",
            "7","8","9",
            "0","(","*"] or self.GetCurrentCharacter().lower() in list(map(chr, range(97, 123))):
            if self.GetCurrentCharacter() in ["1","2","3",
            "4","5","6",
            "7","8","9",
            "0","("] or self.GetCurrentCharacter().lower() in list(map(chr, range(97, 123))):
                nextUnary = self.index()
                self.currentPosition += 1
                currentTree = Node("*",currentTree,nextUnary)
            else:
                self.currentPosition += 1
                nextUnary = self.index()
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


class NodePrinter:
    def printNode(self,node):
        print(node.val)
        self.printNodeWithIndentation(node, 0)


    def printNodeWithIndentation(self,node, indentation):
        if node.leftPtr or node.rightPtr:
            print(self.getIndentation(indentation) + "|")
        if (node.leftPtr):
            print(self.getIndentation(indentation) + "-> " + str(node.leftPtr.val))
            self.printNodeWithIndentation(node.leftPtr, indentation + 1)
		
        if (node.rightPtr):
            print(self.getIndentation(indentation) + "-> " + str(node.rightPtr.val))
            self.printNodeWithIndentation(node.rightPtr, indentation + 1)
        self.getIndentation(1)

    def getIndentation(self,n):
        return "|  " * n	
   
lexer = Lexer("131094+tan(x)")
coolParser = Parser("1-x(-y)")
printer = NodePrinter()
printer.printNode(coolParser.Parser())