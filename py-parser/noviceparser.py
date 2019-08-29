#!/usr/bin/env python3

from sly import Parser
from novicelexer import NoviceLexer
from pprint import pprint
import json
import sys

# https://sly.readthedocs.io/en/latest/sly.html#writing-a-lexer


class NoviceParser(Parser):

    tokens = NoviceLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        # Non-associativity defined for comparison operators because we
        # shouldn't be able to chain them
        ('nonassoc', EQ, NE),
        ('nonassoc', LE, LT),
        ('nonassoc', GE, GT),
        ('left', LEFTSHIFT, RIGHTSHIFT),
        ('left', OR, AND),
        ('right', NOT, UMINUS),
        ('right', PREINCR, PREDECR)
    )

    freq = {
        'param_types': 0,
        'func': 0,
        'var_decl': 0,
        'expr': {
            '+': 0,
            '-': 0,
            '*': 0,
            '/': 0,
            '==': 0,
            '!=': 0,
            '<=': 0,
            '<': 0,
            '>=': 0,
            '>': 0,
            '<<': 0,
            '>>': 0,
            '!': 0,
            '&&': 0,
            '||': 0,
            '++': 0,
            '--': 0,
            'pre++': 0,
            'pre--': 0,
            'uminus': 0
        },
        'opt_expr': 0,
        'assg': {
            '=': 0,
            '+=': 0,
            '-=': 0,
            '*=': 0,
            '/=': 0,
            '++': 0,
            '--': 0,
            'pre++': 0,
            'pre--': 0,
        },
        'opt_assg': 0,
        'basic_incr_for': 0,
        '>1_incr_for': 0,
        'basic_decr_for': 0,
        'ne_for': 0
        }

    # Called in every grammar-handling function, put prints and other stuff
    # for debugging
    def action(self, p):
        # if len(p._namemap) > 1:
        #     print(p[1])
        # self.v += 1
        return self.v
        # pprint(vars(p))
        # pprint(p._stack)
        # print('\n')

    @_('')
    def empty(self, p):
        pass

    start = 'progs'

    v = 0

    @_('progs prog', 'empty')
    def progs(self, p):
        return self.action(p)

    @_('func')
    def prog(self, p):
        return self.action(p)

    @_('ID')
    def var_decl(self, p):
        self.freq['var_decl'] += 1
        return self.action(p)

    @_('INT')
    def var_type(self, p):
        return self.action(p)

    @_('VOID')
    def param_types(self, p):
        self.freq['param_types'] += 1
        return self.action(p)

    @_('var_type ID "(" param_types ")" "{" typedecs stmts "}"',
       'VOID ID "(" param_types ")" "{" typedecs stmts "}"')
    def func(self, p):
        self.freq['func'] += 1
        return self.action(p)

    @_('typedecs typedec', 'empty')
    def typedecs(self, p):
        return self.action(p)

    @_('var_type var_decl ";"')
    def typedec(self, p):
        return self.action(p)

    @_('stmts stmt', 'empty')
    def stmts(self, p):
        return self.action(p)

    @_('WHILE "(" opt_expr ")" stmt',
        'assg ";"',
        '"{" stmts "}"',
        '";"')
    def stmt(self, p):
        return self.action(p)

    # Special for loop grammars

    @_('FOR "(" assgzero ";" less_than ";" increment ")" stmt')
    def stmt(self, p):
        self.freq['basic_incr_for'] += 1
        return self.action(p)

    @_('FOR "(" assgzero ";" less_than ";" larger_incrementer ")" stmt')
    def stmt(self, p):
        self.freq['>1_incr_for'] += 1
        return self.action(p)

    @_('FOR "(" assgnonzero ";" greater_than ";" decrement ")" stmt')
    def stmt(self, p):
        self.freq['basic_decr_for'] += 1
        return self.action(p)

    @_('FOR "(" assgzero ";" not_equal ";" assg ")" stmt',
       'FOR "(" assgnonzero ";" not_equal ";" assg ")" stmt')
    def stmt(self, p):
        self.freq['ne_for'] += 1
        return self.action(p)

    # Catch-all for loop grammar

    @_('FOR "(" opt_assg ";" opt_expr ";" opt_assg ")" stmt')
    def stmt(self, p):
        print('normal for')
        return self.action(p)

    @_('assg', 'empty')
    def opt_assg(self, p):
        self.freq['opt_assg'] += 1
        return self.action(p)

    @_('expr', 'empty')
    def opt_expr(self, p):
        self.freq['opt_expr'] += 1
        return self.action(p)

    # @_('ID ASSIGN expr',
    #    'ID PLUSASSIGN expr',
    #    'ID MINUSASSIGN expr',
    #    'ID TIMESASSIGN expr',
    #    'ID DIVIDEASSIGN expr',
    #    'ID INCR',
    #    'ID DECR',
    #    'INCR ID %prec PREINCR',
    #    'DECR ID %prec PREDECR')
    # def assg(self, p):
    #     return self.action(p)

    @_('ID ASSIGN expr')
    def assg(self, p):
        self.freq['assg']['='] += 1
        return self.action(p)

    @_('ID ASSIGN ZEROCON')
    def assgzero(self, p):
        self.freq['assg']['='] += 1  # change
        return self.action(p)

    @_('ID ASSIGN NONZEROCON')
    def assgnonzero(self, p):
        self.freq['assg']['='] += 1  # change
        return self.action(p)

    @_('ID PLUSASSIGN expr')
    def assg(self, p):
        self.freq['assg']['+='] += 1
        return self.action(p)

    @_('ID PLUSASSIGN NONZEROCON') # only when larger than 1?
    def larger_incrementer(self, p):
        self.freq['assg']['+='] += 1
        return self.action(p)

    @_('ID MINUSASSIGN expr')
    def assg(self, p):
        self.freq['assg']['-='] += 1
        return self.action(p)

    @_('ID TIMESASSIGN expr')
    def assg(self, p):
        self.freq['assg']['*='] += 1
        return self.action(p)

    @_('ID DIVIDEASSIGN expr')
    def assg(self, p):
        self.freq['assg']['/='] += 1
        return self.action(p)

    @_('ID INCR')
    def increment(self, p):
        self.freq['assg']['++'] += 1
        return self.action(p)

    @_('ID DECR')
    def decrement(self, p):
        self.freq['assg']['--'] += 1
        return self.action(p)

    @_('INCR ID %prec PREINCR')
    def assg(self, p):
        self.freq['assg']['pre++'] += 1
        return self.action(p)

    @_('DECR ID %prec PREDECR')
    def assg(self, p):
        self.freq['assg']['pre--'] += 1
        return self.action(p)

    @_('ID',
        '"(" expr ")"',
        'ZEROCON',
        'NONZEROCON'
        # 'INTCON'
       )
    def expr(self, p):
        return self.action(p)

    @_('expr PLUS expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr MINUS expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr TIMES expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr DIVIDE expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr EQ expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr NE expr')
    def not_equal(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr LE expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr LT expr')
    def less_than(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr GE expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr GT expr')
    def greater_than(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr LEFTSHIFT expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr RIGHTSHIFT expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('NOT expr')
    def expr(self, p):
        self.freq['expr'][p[0]] += 1
        return self.action(p)

    @_('expr AND expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr OR expr')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr INCR')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('expr DECR')
    def expr(self, p):
        self.freq['expr'][p[1]] += 1
        return self.action(p)

    @_('INCR expr %prec PREINCR')
    def expr(self, p):
        self.freq['expr']['pre++'] += 1
        return self.action(p)

    @_('DECR expr %prec PREDECR')
    def expr(self, p):
        self.freq['expr']['pre--'] += 1
        return self.action(p)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        self.freq['expr']['uminus'] += 1
        return self.action(p)

    def clear_freq(self):
        for key, val in self.freq.items():
            if isinstance(val, int):
                self.freq[key] = 0
            else:
                for k, v in val.items():
                    self.freq[key][k] = 0


if __name__ == '__main__':
    lexer = NoviceLexer()
    parser = NoviceParser()
    error = False
    try:
        with open(sys.argv[1], 'r') as f:
            parser.parse(lexer.tokenize(f.read()))
        # if no output file provided, dump json to stdout instead
        if (len(sys.argv) < 3):
            print(json.dumps(parser.freq, indent=4))
        else:
            with open(sys.argv[2], 'w') as f:
                json.dump(parser.freq, f, indent=4)
    except FileNotFoundError:
        print('Input file not found!')
        error = True
    except IndexError:
        print('Malformed arguments!')
        error = True
    if error:
        print('Usage: ' + sys.argv[0] + ' INPUTFILE [OUTPUTFILE]')
