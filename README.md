# Проект API YaMDB
___

### Команда разработки

1 [Первый разработчик Сайид-Арби Сайид-Ибрахими](https://github.com/ingarbi)

Пишет всю часть, касающуюся управления пользователями:
- систему регистрации и аутентификации,
- права доступа,
- работу с токеном,
- систему подтверждения через e-mail.

2 [Второй разработчик Александр Ильиных](https://github.com/oeseo)

Пишет модели, view и эндпойнты для
- произведений,
- категорий,
- жанров; реализует импорта данных из csv файлов.

3 [Третий разработчик Михаил Мартынов](https://github.com/Mike198SPB)

Работает над
- отзывами,
- комментариями,
- рейтингом произведений.
___
### Описание проекта.
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в
YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр из списка предустановленных. Добавлять
произведения, категории и жанры может только администратор. Пользователи могут
оставлять комментарии к отзывам. Добавлять отзывы, комментарии и ставить оценки 
могут только аутентифицированные пользователи.
___
### Установка.
1 Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/ingarbi/api_yamdb.git
```
2 Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
* Для Linux/macOS
    ```
    source venv/bin/activate
    ```
* Для windows
    ```
    source venv/scripts/activate
    ```
3 Установить зависимости из файла `requirements.txt`:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4 Выполнить миграции:
```
python manage.py migrate
```
5 Запустить проект:
```
python manage.py runserver
```
___
### Примеры запросов.
####  Регистрация пользователя
```
POST /api/v1/auth/signup/
{
  "email": "string",
  "username": "string"
}
```
####  Получение JWT-токена:
```
POST /api/v1/auth/token/
{
  "username": "string",
  "confirmation_code": "string"
}
```
####  Добавление категории:
```
POST /api/v1/categories/
{
  "name": "string",
  "slug": "string"
}
```
####  Удаление категории:
```
DELETE /api/v1/categories/{slug}/
```
####  Добавление произведения:
```
POST /api/v1/titles/
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

#### Полная документация по эндпоинту /redoc/
___
### Использованные технологии.
- Asgiref
- Atomicwrites
- Attrs
- Certifi
- Charset Normalizer
- Colorama
- Django
- Django Filter
- Django Rest Framework
- Django Rest Framework Simplejwt
- Idna
- Iniconfig
- Packaging
- Pluggy
- Py
- PyJWT
- Pytest
- Pytest Django
- Pytest Pythonpath
- Pytz
- Requests
- Sqlparse
- Toml
- Urllib3
___
### Разработчики Python:

- [Сайид-Арби Сайид-Ибрахими,](https://github.com/ingarbi)
- [Александр Ильиных,](https://github.com/oeseo)
- [Михаил Мартынов.](https://github.com/Mike198SPB)
___
### Ссылка проекта [YaMDB](https://github.com/ingarbi/api_yamdb)