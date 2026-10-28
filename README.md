# Маршруты Кавказского заповедника

Сайт с популярными пешими маршрутами Кавказского биосферного заповедника. На карточке маршрута есть описание, фото и карта: линия пути и точки стоянок с фотографиями.

Проект собран вместе с [Артуром Газизовым](https://github.com/artur8833). Исходная версия жила в форке `artur8833/Popular-routes`. Этот репозиторий — отдельная копия для доработки и портфолио: история коммитов сохранена, пометка «fork» убрана.

## Что есть на сайте

- главная страница с панорамами и списком маршрутов;
- страница маршрута с картой Folium;
- регистрация и вход;
- админка Flask-Admin для маршрутов, координат и фото;
- погода в Сочи, если указан ключ WorldWeatherOnline. Без ключа сайт открывается, в меню будет «Сервис погоды временно не доступен».

## Запуск на Windows

```bat
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
copy webapp\config.example.py webapp\config.py
set FLASK_APP=webapp
flask db upgrade
flask run
```

Сайт откроется на http://127.0.0.1:5000

На Linux и macOS те же шаги, только окружение активируется через `source env/bin/activate`, а конфиг копируется так: `cp webapp/config.example.py webapp/config.py`. Либо запустите `./run.sh` после `chmod +x run.sh`.

## Настройка

В `webapp/config.py`:

- `SQLALCHEMY_DATABASE_URI` — по умолчанию файл `db.sqlite3` в корне проекта;
- `WEATHER_API_KEY` — ключ с [worldweatheronline.com](https://www.worldweatheronline.com/);
- `SECRET_KEY` — любая длинная случайная строка.

Файл `webapp/config.py` не коммитится.

## Администратор

Маршруты добавляются в админке.

```bat
python create_admin.py
```

Скрипт спросит имя и пароль. После входа под этим пользователем в меню появится пункт «Админка» (`/admin`).

Координаты линии маршрута можно загрузить JSON-файлом GeoJSON на страницу `/load/<id>`, где `<id>` — номер маршрута.

## Стек

Python, Flask, SQLite, Flask-Login, Flask-Admin, Flask-Migrate, Folium.
