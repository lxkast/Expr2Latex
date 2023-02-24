#expression     → additive
#additive       → division (("+" | "-") division)*
#division       → term ("/" term)*
#term           → index ("*"? index)*
#index          → unary ("^" unary)*
#negate         → "-"* unary
#func           → UNARY | ("sin", ("cos"), ...) ("^"unary)? ( ( "(" expression ")" ) | unary )
#unary          → NUMBER | VARIABLE | "(" expression ")"

class Node:
    def __init__(self, val, leftPtr, rightPtr):
        self.val = val
        self.leftPtr = leftPtr
        self.rightPtr = rightPtr

class Token:
    def __init__(self, type, val):
        self.type = type
        self.val = val

class Lexer:
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
                self.list.append(Token("additive","+"))
            elif self.currentChar == "*":
               self.list.append(Token("term","*"))
            elif self.currentChar == "-":
                self.list.append(Token("additive","-"))
            elif self.currentChar == "/":
                self.list.append(Token("division","/"))
            elif self.currentChar == "^":
                self.list.append(Token("index","^"))
            elif self.currentChar == "(":
                self.list.append(Token("unary","("))
            elif self.currentChar == ")":
                self.list.append(Token("unary",")"))
            elif self.currentChar == "p":
                self.HandleP()
            elif self.currentChar == "c":
                self.HandleC()
            elif self.currentChar == "s":
                self.HandleS()
            elif self.currentChar == "t":
                self.HandleT()
            elif self.currentChar == "r":
                self.HandleR()
            else:
                self.HandleElse()
            self.currentPosition += 1
            

    def AddToken(self,token):
        self.list.append(token)

    def PeekAhead(self,count):
        if self.currentPosition + count < len(self.string):
            return self.string[self.currentPosition + count]
        else:
            return chr(0) 

    def HandleP(self):
        if self.PeekAhead(1) == "i":
            self.list.append(Token("unary","pi"))
            self.currentPosition += 1
        elif self.PeekAhead(1) == "s" and self.PeekAhead(2) == "i":
            self.list.append(Token("unary","psi"))
            self.currentPosition += 2
        else:
            self.list.append(Token("unary","p"))
    
    def HandleC(self):
        if self.PeekAhead(1) == "o" and self.PeekAhead(2) == "s" and self.PeekAhead(3) == "h":
            self.list.append(Token("func","cosh"))
            self.currentPosition += 3
        elif self.PeekAhead(1) == "o" and self.PeekAhead(2) == "s":
            self.list.append(Token("func","cos"))
            self.currentPosition += 2
        else:
            self.list.append(Token("unary","c"))

    def HandleS(self):
        if self.PeekAhead(1) == "i" and self.PeekAhead(2) == "n" and self.PeekAhead(3) == "h":
            self.list.append(Token("func","sinh"))
            self.currentPosition += 3
        elif self.PeekAhead(1) == "i" and self.PeekAhead(2) == "n":
            self.list.append(Token("func","sin"))
            self.currentPosition += 2
        elif self.PeekAhead(1) == "q" and self.PeekAhead(2) == "r" and self.PeekAhead(3) == "t":
            self.list.append(Token("func","sqrt"))
            self.currentPosition += 3
        else:
            self.list.append(Token("unary","s"))
    
    def HandleT(self):
        if self.PeekAhead(1) == "a" and self.PeekAhead(2) == "n" and self.PeekAhead(3) == "h":
            self.list.append(Token("func","tanh"))
            self.currentPosition += 3
        elif self.PeekAhead(1) == "a" and self.PeekAhead(2) == "n":
            self.list.append(Token("func","tan"))
            self.currentPosition += 2
        else:
            self.list.append(Token("unary","t"))

    def HandleR(self):
        if self.PeekAhead(1) == "o" and self.PeekAhead(2) == "o" and self.PeekAhead(3) == "t":
            self.list.append(Token("func","sqrt"))
            self.currentPosition += 3
        else:
            self.list.append(Token("unary","r"))  

    def HandleElse(self):
        outputToken = self.currentChar
        i = 1
        decimalPlaces = 0
        while ord(self.PeekAhead(i).lower()) <= 57 and ord(self.PeekAhead(i).lower()) >= 48:
            outputToken = str(outputToken) + str(self.PeekAhead(i))
            i += 1
        if self.PeekAhead(i) == ".":
            i += 1
            outputToken += "."
            while ord(self.PeekAhead(i).lower()) <= 57 and ord(self.PeekAhead(i).lower()) >= 48:
                outputToken = str(outputToken) + str(self.PeekAhead(i))
                i += 1
        if outputToken != " ":
            self.list.append(Token("unary",outputToken))
            self.currentPosition += i - 1

