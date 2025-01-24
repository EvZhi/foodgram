# Описание проекта

**Фудграмм** — это веб-приложение, которое позволяет пользователям публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Используемые технологии

- Python  
- Django  
- Django REST Framework  
- Postgres  
- Docker  
- Nginx  
- Gunicorn  
- GitHub Actions



## API ресурсы

### Пользователи:
- `GET /api/users/` — Получить список пользователей  
- `POST /api/users/` — Зарегистрировать нового пользователя  
- `GET /api/users/{id}/` — Посмотреть профиль пользователя  
- `GET /api/users/me/` — Получить информацию о текущем пользователе  
- `POST /api/users/set_password/` — Сменить пароль

### Основные сущности (пример):
#### Теги:
- `GET /api/tags/` — Список всех тегов  
- `GET /api/tags/{id}/` — Получить информацию о теге

#### Рецепты:
- `GET /api/items/` — Получить список записей  
- `POST /api/items/` — Создать новую запись  
- `GET /api/items/{id}/` — Посмотреть запись  
- `PATCH /api/items/{id}/` — Обновить запись  
- `DELETE /api/items/{id}/` — Удалить запись

#### Избранное:
- `POST /api/items/{id}/favorite/` — Добавить запись в избранное  
- `DELETE /api/items/{id}/favorite/` — Убрать запись из избранного

#### Подписки:
- `GET /api/users/subscriptions/` — Список подписок пользователя  
- `POST /api/users/{id}/subscribe/` — Подписаться на автора  
- `DELETE /api/users/{id}/subscribe/` — Отписаться от автора

## Примеры работы с API

### Регистрация пользователя:
**Доступ**: Для всех  
**POST** `http://127.0.0.1:8000/api/users/`
```json
{
    "email": "email@email.ru",
    "username": "username",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "password": "password"
}
```

### Получение токена:
**Доступ**: Для всех  
**POST** `http://127.0.0.1:8000/api/auth/token/login/`
```json
{
    "email": "email@email.ru",
    "password": "password"
}
```

### Список пользователей:
**Доступ**: Для всех  
**GET** `http://127.0.0.1:8000/api/users/`

## Как установить и запустить проект

### Склонировать репозиторий
```bash
git clone https://github.com/username/projectname.git
```

### Настроить переменные окружения

Создайте файл `.env` в корневой папке и добавьте следующее:
```env
POSTGRES_DB=project_db
POSTGRES_USER=project_user
POSTGRES_PASSWORD=project_password
DB_HOST=db
DB_PORT=5432
```

### Запустить приложение через Docker
Перейдите в папку `infra/` и выполните команду:
```bash
docker-compose up -d --build
```

### Как зайти в приложение
После запуска оно будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

