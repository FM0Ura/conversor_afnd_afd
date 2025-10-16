# Importa as bibliotecas necessárias.
# typing para anotações de tipo, que melhoram a legibilidade e verificação do código.
# graphviz para criar visualizações gráficas dos autômatos.
# os para interagir com o sistema operacional, como criar diretórios.
from typing import Any, LiteralString
import graphviz
import os

def calcular_fecho_vazio(estados, transicoes) -> frozenset[Any]:
    """
    Calcula o fecho-ε (ou fecho-vazio) para um conjunto de estados.
    O fecho-ε de um estado 'q' é o conjunto de todos os estados que podem ser alcançados
    a partir de 'q' usando apenas transições vazias (representadas por 'h').

    Args:
        estados (set): Um conjunto de estados para os quais o fecho-ε será calculado.
        transicoes (dict): O dicionário de transições do AFND.

    Returns:
        frozenset: Um conjunto imutável contendo todos os estados no fecho-ε.
    """
    fecho = set(estados)
    pilha = list(estados)
    while pilha:
        estado_atual = pilha.pop()
        # Verifica se existem transições vazias ('h') a partir do estado atual.
        if estado_atual in transicoes and 'h' in transicoes[estado_atual]:
            for proximo_estado in transicoes[estado_atual]['h']:
                if proximo_estado not in fecho:
                    fecho.add(proximo_estado)
                    pilha.append(proximo_estado)
    return frozenset(fecho)

def mover(estados, simbolo, transicoes) -> frozenset[Any]:
    """
    Calcula o conjunto de estados alcançáveis a partir de um conjunto de estados
    com um determinado símbolo do alfabeto.

    Args:
        estados (set): O conjunto de estados de origem.
        simbolo (str): O símbolo da transição.
        transicoes (dict): O dicionário de transições do AFND.

    Returns:
        frozenset: Um conjunto imutável de estados de destino.
    """
    destinos = set()
    for estado in estados:
        if estado in transicoes and simbolo in transicoes[estado]:
            destinos.update(transicoes[estado][simbolo])
    return frozenset(destinos)

def converter_afnd_para_afd(estados_afnd, alfabeto, transicoes_afnd, estado_inicial_afnd, estados_finais_afnd) -> tuple[set[Any], dict[Any, Any], frozenset[Any], set[Any]]:
    """
    Converte um AFND (com ou sem transições vazias) em um AFD equivalente
    usando o algoritmo de construção de subconjuntos.

    Args:
        estados_afnd (set): Conjunto de estados do AFND.
        alfabeto (set): Alfabeto do autômato.
        transicoes_afnd (dict): Transições do AFND.
        estado_inicial_afnd (str): Estado inicial do AFND.
        estados_finais_afnd (set): Conjunto de estados finais do AFND.

    Returns:
        tuple: Uma tupla contendo os componentes do novo AFD:
               (estados_afd, transicoes_afd, estado_inicial_afd, estados_finais_afd).
    """
    # Estruturas de dados para o novo AFD.
    afd_transicoes = {}
    afd_estados = set()
    afd_estados_finais = set()
    
    # O estado inicial do AFD é o fecho-ε do estado inicial do AFND.
    estado_inicial_afd = calcular_fecho_vazio({estado_inicial_afnd}, transicoes_afnd)
    afd_estados_a_processar = [estado_inicial_afd]  # Fila de novos estados do AFD a serem processados.
    afd_estados.add(estado_inicial_afd)

    while afd_estados_a_processar:
        estado_atual_afd_set = afd_estados_a_processar.pop(0)
        
        # Um estado do AFD é final se contiver pelo menos um estado final do AFND.
        if any(s in estados_finais_afnd for s in estado_atual_afd_set):
            afd_estados_finais.add(estado_atual_afd_set)

        afd_transicoes[estado_atual_afd_set] = {}

        for simbolo in alfabeto:
            # Para cada símbolo, calcula o próximo estado do AFD:
            # 1. 'mover' encontra os estados alcançáveis com o símbolo.
            # 2. 'calcular_fecho_vazio' expande o resultado com transições vazias.
            proximo_estado_set = calcular_fecho_vazio(mover(estado_atual_afd_set, simbolo, transicoes_afnd), transicoes_afnd)
            
            if proximo_estado_set:  # Se houver um próximo estado (não for um conjunto vazio)
                if proximo_estado_set not in afd_estados:
                    afd_estados.add(proximo_estado_set)
                    afd_estados_a_processar.append(proximo_estado_set)
                
                afd_transicoes[estado_atual_afd_set][simbolo] = proximo_estado_set

    return afd_estados, afd_transicoes, estado_inicial_afd, afd_estados_finais

