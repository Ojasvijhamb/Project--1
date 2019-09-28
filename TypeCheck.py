import ast

class TypeCheck(ast.NodeVisitor):

    def checkType(self, node):
        return self.visit_Module(node)

    def visit_Module(self, node):
        results = [self.visit(s) for s in node.body]
        return all(results)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_BinOp(self, node):
        return self.visit(node.left) == self.visit(node.right) or type(node.left) == ast.Name or type(node.right) == ast.Name

    def visit_BoolOp(self, node):
        return set([type(self.visit(b)) for b in node.values]) == bool or type(node.op) == ast.Name

    def visit_UnaryOp(self, node):
        return True

    def visit_Assign(self, node):
        return set([self.visit(target) for target in node.targets]) == self.visit(node.value) or type(node.targets[0]) == ast.Name or sum([self.visit(target) == ast.Name for target in node.targets])

    def visit_AugAssign(self, node):
        return True

    def visit_Attribute(self, node):
        return type(node.attr) == 'DataFrame'

    def visit_For(self, node):
        return all([self.visit(s) for s in node.body]) and all([self.visit(s) for s in node.orelse])

    def visit_While(self, node):
        return all([self.visit(s) for s in node.body]) and all([self.visit(s) for s in node.orelse]) and self.visit(node.test)

    def visit_If(self, node):
        return all([self.visit(s) for s in node.body]) and all([self.visit(s) for s in node.orelse])

    def visit_Try(self, node):
        return all([self.visit(s) for s in node.body]) and all([self.visit(s) for s in node.handlers]) and all([self.visit(s) for s in node.orelse]) and all([self.visit(s) for s in node.finalbody])

    def visit_ExceptHandler(self, node):
        return [self.visit(s) for s in node.body]

    def visit_IfExp(self, node):
        return self.visit(node.body) and self.visit(node.orelse)

    def visit_Dict(self, node):
        return True

    def visit_Set(self, node):
        return True

    def visit_Compare(self, node):
        if self.visit(node.left) is int and self.visit(node.comparators[0]) is int:
            return bool
        elif self.visit(node.left) is str and self.visit(node.right) is str:
            return bool
        elif type(self.visit(node.left)) is ast.Name or type(set([self.visit(right) for right in node.comparators]).__contains__(ast.Name)):
            return bool

    def visit_Num(self, node):
        return type(node.n)

    def visit_Str(self, node):
        return type(node)

    def visit_NameConstant(self, node):
        return type(node.value)

    def visit_List(self, node):
        return True

    def visit_Import(self, node):
        return True

    def visit_ImportFrom(self, node):
        return True
