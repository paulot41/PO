"""
Gere a persistência de dados na base SQLite, incluindo Tarefas e Anexos.
"""
import sqlite3
from datetime import datetime
from tarefa import Tarefa
import os

class DatabaseManager:
    """
    Classe responsável por toda a comunicação com a base de dados SQLite.
    """
    def __init__(self, db_path='tarefas.db'):
        self.db_path = db_path
        # Estabelece a ligação com o ficheiro .db
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.criar_tabelas()

    def criar_tabelas(self):
        """
        Cria as tabelas 'tarefas' e 'anexos' caso ainda não existam.
        """
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
                caminho TEXT,
                data BLOB,
                FOREIGN KEY(tarefa_id) REFERENCES tarefas(id)
            )
            """)

    def criar_tarefa(self, tarefa):
        """
        Insere uma nova Tarefa na base de dados.
        """
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
        """
        Remove a tarefa identificada por 'id_tarefa', bem como seus anexos.
        Retorna True se a remoção foi bem-sucedida, False caso contrário.
        """
        with self.conn:
            self.conn.execute("DELETE FROM anexos WHERE tarefa_id = ?", (id_tarefa,))
            cur = self.conn.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
            return cur.rowcount > 0

    def procurar_tarefa(self, id_tarefa):
        """
        Obtém uma tarefa específica pelo seu ID, retornando um objeto Tarefa ou None se não existir.
        """
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
        tarefa.anexos = self.listar_anexos(tarefa.id)
        return tarefa

    def listar_tarefas(self, criterio='prioridade'):
        """
        Lista todas as tarefas na BD, ordenadas pelo critério especificado:
        'prioridade' ou 'tempo' (data_criacao ASC).
        """
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
            tarefa.anexos = self.listar_anexos(tarefa.id)
            tarefas.append(tarefa)
        return tarefas

    def pesquisar_tarefas(self, texto):
        """
        Pesquisa tarefas cujo nome ou ID contenha 'texto' (busca parcial).
        """
        pattern = f"%{texto}%"
        cur = self.conn.execute("""
        SELECT * FROM tarefas
        WHERE nome LIKE ? OR id LIKE ?
        ORDER BY data_criacao ASC
        """, (pattern, pattern))
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
            tarefa.anexos = self.listar_anexos(row['id'])
            tarefas.append(tarefa)
        return tarefas

    def atualizar_tarefa(self, tarefa):
        """
        Actualiza os dados de uma tarefa existente (nome, email, prioridade, etc.).
        """
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

    def adicionar_anexo(self, tarefa_id, caminho):
        """
        Lê um ficheiro do disco e guarda o conteúdo binário na base de dados,
        associando ao ID da tarefa.
        """
        with open(caminho, "rb") as f:
            data_bin = f.read()
        with self.conn:
            self.conn.execute("""
            INSERT INTO anexos (tarefa_id, caminho, data)
            VALUES (?, ?, ?)
            """, (tarefa_id, caminho, data_bin))

    def listar_anexos(self, tarefa_id):
        """
        Devolve uma lista de dicionários com 'id', 'caminho' e 'data' binária
        para cada anexo associado a tarefa_id.
        """
        cur = self.conn.execute("SELECT * FROM anexos WHERE tarefa_id = ?", (tarefa_id,))
        rows = cur.fetchall()
        anexos = []
        for row in rows:
            anexos.append({
                'id': row['id'],
                'caminho': row['caminho'],
                'data': row['data']
            })
        return anexos

    def remover_anexos_por_tarefa(self, tarefa_id):
        with self.conn:
            self.conn.execute("DELETE FROM anexos WHERE tarefa_id = ?", (tarefa_id,))

    def get_numero_tarefas_ano(self, ano):
        """
        Conta quantas tarefas foram criadas num determinado ano para gerar IDs seq/ano.
        """
        cur = self.conn.execute("SELECT COUNT(*) as c FROM tarefas WHERE strftime('%Y', data_criacao) = ?", (str(ano),))
        row = cur.fetchone()
        return row['c']

    def close(self):
        self.conn.close()
