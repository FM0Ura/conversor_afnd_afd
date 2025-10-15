from funcoes import *
# Definição dos arquivos e alfabeto
arquivo_afnd_entrada = 'arquivo_entrada.txt'
alfabeto_afnd = {'0', '1'}

# 1. Processar AFND
estados_afnd, transicoes_afnd, estado_inicial_afnd, estados_finais_afnd = processar_arquivo_entrada(
    arquivo_afnd_entrada)
print("--- AFND de Entrada Carregado ---")
print(f"Estados: {estados_afnd}")
print(f"Estado Inicial: {estado_inicial_afnd}")
print(f"Estados Finais: {estados_finais_afnd}")
print(f"Transições: {transicoes_afnd}\n")
# 2. Gerar visualização do AFND
info_afnd_graphviz = {
    'estados': list(estados_afnd),
    'inicial': estado_inicial_afnd,
    'finais': list(estados_finais_afnd),
    'transicoes': transicoes_afnd
}
gerar_visualizacao_graphviz(
    info_afnd_graphviz, "afnd_entrada", "AFND de Entrada")
# 3. Converter para AFD
afd_estados_set, afd_transicoes, estado_inicial_afd_set, afd_estados_finais_set = converter_afnd_para_afd(
    estados_afnd, alfabeto_afnd, transicoes_afnd, estado_inicial_afnd, estados_finais_afnd
)

# Formatar nomes dos estados do AFD para saída
map_nomes_afd = {s: formatar_nome_estado(s) for s in afd_estados_set}

print("--- AFD Convertido ---")
print(f"Estado Inicial: {map_nomes_afd[estado_inicial_afd_set]}")
print(f"Estados Finais: {{map_nomes_afd[s] for s in afd_estados_finais_set}}")
print("Transições:")
for origem_set, transicoes in afd_transicoes.items():
    for simbolo, destino_set in transicoes.items():
        print(f"  {map_nomes_afd[origem_set]
                   } --{simbolo}--> {map_nomes_afd[destino_set]}")
# 4. Escrever arquivo de saída do AFD
arquivo_afd_saida = 'output/afd_saida.txt'
if not os.path.exists('output'):
    os.makedirs('output')
escrever_arquivo_afd(arquivo_afd_saida, afd_estados_set,
                     afd_transicoes, estado_inicial_afd_set, afd_estados_finais_set)
print(f"\nArquivo de saída do AFD gerado em: '{arquivo_afd_saida}'")
# 5. Gerar visualização do AFD
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
gerar_visualizacao_graphviz(
    info_afd_graphviz, "afd_convertido", "AFD Convertido")

# 6. Parte 2: Reconhecer palavras
arquivo_palavras_entrada = 'palavras.txt'
arquivo_palavras_saida = 'output/resultado_palavras.txt'

# Criar um arquivo de exemplo para teste
palavras_para_teste = ["101", "00110", "1100", "010101", "1", "0", ""]
with open(arquivo_palavras_entrada, 'w') as f:
    for p in palavras_para_teste:
        f.write(p + '\n')
print(f"\nArquivo de palavras para teste criado: '{arquivo_palavras_entrada}'")

with open(arquivo_palavras_entrada, 'r') as f:
    palavras = f.readlines()

resultados = reconhecer_palavras(
    afd_transicoes, estado_inicial_afd_set, afd_estados_finais_set, palavras)

with open(arquivo_palavras_saida, 'w', encoding='utf-8') as f:
    for res in resultados:
        f.write(res + '\n')
print(f"Resultados do reconhecimento de palavras salvos em: '{
      arquivo_palavras_saida}'")