class Parser:
    def __init__(self, list):
        self.list = list
        self.currentPosition = 0

    def GetCurrentCharacter(self):
        if self.currentPosition >= len(self.list):
            return Token("None",chr(0))
        else:
            return self.list[self.currentPosition]

    def unary(self):
        
        if self.GetCurrentCharacter().val == "(":
            self.currentPosition += 1
            newNode = self.Parser()
            if self.GetCurrentCharacter().val == ")":
                self.currentPosition += 1
                return newNode
            elif self.GetCurrentCharacter().type == "None":
                return newNode
            else:    
                raise Exception("Missing closing bracket")
        currentNumber = ""
        if self.GetCurrentCharacter().type == "unary":
            currentNumber = str(self.GetCurrentCharacter().val)
            self.currentPosition += 1
        if currentNumber == "":
            raise Exception("Syntax error")
        # if self.GetCurrentCharacter() in ["1","2","3",
        #         "4","5","6",
        #         "7","8","9",
        #         "0"]:
        #     while self.GetCurrentCharacter() in ["1","2","3",
        #         "4","5","6",
        #         "7","8","9",
        #         "0"]:
        #         currentNumber += self.list[self.currentPosition]
        #         self.currentPosition += 1
        # elif self.GetCurrentCharacter().lower() in list(map(chr, range(97, 123))):
        #     currentNumber += self.GetCurrentCharacter()
        #     self.currentPosition += 1
            
        
        #number = int(currentNumber)
        return Node(Token("unary",currentNumber),None,None)

    def func(self):
        if self.GetCurrentCharacter().type == "func":
            function = self.GetCurrentCharacter().val
            self.currentPosition += 1
            if self.GetCurrentCharacter().type == "index":
                self.currentPosition += 1
                index = self.unary()
                if self.GetCurrentCharacter().val == "(":
                    self.currentPosition += 1
                    expression = self.Parser()
                    self.currentPosition += 1
                    currentTree = Node(Token("func",function),expression,None)
                else:
                    unary = self.unary()
                    currentTree = Node(Token("func",function),unary,None)
                currentTree = Node(Token("index","^"),currentTree,index)
                
            elif self.GetCurrentCharacter().val == "(":
                self.currentPosition += 1
                expression = self.Parser()
                self.currentPosition += 1
                currentTree = Node(Token("func",function),expression,None)
            else:
                unary = self.unary()
                currentTree = Node(Token("func",function),unary,None)
        else:
            currentTree = self.unary()
        return currentTree

    def negate(self):
        negateCount = 0
        tempPosition = self.currentPosition
        while self.GetCurrentCharacter().val == "-":
            negateCount += 1
            self.currentPosition += 1
        currentTree = self.func()
        if negateCount % 2 == 1:
            currentTree = Node(Token("term","*"),Node(Token("unary","-1"),None,None),currentTree)
        return currentTree

    def index(self):
        currentTree = self.negate()
        while self.GetCurrentCharacter().type == "index":
            self.currentPosition += 1
            nextTerm = self.negate()
            currentTree = Node(Token("index","^"),currentTree,nextTerm)

        return currentTree


    def term(self):
        currentTree = self.index()

        while self.GetCurrentCharacter().type == "unary" or self.GetCurrentCharacter().type == "term" or self.GetCurrentCharacter().type == "func":
            if (self.GetCurrentCharacter().type == "unary" and self.GetCurrentCharacter().val != ")") or self.GetCurrentCharacter().val == "(":
                nextUnary = self.index()
                currentTree = Node(Token("term","*"),currentTree,nextUnary)
            elif self.GetCurrentCharacter().val == "*":
                self.currentPosition += 1
                nextUnary = self.index()
                currentTree = Node(Token("term*","*"),currentTree,nextUnary)
            elif self.GetCurrentCharacter().type == "func":
                nextUnary = self.index()
                currentTree = Node(Token("term","*"),currentTree,nextUnary)
            else:
                break
        return currentTree
                

    def division(self):
        currentTree = self.term()
        while self.GetCurrentCharacter().type == "division":
            self.currentPosition += 1
            nextTerm = self.term()
            currentTree = Node(Token("division","/"),currentTree,nextTerm)
        return currentTree

    def additive(self):
        currentTree = self.division()
        while self.GetCurrentCharacter().type == "additive":
            currentToken = self.GetCurrentCharacter().val
            self.currentPosition += 1
            nextDivision = self.division()
            currentTree = Node(Token("additive",currentToken),currentTree,nextDivision)
        return currentTree

    def Parser(self):
        returnval = self.additive()
        return returnval


