from lexer import *
from parser import *
import sys

def test():
    print("Teeny Tiny Compiler")
    if len(sys.argv)!=2:
        sys.exit("Error: Compiler needs source file as argument")
    
    with open(sys.argv[1],'r') as InputFile:
        source = InputFile.read()

    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()
    print("Parsing completed")
test()