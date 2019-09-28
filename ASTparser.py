import ast

class ASTParser:
    def __init__(self, location):
        self.location = location

    def getAstObject(self):
        code = open(self.location).read()
        return ast.parse(source = code, filename=self.location)
