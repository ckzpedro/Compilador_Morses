from MorsesLex import lexer
from MorsesSint import parse_code

with open("./MorseR/prog.txt", "r") as arquivo:
    codigo = arquivo.read()

parse_code(codigo)