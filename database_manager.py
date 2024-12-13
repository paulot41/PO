import sqlite3
from datetime import datetime
from tarefa import Tarefa

class DatabaseManager:
    def __init__(self, db_path='tarefas.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.criar_tabelas()

    def criar_tabelas(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT,
                telefone TEXT,
                morada TEXT,
                prioridade INTEGER,
                descricao TEXT,
                data_criacao TEXT,
                escalonada INTEGER
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS anexos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarefa_id TEXT NOT NULL,
                caminho TEXT NOT NULL,
                FOREIGN KEY(tarefa_id) REFERENCES tarefas(id)
            )
            """)

    def criar_tarefa(self, tarefa):
        with self.conn:
            self.conn.execute("""
            INSERT INTO tarefas (id, nome, email, telefone, morada, prioridade, descricao, data_criacao, escalonada)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tarefa.id,
                tarefa.nome,
                tarefa.email,
                tarefa.telefone,
                tarefa.morada,
                tarefa.prioridade,
                tarefa.descricao,
                tarefa.data_criacao.isoformat(),
                1 if tarefa.escalonada else 0
            ))

    def remover_tarefa(self, id_tarefa):
        with self.conn:
            cur = self.conn.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
            return cur.rowcount > 0

    def procurar_tarefa(self, id_tarefa):
        cur = self.conn.execute("SELECT * FROM tarefas WHERE id = ?", (id_tarefa,))
        row = cur.fetchone()
        if row is None:
            return None
        tarefa = Tarefa(
            id=row['id'],
            nome=row['nome'],
            email=row['email'],
            telefone=row['telefone'],
            morada=row['morada'],
            prioridade=row['prioridade'],
            descricao=row['descricao'],
            data_criacao=datetime.fromisoformat(row['data_criacao']),
            escalonada=(row['escalonada'] == 1)
        )
        return tarefa

    def listar_tarefas(self, criterio='prioridade'):
        if criterio == 'tempo':
            order = "data_criacao ASC"
        else:
            order = "prioridade ASC"
        cur = self.conn.execute(f"SELECT * FROM tarefas ORDER BY {order}")
        rows = cur.fetchall()
        tarefas = []
        for row in rows:
            tarefa = Tarefa(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                telefone=row['telefone'],
                morada=row['morada'],
                prioridade=row['prioridade'],
                descricao=row['descricao'],
                data_criacao=datetime.fromisoformat(row['data_criacao']),
                escalonada=(row['escalonada'] == 1)
            )
            tarefas.append(tarefa)
        return tarefas

    def atualizar_tarefa(self, tarefa):
        with self.conn:
            cur = self.conn.execute("""
            UPDATE tarefas SET 
                nome=?,
                email=?,
                telefone=?,
                morada=?,
                prioridade=?,
                descricao=?,
                data_criacao=?,
                escalonada=?
            WHERE id=?
            """, (
                tarefa.nome,
                tarefa.email,
                tarefa.telefone,
                tarefa.morada,
                tarefa.prioridade,
                tarefa.descricao,
                tarefa.data_criacao.isoformat(),
                1 if tarefa.escalonada else 0,
                tarefa.id
            ))
            return cur.rowcount > 0

    def close(self):
        self.conn.close()
