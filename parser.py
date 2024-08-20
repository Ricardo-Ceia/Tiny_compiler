import sys
from lexer import *


class Parser:
    def __init__(self, lexer,emitter):
        self.lexer = lexer
        self.emitter=emitter
        self.symbols = set()
        self.labelsDeclared = set()
        self.labelsGotoed = set()
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    

    
    def checkToken(self, kind):
        return kind == self.curToken.kind

    
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    
    def match(self, kind):
        if not self.checkToken(kind):
            Parser.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
       

    
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    @staticmethod
    def abort(message):
        sys.exit("Error. " + message)


 
    def program(self):
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(){")
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()      
        while not self.checkToken(TokenType.EOF):
            self.statement()
        
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")
        for label in self.labelsDeclared:
            if  label  not  in self.labelsGotoed:
                Parser.abort(f"Trying to GOTO to undifined LABEL: "+label)

       


   
    def statement(self):
       

        # "PRINT" (expression | string)
        if self.checkToken(TokenType.PRINT):
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine("printf(\"" + self.curToken.text + "\\n\");")
                self.nextToken()

            else:
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TokenType.IF):
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine("){")
           
            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emitLine("}")
        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine("){")
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine("}")
        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            self.nextToken()
            if self.curToken.text in self.labelsDeclared:
                Lexer.abort("Label already exists: ",self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)
            self.emitter.emitLine(self.curToken.text+":")
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.emitter.emitLine("got "+self.curToken.text+";")
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            self.nextToken()

            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine("float "+self.curToken.text+";")
            self.emitter.emit(self.curToken.text+" = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            
            self.expression()
            self.emitter.emitLine(";")
        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            self.nextToken()
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine("float "+self.curToken.text+";")
            self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.curToken.text + ")) {")
            self.emitter.emitLine(self.curToken.text + " = 0;")
            self.emitter.emitLine("// use %*s so the input is read but ignored")
            self.emitter.emit("scanf(\"%")
            self.emitter.emitLine("*s\");")
            self.emitter.emitLine("}")
            self.match(TokenType.IDENT)

       
        else:
            Parser.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # Newline.
        self.nl()


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
        else:
            Parser.abort("Expected comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()


    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        self.term()
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()


    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()


    # unary ::= ["+" | "-"] primary
    def unary(self):
        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()        
        self.primary()


    # primary ::= number | ident
    def primary(self):
        if self.checkToken(TokenType.NUMBER):
            self.emitter.emit(self.curToken.text) 
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            if self.curToken.text not in self.symbols:
                Parser.abort(f"Referencing undifined variable: {self.curToken.text}")
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        else:
            # Error!
            Parser.abort("Unexpected token at " + self.curToken.text)

    # nl ::= '\n'+
    def nl(self):
        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        # But we will allow extra newlines too, of course.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()