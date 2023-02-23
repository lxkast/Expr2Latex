# Expr2Latex
Mathematical expression to LaTeX converter written in Python

# Usage
## Creating lexer
```py
lexer = Lexer("root(1+tan^2x)")
```
## Creating parser
```py
coolParser = Parser(lexer.list)
parsed = coolParser.Parser()
```
## Printing tree (for debugging)
```py
printer = NodePrinter()
printer.printNode(parsed)
```
## Output LaTeX
```py
print(LaTeXBuilder().build(parsed))
```
