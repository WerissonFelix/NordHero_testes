# 🎵 NORD HERO

**NORD HERO** é um jogo de ritmo desenvolvido em **Python** com **Pygame** e **pygame-menu**.  

Consiste em valorar a cultura nordestina por meio do contato entre jogo e música de forma lúdica.

É possível escolher a música de acordo com o nível de dificuldade desejada, permitindo a customização do estilo da partida.

O objetivo do jogo é acertar as notas no tempo correto utilizando as teclas indicadas na tela, acumulando pontos conforme a precisão do jogador.
---
## 🌐 Links Importantes
# Planilha
```Text
https://docs.google.com/spreadsheets/d/1T2XSy7NpLsRkdkxux9JnRgOK-wjYF0P2s0cBXR7m5Qc/edit?usp=sharing
```
# Drive
```Text
https://drive.google.com/drive/folders/1rl5iMOgW-th0i1TBMqgVqCrCdI3Dv5LT?usp=sharing
```
## 🚀 Release 1.0

| Funcionalidade | Descrição |
|---------------|----------|
| Sistema de Usuário | Cadastro, login, validação de dados e persistência em banco SQLite. |
| Interface Completa | Telas de navegação (login, cadastro, home, menus e jogo). |
| Escolha de Dificuldade | Seleção entre níveis de dificuldade (Easy, Normal, Hard). |
| Escolha de Música | Seleção da música para iniciar a partida. |
| Sistema de Jogo | Execução da partida com notas, lanes e input do jogador. |
| Sistema de Pontuação | Cálculo de pontos com base na precisão dos acertos. |
| Sistema de Pausa | Permite pausar e retomar o jogo. |
| Resumo Final | Exibe estatísticas da partida ao final. |

---

## 🚀 Release 2.0

| Funcionalidade | Descrição |
|---------------|----------|
| Configuração de Controles | Permitir ao usuário personalizar as teclas do jogo. |
| Classificação por Instrumento | Organizar músicas com base no instrumento principal. |
| Classificação por Tipo | Separar músicas entre instrumental e vocal. |
| Expansão de Controles | Adicionar mais teclas em níveis de dificuldade mais altos. |
| Ranking "Global" | Criar ranking entre jogadores para cada música. |
| Envio de email| Código de verificação para atualizar senha. |

---

## 🚀 Release 3.0

| Funcionalidade | Descrição |
|---------------|----------|
| A definir | Funcionalidades futuras ainda não especificadas. |
## 🕹️ Sobre o Projeto

O **NORD HERO** funciona como um jogo musical em que o usuário escolhe uma dificuldade, seleciona uma música e joga acompanhando as notas que aparecem na tela.

Durante a partida, o jogador precisa pressionar as teclas corretas no momento certo.  
A pontuação é calculada com base na precisão do acerto, podendo receber avaliações como:

- **Perfect**
- **Good**
- **Bad**
- **Miss**

Ao final da música, o sistema exibe um resumo da partida com quantidade total de notas, notas acertadas, porcentagem de acerto e ranking final.

---

## 🚀 Funcionalidades

## 👤 Sistema de Usuário

O sistema de usuário permite gerenciar contas com validação de dados e persistência em banco SQLite.

| Funcionalidade | Descrição |
|---------------|----------|
| Cadastro | Permite criar uma nova conta com nome, e-mail e senha. |
| Login | Autentica o usuário com base nas credenciais cadastradas. |
| Validação de Nome | Garante que o nome tenha tamanho adequado e contenha apenas letras. |
| Validação de Email | Verifica formato válido e evita duplicidade no banco. |
| Validação de Senha | Exige critérios como tamanho mínimo, número e símbolo. |
| Atualização de Perfil | Permite alterar nome, e-mail e senha do usuário. |
| Exclusão de Conta | Remove permanentemente o usuário do banco de dados. |
| Persistência | Armazena os dados utilizando SQLite (`Banco.db`). |

---

## 🎮 Sistema de Jogo

Responsável por toda a lógica da partida, incluindo notas, pontuação e interação do jogador.

