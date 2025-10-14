# Conversor de AFND-ε para AFD e Reconhecedor de Palavras

Este projeto implementa a conversão de um Autômato Finito Não Determinístico com transições ε (AFND-ε) para um Autômato Finito Determinístico (AFD) equivalente. Além disso, o código é capaz de testar se um conjunto de palavras é aceito pelo autômato gerado e criar uma representação visual de ambos os autômatos.

## Pré-requisitos

Antes de executar o projeto, certifique-se de que você possui:

1.  **Python 3.x** instalado.
2.  A biblioteca **Graphviz** para Python. Instale-a com o seguinte comando:
    ```bash
    pip install graphviz
    ```
3.  O software **Graphviz**. A biblioteca Python é apenas uma interface. Você precisa instalar o software principal.
    *   **Windows**: Baixe o instalador em [https://graphviz.org/download/](https://graphviz.org/download/) e adicione o diretório `bin` da instalação ao `PATH` do sistema.
    *   **Linux (Debian/Ubuntu)**:
        ```bash
        sudo apt-get install graphviz
        ```
    *   **macOS (usando Homebrew)**:
        ```bash
        brew install graphviz
        ```

## Como Utilizar

Siga os passos abaixo para executar o projeto:

### 1. Prepare o Arquivo de Entrada do AFND

Edite o arquivo `arquivo_entrada.txt` para definir o seu Autômato Finito Não Determinístico. A estrutura do arquivo deve ser a seguinte:

-   **Linha 1**: Todos os estados do autômato, separados por espaço.
-   **Linha 2**: O estado inicial.
-   **Linha 3**: Os estados finais, separados por espaço.
-   **Linhas seguintes**: As transições, uma por linha, no formato `estado_origem simbolo estado_destino`.
    -   Para transições ε (vazias), utilize a letra `h` como símbolo.

**Exemplo de `arquivo_entrada.txt`:**

```
q0 q1 q2
q0
q2
q0 0 q0
q0 0 q1
q0 h q1
q1 1 q2
```

### 2. Prepare o Arquivo de Palavras

Edite o arquivo `palavras.txt` e insira as palavras que você deseja testar no autômato. Coloque uma palavra por linha.

**Exemplo de `palavras.txt`:**

```
101
00110
1100
0
1
```

### 3. Execute o Notebook

Abra o arquivo `main.ipynb` em um ambiente compatível com Jupyter Notebooks (como o VS Code) e execute todas as células.

O notebook irá realizar as seguintes ações em ordem:
1.  Carregar o AFND do `arquivo_entrada.txt`.
2.  Gerar uma imagem do AFND (`output/afnd_entrada.png`).
3.  Converter o AFND para um AFD.
4.  Salvar a definição do AFD em `output/afd_saida.txt`.
5.  Gerar uma imagem do AFD convertido (`output/afd_convertido.png`).
6.  Testar as palavras de `palavras.txt` no AFD e salvar os resultados em `output/resultado_palavras.txt`.

### 4. Verifique os Resultados

Após a execução, a pasta `output/` conterá os seguintes arquivos:

-   `afnd_entrada.png`: Imagem do autômato não determinístico de entrada.
-   `afd_convertido.png`: Imagem do autômato determinístico resultante.
-   `afd_saida.txt`: A definição formal do AFD convertido.
-   `resultado_palavras.txt`: Indica se cada palavra de entrada foi "aceita" ou "não aceita".

## Estrutura do Projeto

-   `main.ipynb`: Notebook principal que orquestra todo o processo.
-   `funcoes.py`: Módulo com todas as funções para conversão, visualização e reconhecimento de palavras.
-   `arquivo_entrada.txt`: Arquivo para definir o AFND.
-   `palavras.txt`: Arquivo com as palavras a serem testadas.
-   `output/`: Diretório onde todos os arquivos de saída são gerados.
-   `README.md`: Este arquivo.
