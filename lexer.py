import enum
import sys 

class Lexer:
    def __init__(self,src):
        self.src = src+'\n'
        self.currChar = ''
        self.currPos = -1
        self.nextChar()

    def nextChar(self):
        self.currPos += 1
        if self.currPos >= len(self.src):
            return '\0'
        self.currChar = self.src[self.currPos] 

    def peek(self):
        nextPosition = self.currPos+1
        if nextPosition >= len(self.src):
            return '\0'
        return self.src[nextPosition]

    def abort(self,msg):
        sys.exit("Lexing error. "+msg)

    def skipWhiteSpace(self):
        while self.currChar == ' ' or self.currChar =='\t' or self.currChar == '\r':
            self.nextChar()

    def skipComment(self):
        if self.currChar == '#':
            while self.currChar != '\n':
                self.nextChar() 

    def getToken(self):
        self.skipWhiteSpace()
        self.skipComment()
        token = None
        if self.currChar == '+':
            token = Token(self.currChar, TokenType.PLUS)
        elif self.currChar == '-':
            token = Token(self.currChar, TokenType.MINUS)
        elif self.currChar == '*':
            token = Token(self.currChar, TokenType.ASTERISK)
        elif self.currChar == '/':
            token = Token(self.currChar, TokenType.SLASH)
        elif self.currChar == '\n':
            token = Token(self.currChar, TokenType.NEWLINE)
        elif self.currChar == '\0':
            token = Token('', TokenType.EOF)
        elif self.currChar == '=':
            if self.peek() == '=':
                lastChar = self.currChar
                self.nextChar()
                token = Token(lastChar+self.currChar,TokenType.EQEQ)
            else:
                token = Token(self.currChar,TokenType.EQ)
        elif self.currChar == '>':
            if self.peek() == '=':
                lastChar = self.currChar
                self.nextChar()
                token = Token(lastChar+self.currChar,TokenType.GTEQ)
            else:
                token = Token(self.currChar,TokenType.GT)
        elif self.currChar == '<':
                if self.peek() == '=':
                    lastChar = self.currChar
                    self.nextChar()
                    token = Token(lastChar + self.currChar, TokenType.LTEQ)
                else:
                    token = Token(self.curChar, TokenType.LT)
        elif self.currChar == '!':
                if self.peek() == '=':
                    lastChar = self.currChar
                    self.nextChar()
                    token = Token(lastChar + self.currChar, TokenType.NOTEQ)
                else:
                    self.abort("Expected != got !" + self.peek()) 
        elif self.currChar == '\"':
            self.nextChar()
            startPos = self.currPos 
            while self.currChar != '\"':
                if self.currChar == '\r' or self.currChar == '\n' or self.currChar == '\t' or self.currChar == '\\' or self.currChar == '%':
                    self.abort("Illegal character in the string.")
                self.nextChar()
            token = Token(self.src[startPos: self.currPos],TokenType.STRING)
        elif self.currChar.isdigit():
            startPos = self.currPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':
                self.nextChar()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()
            token = Token(self.src[startPos:self.currPos],TokenType.NUMBER)
        elif self.currChar.isalpha():
            startPos = self.currPos
            while self.peek().isalnum():
                self.nextChar()
            keyword = Token.checkIfKeyword(self.src[startPos:self.currPos+1])
            if keyword == None:
                token = Token(self.src[startPos:self.currPos+1],TokenType.IDENT)
            else:
                token = Token(self.src[startPos:self.currPos+1],keyword)
        else:
           self.abort("Unknown token." + self.currChar)
        self.nextChar()  
        return token      


class Token:
    def __init__(self,TokenText,TokenKind):
        self.text = TokenText
        self.kind = TokenKind 

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind 
        return None
    
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206	
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
          
