BNF:

program ::= statement
            | statement program

statement = Return(expr)
           | Assign(expr* targets, expr value)
           | AugAssign(expr target, operator op, expr value)
           | For(expr target, expr iter, stmt* body, stmt* orelse)
           | While(expr test, stmt* body, stmt* orelse)
           | If(expr test, stmt* body, stmt* orelse)
           | Try(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
           | Import(alias* names)

expr =   BoolOp(boolop op, expr* values)
         | BinOp(expr left, operator op, expr right)
         | UnaryOp(unaryop op, expr operand)
         | IfExp(expr test, expr body, expr orelse)
         | Dict(expr* keys, expr* values)
         | Set(expr* elts)
         | Compare(expr left, cmpop* ops, expr* comparators)
         | Num(object n)
         | Str(string s)
         | Name(identifier id, expr_context ctx)
         | List(expr* elts, expr_context ctx)
         | Tuple(expr* elts, expr_context ctx)
         | Attribute(expr value, identifier attr, expr_context ctx)
         | Name(identifier id, expr_context ctx)


excepthandler = ExceptHandler(stmt* body)
attr = 'DataFrame'
boolop = And | Or
operator = Add | Sub | Mult | Div
unaryop = Invert | Not | UAdd | USub



I have implemented 3 algorithms to fulfil the requirement of the project.

First of all, the ASTParser reads the .py file at a given location and returns an AST instance of the code

The SubsetEstimator runs an algorithm to check given an input .py file, if the input is a language of the subset. The output is Boolean.
To initiate the subset estimator, use the method isLanguageSubset() with the AST instace as the argument.

The MemoryEstimator calculates an upperbound on the memory required for the pandas workflow by doing a static analysis. The output is in bytes.
To initiate the Memory estimator, use the method getMemory() with the ast instance as an argument.

The TypeCheck is a type checker algorithm for the ast instance provided. The output is Binary.
To initiate, use the method checkType() with the ast instance as the argument.





