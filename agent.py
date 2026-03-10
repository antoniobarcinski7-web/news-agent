import os
import anthropic
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
TELEGRAM_BOT_TOKEN = "".join(os.getenv("TELEGRAM_BOT_TOKEN", "").split())
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def fetch_economy_news() -> list[dict]:
    """Busca notícias de economia via NewsAPI."""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "business",
        "language": "pt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    articles = response.json().get("articles", [])

    # Fallback para inglês se não houver notícias em português
    if not articles:
        params["language"] = "en"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])

    return articles


def summarize_news(articles: list[dict]) -> str:
    """Usa Claude para resumir e formatar as notícias."""
    if not articles:
        return "Nenhuma notícia encontrada hoje."

    news_text = ""
    for i, article in enumerate(articles, 1):
        title = article.get("title", "Sem título")
        description = article.get("description") or ""
        source = article.get("source", {}).get("name", "Desconhecido")
        url = article.get("url", "")
        news_text += f"{i}. [{source}] {title}\n{description}\nLink: {url}\n\n"

    message = claude.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Você é um assistente especializado em economia. "
                    "Abaixo estão as principais notícias de economia do dia. "
                    "Resuma-as de forma clara e objetiva em português brasileiro, "
                    "destacando os pontos mais relevantes de cada uma. "
                    "Formate a resposta para Telegram usando emojis e markdown simples. "
                    "No final, adicione um breve comentário sobre o cenário econômico geral.\n\n"
                    f"Notícias:\n{news_text}"
                ),
            }
        ],
    )

    return message.content[0].text


def send_telegram_message(text: str) -> None:
    """Envia mensagem via Telegram Bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    today = datetime.now().strftime("%d/%m/%Y")
    full_message = f"📰 *Notícias de Economia — {today}*\n\n{text}"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": full_message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    print(f"[{datetime.now()}] Mensagem enviada com sucesso!")


def main() -> None:
    print(f"[{datetime.now()}] Iniciando agente de notícias...")
    articles = fetch_economy_news()
    summary = summarize_news(articles)
    send_telegram_message(summary)


if __name__ == "__main__":
    main()
