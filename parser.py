import ply.yacc as yacc
from lexer import tokens

start = 'statements'

def p_statements_multiple(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]

def p_statement_declare(p):
    'statement : INT ID SEMICOLON'
    p[0] = ('declare', p[2])

def p_statement_assign(p):
    'statement : ID EQUALS expression SEMICOLON'
    p[0] = ('assign', p[1], p[3])

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = (p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = (p[2], p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ('num', p[1])

def p_factor_id(p):
    'factor : ID'
    p[0] = ('id', p[1])

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def parse(code):
    return parser.parse(code)
