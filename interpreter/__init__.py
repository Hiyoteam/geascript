from sly import Lexer, Parser
from util import _

class CalcLexer(Lexer):
    tokens = { "NAME", "NUMBER", "PLUS", "TIMES", "MINUS", "DIVIDE", "ASSIGN", "LPAREN", "RPAREN", "STRING", "ECHO", "EXIT"}
    ignore = ' \t'

    # Tokens
    EXIT = 'exit'
    ECHO = 'echo'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    STRING = r'"[^"]*"'
    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    
    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', "PLUS", "MINUS"),
        ('left', "TIMES", "DIVIDE"),
        ('right', "UMINUS"),
        )

    def __init__(self):
        self.names = { }

    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_("EXIT expr")
    def statement(self, p):
        exit(int(p.expr))

    @_("EXIT")
    def statement(self, p):
        exit(0)

    @_("ECHO expr")
    def statement(self, p):
        print(p.expr)
    
    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)
    
    @_('STRING')
    def expr(self, p):
        return str(p.STRING).strip("\"")

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('gea-repl > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))