| Funcionalidade | Descrição |
|---------------|----------|
| Escolha de Dificuldade | Define o nível do jogo (Easy, Normal, Hard). |
| Escolha de Música | Permite selecionar a música da partida. |
| Sistema de Notas | Gera e movimenta notas sincronizadas com a música. |
| Sistema de Lanes | Organiza as colunas onde as notas aparecem. |
| Input do Jogador | Captura teclas pressionadas para acerto das notas. |
| Sistema de Pontuação | Calcula pontos com base na precisão (Perfect, Good, Bad, Miss). |
| Feedback Visual | Exibe o resultado do acerto em tempo real. |
| Sistema de Pausa | Permite pausar e retomar a partida. |
| Resumo Final | Mostra estatísticas da partida ao final. |

---

## 🧠 Como o Jogo Funciona

O fluxo principal do jogo segue esta ordem:

```text
main.py
   ↓
Tela inicial
   ↓
Login ou criação de conta
   ↓
Home do usuário
   ↓
Escolha da dificuldade
   ↓
Escolha da música
   ↓
Carregamento da partida
   ↓
Contagem regressiva
   ↓
Jogo em execução
   ↓
Resumo final
```

## 🧩 Principais Pastas

## 📁 Estrutura do Projeto

O código está organizado para facilitar a manutenção e escalabilidade:

| Diretório/Arquivo | Descrição |
|------------------|----------|
| `main.py` | Ponto de entrada que inicializa a aplicação e abre a tela inicial. |
| `DataBase/` | Contém a lógica de banco de dados (criação de tabelas, inserts, selects, updates e deletes). |
| `Features/` | Responsável pelas validações de dados (nome, e-mail e senha). |
| `Game/` | Contém toda a lógica principal do jogo (configuração, gerenciamento da partida, notas, lanes e textos). |
| `Screens/` | Contém as telas da aplicação (login, cadastro, home, jogo, pausa, resumo, etc). |
| `Images/` | Armazena as imagens utilizadas nas interfaces do jogo. |
| `Banco.db` | Arquivo do banco de dados SQLite com as informações dos usuários. |

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| **Python** | Linguagem principal do projeto |
| **Pygame** | Criação da janela, eventos, jogo e renderização |
| **pygame-menu** | Criação dos menus e telas |
| **SQLite** | Banco de dados local |
| **email-validator** | Validação de emails |
| **password-validator** | Validação de regras da senha |



## 📦 Dependências do Projeto

As bibliotecas abaixo são utilizadas para o funcionamento do sistema:

| Dependência | Descrição |
|------------|----------|
| `pygame` | Responsável pela criação da janela, renderização gráfica e gerenciamento de eventos do jogo. |
| `pygame-menu` | Utilizado para criação das interfaces, menus e navegação entre telas. |
| `email-validator` | Realiza a validação de formato e consistência de e-mails. |
| `password-validator` | Aplica regras de segurança para validação de senhas. |
| `sqlite3` | Biblioteca padrão do Python para manipulação do banco de dados SQLite. |


## 🖥️ Como Instalar e Executar

Siga os passos abaixo para rodar o projeto localmente.

### 📥 1. Clonar o repositório

```bash
git clone https://github.com/WerissonFelix/NordHero_testes.git
cd NordHero_testes
```
## 🐍 Ambiente Virtual (venv)

Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto.

### Criar o ambiente virtual

```bash
python -m venv .venv
```

### Ativar o ambiente virtual

## windows
```bash
.venv\Scripts\activate
```

## Linux/Mac

```bash
source .venv/bin/activate
```
## 📦 Instalação das Dependências

Para instalar todas as dependências do projeto, utilize o terminal com o ambiente virtual ativado.

### 🔧 Instalação direta

```bash
python -m pip install -r requirements.txt
```

## 👨‍💻 Desenvolvedores

Este projeto foi desenvolvido por:

| Nome | Função |
|------|--------|
| **Werisson Félix** | Desenvolvimento geral, lógica do jogo e integração dos sistemas |
| **Cauã Araujo** | Interface, telas e experiência do usuário |
