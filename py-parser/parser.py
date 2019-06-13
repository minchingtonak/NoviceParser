
from sly import Parser
from lexer import CLexer
import sys
from pprint import pprint


class CParser(Parser):

    tokens = CLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        # Non-associativity defined for comparison operators because we
        # shouldn't be able to chain them
        ('nonassoc', EQ, NE),
        ('nonassoc', LE, LT),
        ('nonassoc', GE, GT),
        ('left', OR, AND),
        ('right', NOT, UMINUS)
    )

    # Called in every grammar-handling function, put prints and other stuff
    # for debugging
    def action(self, p):
        pprint(p._stack)
        print('\n\n')

    @_('')
    def empty(self, p):
        pass

    start = 'progs'

    v = 0

    @_('progs prog', 'empty')
    def progs(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('func')
    def prog(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('ID')
    def var_decl(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('INT')
    def var_type(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('VOID')
    def param_types(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('var_type ID "(" param_types ")" "{" typedecs stmts "}"',
       'VOID ID "(" param_types ")" "{" typedecs stmts "}"')
    def func(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('typedecs typedec', 'empty')
    def typedecs(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('var_type var_decl ";"')
    def typedec(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('stmts stmt', 'empty')
    def stmts(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('FOR "(" opt_assg ";" opt_expr ";" opt_assg ")" stmt',
       'assg ";"', '"{" stmts "}"', '";"')
    def stmt(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('assg', 'empty')
    def opt_assg(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('expr', 'empty')
    def opt_expr(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('ID ASSIGN expr')
    def assg(self, p):
        self.action(p)
        self.v += 1
        return self.v

    @_('MINUS expr %prec UMINUS',
       'expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr',
       'expr EQ expr',
       'expr NE expr',
       'expr LE expr',
       'expr LT expr',
       'expr GE expr',
       'expr GT expr',
       'NOT expr',
       'expr AND expr',
       'expr OR expr',
       'ID',
       '"(" expr ")"',
       'INTCON')
    def expr(self, p):
        self.action(p)
        self.v += 1
        return self.v


if __name__ == '__main__':
    lexer = CLexer()
    parser = CParser()
    with open(sys.argv[1], 'r') as f:
        print(parser.parse(lexer.tokenize(f.read())))
