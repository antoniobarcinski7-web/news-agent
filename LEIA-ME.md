# Agente de Notícias de Economia — Telegram

Este agente busca notícias de economia todo dia às 08:00, resume com inteligência artificial e envia direto no seu Telegram.

Ele roda **gratuitamente na nuvem** usando o GitHub Actions — sem precisar deixar o computador ligado.

---

## Passo 1 — Obter as chaves necessárias

Antes de qualquer coisa, você precisa de 4 chaves. Veja como obter cada uma:

### 🔑 NEWS_API_KEY
1. Acesse https://newsapi.org
2. Clique em "Get API Key" e crie uma conta gratuita
3. Após o cadastro, sua chave aparece no painel

### 🔑 ANTHROPIC_API_KEY
1. Acesse https://console.anthropic.com
2. Faça login ou crie uma conta
3. Vá em "API Keys" no menu lateral e clique em "Create Key"

### 🔑 TELEGRAM_BOT_TOKEN
1. Abra o Telegram e pesquise por `@BotFather`
2. Envie o comando `/newbot`
3. Escolha um nome e um username para o seu bot
4. O BotFather vai te enviar um token parecido com: `123456789:AAFxxxxxxxxxxxxxxxx`

> Após criar o bot, envie qualquer mensagem para ele no Telegram. Isso é obrigatório para ele conseguir te enviar mensagens.

### 🔑 TELEGRAM_CHAT_ID
1. Abra o Telegram e pesquise por `@userinfobot`
2. Envie qualquer mensagem para ele
3. Ele vai responder com seu Chat ID (um número como `987654321`)

---

## Passo 2 — Criar repositório no GitHub

1. Acesse https://github.com e crie uma conta se ainda não tiver
2. Clique em **"New repository"**
3. Dê um nome (ex: `news-agent`) e clique em **"Create repository"**
4. Faça upload de todos os arquivos desta pasta para o repositório

---

## Passo 3 — Adicionar as chaves no GitHub (Secrets)

As chaves não ficam no código — ficam protegidas no GitHub como "Secrets".

1. No seu repositório, clique em **Settings**
2. No menu lateral, clique em **Secrets and variables → Actions**
3. Clique em **"New repository secret"** e adicione cada uma das 4 chaves:

| Nome do Secret | Valor |
|---|---|
| `NEWS_API_KEY` | Sua chave da NewsAPI |
| `ANTHROPIC_API_KEY` | Sua chave da Anthropic |
| `TELEGRAM_BOT_TOKEN` | Token do seu bot no Telegram |
| `TELEGRAM_CHAT_ID` | Seu Chat ID do Telegram |

---

## Passo 4 — Testar manualmente

Antes de aguardar o horário automático, teste para ver se está tudo funcionando:

1. No seu repositório, clique em **Actions**
2. Clique em **"Agente de Notícias de Economia"** no menu lateral
3. Clique em **"Run workflow"** → **"Run workflow"**
4. Aguarde alguns segundos e verifique se a mensagem chegou no seu Telegram

---

## Como funciona na nuvem

O GitHub Actions executa o agente automaticamente todo dia às **08:00 (horário de Brasília)**, de graça, sem precisar do seu computador ligado.

O arquivo `.github/workflows/news-agent.yml` é quem define esse agendamento.

---

## Estrutura dos arquivos

```
news-agent/
├── .github/
│   └── workflows/
│       └── news-agent.yml  ← agendamento na nuvem (GitHub Actions)
├── agent.py                ← código principal do agente
├── requirements.txt        ← dependências do projeto
├── .env.example            ← modelo de variáveis (só para uso local)
└── LEIA-ME.md              ← este guia
```

---

## Dúvidas frequentes

**Posso mudar o horário de envio?**
Sim. No arquivo `.github/workflows/news-agent.yml`, altere a linha:
```
- cron: "0 11 * * *"
```
O formato é `minuto hora * * *` em UTC. Brasília é UTC-3, então some 3 horas ao horário desejado. Ex: para 09:00 BRT use `0 12 * * *`.

**O GitHub Actions é realmente gratuito?**
Sim. Repositórios públicos têm uso ilimitado. Repositórios privados têm 2.000 minutos gratuitos por mês — mais do que suficiente para este agente.

**Preciso do terminal para rodar na nuvem?**
Não. Depois de configurar o GitHub, tudo roda automaticamente. O terminal só seria necessário para testes locais.
