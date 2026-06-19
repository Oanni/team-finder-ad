# CrewLink (TeamFinder, вариант 1)

Pet-платформа для поиска команды над side-проектами.  
Это моя персональная реализация учебного задания **TeamFinder**: я переработал архитектуру бэкенда под свой стиль, сохранив совместимость с HTML-шаблонами и моделями `User` / `Project`.

**Автор репозитория:** Алексей Ибетуллов (`ibetu`)  
**Стек:** Django 5.2 · PostgreSQL 16 · Docker · Pillow

---

## Что реализовано

### Базовый функционал
- регистрация и вход по email;
- каталог проектов с пагинацией (12 на страницу);
- профиль участника, редактирование визитки, смена пароля;
- создание / редактирование / завершение своих проектов;
- участие в чужих открытых проектах.

### Вариант 1 — избранное
- переключение избранного (`POST /projects/<id>/toggle-favorite/`);
- личная страница `/projects/favorites/`.

### Вариант 1 — фильтры участников
На `/users/list/` для авторизованных пользователей:
- авторы избранных проектов;
- авторы проектов, где я участник;
- кому нравятся мои проекты;
- участники моих проектов.

---

## Как устроен мой бэкенд

Реализовал логику по слоям:

| Слой | Назначение |
|------|------------|
| `users/views.py`, `projects/views.py` | тонкие HTTP-обработчики |
| `users/catalog.py`, `projects/queries.py` | выборки и фильтрация |
| `projects/actions.py` | JSON-действия (избранное, участие, закрытие) |
| `users/validators.py`, `users/portrait.py` | валидация и генерация аватаров |
| `team_finder/paging.py` | общая пагинация |


---

## Быстрый старт (Windows)

### 1. Окружение

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> **Python 3.14:** если `psycopg2-binary` не ставится, используйте  
> `pip install "psycopg[binary]"` — Django 5.2 работает с psycopg3.

### 2. Переменные окружения

```powershell
Copy-Item .env_example .env
```

Минимальный `.env`:

```env
DJANGO_SECRET_KEY=your-secret-here
DJANGO_DEBUG=True
POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TASK_VERSION=1
```

### 3. PostgreSQL в Docker

```powershell
docker compose up -d
```

Если образ `postgres:16` не скачивается, можно поднять Alpine-вариант:

```powershell
docker run -d --name teamfinder_db -p 5432:5432 --env-file .env `
  -v teamfinder_postgres_data:/var/lib/postgresql/data postgres:16-alpine
```

### 4. Миграции и запуск

```powershell
venv\Scripts\python manage.py migrate
venv\Scripts\python manage.py runserver
```

Приложение: [http://127.0.0.1:8000/projects/list/](http://127.0.0.1:8000/projects/list/)

---

## Демо-данные (создаются миграциями)

Пароль для всех демо-аккаунтов: **`crewlink2026`**

### Участники

| Email | Имя | Роль в демо |
|-------|-----|-------------|
| `ibetu@crewlink.dev` | Алексей Ибетуллов | Я |
| `sofia.m@crewlink.dev` | София Морозова | дизайн / фронт |
| `artyom.k@crewlink.dev` | Артём Климов | DevOps |
| `ops@crewlink.dev` | Команда Админ | суперпользователь |

### Проекты

| Название | Автор | Статус |
|----------|-------|--------|
| Проект 1 | Алексей Ибетуллов | открыт |
| Проект 2 | София Морозова | открыт |
| Проект 3 | Алексей Ибетуллов | закрыт |

Файлы сидов:
- `users/migrations/0004_seed_demo_members.py`
- `projects/migrations/0003_seed_demo_ventures.py`

---

## Сброс базы после смены миграций

Если переименовывали migration-файлы, нужен чистый прогон:

```powershell
docker stop teamfinder_db
docker rm teamfinder_db
docker volume rm teamfinder_postgres_data
docker run -d --name teamfinder_db -p 5432:5432 --env-file .env `
  -v teamfinder_postgres_data:/var/lib/postgresql/data postgres:16-alpine
venv\Scripts\python manage.py migrate
```

---

## Заметки для ревьюера

- Для проверки избранного и фильтров войдите под `ibetu@crewlink.dev`.
