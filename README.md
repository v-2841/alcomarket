# alcomarket
Интернет-магазин алкогольной продукции.

Пользователи могут зарегистрироваться, сделать заказ, посмотреть заказы в личном кабинете, восстановить пароль по токену из email. Имеется форма обратной связи.

Кастомизирована администраторская зона, важные события пересылаются в сообщении telegram.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/v-2841/alcomarket.git
```

```
cd alcomarket
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Иницализация
Создать суперпользователя:
```
python manage.py createsuperuser
```
Создать файл .env с переменными среды по примеру .env.example.

В администраторской зоне создать карточки товаров.

## Стек технологий:
- Python
- Django
- Postgresql
- Redis
- Celery
- HTML
- Bootstrap 5
- CSS
- Python-telegram-bot
- Poetry