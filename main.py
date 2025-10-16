# Importa todas as funções do arquivo funcoes.py
from funcoes import *

# --- Configurações Iniciais ---
# Define o nome do arquivo que contém a definição do AFND (Autômato Finito Não Determinístico).
arquivo_afnd_entrada = 'arquivo_entrada.txt'
# Define o alfabeto do autômato.
alfabeto_afnd = {'0', '1'}

# --- Etapa 1: Processamento do AFND de Entrada ---
# Chama a função para ler e processar o arquivo de entrada do AFND.
# A função retorna os estados, as transições, o estado inicial e os estados finais do AFND.
estados_afnd, transicoes_afnd, estado_inicial_afnd, estados_finais_afnd = processar_arquivo_entrada(
    arquivo_afnd_entrada)
# Imprime as informações do AFND carregado para verificação.
print("--- AFND de Entrada Carregado ---")
print(f"Estados: {estados_afnd}")
print(f"Estado Inicial: {estado_inicial_afnd}")
print(f"Estados Finais: {estados_finais_afnd}")
print(f"Transições: {transicoes_afnd}\n")

# --- Etapa 2: Geração da Visualização Gráfica do AFND ---
# Prepara os dados do AFND em um dicionário para a função de visualização.
info_afnd_graphviz = {
    'estados': list(estados_afnd),
    'inicial': estado_inicial_afnd,
    'finais': list(estados_finais_afnd),
    'transicoes': transicoes_afnd
}
# Gera uma representação gráfica do AFND usando a biblioteca Graphviz e a salva em um arquivo.
gerar_visualizacao_graphviz(
    info_afnd_graphviz, "afnd_entrada", "AFND de Entrada")

# --- Etapa 3: Conversão do AFND para AFD ---
# Realiza a conversão do AFND para um AFD (Autômato Finito Determinístico) usando o algoritmo de construção de subconjuntos.
# A função retorna os novos estados, transições, estado inicial e estados finais do AFD.
afd_estados_set, afd_transicoes, estado_inicial_afd_set, afd_estados_finais_set = converter_afnd_para_afd(
    estados_afnd, alfabeto_afnd, transicoes_afnd, estado_inicial_afnd, estados_finais_afnd
)

# Os estados do AFD são conjuntos de estados do AFND.
# Para facilitar a leitura, criamos um mapa para nomes mais simples (ex: {q0, q1} -> S0).
map_nomes_afd = {s: formatar_nome_estado(s) for s in afd_estados_set}

# Imprime as informações do AFD resultante.
print("--- AFD Convertido ---")
print(f"Estado Inicial: {map_nomes_afd[estado_inicial_afd_set]}")
print(f"Estados Finais: {{map_nomes_afd[s] for s in afd_estados_finais_set}}")
print("Transições:")
# Itera sobre as transições do AFD para imprimi-las de forma legível.
for origem_set, transicoes in afd_transicoes.items():
    for simbolo, destino_set in transicoes.items():
        print(f"  {map_nomes_afd[origem_set]
                   } --{simbolo}--> {map_nomes_afd[destino_set]}")

# --- Etapa 4: Geração do Arquivo de Saída do AFD ---
# Define o nome do arquivo de saída para o AFD.
arquivo_afd_saida = 'output/afd_saida.txt'
# Garante que o diretório 'output' exista antes de salvar o arquivo.
if not os.path.exists('output'):
    os.makedirs('output')
# Escreve a definição formal do AFD em um arquivo de texto.
escrever_arquivo_afd(arquivo_afd_saida, afd_estados_set,
                     afd_transicoes, estado_inicial_afd_set, afd_estados_finais_set)
print(f"\nArquivo de saída do AFD gerado em: '{arquivo_afd_saida}'")

# --- Etapa 5: Geração da Visualização Gráfica do AFD ---
# Prepara os dados do AFD para a função de visualização, usando os nomes formatados.
transicoes_afd_graphviz = {}
for origem_set, transicoes_simbolo in afd_transicoes.items():
    origem_nome = map_nomes_afd[origem_set]
    transicoes_afd_graphviz[origem_nome] = {}
    for simbolo, destino_set in transicoes_simbolo.items():
        transicoes_afd_graphviz[origem_nome][simbolo] = {
            map_nomes_afd[destino_set]}

info_afd_graphviz = {
    'estados': list(map_nomes_afd.values()),
    'inicial': map_nomes_afd[estado_inicial_afd_set],
    'finais': [map_nomes_afd[s] for s in afd_estados_finais_set],
    'transicoes': transicoes_afd_graphviz
}
# Gera uma representação gráfica do AFD e a salva em um arquivo.
gerar_visualizacao_graphviz(
    info_afd_graphviz, "afd_convertido", "AFD Convertido")

# --- Etapa 6: Reconhecimento de Palavras com o AFD ---
# Define os arquivos de entrada (com as palavras) e saída (com os resultados).
arquivo_palavras_entrada = 'palavras.txt'
arquivo_palavras_saida = 'output/resultado_palavras.txt'

# Para fins de demonstração, cria um arquivo com palavras de teste.
palavras_para_teste = ["101", "00110", "1100", "010101", "1", "0", "", "0111110"]
with open(arquivo_palavras_entrada, 'w') as f:
    for p in palavras_para_teste:
        f.write(p + '\n')
print(f"\nArquivo de palavras para teste criado: '{arquivo_palavras_entrada}'")

# Lê as palavras do arquivo de entrada.
with open(arquivo_palavras_entrada, 'r') as f:
    palavras = f.readlines()

# Chama a função que simula o AFD para cada palavra e verifica se é aceita ou rejeitada.
resultados = reconhecer_palavras(
    afd_transicoes, estado_inicial_afd_set, afd_estados_finais_set, palavras)

# Salva os resultados (aceita/rejeita para cada palavra) no arquivo de saída.
with open(arquivo_palavras_saida, 'w', encoding='utf-8') as f:
    for res in resultados:
        f.write(res + '\n')
print(f"Resultados do reconhecimento de palavras salvos em: '{arquivo_palavras_saida}'")
