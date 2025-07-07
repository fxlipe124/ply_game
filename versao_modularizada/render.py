from PIL import Image, ImageDraw
import pygame
import json
from utils import get_pil_color, get_pygame_color

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