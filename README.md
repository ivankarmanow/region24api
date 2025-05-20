# Region 24 API

## Скачивание и установка зависимостей

```shell
git clone git@github.com:ivankarmanow/region24api.git
cd region24api
python3 -m venv .venv
source .venv/bin/Activate.ps1
pip install -r requirements.txt
```

## Настройка

Все настройки из файла .env.example нужно перенести в .env, заменяя на реальные данные.
Далее запустить миграции

```shell
alembic upgrade head
```

## Запуск

```shell
uvicorn app.app:app
```