import ply.lex as lex
import ply.yacc as yacc
import json
from PIL import Image, ImageDraw
import pygame

tokens = ('CENARIO', 'MAPA', 'OBJETO', 'DIMENSAO', 'TIPO_TERRENO', 'TIPO', 'POSICAO', 'ID', 'STRING', 'NUMBER')
literals = ['{', '}', '(', ')', '=', ',', ';']
reserved = {
    'cenario': 'CENARIO',
    'mapa': 'MAPA',
    'objeto': 'OBJETO',
    'dimensao': 'DIMENSAO',
    'tipo_terreno': 'TIPO_TERRENO',
    'tipo': 'TIPO',
    'posicao': 'POSICAO'
}

valid_terrain_types = ['grama', 'areia', 'agua']
valid_object_types = ['arvore', 'pedra', 'jogador']

colors = {
    'grama': (0, 100, 0),  # Verde
    'areia': (255, 255, 0),  # Amarelo
    'agua': (0, 0, 150),  # Azul
    'arvore': (139, 69, 19),  # Marrom
    'pedra': (128, 128, 128),  # Cinza
    'jogador': (0, 0, 255)  # Azul
}

def get_pil_color(color_name):
    return colors.get(color_name, (0, 0, 0))  # Padrão: preto

def get_pygame_color(color_name):
    return colors.get(color_name, (0, 0, 0))  # Padrão: preto

# Regras do lexer
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_comment(t):
    r'//.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Caractere inválido '{t.value[0]}' na linha {t.lineno}, posição {t.lexpos}")
    t.lexer.skip(1)

# Regras do parser
def p_program(p):
    '''program : scenario
               | program scenario'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_scenario(p):
    '''scenario : CENARIO ID '{' mapa objetos '}' '''
    p.parser.object_names = set()
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

# Cria lexer e parser
lexer = lex.lex()
parser = yacc.yacc()
parser.object_names = set()

# Funções utilitárias
def validate_objects(data):
    width, height = data['mapa']['dimensao']
    for obj in data['objetos']:
        x, y = obj['posicao']
        w, h = obj['dimensao']
        if x + w > width or y + h > height:
            raise ValueError(f"Objeto '{obj['nome']}' excede os limites do mapa ({width}, {height})")

def check_object_overlap(objects):
    for i, obj1 in enumerate(objects):
        x1, y1 = obj1['posicao']
        w1, h1 = obj1['dimensao']
        rect1 = (x1, y1, x1 + w1, y1 + h1)
        for j, obj2 in enumerate(objects[i + 1:], start=i + 1):
            x2, y2 = obj2['posicao']
            w2, h2 = obj2['dimensao']
            rect2 = (x2, y2, x2 + w2, y2 + h2)
            if not (rect1[2] <= rect2[0] or rect2[2] <= rect1[0] or
                    rect1[3] <= rect2[1] or rect2[3] <= rect1[1]):
                raise ValueError(
                    f"Sobreposição detectada entre '{obj1['nome']}' em {obj1['posicao']} (dim: {obj1['dimensao']}) "
                    f"e '{obj2['nome']}' em {obj2['posicao']} (dim: {obj2['dimensao']})")

def generate_image(data, filename='cenario.png'):
    width, height = data['mapa']['dimensao']
    img = Image.new('RGB', (width, height), color=get_pil_color(data['mapa']['tipo_terreno']))
    draw = ImageDraw.Draw(img)
    for obj in data['objetos']:
        x, y = obj['posicao']
        w, h = obj['dimensao']
        color = get_pil_color(obj['tipo'])
        draw.rectangle((x, y, x + w, y + h), fill=color, outline='black')
    img.save(filename)
    print(f"Imagem salva como '{filename}'")

def save_json(data, filename='cenario.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"JSON salvo como '{filename}'")

def display_pygame(data):
    pygame.init()
    width, height = data['mapa']['dimensao']
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(data['cenario'])
    screen.fill(get_pygame_color(data['mapa']['tipo_terreno']))
    for obj in data['objetos']:
        x, y = obj['posicao']
        w, h = obj['dimensao']
        color = get_pygame_color(obj['tipo'])
        pygame.draw.rect(screen, color, (x, y, w, h))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, w, h), 1)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

# Entrada
input_data = """
cenario cenario_floresta {
  mapa {
    dimensao = (1000, 600);
    tipo_terreno = grama;
  }
  objeto arvore1 {
    tipo = arvore;
    posicao = (800, 400);
    dimensao = (50, 100);
  }
  objeto arvore2 {
    tipo = arvore;
    posicao = (500, 150);
    dimensao = (30, 80);
  }
  objeto pedra1 {
    tipo = pedra;
    posicao = (50, 50);
    dimensao = (40, 30);
  }
  objeto pedra2 {
    tipo = pedra;
    posicao = (100, 300);
    dimensao = (40, 30);
  }
  objeto personagem {
    tipo = jogador;
    posicao = (100, 500);
    dimensao = (30, 50);
  }
}

cenario cenario_deserto {
  mapa {
    dimensao = (800, 400);
    tipo_terreno = areia;
  }
  objeto pedra1 {
    tipo = pedra;
    posicao = (100, 100);
    dimensao = (50, 50);
  }
  objeto cacto1 {
    tipo = arvore;
    posicao = (600, 200);
    dimensao = (30, 60);
  }
  objeto personagem {
    tipo = jogador;
    posicao = (200, 300);
    dimensao = (30, 50);
  }
}

cenario cenario_lago {
  mapa {
    dimensao = (1200, 800);
    tipo_terreno = agua;
  }
  objeto ilha1 {
    tipo = pedra;
    posicao = (500, 300);
    dimensao = (100, 100);
  }
  objeto barco1 {
    tipo = jogador;
    posicao = (700, 500);
    dimensao = (40, 20);
  }
}
"""

try:
    result = parser.parse(input_data)
    if not result:
        raise ValueError("Parsing falhou: Nenhum resultado produzido")
    print("\nParsing bem-sucedido!")

    scenarios = result if isinstance(result, list) else [result]
    for scenario in scenarios:
        validate_objects(scenario)
        check_object_overlap(scenario['objetos'])

    print("\nEscolha uma opção para todos os cenários:")
    print("1. Gerar arquivos PNG")
    print("2. Gerar arquivos JSON")
    print("3. Visualizar no Pygame (um cenário por vez)")
    print("4. Sair")
    choice = input("Digite o número da opção (1, 2, 3 ou 4): ")

    if choice == '4':
        print("Saindo...")
    elif choice == '1':
        for i, scenario in enumerate(scenarios, 1):
            generate_image(scenario, f'cenario_{i}.png')
    elif choice == '2':
        for i, scenario in enumerate(scenarios, 1):
            save_json(scenario, f'cenario_{i}.json')
    elif choice == '3':
        for i, scenario in enumerate(scenarios, 1):
            print(f"\nExibindo cenário {i}: {scenario['cenario']}")
            display_pygame(scenario)
    else:
        print("Opção inválida. Escolha 1, 2, 3 ou 4.")

except SyntaxError as se:
    print(f"Erro de sintaxe: {se}")
except ValueError as ve:
    print(f"Erro de validação: {ve}")
except Exception as e:
    print(f"Erro inesperado: {type(e).__name__}: {e}")
