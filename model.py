import sqlite3

class TorneioModel:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS torneios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                premiacao TEXT NOT NULL,
                num_participantes INTEGER NOT NULL
            )
            """)
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS participantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                torneio_id INTEGER,
                nome TEXT NOT NULL,
                FOREIGN KEY (torneio_id) REFERENCES torneios (id)
            )
            """)
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS confrontos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                torneio_id INTEGER,
                participante1 TEXT,
                participante2 TEXT,
                fase TEXT,
                FOREIGN KEY (torneio_id) REFERENCES torneios (id)
            )
            """)

    def criar_torneio(self, nome, premiacao, num_participantes):
        with self.connection:
            cursor = self.connection.execute("""
            INSERT INTO torneios (nome, premiacao, num_participantes)
            VALUES (?, ?, ?)
            """, (nome, premiacao, num_participantes))
            return cursor.lastrowid

    def adicionar_participante(self, torneio_id, nome):
        with self.connection:
            self.connection.execute("""
            INSERT INTO participantes (torneio_id, nome)
            VALUES (?, ?)
            """, (torneio_id, nome))

    def obter_participantes(self, torneio_id):
        cursor = self.connection.execute("""
        SELECT nome FROM participantes
        WHERE torneio_id = ?
        """, (torneio_id,))
        return [row[0] for row in cursor.fetchall()]


    def criar_confronto(self, torneio_id, participante1, participante2, fase):
        with self.connection:
            cursor = self.connection.execute("""
            INSERT INTO confrontos (torneio_id, participante1, participante2, fase)
            VALUES (?, ?, ?, ?)
            """, (torneio_id, participante1, participante2, fase))
            return cursor.lastrowid

    def obter_confronto_id_por_fase(self, torneio_id, fase, posicao):
        cursor = self.connection.execute("""
        SELECT id FROM confrontos
        WHERE torneio_id = ? AND fase = ?
        """, (torneio_id, fase))
   
    def atualizar_confronto(self, confronto_id, vencedor):
        with self.connection:
            self.connection.execute("""
            UPDATE confrontos
            SET vencedor = ?
            WHERE id = ?
            """, (vencedor, confronto_id))

    
       
