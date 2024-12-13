from datetime import datetime
from database_manager import DatabaseManager
from tarefa import Tarefa

class GestorDeTarefas:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager if db_manager else DatabaseManager()

    def adicionar_tarefa(self, tarefa):
        self.db_manager.criar_tarefa(tarefa)

    def remover_tarefa(self, id_tarefa):
        return self.db_manager.remover_tarefa(id_tarefa)

    def procurar_tarefa(self, id_tarefa):
        return self.db_manager.procurar_tarefa(id_tarefa)

    def listar_tarefas(self, ordenacao='prioridade'):
        return self.db_manager.listar_tarefas(ordenacao)

    def atualizar_tarefa(self, tarefa):
        return self.db_manager.atualizar_tarefa(tarefa)

    def escalonar_tarefas(self):
        tarefas = self.db_manager.listar_tarefas('tempo')
        alterado = False
        for tarefa in tarefas:
            dias = (datetime.now() - tarefa.data_criacao).days
            if dias > 15 and not tarefa.escalonada:
                tarefa.escalonada = True
                tarefa.prioridade = 1
                self.db_manager.atualizar_tarefa(tarefa)
                alterado = True
        return alterado
