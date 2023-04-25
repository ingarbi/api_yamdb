# Проект «api_yamdb»
___
# Установка.
1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:oeseo/api_yamdb.git
```

2. Cоздать и активировать виртуальное окружение:
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
3. Установить зависимости из файла `requirements.txt`:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Выполнить миграции:
```
python manage.py migrate
```
5. Запустить проект:
```
python manage.py runserver
```
___

```python
# Разработчик Python: Александр Ильиных
```
