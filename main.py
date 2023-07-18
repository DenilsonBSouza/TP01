from grafoPonderado import GrafoPonderado
from unidecode import unidecode
import csv
import time
import os.path
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Inicializar o Tkinter
root = Tk()
root.withdraw() # Remover a janela padrão do Tkinter  

g = GrafoPonderado() # Grafo ponderado
data = [] # Lista de votações

start_time = time.time() # Iniciar a contagem do tempo de execução
votacoes_por_deputado = {} # Dicionário de votações por deputado

nome_arquivo = None
while not nome_arquivo:
    print(" ")
# Solicitar ao usuário que escolha o arquivo
    print("Informe o arquivo de votações: ")
    nome_arquivo = askopenfilename()
    
    # Verificar se o usuário selecionou um arquivo
    if nome_arquivo:
        if nome_arquivo.lower().endswith('.csv'):
            try:
                arquivo = open(nome_arquivo, 'r')
                diretorio = os.path.dirname(nome_arquivo)
                # Realize as operações desejadas com o arquivo aqui
                arquivo.close()
                nome_arquivo = os.path.basename(nome_arquivo)
                print("Arquivo selecionado:","<"+nome_arquivo+">")
            except FileNotFoundError:
                print("O arquivo não foi encontrado.")
                sys.exit(1)  # Sair do programa em caso de arquivo não encontrado
        else:
            print("O arquivo selecionado não é um arquivo CSV. Favor selecionar um arquivo válido.")  
            sys.exit(1)  # Sair do programa em caso de arquivo não encontrado 
    else:
        print("Nenhum arquivo selecionado.")
        sys.exit(1)  # Sair do programa em caso de arquivo não encontrado

print("Processando..." + "\n")       

if diretorio:
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    with open(caminho_arquivo, newline="", encoding="latin-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader)
        for row in reader:
            data.append(row)
        
for i in range(len(data)):
    voto = unidecode(data[i][3])
    idVotacao = data[i][0]
    deputado1 = unidecode(data[i][6])
    deputado_id = data[i][4]

    if voto != "-":
        if deputado1 not in votacoes_por_deputado:
            votacoes_por_deputado[deputado1] = set()

        votacoes_por_deputado[deputado1].add(idVotacao)

        for j in range(i+1, len(data)):
            voto2 = unidecode(data[j][3])
            idVotacao2 = data[j][0]
            deputado2 = unidecode(data[j][6])
            deputado_id2 = data[j][4]

            if (
                voto2 != "-"
                and idVotacao == idVotacao2
                and deputado1 != deputado2
                and deputado_id != deputado_id2
                and voto == voto2
            ):
                if deputado2 not in votacoes_por_deputado:
                    votacoes_por_deputado[deputado2] = set()

                votacoes_por_deputado[deputado1].add(idVotacao)
                votacoes_por_deputado[deputado2].add(idVotacao2)

                if not g.no_existe(deputado1):
                    g.adicionar_no(deputado1)
                if not g.no_existe(deputado2):
                    g.adicionar_no(deputado2)

                if not g.aresta_existe(deputado2, deputado1):
                    g.adicionar_aresta(deputado1, deputado2, 1)
                else:
                    g.lista_adj[deputado1][deputado2] += 1

# Atualizar o número de votações para cada deputado
for deputado in votacoes_por_deputado:
    votacoes_por_deputado[deputado] = len(votacoes_por_deputado[deputado])

# Classificar os deputados por votação e relacionamento
deputados_ordenados = sorted(votacoes_por_deputado.items(), key=lambda x: (-x[1], x[0]))

with open(f"votacaoVotos_2023_graph.txt", "w", encoding="utf-8") as arquivo_grafo:
    arquivo_grafo.write(f"{g.num_nos} {g.num_arestas}\n")
    for deputado, num_votacoes in deputados_ordenados:
        deputado_formatted = deputado.replace(" ", "_")
        edges = g.lista_adj.get(deputado)

        if edges:
            for deputado2, weight in edges.items():
                deputado2_formatted = deputado2.replace(" ", "_")
                arquivo_grafo.write(f"{deputado_formatted} {deputado2_formatted} {weight}\n")

with open(f"votacaoVotos_2023_deputados.txt", "w", encoding="utf-8") as arquivo_votacoes:
    arquivo_votacoes.write(f"{len(votacoes_por_deputado)}\n")
    for deputado, num_votacoes in deputados_ordenados:
        deputado_formatted = deputado.replace(" ", "_")
        arquivo_votacoes.write(f"{deputado_formatted} {num_votacoes}\n")

end_time = time.time()
tempo_execucao = end_time - start_time
#print("Tempo de execução: {:.2f} segundos".format(tempo_execucao)) 

print("O grafo foi escrito nos arquivos:")
print(" - "+ arquivo_grafo.name)
print(" - "+ arquivo_votacoes.name + "\n")
