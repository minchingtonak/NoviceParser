#!/usr/bin/env python3

from sly import Lexer
# import sys
# sys.path.append('../..')


class NoviceLexer(Lexer):
    def __init__(self):
        self.nesting_level = 0
        self.lineno = 1

    tokens = {
        ID,
        # EXTERN,
        VOID,
        # RETURN,
        # CHAR,
        INT,
        # IF,
        # ELSE,
        WHILE,
        FOR,
        # INTCON,
        NONZEROCON,
        ZEROCON,
        PLUSASSIGN,
        MINUSASSIGN,
        TIMESASSIGN,
        DIVIDEASSIGN,
        INCR,
        DECR,
        LEFTSHIFT,
        RIGHTSHIFT,
        EQ,
        NE,
        LE,
        LT,
        GE,
        GT,
        AND,
        OR,
        NOT,
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        ASSIGN
    }

    literals = {'(', ')', '{', '}', '[', ']', ';', ','}

    ignore = ' \t'
    ignore_linecomment = r'\/\/.*'
    ignore_comment = r'\/\*[\s\S]*?\*\/'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Keywords defined as special cases in the set of IDs
    # ID['extern'] = EXTERN
    ID['void'] = VOID
    # ID['return'] = RETURN
    # ID['char'] = CHAR
    ID['int'] = INT
    # ID['if'] = IF
    # ID['else'] = ELSE
    ID['while'] = WHILE
    ID['for'] = FOR

    # INTCON = r'\d+'
    NONZEROCON = r'[1-9][0-9]*'
    ZEROCON = r'0'

    PLUSASSIGN = r'\+='
    MINUSASSIGN = r'-='
    TIMESASSIGN = r'\*='
    DIVIDEASSIGN = r'\/='
    INCR = r'\+\+'
    DECR = r'--'

    LEFTSHIFT = r'<<'
    RIGHTSHIFT = r'>>'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    AND = r'&&'
    OR = r'\|\|'
    NOT = r'!'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='

    def ignore_comment(self, t):
        print('LEXER: ignoring block comment')

    def ignore_linecomment(self, t):
        print('LEXER: ignoring line comment')

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Error handling
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    # Convert integer constants into their integer value
    def NONZEROCON(self, t):
        t.value = int(t.value)
        return t

    def ZEROCON(self, t):
        t.value = int(t.value)
        return t
    
    # Keep track of nesting level
    @_(r'\{')
    def lbrace(self, t):
        t.type = '{'
        self.nesting_level += 1
        return t

    @_(r'\}')
    def rbrace(self, t):
        t.type = '}'
        self.nesting_level -= 1
        return t

    # Wrapper for superclass tokenize to take care of line counting
    def tokenize(self, data):
        return super(NoviceLexer, self).tokenize(data, lineno=self.lineno)


# Run this code with `python3 lexer.py < intputfile.c`
# you need to have sly installed
if __name__ == '__main__':
    lexer = NoviceLexer()
    while True:
        try:
            data = input()
            data += '\n'  # Manually concatenate a newline to simulate line endings for the lexer
        except EOFError:
            break
        for tok in lexer.tokenize(data):
            print(
                '(type=%10r, value=%15r, line=%3r)' %
                (tok.type, tok.value, tok.lineno))
