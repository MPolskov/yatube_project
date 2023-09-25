# Проект YaTube
### Описание
Учебный проект по Django.

Социальная сеть блогеров.
Пользователь может опубликовать запись дневника (редактировать, удалять), а также подписываться на других авторов.
Записи сортируются по дате публикации, по 10 записей на странице. Можно вывести записи авторов на которых пользователь подписан.

### Технологии
* Python 3.9
* Django 2.2
* django-debug-toolbar 2.2
* HTML и CSS
* Bootstrap

## Установка и запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:MPolskov/yatube_project.git
```
```
cd yatube_project
```
Cоздать и активировать виртуальное окружение:
```
# для Windows:
py -3.9 -m venv venv
# для Linux:
python3.9 -m venv venv
```
```
# для Windows:
source venv/Scripts/activate
# для Linux:
sourse venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить сервер:
```
python manage.py runserver 0.0.0.0:8000
```
### Автор
Полшков Михаил
