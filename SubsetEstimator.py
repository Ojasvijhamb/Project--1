import ast


class LanguageSubsetEstimator(ast.NodeVisitor):

    def isLanguageSubset(self, node):
        return self.visit_Module(node)

    def visit_Module(self, node):
        results = [self.visit(s) for s in node.body]
        return all(results)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Return(self, node):
        return self.visit(node.value)

    def visit_Assign(self, node):
        return [self.visit(target) for target in node.targets] and self.visit(node.value)

    def visit_AugAssign(self, node):
        return self.visit(node.op) and self.visit(node.value)

    def visit_Call(self, node):
        return self.visit(node.func)

    def visit_Attribute(self, node):
        return True if node.attr is 'DataFrame' else False

    def visit_For(self, node):
        return all([self.visit(s) for s in node.body]) and all([self.visit(s) for s in node.orelse])

    def visit_While(self, node):
        return all([self.visit(s) for s in node.body]) and all([self.visit(s) for s in node.orelse]) and self.visit(node.test)

    def visit_Compare(self, node):
        return self.visit(node.left) and all([self.visit(comp) for comp in node.comparators])

    def visit_If(self, node):
        return all([self.visit(s) for s in node.body]) and all([self.visit(s) for s in node.orelse])

    def visit_Try(self, node):
        return all([self.visit(s) for s in node.body]) and all([self.visit(s) for s in node.handlers]) and all([self.visit(s) for s in node.orelse]) and all([self.visit(s) for s in node.finalbody])

    def visit_ExceptHandler(self, node):
        return [self.visit(s) for s in node.body]

    def visit_BinOp(self, node):
        return self.visit(node.left) and self.visit(node.right)

    def visit_BoolOp(self, node):
        return all([self.visit(b) for b in node.values])

    def visit_UnaryOp(self, node):
        return self.visit(node.operand)

    def visit_IfExp(self, node):
        #('IfEXP')
        return self.visit(node.body) and self.visit(node.orelse)

    def visit_Dict(self, node):
        return all([self.visit(key) for key in node.keys] + [self.visit(value) for value in node.values])

    def visit_Set(self, node):
        return all([self.visit(elt) for elt in node.elts])

    def visit_Num(self, node):
        return True

    def visit_Str(self, node):
        return True

    def visit_NameConstant(self, node):
        return True

    def visit_Name(self, node):
        return True

    def visit_List(self, node):
        return all([self.visit(elt) for elt in node.elts])

    def visit_Tuple(self, node):
        return all([self.visit(elt) for elt in node.elts])

    def visit_Add(self, node):
        return True

    def visit_Sub(self, node):
        return True

    def visit_Mult(self, node):
        return True

    def visit_Div(self, node):
        return True

    def visit_Import(self, node):
        return True

    def visit_ImportFrom(self, node):
        return True