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
    'agua': (0, 0, 255),  # Azul
    'arvore': (139, 69, 19),  # Marrom
    'pedra': (128, 128, 128),  # Cinza
    'jogador': (0, 0, 255)  # Azul
}

def get_pil_color(color_name):
    return colors.get(color_name, (0, 0, 0))  # Padrão: preto

def get_pygame_color(color_name):
    return colors.get(color_name, (0, 0, 0))  # Padrão: preto

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