from datetime import datetime

class Tarefa:
    def __init__(self, id, nome, email, telefone, morada, prioridade, descricao, data_criacao=None, escalonada=False):
        if not id:
            raise ValueError("O campo 'id' é obrigatório.")
        if not nome:
            raise ValueError("O campo 'nome' é obrigatório.")
        if prioridade not in [1, 2, 3]:
            raise ValueError("A prioridade deve ser 1 (Alta), 2 (Média) ou 3 (Baixa).")

        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.morada = morada
        self.prioridade = prioridade
        self.descricao = descricao
        self.data_criacao = data_criacao if data_criacao else datetime.now()
        self.escalonada = escalonada

    def __str__(self):
        status = "Escalonada" if self.escalonada else "Não Escalonada"
        return (f"ID: {self.id}\n"
                f"Nome: {self.nome}\n"
                f"Email: {self.email}\n"
                f"Telefone: {self.telefone}\n"
                f"Morada: {self.morada}\n"
                f"Prioridade: {self.prioridade}\n"
                f"Descrição: {self.descricao}\n"
                f"Data de Criação: {self.data_criacao.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Status: {status}")