class NodePrinter:
    def printNode(self,node):
        print((node.val).val)
        self.printNodeWithIndentation(node, 0)


    def printNodeWithIndentation(self,node, indentation):
        if node.leftPtr or node.rightPtr:
            print(self.getIndentation(indentation) + "|")
        if (node.leftPtr):
            print(self.getIndentation(indentation) + "-> " + str(node.leftPtr.val.val))
            self.printNodeWithIndentation(node.leftPtr, indentation + 1)
		
        if (node.rightPtr):
            print(self.getIndentation(indentation) + "-> " + str(node.rightPtr.val.val))
            self.printNodeWithIndentation(node.rightPtr, indentation + 1)
        self.getIndentation(1)

    def getIndentation(self,n):
        return "|  " * n	

class LaTeXBuilder:
    finalLatex = ""

    def write(self,string):
        self.finalLatex += string

    def build(self,tree):
        self.process(tree)
        self.finalLatex = "$" + self.finalLatex + "$"
        return self.finalLatex

    def process(self,tree):
        if tree.val.type == "unary":
            self.write(tree.val.val)
        elif tree.val.type == "additive":
            self.process(tree.leftPtr)
            self.write(tree.val.val)
            self.process(tree.rightPtr)
        elif tree.val.type == "division":
            self.write("\\frac{")
            self.process(tree.leftPtr)
            self.write("}{")
            self.process(tree.rightPtr)
            self.write("}")
        elif tree.val.type == "index":
            if tree.leftPtr.val.type != "unary" and  tree.leftPtr.val.type != "func":
                self.write("(")
                self.process(tree.leftPtr)
                self.write(")")
            else:
                self.process(tree.leftPtr)
            self.write(tree.val.val)
            if tree.rightPtr.val.type != "unary" and tree.rightPtr.val.type != "func":
                self.write("{")
                self.process(tree.rightPtr)
                self.write("}")
            else:
                self.process(tree.rightPtr)
        elif tree.val.type == "func":
            if (tree.val.val == "sqrt"):
                self.write(f"\\{tree.val.val}")
                self.write("{")
                self.process(tree.leftPtr)
                self.write("}")
            else:
                self.write(f"\\{tree.val.val}")
                self.write("(")
                self.process(tree.leftPtr)
                self.write(")")
        elif tree.val.type == "term*":
            if tree.leftPtr.val.type != "unary" and  tree.leftPtr.val.type != "func":
                self.write("(")
                self.process(tree.leftPtr)
                self.write(")")
            else:
                self.process(tree.leftPtr)
            self.write(tree.val.val)
            if tree.rightPtr.val.type != "unary" and tree.rightPtr.val.type != "func":
                self.write("(")
                self.process(tree.rightPtr)
                self.write(")")
            else:
                self.process(tree.rightPtr)
        elif tree.val.type == "term":

		# Write left (and wrap in brackets if it's not a unary or func)
		if tree.leftPtr.val.type != "unary" and  tree.leftPtr.val.type != "func":
			self.write("(")
			self.process(tree.leftPtr)
			self.write(")")
		else:
			self.process(tree.leftPtr)

		# If we just wrote a number and we're about to write another, we need to put brackets around the right.
		insertBracketsCauseBothNumbers = False
		if ord(finalLatex[len(finalLatex) - 1]) <= 57 and ord(finalLatex[len(finalLatex) - 1]) >= 48 and ord(tree.rightPtr.val.val[0]) <= 57 and ord(tree.rightPtr.val.val[0]) >= 48:
			self.write("(")
			insertBracketsCauseBothNumbers = True

		# Write right (and wrap in brackets if it's not a unary or func)
		if tree.rightPtr.val.type != "unary" and tree.rightPtr.val.type != "func":
			self.write("(")
			self.process(tree.rightPtr)
			self.write(")")
		else:
			self.process(tree.rightPtr)

		if insertBracketsCauseBothNumbers == True:
			self.write(")")
