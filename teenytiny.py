from lexer import *
import time 
def main():
    source = "IF+-123 foo*THEN/"
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()
        time.sleep(3)

main()