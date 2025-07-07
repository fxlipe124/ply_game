import ply.yacc as yacc
from utils import tokens, valid_terrain_types, valid_object_types

tokens = tokens

def p_program(p):
    '''program : scenario
               | program scenario'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_scenario(p):
    '''scenario : CENARIO ID '{' mapa objetos '}' '''
    p.parser.object_names = set()  # Reset object_names for each scenario
    p[0] = {
        'cenario': p[2],
        'mapa': p[4],
        'objetos': p[5]
    }

def p_mapa(p):
    '''mapa : MAPA '{' dimensao tipo_terreno '}' '''
    width, height = p[3]
    if width <= 0 or height <= 0:
        raise ValueError(f"Dimensões inválidas do mapa {p[3]} (valores não positivos) na linha {p.lineno(3)}")
    if width > 10000 or height > 10000:
        raise ValueError(f"Dimensões do mapa excedem o limite máximo (10000) na linha {p.lineno(3)}")
    p[0] = {'dimensao': p[3], 'tipo_terreno': p[4]}

def p_dimensao(p):
    '''dimensao : DIMENSAO '=' pair ';' '''
    width, height = p[3]
    if width < 0 or height < 0:
        raise ValueError(f"Dimensões negativas não permitidas {p[3]} na linha {p.lineno(3)}")
    p[0] = p[3]

def p_tipo_terreno(p):
    '''tipo_terreno : TIPO_TERRENO '=' ID ';' '''
    if p[3] not in valid_terrain_types:
        raise ValueError(f"Tipo de terreno inválido '{p[3]}' na linha {p.lineno(3)}")
    p[0] = p[3]

def p_objetos(p):
    '''objetos :
               | objetos objeto'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_objeto(p):
    '''objeto : OBJETO ID '{' tipo posicao dimensao '}' '''
    if p[2] in p.parser.object_names:
        raise ValueError(f"Nome de objeto duplicado '{p[2]}' na linha {p.lineno(2)}")
    p.parser.object_names.add(p[2])
    p[0] = {
        'nome': p[2],
        'tipo': p[4],
        'posicao': p[5],
        'dimensao': p[6]
    }

def p_tipo(p):
    '''tipo : TIPO '=' ID ';' '''
    if p[3] not in valid_object_types:
        raise ValueError(f"Tipo de objeto inválido '{p[3]}' na linha {p.lineno(3)}")
    p[0] = p[3]

def p_posicao(p):
    '''posicao : POSICAO '=' pair ';' '''
    p[0] = p[3]

def p_pair(p):
    '''pair : '(' NUMBER ',' NUMBER ')' '''
    if p[2] < 0 or p[4] < 0:
        raise ValueError(f"Valores negativos não permitidos na linha {p.lineno(2)}")
    if p[2] > 10000 or p[4] > 10000:
        raise ValueError(f"Valores excedem o limite máximo (10000) na linha {p.lineno(2)}")
    p[0] = [p[2], p[4]]

def p_error(p):
    if p:
        raise SyntaxError(
            f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na linha {p.lineno}, posição {p.lexpos}")
    else:
        raise SyntaxError("Erro de sintaxe no final do arquivo")

def create_parser():
    parser = yacc.yacc()
    parser.object_names = set()  # Initialize object_names attribute
    return parser