from model import TorneioModel

class TorneioController:
    def __init__(self, db_path):
        # Inicializa o controlador com o caminho do banco de dados
        self.model = TorneioModel(db_path)  # Instancia o modelo com o caminho do bd
        self.torneios = {}  # Armazena informações dos torneios criados
        self.confrontos = {}  
        self.participantes = {}  

    def criar_torneio(self, nome, premiacao, num_participantes):
        # Cria um novo torneio no banco de dados através do model
        torneio_id = self.model.criar_torneio(nome, premiacao, num_participantes)
        # Armazena o torneio criado no dicionário self.torneios
        self.torneios[torneio_id] = {
            "nome": nome,  
            "premiacao": premiacao,  
            "num_participantes": num_participantes,  
        }
        # Inicializa a lista de participantes do torneio
        self.participantes[torneio_id] = []
        return torneio_id

    def adicionar_participante(self, torneio_id, nome):
        # Adiciona participante ao torneio no banco de dados
        self.model.adicionar_participante(torneio_id, nome)
        # Adiciona o nome do participante à lista local de participantes do torneio
        self.participantes[torneio_id].append(nome)

    def obter_participantes(self, torneio_id):
        # Obtém a lista de participantes do torneio a partir do banco de dados
        return self.model.obter_participantes(torneio_id)

    def obter_confronto_id_por_fase(self, torneio_id, fase, posicao):
        return self.model.obter_confronto_id_por_fase(torneio_id, fase, posicao)

    def atualizar_vencedor(self, torneio_id, confronto_id, vencedor):
        # Atualiza o vencedor de um confronto no banco de dados
        self.model.atualizar_confronto(confronto_id, vencedor)

        # Verifica a fase do confronto e atualiza o vencedor nas fases subsequentes
        fase, posicao = self.obter_fase_e_posicao_confronto(confronto_id)
        if fase == "quartas":
            # Atualiza o vencedor para a fase de semifinais
            self.confrontos[torneio_id]["semis"][posicao // 2] = vencedor
        elif fase == "semis":
            # Atualiza o vencedor para a fase final
            self.confrontos[torneio_id]["final"] = vencedor
        elif fase == "final":
            # Armazena o vencedor final do torneio
            self.confrontos[torneio_id]["vencedor"] = vencedor

    def gerar_confrontos(self, torneio_id):
        # Obtém a lista dos participantes do torneio
        participantes = self.obter_participantes(torneio_id)

        # Gera os confrontos com base no número de participantes
        if len(participantes) == 2:
            self.criar_final(torneio_id, participantes)  # Cria apenas a final
        elif len(participantes) == 4:
            self.criar_semifinais(torneio_id, participantes)  # Cria semifinais para 4 participntes
        elif len(participantes) == 8:
            self.criar_quartas_finais(torneio_id, participantes)  # Cria quartas de final para 8 participantrs

    def criar_final(self, torneio_id, participantes):
        # Cria um confronto entre os dois participantes na fase "Final"
        self.model.criar_confronto(torneio_id, participantes[0], participantes[1], "Final")

    def criar_semifinais(self, torneio_id, participantes):
        # Verifica se há participantes suficientes para as semifinais
        if len(participantes) < 4:
            raise ValueError("Número insuficiente de participantes para as semifinais.")

        # Cria confrontos de semifinais, com dois participantes em cada confronto
        for i in range(0, len(participantes), 2):
            self.model.criar_confronto(torneio_id, participantes[i], participantes[i + 1], "semifinal")

    def criar_quartas_finais(self, torneio_id, participantes):
        # Verifica se há participantes suficientes para as quartas de final
        if len(participantes) < 8:
            raise ValueError("Número insuficiente de participantes para as quartas de final.")

        # Cria confrontos de quartas de final, com dois participantes em cada confronto
        for i in range(0, len(participantes), 2):
            self.model.criar_confronto(torneio_id, participantes[i], participantes[i + 1], "quartas")
