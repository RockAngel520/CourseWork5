# Habits Tracker

Django-приложение для отслеживания привычек с использованием Celery и Redis.

## Технологии

- Django 5.2
- PostgreSQL 16
- Redis
- Celery
- Docker & Docker Compose

## Предварительные требования

- Docker
- Docker Compose
- Файл .env с переменными окружения

## Быстрый запуск

### 1. Создание файла .env. Пример есть в .env.example
Создайте файл `.env` в корне проекта:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=habits_db
DATABASE_USER=habits_user
DATABASE_PASSWORD=habits_password
DATABASE_HOST=db
DATABASE_PORT=5432
TG_API_KEY=your-telegram-bot-token
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 2. Запуск проекта
```
# Сборка и запуск всех сервисов
docker-compose up --build

# Или для запуска в фоновом режиме
docker-compose up -d --build
```

Приложение будет доступно по адресу: http://localhost:8000

## Проверка работоспособности сервисов
### Статус всех сервисов
```
docker-compose ps
```
Ожидаемый результат: Все сервисы в статусе Up или Up (healthy)

## Проверка Django (web)
```
# Доступность веб-сервера
curl -I http://localhost:8000

# Проверка здоровья Django
docker-compose exec web python manage.py check

# Проверка миграций
docker-compose exec web python manage.py showmigrations
```

## Проверка PostgreSQL (db)
```
# Подключение к БД
docker-compose exec db pg_isready -U habits_user -d habits_db

# Список баз данных
docker-compose exec db psql -U habits_user -d habits_db -c "\l"

# Список таблиц
docker-compose exec db psql -U habits_user -d habits_db -c "\dt"
```

## Проверка Redis
```
# Проверка подключения
docker-compose exec redis redis-cli ping

# Информация о Redis
docker-compose exec redis redis-cli info server
```

## Проверка Celery Worker
```
# Статус Celery
docker-compose exec celery celery -A config inspect ping

# Зарегистрированные задачи
docker-compose exec celery celery -A config inspect registered

# Статус воркеров
docker-compose exec celery celery -A config status
```

## Проверка Celery Beat
```
# Логи Beat
docker-compose logs celery_beat --tail=20
```

## Команды для управления
### Основные команды
```
# Запуск проекта
docker-compose up --build

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f
docker-compose logs -f web
docker-compose logs -f celery

# Пересборка
docker-compose build --no-cache
```

### Системные команды
```
# Статус контейнеров
docker-compose ps

# Остановка с удалением данных
docker-compose down -v

# Перезапуск сервиса
docker-compose restart web
```

## Структура сервисов
- web - Django приложение (порт 8000)
- db - PostgreSQL база данных (порт 5432)
- redis - Redis для кэша и Celery (порт 6379)
- celery - Celery worker для фоновых задач
- celery_beat - Celery beat для периодических задач