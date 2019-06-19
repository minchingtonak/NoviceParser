
from sly import Parser
from lexer import CLexer
import sys
from pprint import pprint

# https://sly.readthedocs.io/en/latest/sly.html#writing-a-lexer


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

    freq = {'param_types': 0, 'func': 0, 'var_decl': 0, 'expr': 0, 'opt_expr': 0, 'assg': 0, 'opt_assg': 0}

    # Called in every grammar-handling function, put prints and other stuff
    # for debugging
    def action(self, p):
        pprint(vars(p))
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
        self.freq['var_decl'] += 1
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
        self.freq['param_types'] += 1
        self.action(p)
        self.v += 1
        return self.v

    @_('var_type ID "(" param_types ")" "{" typedecs stmts "}"',
       'VOID ID "(" param_types ")" "{" typedecs stmts "}"')
    def func(self, p):
        self.freq['func'] += 1
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
        self.freq['opt_assg'] += 1
        self.action(p)
        self.v += 1
        return self.v

    @_('expr', 'empty')
    def opt_expr(self, p):
        self.freq['opt_expr'] += 1
        self.action(p)
        self.v += 1
        return self.v

    @_('ID ASSIGN expr')
    def assg(self, p):
        self.freq['assg'] += 1
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
        self.freq['expr'] += 1
        self.action(p)
        self.v += 1
        return self.v


if __name__ == '__main__':
    lexer = CLexer()
    parser = CParser()
    with open(sys.argv[1], 'r') as f:
        print(parser.parse(lexer.tokenize(f.read())))
    
    for key,val in parser.freq.items():
        print(key, val)
