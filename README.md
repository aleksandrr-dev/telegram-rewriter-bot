# 🌍 StyleRewriter AI — Telegram Bot

A powerful bilingual Telegram bot that translates and rewrites text using a locally hosted LLM. Features an extensive language library spanning modern, ancient, liturgical, and constructed languages — with an intuitive inline keyboard interface in both English and Russian.

## Features

- **Three modes:**
  - 🌍 **Translate** — pure translation to any target language
  - ✏️ **Rewrite** — rewrite text in a chosen style without changing language
  - 🔄 **Translate + Rewrite** — translate AND rewrite in a chosen style simultaneously

- **40 supported languages** including:
  - Modern: English, Russian, Spanish, French, German, Italian, Portuguese, Dutch, Polish, Japanese, Chinese, Korean, Arabic, Turkish, Swedish, Norwegian, Danish, Finnish, Belarusian, Czech, Hindi, Persian, Vietnamese, Thai
  - Ancient & Classical: Latin, Ancient Greek, Koine Greek, Biblical Hebrew, Aramaic, Sanskrit, Sumerian, Proto-Indo-European, Old Norse, Old English, Old Russian, Church Slavonic, Scythian, Ossetian
  - Constructed: Elvish (Sindarin)

- **5 writing styles:** Formal, Casual, Funny, Aggressive, Poetic
- **Bilingual interface** — all menus and buttons in English and Russian
- **Fully private** — powered by a local LLM, no data sent to external servers
- **Paginated language selection** — clean navigation through all 40 languages

## Requirements

- Python 3.8+
- [LM Studio](https://lmstudio.ai) running locally on `http://localhost:1234`
- A Telegram bot token from [@BotFather](https://t.me/botfather)

## Installation

1. Clone the repository:

git clone https://github.com/aleksandrr-dev/telegram-rewriter-bot.git
cd telegram-rewriter-bot

2. Install dependencies:

pip install -r requirements.txt

3. Create a `config.py` file in the project folder and add your Telegram bot token:
```python
BOT_TOKEN = "your-token-here"
```
Get your token from [@BotFather](https://t.me/botfather) on Telegram.

4. Start LM Studio and enable the local server in the Developer tab

5. Run the bot:

python bot.py

## Usage

1. Open Telegram and start a chat with your bot
2. Send `/start` to see the main menu
3. Choose a mode — Translate, Rewrite, or Translate + Rewrite
4. Select your target language and style
5. Send your text and receive the result instantly

## Roadmap

- 📷 **Image OCR Translation** — extract and translate text from images using Tesseract
- 🎤 **Voice message transcription and translation**
- 📄 **Document translation support**

## Tech Stack

- [python-telegram-bot](https://python-telegram-bot.org/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- Local LLM via [LM Studio](https://lmstudio.ai)

## License

MIT License
