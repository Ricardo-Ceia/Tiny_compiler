import sys
from lexer import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currToken=None
        self.peekToken=None
        self.nextToken()
        self.nextToken()

    def match(self, kind):
        if not self.currToken.kind==kind:
            Parser.abort("Epected "+kind.name+" ,got "+self.currToken.kind.name)
        self.nextToken()

    def nextToken(self):
        self.currToken = self.peekToken
        self.peekToken = self.lexer.getToken()


    def program(self):
        print("PROGRAM")
        while self.currToken.kind==TokenType.NEWLINE:
            self.nextToken()
        while not self.currToken.kind==TokenType.EOF:
            self.statement()

    def statement(self):
        if self.currToken.kind==TokenType.PRINT:
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.currToken.kind==TokenType.STRING:
                self.nextToken()
        elif self.currToken.kind==TokenType.IF:
            print("STATEMENT-IF")
            self.nextToken()
            self.comparision()

            self.match(TokenType.THEN)
            self.nl()

            while self.currToken.kind!=TokenType.ENDIF:
                self.statement()
            self.match(TokenType.EOF)
        elif self.currToken.kind==TokenType.WHILE:
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparision()
            self.match(TokenType.REPEAT)
            self.nl()

            while self.currToken.kind!=TokenType.EOF:
                self.statement()
            self.match(TokenType.ENDWHILE)
        elif self.currToken.kind==TokenType.LABEL:
            print("STATEMENT-LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)
        elif self.currToken.kind==TokenType.GOTO:
            print("STATEMENT-GOTO")
            self.nextToken()
            self.match(TokenType.IDENT)
        elif self.currToken.kind==TokenType.LET:
            print("STATEMENT-LET")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
        elif self.currToken.kind==TokenType.INPUT:
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.IDENT)
        else:
            Parser.abort(f"Invalid statement at {self.currToken.text} ({self.currToken.kind.name})")
        self.nl()


    def nl(self):
        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while self.currToken.kind==TokenType.NEWLINE:
            self.nextToken()

    @staticmethod
    def abort(msg):
        sys.exit("Error. " + msg)