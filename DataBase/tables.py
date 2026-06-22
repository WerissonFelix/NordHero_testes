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
            telefone varchar(255) NOT NULL,
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
            type varchar(255) NOT NULL,
            
            bpm FLOAT NOT NULL,
            duration_seconds INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            
            story_difficulty_id INTEGER NOT NULL,
            
            FOREIGN KEY(story_difficulty_id) REFERENCES difficulties(id)
        )  
    """
    
    cursor.execute(query)
    connection.commit()

def table_multiplayer_songs():
    """ 
    Cria a tabela de músicas para o modo multiplayer.
    
    Armazena dados específicos para o modo multiplayer:
    - título
    - caminho do arquivo
    - referência para as músicas instrumental e vocal usadas no modo multiplayer
    - referência para a dificuldade usada no modo multiplayer
    """  
    query = """
        CREATE TABLE IF NOT EXISTS multiplayer_songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            title varchar(255) NOT NULL,
            
            instrumental_song INTEGER NOT NULL,
            vocal_song INTEGER NOT NULL,
            
            bpm FLOAT NOT NULL,
            duration_seconds INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            
            story_difficulty_id INTEGER NOT NULL,
            
            foreign KEY(story_difficulty_id) REFERENCES difficulties(id),    
            foreign KEY(instrumental_song) REFERENCES songs(id),
            foreign KEY(vocal_song) REFERENCES songs(id)
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
            notes_hit_id INTEGER NOT NULL,
            
            score INTEGER NOT NULL,
            accuracy FLOAT NOT NULL,
            rank varchar(10) NOT NULL,
            
            FOREIGN KEY(chart_id) REFERENCES song_charts(id),
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(notes_hit_id) REFERENCES notes_hit(id) 
        )
    """
    
    cursor.execute(query)
    connection.commit()

def notes_hit():
    query = """
        CREATE TABLE IF NOT EXISTS notes_hit(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chart_id INTEGER NOT NULL,
             
             
            qtd_miss INTEGER NOT NULL,
            qtd_bad INTEGER NOT NULL,
            qtd_good INTEGER NOT NULL,
            qtd_perfect INTEGER NOT NULL,
            
            FOREIGN KEY(chart_id) REFERENCES song_charts(id),
            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """

    cursor.execute(query)
    connection.commit()

def table_achievements():
    query = """
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key VARCHAR(100) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            icon VARCHAR(10) NOT NULL
        )
    """
    
    cursor.execute(query)
    connection.commit()
  
def table_user_achievements():
    query = """
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_id INTEGER NOT NULL,
            unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(achievement_id) REFERENCES achievements(id),
            UNIQUE(user_id, achievement_id)
        )
    """
    cursor.execute(query)
    connection.commit()

ACHIEVEMENTS_CATALOG = [
    ("first_note",    "Primeira Nota",       "Complete sua primeira partida.",                         "🎵"),
    ("5_songs",       "Aquecendo",           "Jogue 5 partidas no total.",                             "🔥"),
    ("20_songs",      "Dedicação",           "Jogue 20 partidas no total.",                            "🎮"),
    ("50_songs",      "Veterano",            "Jogue 50 partidas no total.",                            "🏅"),
    ("first_s",       "Nota Máxima",         "Obtenha rank S em qualquer música.",                     "⭐"),
    ("first_a",       "Quase Perfeito",      "Obtenha rank A ou melhor em qualquer música.",           "🌟"),
    ("3_s_ranks",     "Imbatível",           "Obtenha rank S em 3 músicas diferentes.",                "🏆"),
    ("perfect_game",  "Perfeição",           "Termine uma música sem nenhum Miss.",                    "💎"),
    ("100_perfects",  "Precisão Cirúrgica",  "Acumule 100 notas Perfect no total.",                    "🎯"),
    ("500_perfects",  "Mãos de Ouro",        "Acumule 500 notas Perfect no total.",                    "🥇"),
    ("100_notes",     "Em Ritmo",            "Acumule 100 notas acertadas (Good+Perfect) no total.",   "🎶"),
    ("first_hard",    "Corajoso",            "Complete uma música na dificuldade Hard.",                "💀"),
    ("beat_hard",     "Dominou o Hard",      "Obtenha rank B ou melhor em uma música Hard.",           "⚔️"),
    ("play_all",      "Colecionador",        "Jogue pelo menos uma vez cada música disponível.",        "📀"),
    ("2players",      "Parceria",            "Complete uma partida no modo 2 Players.",                 "🤝"),
]

def seed_achievements():
    for key, name, desc, icon in ACHIEVEMENTS_CATALOG:
        cursor.execute(
            "INSERT OR IGNORE INTO achievements (key, name, description, icon) VALUES (?, ?, ?, ?)",
            (key, name, desc, icon)
        )
    connection.commit()
     
table_user()
table_songs()
table_difficulties()
table_song_charts()
table_socores()
table_multiplayer_songs()
notes_hit()
table_achievements()
table_user_achievements()
seed_achievements()