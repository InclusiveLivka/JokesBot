# JokesBot

## Информация (INFO)

- Версия python: `3.11.4`
- Версия пакетов в файле `requirements.txt`

## Настройка (Setting)

Далее нужно `.env.example` скопировать и переименовать в `.env` и заполнить значениями:

```bash
BOT_TOKEN=YOUR_BOT_TOKEN # Токен Telegram бота
```

## Запуск бота

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```
