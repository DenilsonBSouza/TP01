import heapq

class GrafoPonderado:
    
    def __init__(self):
        self.lista_adj = {}
        self.num_nos = 0
        self.num_arestas = 0

    def adicionar_no(self, no):
        if no in self.lista_adj:
            print(f"AVISO: No {no} já existe")
            return
        self.lista_adj[no] = {}
        self.num_nos += 1

    def adicionar_aresta(self, no1, no2, peso):
        if no1 not in self.lista_adj:
            self.adicionar_no(no1)
        if no2 not in self.lista_adj:
            self.adicionar_no(no2)
        if not self.aresta_existe(no1, no2):    
            self.lista_adj[no1][no2] = peso
            self.num_arestas += 1
        else:
            self.lista_adj[no1][no2] += peso
      
    def no_existe(self, no):
        self.lista_adj.get(no, None) != None
        return no in self.lista_adj    

    def adicionar_aresta_bidirecional(self, no1, no2, peso):
        self.adicionar_aresta(no1, no2, peso)
        self.adicionar_aresta(no2, no1, peso)

    def peso_aresta(self, no1, no2):
        return self.lista_adj[no1][no2]

    def aresta_existe(self, no1, no2):
        return no2 in self.lista_adj[no1]

    def remove_aresta(self, no1, no2):
        try:
          self.lista_adj[no1].pop(no2)
          self.num_arestas -= 1
        except KeyError as e:
            print(f"AVISO: Aresta {no1} -> {no2} não existe")

    def remove_no(self, no):
         for no2 in self.lista_adj:
             if no in self.lista_adj[no2]:
                 self.lista_adj[no2].pop(no)
                 self.num_arestas -= 1
         self.num_arestas -= len(self.lista_adj[no])
         self.num_nos -= 1
         self.lista_adj.pop(no)

    def __str__(self):
        saida = ""
        for no in self.lista_adj:
            saida += f"{no}: {self.lista_adj[no]}\n"
        return saida
    
    def extract_min(self, Q, dist):
        min_dist = float("inf")
        min_node = None
        for node in Q:
            if dist[node] < min_dist:
                min_dist = dist[node]
                min_node = node
        return min_node

    def dijkstra(self, s):
        dist = {}
        pred = {}
        Q = []
        for node in self.lista_adj:
            dist[node] = float('inf')
            pred[node] = None
            Q.append(node)
        dist[s] = 0
        while len(Q) > 0:
            # u = min(Q, key=lambda x: dist[x])
            u = self.extract_min(Q, dist)
            Q.remove(u)
            for v in self.lista_adj[u]:
                w = self.lista_adj[u][v]
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    pred[v] = u
        return (dist, pred)


    def dijkstra_pq(self, s):
        dist = {}
        pred = {}
        for node in self.lista_adj:
            dist[node] = float('inf')
            pred[node] = None
        pq = [(0, s)]
        dist[s] = 0
        while pq:
            u_dist, u = heapq.heappop(pq)
            for v in self.lista_adj[u]:
                w = self.lista_adj[u][v]
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    pred[v] = u
                    heapq.heappush(pq, (dist[v], v))
        return (dist, pred)
    
    def bellman_ford(self, s):
        dist = {}
        pred = {}
        for node in self.lista_adj:
            dist[node] = float('inf')
            pred[node] = None
        dist[s] = 0
        for i in range(self.node_count - 1):
            for u in self.lista_adj:
                for v in self.lista_adj[u]:
                    w = self.lista_adj[u][v]
                    if dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w
                        pred[v] = u
        for u in self.lista_adj:
            for v in self.lista_adj[u]:
                w = self.lista_adj[u][v]
                if dist[v] > dist[u] + w:
                    # Negative cycle detected
                    print("WARN: Negative cycle detected")
                    return (None, None)
        return (dist, pred)

    def bellman_ford_improved(self, s):
        dist = {}
        pred = {}
        for node in self.lista_adj:
            dist[node] = float('inf')
            pred[node] = None
        dist[s] = 0
        for i in range(self.node_count - 1):
            swapped = False
            for u in self.lista_adj:
                for v in self.lista_adj[u]:
                    w = self.lista_adj[u][v]
                    if dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w
                        pred[v] = u
                        swapped = True
            if not swapped:
                break
        return (dist, pred)

    def floyd_warshall(self):
        dist = {}
        pred = {}
        for i in self.lista_adj:
            dist[i] = {}
            pred[i] = {}
            for j in self.lista_adj:
                if i == j:
                    dist[i][j] = 0
                    pred[i][j] = None
                elif j in self.lista_adj[i]:
                    dist[i][j] = self.lista_adj[i][j]
                    pred[i][j] = i
                else:
                    dist[i][j] = float('inf')
                    pred[i][j] = None
        for k in self.lista_adj:
            for i in self.lista_adj:
                for j in self.lista_adj:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]
        return dist, pred
    
    def ler_arquivo(self, nome_arquivo):
        file = open(nome_arquivo, "r")
        i = 0
        for linha in file:
            i += 1
            if i == 1:
                continue
            conteudo = linha.strip().split(" ")
            u = (conteudo[0])
            v = (conteudo[1])
            w = int(conteudo[2])
            self.adicionar_aresta(u, v, w)
        file.close()