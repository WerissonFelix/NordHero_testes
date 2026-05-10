import sqlite3
import os

project_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(project_path, "Banco.db")

connection  = sqlite3.connect(db_path)

#Curso é tipo uma ponte que manda uma ação pro banco, tipo isso
cursor = connection.cursor()
connection.execute("PRAGMA foreign_keys = ON")

def table_user():
    """
    Cria a tabela 'user' no banco de dados.
    
    Cria a estrutura da tabela com colunas para identificação,
    nome, email (único) e senha. 
    """
    query = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(255) NOT NULL,
            email varchar(255) NOT NULL UNIQUE,
            password varchar(255) NOT NULL
        )
    """

    cursor.execute(query)
    connection.commit()

    print("Table user created successfully")

def table_songs():
    """
    Cria a tabela de músicas do jogo.

    Armazena dados globais da música:
    - título
    - artista
    - bpm
    - duração

    Essas informações não mudam entre dificuldades.
    """
    query = """
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            title varchar(255) NOT NULL,
            artist varchar(255) NOT NULL,
            
            bpm FLOAT NOT NULL,
            duration_seconds INTEGER NOT NULL
        )  
    """
    
    cursor.execute(query)
    connection.commit()

def table_difficulties():
    """
    Cria a tabela de dificuldades.

    Define os níveis disponíveis no jogo:
    - Easy
    - Normal
    - Hard
    """

    
    query = """
        CREATE TABLE IF NOT EXISTS difficulties(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(255) not null
        )
    """
    
    cursor.execute(query)
    connection.commit()

def table_song_charts():
    """
    Cria a tabela de charts das músicas.

    Um chart representa:
    - uma música
    - em uma dificuldade específica

    Armazena dados relacionados ao gameplay:
    - score máximo possível
    - quantidade de notas
    """
    
    query = """
        CREATE TABLE IF NOT EXISTS song_charts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            song_id INTEGER NOT NULL,
            difficulty_id INTEGER NOT NULL,
            
            max_possible_score INTEGER NOT NULL,
            notes_count INTEGER NOT NULL,
            
            FOREIGN KEY(song_id) REFERENCES songs(id),
            FOREIGN KEY(difficulty_id) REFERENCES difficulties(id)
            
            UNIQUE(song_id, difficulty_id)
        )
    """
    
    cursor.execute(query)
    connection.commit()


def table_socores():
    """
    Cria a tabela de scores dos jogadores.

    Registra o histórico de partidas:
    - jogador
    - chart jogado
    - pontuação
    - accuracy
    - rank/classificação

    Essa tabela é usada para:
    - ranking global
    - histórico individual
    - estatísticas do jogador
    """
    
    query = """
        CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            user_id INTEGER NOT NULL,
            chart_id INTEGER NOT NULL,
            
            score INTEGER NOT NULL,
            accuracy FLOAT NOT NULL,
            rank varchar(10) NOT NULL,
            
            FOREIGN KEY(chart_id) REFERENCES song_charts(id),
            FOREIGN KEY(user_id) REFERENCES user(id)     
        )
    """
    
    cursor.execute(query)
    connection.commit()
    
table_user()
table_songs()
table_difficulties()
table_song_charts()
table_socores()