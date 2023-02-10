#expression     → additive
#additive       → division (("+" | "-") division)*
#division       → term ( "/" term)*
#term           → unary unary* | unary " * " unary
#term           → unary ("*"? unary)*
#unary          → NUMBER | VARIABLE | "(" expression ")"


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
                self.currentPosition += 1
                return newNode
            else:    
                raise Exception("Missing closing bracket")
        currentNumber = ""
        while self.GetCurrentCharacter() in ["1","2","3", ### put this loop at the top because need to constantly check if new term has ()
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
            if self.GetCurrentCharacter() in ["1","2","3",
            "4","5","6",
            "7","8","9",
            "0","("]:


                nextUnary = self.unary()
                self.currentPosition += 1
                currentTree = Node("*",currentTree,nextUnary)
            else:
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
   

coolParser = Parser("3((1+2)/3)")
printer = NodePrinter()
printer.printNode(coolParser.Parser())