def formatar_nome_estado(estado_set) -> LiteralString:
    """
    Cria um nome de estado legível a partir de um conjunto de estados do AFND.
    Exemplo: o conjunto {'q0', 'q2'} se torna a string "q0q2".

    Args:
        estado_set (frozenset): O conjunto de estados que forma um único estado do AFD.

    Returns:
        str: O nome formatado para o estado do AFD.
    """
    return "".join(sorted(list(estado_set)))

def escrever_arquivo_afd(nome_arquivo, afd_estados, afd_transicoes, estado_inicial_afd, afd_estados_finais) -> None:
    """
    Escreve a definição formal do AFD em um arquivo de texto.

    Args:
        nome_arquivo (str): O caminho do arquivo de saída.
        afd_estados (set): Conjunto de estados do AFD.
        afd_transicoes (dict): Dicionário de transições do AFD.
        estado_inicial_afd (frozenset): Estado inicial do AFD.
        afd_estados_finais (set): Conjunto de estados finais do AFD.
    """
    # Mapeia cada conjunto de estados (estado do AFD) para seu nome formatado.
    mapeamento_nomes = {s: formatar_nome_estado(s) for s in afd_estados}

    with open(nome_arquivo, 'w') as f:
        # Linha 0: Lista de todos os estados.
        f.write(" ".join(mapeamento_nomes.values()) + '\n')
        # Linha 1: Estado inicial.
        f.write(mapeamento_nomes[estado_inicial_afd] + '\n')
        # Linha 2: Lista de estados finais.
        f.write(" ".join(mapeamento_nomes[s] for s in afd_estados_finais) + '\n')
        # Demais linhas: Transições no formato "origem simbolo destino".
        for estado_origem_set, transicoes_simbolo in afd_transicoes.items():
            for simbolo, estado_destino_set in transicoes_simbolo.items():
                nome_origem = mapeamento_nomes[estado_origem_set]
                nome_destino = mapeamento_nomes[estado_destino_set]
                f.write(f"{nome_origem} {simbolo} {nome_destino}\n")

def gerar_visualizacao_graphviz(automato_info, nome_arquivo, titulo) -> None:
    """
    Gera uma imagem (.png) do autômato usando a biblioteca Graphviz.

    Args:
        automato_info (dict): Dicionário com as informações do autômato (estados, inicial, finais, transições).
        nome_arquivo (str): Nome base para o arquivo de saída (sem extensão).
        titulo (str): Título do grafo.
    """
    dot = graphviz.Digraph(comment=titulo)
    dot.attr(rankdir='LR')  # Layout da esquerda para a direita.
    
    # Define os estados finais com círculo duplo.
    dot.attr('node', shape='doublecircle')
    for estado in automato_info['finais']:
        dot.node(estado)

    # Define os demais estados com círculo simples.
    dot.attr('node', shape='circle')
    for estado in set(automato_info['estados']) - set(automato_info['finais']):
        dot.node(estado)
        
    # Adiciona uma seta para indicar o estado inicial.
    dot.node('', shape='point')
    dot.edge('', automato_info['inicial'])

    # Adiciona as transições (arestas) ao grafo.
    for origem, transicoes in automato_info['transicoes'].items():
        for simbolo, destinos in transicoes.items():
            for destino in destinos:
                dot.edge(origem, destino, label=simbolo)
    
    # Garante que o diretório de saída exista.
    if not os.path.exists('output'):
        os.makedirs('output')

    # Salva o grafo como uma imagem PNG.
    caminho_completo = os.path.join('output', nome_arquivo)
    dot.render(caminho_completo, view=False, format='png')
    print(f"Visualização do {titulo} salva em '{caminho_completo}.png'")

