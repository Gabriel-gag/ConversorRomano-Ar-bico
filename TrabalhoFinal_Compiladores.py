import ply.lex as lex
import ply.yacc as yacc

# Tokens
tokens = ('LETTER',)

# Expressões regulares
def t_LETTER(t):
    r'I|V|X|L|C|D|M|i|v|x|l|c|d|m'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# Parser
def p_statement(p):
    '''
    statement : RomanNumeral
              | LETTER
              | empty
    '''
    if p[1]:
        if isinstance(p[1], str):
            print(f"Roman numeral: {p[1]}")
            convert_roman_to_decimal(p[1])
        else:
            print(f"Single letter: {p[1]}")

def p_RomanNumeral(p):
    '''
    RomanNumeral : LETTER RomanTail
                 | empty
                 | LETTER
    '''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = ''

def p_RomanTail(p):
    '''
    RomanTail : LETTER RomanTail
              | empty
    '''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = ''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

def convert_roman_to_decimal(roman_numeral):
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0

    for numeral in reversed(roman_numeral):
        value = roman_numerals[numeral.upper()]
        # Regra: Limite de repetição para I, X, C, M
        if numeral.upper() in ['I', 'X', 'C', 'M']:
            if roman_numeral.upper().count(numeral.upper()) > 3:
                print(f"Invalid Roman numeral: {roman_numeral}. Não podem existir 4 caracteres repetidos consecutivamente.")
                return
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    print(f"Decimal value: {total}")

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('Enter a Roman numeral or a single letter: ')
    except EOFError:
        break
    if not s:
        continue
    parser.parse(s)