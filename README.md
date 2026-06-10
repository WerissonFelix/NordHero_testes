# 🎵 NORD HERO

**NORD HERO** é um jogo de ritmo desenvolvido em **Python** com **Pygame** e **pygame-menu**, criado para valorizar a cultura nordestina por meio da música de forma lúdica e interativa.

O jogador escolhe uma música de acordo com o nível de dificuldade desejado e deve pressionar as teclas corretas no tempo certo, acumulando pontos conforme a precisão dos acertos.

---

## 🌐 Links Importantes

**Artigo:**
```
https://pt.overleaf.com/read/tgztjgfnrstz#18f55a
```

**Planilha:**
```
https://docs.google.com/spreadsheets/d/1T2XSy7NpLsRkdkxux9JnRgOK-wjYF0P2s0cBXR7m5Qc/edit?usp=sharing
```

**Drive:**
```
https://drive.google.com/drive/folders/1rl5iMOgW-th0i1TBMqgVqCrCdI3Dv5LT?usp=sharing
```

---

## 🚀 Release 1.0

| Funcionalidade | Descrição |
|---|---|
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
|---|---|
| Configuração de Controles | Permite ao usuário personalizar as teclas do jogo. |
| Classificação por Tipo | Separa músicas entre instrumental e vocal. |
| Modo 2 Players | Extenção do single player para suportar duas pessoas. |
| Modo 2 Players - Versus | Jogadores jogam contra. |
| Modo 2 Players - Coop | Jogadores jogam juntos. |
| Notas Longas | Notas com mais de 1 segundo de duração e que suas ondas sonoras são prolongadas. |
| Notas Inimigas | Notas que roubam 300 pontos do oponente, caso ele as acerte |
| Notas Rainbow | Notas que que têm 1000 pontos extras, caso os jogadores as acerte |
| Ranking Global | Cria ranking entre jogadores para cada música. |
| Verificação por Email | Envio de código de verificação ao criar conta ou atualizar senha. |
| Verificação por SMS/WhatsApp | Inovação: o usuário escolhe se deseja receber o código por **Email** ou **WhatsApp** ao criar conta, via integração com a API da Twilio. |

---

## 🚀 Release 3.0

| Funcionalidade | Descrição |
|---|---|
| A definir | Funcionalidades futuras ainda não especificadas. |

## 🕹️ Como o Jogo Funciona

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

Durante a partida, o jogador pressiona as teclas corretas no momento em que as notas chegam à zona de acerto. A pontuação é calculada com base na precisão:

- **Perfect** — acerto no tempo exato
- **Good** — acerto com leve atraso
- **Bad** — acerto fora do tempo ideal
- **Miss** — nota não acertada

---

## 📁 Estrutura do Projeto

```
NordHero/
├── main.py                  # Ponto de entrada da aplicação
├── Banco.db                 # Banco de dados SQLite
├── requirements.txt         # Dependências do projeto
├── .env                     # Credenciais sensíveis (não versionar)
│
├── DataBase/
│   ├── inserts.py
│   ├── selects.py
│   ├── updates.py
│   ├── deletes.py
│   └── repositories/
│       └── user_repository.py
│
├── Features/
│   ├── Dados_Verificacao.py     # Coordena validação e fluxo de verificação
│   ├── EmailValidator.py
│   ├── PasswordValidate.py
│   ├── NameValidator.py
│   ├── TelefoneValidator.py
│   ├── SendEmail.py             # Envio de código por email (SMTP)
│   └── SendSms.py               # Envio de código por WhatsApp (Twilio)
│
├── Screens/
│   ├── Inital.py
│   ├── Creat_Account.py
│   ├── Choice_Verification.py   # Tela de escolha Email / WhatsApp
│   ├── Codigo_Email.py
│   ├── Home.py
│   ├── Data_error.py
│   ├── Atualizar_Senha.py
│   └── profile_options.py
│
├── Game/
│   └── (lógica da partida, notas, lanes, pontuação)
│
├── Images/
│   └── (assets visuais das telas)
│
└── models/
    └── user.py
```

---

## 🧠 Organização dos Módulos

**`Features/`** — Camada de regras de negócio e serviços externos. Concentra todas as validações de dados e integrações com APIs (email e WhatsApp). O módulo `Dados_Verificacao.py` age como orquestrador: recebe os dados do formulário, chama cada validador, decide o fluxo de verificação e chama a operação correta no banco.

**`Screens/`** — Camada de interface. Cada arquivo representa uma tela do sistema. As telas não contêm lógica de negócio — apenas capturam input do usuário e delegam ao módulo correto em `Features/`.

**`DataBase/`** — Camada de persistência. Separada em operações atômicas (insert, select, update, delete) e repositories que abstraem o acesso ao SQLite.

**`Game/`** — Lógica exclusiva da partida. Isolada das demais camadas para facilitar manutenção e expansão.

---

## 🛠️ Tecnologias e Bibliotecas

| Biblioteca | Finalidade | Justificativa |
|---|---|---|
| `pygame-ce` | Janela, renderização, eventos e lógica do jogo | Fork mantido da comunidade com correções de bugs e melhor suporte a versões modernas do Python |
| `pygame-menu-ce` | Criação de menus e telas de navegação | Permite construir interfaces funcionais sem implementar um sistema de UI do zero |
| `sqlite3` | Banco de dados local | Biblioteca padrão do Python; sem dependência externa, ideal para projetos desktop offline |
| `email-validator` | Validação de formato de email | Garante conformidade com o padrão RFC antes de persistir no banco |
| `password-validator` | Validação de regras de senha | Abstrai a lógica de regras (tamanho, números, símbolos) de forma declarativa |
| `phonenumbers` | Validação e parsing de números de telefone | Biblioteca do Google; suporta formatos internacionais e valida se o número é real para o país |
| `twilio` | Envio de mensagens via WhatsApp | API amplamente utilizada, com suporte a WhatsApp Business e sandbox para testes |
| `python-dotenv` | Carregamento de variáveis de ambiente | Mantém credenciais sensíveis fora do código-fonte, seguindo boas práticas de segurança |
| `smtplib` | Envio de email (stdlib) | Biblioteca padrão do Python para envio de emails via SMTP, sem dependência adicional |

---

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/WerissonFelix/NordHero_testes.git
cd NordHero_testes
```

### 2. Criar e ativar ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar

```bash
python main.py
```

---

## 👨‍💻 Desenvolvedores

| Nome | Função |
|---|---|
| **Werisson Félix** | Desenvolvimento geral, lógica do jogo e integração dos sistemas |
| **Cauã Araujo** | Interface, telas e experiência do usuário |
