from interpreter import GeaLexer, GeaParser

if __name__ == '__main__':
    lexer = GeaLexer()
    parser = GeaParser()
    while True:
        try:
            text = input('gea-repl > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))