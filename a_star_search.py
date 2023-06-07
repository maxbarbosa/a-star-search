import heapq as hp

BUSCA_INICIANDO = 0
BUSCA_FALHOU = 1
BUSCA_SUCESSO = 2

def acao(destino, custo):
    return {'destino': destino, 'custo': custo}

estados_romenia = [
    { 'estado': 'Arad',
      'acoes': [acao('Zerind', 75), acao('Sibiu', 140), acao('Timisoara', 118)] },

    { 'estado': 'Zerind',
      'acoes': [acao('Arad', 75), acao('Oradea', 71)] },

    { 'estado': 'Timisoara',
      'acoes': [acao('Arad', 118), acao('Lugoj', 111)] },

    { 'estado': 'Sibiu',
      'acoes': [acao('Arad', 140), acao('Oradea', 151), acao('Fagaras', 99),
                acao('Rimnicu Vilcea', 80)] },

    { 'estado': 'Oradea',
      'acoes': [acao('Zerind', 71), acao('Sibiu', 151)] },

    { 'estado': 'Lugoj',
      'acoes': [acao('Timisoara', 111), acao('Mehadia', 70)] },

    { 'estado': 'Mehadia',
      'acoes': [acao('Lugoj', 70), acao('Drobeta', 75)] },

    { 'estado': 'Drobeta',
      'acoes': [acao('Mehadia', 75), acao('Craiova', 120)] },

    { 'estado': 'Craiova',
      'acoes': [acao('Drobeta', 120), acao('Rimnicu Vilcea', 146),
                acao('Pitesti', 138)] },

    { 'estado': 'Rimnicu Vilcea',
      'acoes': [acao('Sibiu', 80), acao('Craiova', 146), acao('Pitesti', 97)] },

    { 'estado': 'Fagaras',
      'acoes': [acao('Sibiu', 99), acao('Bucharest', 211)] },

    { 'estado': 'Pitesti',
      'acoes': [acao('Rimnicu Vilcea', 97), acao('Craiova', 138), acao('Bucharest', 101)] },

    { 'estado': 'Giurgiu',
      'acoes': [acao('Bucharest', 90)] },

    { 'estado': 'Bucharest',
      'acoes': [acao('Fagaras', 211), acao('Pitesti', 101), acao('Giurgiu', 90),
                acao('Urziceni', 85)] },

    { 'estado': 'Urziceni',
      'acoes': [acao('Bucharest', 85), acao('Vaslui', 142), acao('Hirsova', 98)] },

    { 'estado': 'Hirsova',
      'acoes': [acao('Urziceni', 98), acao('Eforie', 86)] },

    { 'estado': 'Eforie',
      'acoes': [acao('Hirsova', 86)] },

    { 'estado': 'Vaslui',
      'acoes': [acao('Urziceni', 142), acao('Iasi', 92)] },

    { 'estado': 'Iasi',
      'acoes': [acao('Vaslui', 92), acao('Neamt', 87)] },

    { 'estado': 'Neamt',
      'acoes': [acao('Iasi', 87)] }
]

distancias = {
            'Arad': 366,
            'Bucharest': 0,
            'Craiova': 160,
            'Drobeta': 242,
            'Eforie': 161,
            'Fagaras': 176,
            'Giurgiu': 77,
            'Hirsova': 151,
            'Iasi': 226,
            'Lugoj': 244,
            'Mehadia': 241,
            'Neamt': 234,
            'Oradea': 380,
            'Pitesti': 100,
            'Rimnicu Vilcea': 193,
            'Sibiu': 253,
            'Timisoara': 329,
            'Urziceni': 80,
            'Vaslui': 199,
            'Zerind': 374
        }

class No:
    def __init__(self, estado, custo, pai, acao):
        self.estado = estado
        self.custo = custo
        self.pai = pai
        self.acao = acao
        self.f_avaliacao = custo + distancias[estado]

    def __lt__(self, other):
        return self.f_avaliacao < other.f_avaliacao
    
    def __str__(self):
        return f'({self.estado}, custo = {self.custo}, f = {self.f_avaliacao})'
    
    def __repr__(self):
        return self.__str__()
    
    def filhos(self, problema):
        espaco_acoes = next(e for e in problema.espaco_estados if e['estado'] == self.estado)

        resultado = []
        for acao in espaco_acoes['acoes']:
            filho = No(acao['destino'], acao['custo'], self, acao['destino'])
            resultado.append(filho)

        return resultado
    
    def constroi_solucao(self):
        no_atual = self
        solucao = [no_atual]
        while no_atual.pai is not None:
            no_atual = no_atual.pai
            solucao.insert(0, no_atual)

        return solucao

class Problema:
    def __init__(self, espaco_estados, inicial, objetivo):
        self.espaco_estados = espaco_estados
        self.inicial = inicial
        self.objetivo = objetivo

class BuscaAStar:
    def __init__(self, problema):
        self.problema = problema
        self.explorados = [problema.inicial.estado]
        self.solucao = []
        self.fronteira = []
        hp.heappush(self.fronteira, problema.inicial)
        
        self.situacao = BUSCA_INICIANDO

    def executar(self):
        while self.situacao != BUSCA_FALHOU and self.situacao != BUSCA_SUCESSO:
            self.passo_busca()

        if self.situacao == BUSCA_FALHOU:
            print("Busca falhou")
        elif self.situacao == BUSCA_SUCESSO:
            print("Busca teve sucesso")
            print(f"Solucao: {self.solucao}")

        return
    
    def passo_busca(self):
        if (self.situacao == BUSCA_FALHOU):
            print("Busca falhou")
            return
        
        if (self.situacao == BUSCA_SUCESSO):
            print("Busca chegou ao objetivo com sucesso")
            return

        try:
            no = hp.heappop(self.fronteira)
        except IndexError:
            self.situacao = BUSCA_FALHOU
            return

        if self.problema.objetivo(no):
            self.situacao = BUSCA_SUCESSO
            self.solucao = no.constroi_solucao()
            return

        for filho in no.filhos(self.problema):
            if filho.estado not in self.explorados:
                hp.heappush(self.fronteira, filho)
                self.explorados.append(filho.estado)

        return