import ast
import collections
from collections import OrderedDict, abc
import functools
from io import StringIO
import itertools
import sys

class StaticMemoryEstimator(ast.NodeVisitor):
    def __init__(self):
        self.memory = 0

    def getMemory(self, node):
        self.visit_Module(node)
        return self.memory

    def visit_Module(self, node):
        [self.visit(s) for s in node.body]

    def visit_FunctionDef(self, node):
        [self.visit(s) for s in node.body]

    def visit_AsyncFunctionDef(self, node):
        [self.visit(s) for s in node.body]

    def visit_Assign(self, node):
        [self.visit(target) for target in node.targets]
        self.visit(node.value)

    def visit_AugAssign(self, node):
        self.visit(node.target)
        self.visit(node.value)

    def visit_For(self, node):
        [self.visit(s) for s in node.body]
        [self.visit(s) for s in node.orelse]

    def visit_AsyncFor(self, node):
        currentMem = self.memory
        [self.visit(s) for s in node.body]
        [self.visit(s) for s in node.orelse]
        addedMemory = self.memory - currentMem
        self.memory += (len(node.iter.elts) - 1) * addedMemory

    def visit_While(self, node):
        [self.visit(s) for s in node.body]
        [self.visit(s) for s in node.orelse]

    def visit_If(self, node):
        [self.visit(s) for s in node.body]
        [self.visit(s) for s in node.orelse]

    def visit_With(self, node):
        [self.visit(s) for s in node.body]

    def visit_AsyncWith(self, node):
        [self.visit(s) for s in node.body]

    def visit_Try(self, node):
        [self.visit(s) for s in node.body]
        [self.visit(s) for s in node.handlers]
        [self.visit(s) for s in node.orelse]
        [self.visit(s) for s in node.finalbody]

    def visit_Expr(self, node):
        #('Expr')
        self.visit(node.value)

    def visit_BoolOp(self, node):
        #('BoolOp')
        [self.visit(b) for b in node.values]

    def visit_BinOp(self, node):
        #('BinOp')
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        #('UnaryOP')
        self.visit(node.operand)

    def visit_Lambda(self, node):
        #('Lambda')
        self.visit(node.body)

    def visit_IfExp(self, node):
        #('IfEXP')
        self.visit(node.body)
        self.visit(node.orelse)

    def visit_Dict(self, node):
        #('Dict')
        [self.visit(key) for key in node.keys]
        [self.visit(value) for value in node.values]

    def visit_Set(self, node):
        #('set')
        [self.visit(elt) for elt in node.elts]

    def visit_ListComp(self, node):
        #('listComp')
        self.generic_visit(node)

    def visit_SetComp(self, node):
        #('setComp')
        self.generic_visit(node)

    def visit_DictComp(self, node):
        #('dictComp')
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        #('generatorExp')
        self.generic_visit(node)

    def visit_Await(self, node):
        #('Await')
        self.generic_visit(node)

    def visit_Yield(self, node):
        #('Yield')
        self.generic_visit(node)

    def visit_YieldFrom(self, node):
        #('yieldForm')
        self.generic_visit(node)

    def visit_Compare(self, node):
        #('Compare')
        self.visit(node.left)
        [self.visit(comp) for comp in node.comparators]

    def visit_Call(self, node):
        #('call')
        self.visit(node.func)
        [self.visit(arg) for arg in node.args]
        [self.visit(keyword) for keyword in node.keywords]

    def visit_Num(self, node):
        #('Num')
        self.memory += sys.getsizeof(node)

    def visit_Str(self, node):
        #('str')
        self.memory += sys.getsizeof(node)

    def visit_FormattedValue(self, node):
        #('formattedValue')
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        #('JoinedStr')
        [self.visit(value) for value in node.values]

    def visit_Bytes(self, node):
        #('bytes')
        self.memory += sys.getsizeof(node)

    def visit_NameConstant(self, node):
        #('NameConstant')
        self.memory += sys.getsizeof(node)

    def visit_Ellipsis(self, node):
        #('Ellipsis')
        self.generic_visit(node)

    def visit_Constant(self, node):
        #('Constant')
        self.memory += sys.getsizeof(node)

    def visit_Attribute(self, node):
        #('Attribute')
        self.visit(node.value)

    def visit_Subscript(self, node):
        #('Subscript')
        self.visit(node.value)

    def visit_Starred(self, node):
        #('Starred')
        self.generic_visit(node)

    def visit_Name(self, node):
        #('name')
        self.generic_visit(node)

    def visit_List(self, node):
        #('List')
        [self.visit(elt) for elt in node.elts]

    def visit_Tuple(self, node):
        #('Tuple')
        [self.visit(elt) for elt in node.elts]


