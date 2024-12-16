"""
Representa a classe Tarefa, que encapsula dados e lógica básica de uma tarefa.
"""
from datetime import datetime

class Tarefa:
    """
    Classe básica para armazenar informações de uma tarefa no sistema.
    """
    def __init__(self, id, nome, email, telefone, morada, prioridade, descricao, data_criacao=None, escalonada=False):
        # ID pode ser informado ou, se vazio, será gerado automaticamente (ex: "1/2024").
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.morada = morada
        # prioridade: 1 (Alta), 2 (Média) ou 3 (Baixa)
        self.prioridade = prioridade
        self.descricao = descricao
        self.data_criacao = data_criacao if data_criacao else datetime.now()
        self.escalonada = escalonada
        # lista de anexos pode ser carregada do DB; aqui apenas guardamos em memória se necessário
        self.anexos = []

    def __str__(self):
        return f"{self.id} - {self.nome}"
