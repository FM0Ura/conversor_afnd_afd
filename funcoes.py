from typing import Any, LiteralString
import graphviz
import os

def calcular_fecho_vazio(estados, transicoes) -> frozenset[Any]:
    """Calcula o fecho-ε para um conjunto de estados."""
    fecho = set(estados)
    pilha = list(estados)
    while pilha:
        estado_atual = pilha.pop()
        # Verifica transições vazias ('h') a partir do estado atual
        if estado_atual in transicoes and 'h' in transicoes[estado_atual]:
            for proximo_estado in transicoes[estado_atual]['h']:
                if proximo_estado not in fecho:
                    fecho.add(proximo_estado)
                    pilha.append(proximo_estado)
    return frozenset(fecho)

def mover(estados, simbolo, transicoes) -> frozenset[Any]:
    """Calcula o conjunto de estados alcançáveis a partir de um conjunto de estados com um dado símbolo."""
    destinos = set()
    for estado in estados:
        if estado in transicoes and simbolo in transicoes[estado]:
            destinos.update(transicoes[estado][simbolo])
    return frozenset(destinos)

def converter_afnd_para_afd(estados_afnd, alfabeto, transicoes_afnd, estado_inicial_afnd, estados_finais_afnd) -> tuple[set[Any], dict[Any, Any], frozenset[Any], set[Any]]:
    """Converte um AFND-ε em um AFD."""
    # Estruturas de dados para o novo AFD
    afd_transicoes = {}
    afd_estados = set()
    afd_estados_finais = set()
    
    # O estado inicial do AFD é o fecho-ε do estado inicial do AFND
    estado_inicial_afd = calcular_fecho_vazio({estado_inicial_afnd}, transicoes_afnd)
    afd_estados_a_processar = [estado_inicial_afd]
    afd_estados.add(estado_inicial_afd)

    while afd_estados_a_processar:
        estado_atual_afd_set = afd_estados_a_processar.pop(0)
        
        # Verifica se o estado atual do AFD contém algum estado final do AFND
        if any(s in estados_finais_afnd for s in estado_atual_afd_set):
            afd_estados_finais.add(estado_atual_afd_set)

        afd_transicoes[estado_atual_afd_set] = {}

        for simbolo in alfabeto:
            # Calcula o próximo estado
            proximo_estado_set = calcular_fecho_vazio(mover(estado_atual_afd_set, simbolo, transicoes_afnd), transicoes_afnd)
            
            if proximo_estado_set:
                if proximo_estado_set not in afd_estados:
                    afd_estados.add(proximo_estado_set)
                    afd_estados_a_processar.append(proximo_estado_set)
                
                afd_transicoes[estado_atual_afd_set][simbolo] = proximo_estado_set

    return afd_estados, afd_transicoes, estado_inicial_afd, afd_estados_finais

def formatar_nome_estado(estado_set) -> LiteralString:
    """Cria um nome de estado concatenado a partir de um conjunto de estados."""
    return "".join(sorted(list(estado_set)))

def escrever_arquivo_afd(nome_arquivo, afd_estados, afd_transicoes, estado_inicial_afd, afd_estados_finais) -> None:
    """Escreve a definição do AFD em um arquivo de texto."""
    mapeamento_nomes = {s: formatar_nome_estado(s) for s in afd_estados}

    with open(nome_arquivo, 'w') as f:
        # Linha 0: Estados
        f.write(" ".join(mapeamento_nomes.values()) + '\n')
        # Linha 1: Estado inicial
        f.write(mapeamento_nomes[estado_inicial_afd] + '\n')
        # Linha 2: Estados finais
        f.write(" ".join(mapeamento_nomes[s] for s in afd_estados_finais) + '\n')
        # Demais linhas: Transições
        for estado_origem_set, transicoes_simbolo in afd_transicoes.items():
            for simbolo, estado_destino_set in transicoes_simbolo.items():
                nome_origem = mapeamento_nomes[estado_origem_set]
                nome_destino = mapeamento_nomes[estado_destino_set]
                f.write(f"{nome_origem} {simbolo} {nome_destino}\n")

def gerar_visualizacao_graphviz(automato_info, nome_arquivo, titulo) -> None:
    """Gera uma imagem do automato usando GraphViz."""
    dot = graphviz.Digraph(comment=titulo)
    dot.attr(rankdir='LR')
    dot.attr('node', shape='doublecircle')
    for estado in automato_info['finais']:
        dot.node(estado)

    dot.attr('node', shape='circle')
    for estado in set(automato_info['estados']) - set(automato_info['finais']):
        dot.node(estado)
        
    # Seta para o estado inicial
    dot.node('', shape='point')
    dot.edge('', automato_info['inicial'])

    for origem, transicoes in automato_info['transicoes'].items():
        for simbolo, destinos in transicoes.items():
            for destino in destinos:
                dot.edge(origem, destino, label=simbolo)
    
    # Evita erro se o diretório não existir
    if not os.path.exists('output'):
        os.makedirs('output')

    caminho_completo = os.path.join('output', nome_arquivo)
    dot.render(caminho_completo, view=False, format='png')
    print(f"Visualização do {titulo} salva em '{caminho_completo}.png'")

def reconhecer_palavras(afd_transicoes, estado_inicial_afd, afd_estados_finais, palavras) -> list[Any]:
    """Verifica se uma lista de palavras é aceita pelo AFD."""
    mapeamento_nomes = {s: formatar_nome_estado(s) for s in afd_transicoes.keys()}
    
    # Inverte o mapeamento para encontrar o conjunto a partir do nome
    mapa_reverso_nomes = {v: k for k, v in mapeamento_nomes.items()}
    
    estado_inicial_nome = formatar_nome_estado(estado_inicial_afd)
    estados_finais_nomes = {formatar_nome_estado(s) for s in afd_estados_finais}

    resultados = []
    for palavra in palavras:
        palavra = palavra.strip()
        if not palavra: # Palavra vazia
             if estado_inicial_nome in estados_finais_nomes:
                 resultados.append(f"{palavra if palavra else 'ε'} aceito")
             else:
                 resultados.append(f"{palavra if palavra else 'ε'} não aceito")
             continue

        estado_atual_nome = estado_inicial_nome
        aceita = True
        
        for simbolo in palavra:
            estado_atual_set = mapa_reverso_nomes.get(estado_atual_nome)
            
            if estado_atual_set and simbolo in afd_transicoes.get(estado_atual_set, {}):
                proximo_estado_set = afd_transicoes[estado_atual_set][simbolo]
                estado_atual_nome = formatar_nome_estado(proximo_estado_set)
            else:
                aceita = False
                break
        
        if aceita and estado_atual_nome in estados_finais_nomes:
            resultados.append(f"{palavra} aceito")
        else:
            resultados.append(f"{palavra} não aceito")
            
    return resultados

def processar_arquivo_entrada(caminho_arquivo) -> tuple[set[str], dict[Any, Any], str, set[str]]:
    """Lê e processa o arquivo de entrada do AFND."""
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
