from lexer import create_lexer
from parser import create_parser
from utils import validate_objects, check_object_overlap
from render import generate_image, save_json, display_pygame

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
"""

def main():
    lexer = create_lexer()
    parser = create_parser()

    try:
        result = parser.parse(input_data)
        if not result:
            raise ValueError("Parsing falhou: Nenhum resultado produzido")
        print("\n\nParsing bem-sucedido!")

        scenarios = result if isinstance(result, list) else [result]
        for scenario in scenarios:
            validate_objects(scenario)
            check_object_overlap(scenario['objetos'])

        print("Escolha uma opção para todos os cenários:")
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

if __name__ == "__main__":
    main()