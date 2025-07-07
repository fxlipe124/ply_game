# Interpretador de Cenários 2D

Este projeto implementa um interpretador de cenários 2D utilizando Python, com uma estrutura modularizada. Ele utiliza a biblioteca **PLY (Python Lex-Yacc)** para análise léxica e sintática, **PIL (Python Imaging Library)** para geração de imagens PNG e **Pygame** para visualização gráfica interativa. O interpretador processa descrições textuais de cenários (como mapas de jogos com objetos), valida suas regras e gera saídas em formatos JSON, PNG e visualizações interativas.

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

- `venv/`: Ambiente virtual do projeto.
- `main.py`: Código principal que coordena a execução do interpretador.
- `lexer.py`: Módulo responsável pela análise léxica.
- `parser.py`: Módulo responsável pela análise sintática e construção da AST.
- `utils.py`: Módulo com funções auxiliares, como conversão de cores e validações.
- `render.py`: Módulo para geração de imagens PNG e visualização com Pygame.
- `parser_out/`: Diretório para saídas geradas (e.g., `cenario_X.json`, `cenario_X.png`).
- `README.md`: Este arquivo, com instruções e documentação.

## Como Usar

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/fxlipe124/interpretador-cenarios.git
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

```plaintext
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

## Regras da Gramática

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

### Análise Léxica (`lexer.py`)

- Define tokens e literais para processar a entrada textual.
- **Tokens**: `CENARIO`, `MAPA`, `OBJETO`, `DIMENSAO`, `TIPO_TERRENO`, `TIPO`, `POSICAO`, `ID`, `STRING`, `NUMBER`.
- **Literais**: `{`, `}`, `(`, `)`, `=`, `,`, `;`.
- Ignora comentários (`//`), espaços e tabulações.

### Análise Sintática (`parser.py`)

- Converte tokens em uma árvore sintática (AST).
- Exemplo de regra: `scenario : CENARIO ID '{' mapa objetos '}'`.

### Validações Semânticas (`utils.py`)

- **Limites do Mapa**: Verifica se objetos estão dentro das dimensões definidas.
- **Sobreposição de Objetos**: Verifica colisões entre retângulos com complexidade O(n²/2).

### Saídas (`render.py`)

- **PNG**: Usa PIL para criar imagens com terreno de fundo e objetos como retângulos coloridos.
- **JSON**: Salva a estrutura do cenário em um arquivo com indentação.
- **Pygame**: Exibe o cenário em uma janela gráfica interativa.

## Contribuição

1. Faça um fork do repositório.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Commit suas mudanças:
   ```bash
   git commit -m 'Adiciona nova funcionalidade'
   ```
4. Push para a branch:
   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. Abra um Pull Request.
