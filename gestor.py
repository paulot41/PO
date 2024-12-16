"""
Lógica de negócio que interage com o DatabaseManager.
"""
from datetime import datetime
from database_manager import DatabaseManager
from tarefa import Tarefa

class GestorDeTarefas:
    """
    Classe intermédia que contém a lógica de negócio das tarefas,
    usando o DatabaseManager para persistência.
    """
    def __init__(self, db_manager=None):
        self.db_manager = db_manager if db_manager else DatabaseManager()

    def gerar_id_tarefa(self):
        """
        Gera automaticamente IDs no formato num/ano, ex: "1/2024".
        """
        ano_atual = datetime.now().year
        numero_atual = self.db_manager.get_numero_tarefas_ano(ano_atual)
        proximo_numero = numero_atual + 1
        return f"{proximo_numero}/{ano_atual}"

    def adicionar_tarefa(self, tarefa):
        """
        Se o ID estiver vazio, gera um novo. Em seguida, cria a tarefa na base de dados.
        """
        if not tarefa.id:
            tarefa.id = self.gerar_id_tarefa()
        self.db_manager.criar_tarefa(tarefa)

    def remover_tarefa(self, id_tarefa):
        return self.db_manager.remover_tarefa(id_tarefa)

    def procurar_tarefa(self, id_tarefa):
        return self.db_manager.procurar_tarefa(id_tarefa)

    def listar_tarefas(self, ordenacao='prioridade'):
        return self.db_manager.listar_tarefas(ordenacao)

    def pesquisar_tarefas(self, texto):
        """
        Pesquisa tarefas cujo 'nome' ou 'id' contenha 'texto'.
        """
        return self.db_manager.pesquisar_tarefas(texto)

    def atualizar_tarefa(self, tarefa):
        return self.db_manager.atualizar_tarefa(tarefa)

    def escalonar_tarefas(self):
        """
        Escalona tarefas com mais de 15 dias (prioridade=1, escalonada=True).
        Retorna True se escalonou alguma, False caso contrário.
        """
        tarefas = self.db_manager.listar_tarefas('tempo')
        alterado = False
        from datetime import datetime
        for tarefa in tarefas:
            dias = (datetime.now() - tarefa.data_criacao).days
            if dias > 15 and not tarefa.escalonada:
                tarefa.escalonada = True
                tarefa.prioridade = 1
                self.db_manager.atualizar_tarefa(tarefa)
                alterado = True
        return alterado

    def adicionar_anexo(self, tarefa_id, caminho):
        self.db_manager.adicionar_anexo(tarefa_id, caminho)

    def listar_anexos(self, tarefa_id):
        return self.db_manager.listar_anexos(tarefa_id)