def reconhecer_palavras(afd_transicoes, estado_inicial_afd, afd_estados_finais, palavras) -> list[Any]:
    """
    Simula o AFD para uma lista de palavras e verifica se cada uma é aceita ou não.

    Args:
        afd_transicoes (dict): Dicionário de transições do AFD.
        estado_inicial_afd (frozenset): Estado inicial do AFD.
        afd_estados_finais (set): Conjunto de estados finais do AFD.
        palavras (list[str]): Lista de palavras a serem testadas.

    Returns:
        list[str]: Uma lista de strings indicando se cada palavra foi "aceita" ou "não aceita".
    """
    # Cria mapeamentos para facilitar a manipulação dos nomes dos estados.
    mapeamento_nomes = {s: formatar_nome_estado(s) for s in afd_transicoes.keys()}
    mapa_reverso_nomes = {v: k for k, v in mapeamento_nomes.items()}
    
    estado_inicial_nome = formatar_nome_estado(estado_inicial_afd)
    estados_finais_nomes = {formatar_nome_estado(s) for s in afd_estados_finais}

    resultados = []
    for palavra in palavras:
        palavra = palavra.strip()
        
        # Caso especial: palavra vazia (ε).
        if not palavra:
             if estado_inicial_nome in estados_finais_nomes:
                 resultados.append(f"{'ε'} aceito")
             else:
                 resultados.append(f"{'ε'} não aceito")
             continue

        estado_atual_nome = estado_inicial_nome
        aceita = True
        
        # Processa cada símbolo da palavra.
        for simbolo in palavra:
            estado_atual_set = mapa_reverso_nomes.get(estado_atual_nome)
            
            # Verifica se existe uma transição válida.
            if estado_atual_set and simbolo in afd_transicoes.get(estado_atual_set, {}):
                proximo_estado_set = afd_transicoes[estado_atual_set][simbolo]
                estado_atual_nome = formatar_nome_estado(proximo_estado_set)
            else:
                # Se não houver transição, a palavra é rejeitada.
                aceita = False
                break
        
        # A palavra é aceita se, após consumir todos os símbolos, o estado atual for final.
        if aceita and estado_atual_nome in estados_finais_nomes:
            resultados.append(f"{palavra} aceito")
        else:
            resultados.append(f"{palavra} não aceito")
            
    return resultados

def processar_arquivo_entrada(caminho_arquivo) -> tuple[set[str], dict[Any, Any], str, set[str]]:
    """
    Lê e processa o arquivo de texto que define o AFND.

    O arquivo deve ter o seguinte formato:
    - Linha 0: Estados, separados por espaço.
    - Linha 1: Estado inicial.
    - Linha 2: Estados finais, separados por espaço.
    - Demais linhas: Transições no formato "origem simbolo destino".

    Args:
        caminho_arquivo (str): O caminho para o arquivo de entrada.

    Returns:
        tuple: Uma tupla contendo (estados, transicoes, estado_inicial, estados_finais).
    """
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

    estados = set(linhas[0].strip().split())
    estado_inicial = linhas[1].strip()
    estados_finais = set(linhas[2].strip().split())
    
    transicoes = {}
    for linha in linhas[3:]:
        partes = linha.strip().split()
        if len(partes) == 3:
            origem, simbolo, destino = partes
            if origem not in transicoes:
                transicoes[origem] = {}
            if simbolo not in transicoes[origem]:
                transicoes[origem][simbolo] = set()
            transicoes[origem][simbolo].add(destino)
    
    return estados, transicoes, estado_inicial, estados_finais
