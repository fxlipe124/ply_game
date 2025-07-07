# Interpretador de Cenários 2D

Este projeto implementa um interpretador de cenários 2D utilizando Python, PLY (Python Lex-Yacc) para análise léxica e sintática, PIL (Python Imaging Library) para geração de imagens PNG, e Pygame para visualização gráfica. O interpretador processa descrições textuais de cenários (como mapas de jogos com objetos), valida suas regras, e gera saídas em formatos JSON, PNG e visualizações interativas.

## Funcionalidades

- **Análise Léxica e Sintática**: Processa descrições textuais de cenários com gramática definida, utilizando PLY.
- **Validações Semânticas**: Garante dimensões válidas, ausência de sobreposição de objetos e tipos corretos.
- **Saídas**:
  - Arquivos JSON com a estrutura do cenário.
  - Imagens PNG representando o cenário.
  - Visualização gráfica interativa com Pygame.
- **Interface Interativa**: Menu para selecionar ações (gerar PNG, JSON ou visualizar no Pygame).
- **Tratamento de Erros**: Mensagens detalhadas para erros de sintaxe, validação e execução.

## Requisitos

- **Python**: Versão 3.8 ou superior.
- **Bibliotecas**:
  - `ply`: Para análise léxica e sintática.
  - `Pillow`: Para geração de imagens PNG.
  - `pygame`: Para visualização gráfica.
- Instale as dependências com:
  ```bash
  pip install ply Pillow pygame
  ```

## Estrutura do Projeto

- `main.py`: Código principal contendo o interpretador, validações e funções de saída.
- `README.md`: Este arquivo, com instruções e documentação.
- Saídas geradas:
  - `cenario_X.json`: Arquivos JSON dos cenários.
  - `cenario_X.png`: Imagens PNG dos cenários.

## Como Usar

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu_usuario/interpretador-cenarios.git
   cd interpretador-cenarios
   ```

2. **Configure o Ambiente**:
   Instale as dependências listadas acima.

3. **Execute o Programa**:
   ```bash
   python main.py
   ```
   O programa processa uma entrada de exemplo embutida (ou você pode fornecer um arquivo de entrada).

4. **Interaja com o Menu**:
   Após o parsing, o programa exibe um menu para cada cenário:
   - `1`: Gerar imagem PNG.
   - `2`: Gerar arquivo JSON.
   - `3`: Visualizar no Pygame.
   - `4`: Sair.

## Formato da Entrada

A entrada é um texto que descreve cenários com mapas e objetos. Exemplo:

```text
cenario cenario_floresta {
  mapa {
    dimensao = (1000, 600);
    tipo_terreno = grama;
  }
  objeto arvore1 {
    tipo = arvore;
    posicao = (100, 100);
    dimensao = (50, 50);
  }
  objeto pedra1 {
    tipo = pedra;
    posicao = (200, 200);
    dimensao = (30, 30);
  }
  objeto personagem {
    tipo = jogador;
    posicao = (500, 300);
    dimensao = (20, 20);
  }
}
```

### Regras da Gramática
- **Cenário**: Definido por `cenario ID { mapa objetos }`.
- **Mapa**: Contém `dimensao = (NUMBER, NUMBER);` e `tipo_terreno = (grama | areia | agua);`.
- **Objetos**: Lista de `objeto ID { tipo = (arvore | pedra | jogador); posicao = (NUMBER, NUMBER); dimensao = (NUMBER, NUMBER); }`.
- **Validações**:
  - Dimensões positivas e ≤ 10.000.
  - Tipos de terreno: `grama`, `areia`, `agua`.
  - Tipos de objeto: `arvore`, `pedra`, `jogador`.
  - Sem sobreposição de objetos.
  - Nomes de objetos únicos por cenário.

## Componentes do Código

### 1. Análise Léxica (Lexer)
Define tokens e literais para processar a entrada textual. Exemplo de regra para identificadores:

```python
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t
```

- **Tokens**: `CENARIO`, `MAPA`, `OBJETO`, `DIMENSAO`, `TIPO_TERRENO`, `TIPO`, `POSICAO`, `ID`, `STRING`, `NUMBER`.
- **Literais**: `{`, `}`, `(`, `)`, `=`, `,`, `;`.
- Ignora comentários (`//`), espaços e tabulações.

### 2. Análise Sintática (Parser)
Converte tokens em uma árvore sintática (AST). Exemplo de regra para cenário:

```python
def p_scenario(p):
    '''scenario : CENARIO ID '{' mapa objetos '}' '''
    p.parser.object_names = set()
    p[0] = {
        'cenario': p[2],
        'mapa': p[4],
        'objetos': p[5]
    }
```

- Gera uma lista de dicionários representando cenários.
- Valida tipos, dimensões e nomes únicos.

### 3. Validações Semânticas
- **Limites do Mapa**:
  ```python
  def validate_objects(data):
      width, height = data['mapa']['dimensao']
      for obj in data['objetos']:
          x, y = obj['posicao']
          w, h = obj['dimensao']
          if x + w > width or y + h > height:
              raise ValueError(f"Objeto '{obj['nome']}' excede os limites do mapa")
  ```
- **Sobreposição de Objetos**:
  Verifica colisões entre retângulos delimitadores com complexidade O(n²/2).

### 4. Saídas
- **PNG**: Usa PIL para criar imagens com terreno de fundo e objetos como retângulos coloridos.
  ```python
  def generate_image(data, filename='cenario.png'):
      width, height = data['mapa']['dimensao']
      img = Image.new('RGB', (width, height), color=get_pil_color(data['mapa']['tipo_terreno']))
      draw = ImageDraw.Draw(img)
      for obj in data['objetos']:
          x, y = obj['posicao']
          w, h = obj['dimensao']
          draw.rectangle((x, y, x + w, y + h), fill=get_pil_color(obj['tipo']), outline='black')
      img.save(filename)
  ```
- **JSON**: Salva a estrutura do cenário em um arquivo com indentação.
- **Pygame**: Exibe o cenário em uma janela gráfica interativa.

## Limitações

- **Complexidade da Verificação de Sobreposição**: O(n²/2) para comparação par a par de objetos.
- **Escalabilidade**: Mapas muito grandes (>10.000 pixels) ou com muitos objetos podem ser lentos.
- **Extensibilidade**: Adicionar novos tipos de terreno ou objeto requer atualizar dicionários de validação e cores.

## Possíveis Melhorias

- Otimizar a verificação de sobreposição com estruturas espaciais (e.g., quadtrees).
- Suportar entrada de arquivos externos.
- Adicionar mais tipos de terreno e objetos.
- Implementar animações ou interatividade no Pygame.

## Contribuição

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`).
4. Push para a branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
