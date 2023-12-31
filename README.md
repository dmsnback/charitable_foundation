[](#Начало)

# Приложение QRKot 

- [Описание](#Описание)
- [Технологии](#Технологии)
- [Запуск](#Запуск)
- [Автор](#Автор)


## Описание

__QRKot__ - приложение для Благотворительного фонда поддержки котиков.

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Проекты

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

### Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

### Пользователи

Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.


#

### Технологии

![Static Badge](https://img.shields.io/badge/python-gray?style=for-the-badge&logo=Python&link=https%3A%2F%2Fwww.python.org)
![Static Badge](https://img.shields.io/badge/FastAPI-gray?style=for-the-badge&logo=fastapi&link=https%3A%2F%2Ffastapi.tiangolo.com)
![Static Badge](https://img.shields.io/badge/FastAPI-users-gray?style=for-the-badge&logo=fastapi&link=https%3A%2F%2Ffastapi.tiangolo.com)
![Static Badge](https://img.shields.io/badge/SQLAlchemy-gray?style=for-the-badge&logo=alchemy&link=https%3A%2F%2Fwww.sqlalchemy.org)
![Static Badge](https://img.shields.io/badge/Pydantic-gray?style=for-the-badge&logo=pydantic&link=https%3A%2F%2Fdocs.pydantic.dev%2Flatest%2F)
![Static Badge](https://img.shields.io/badge/aioGoogle-gray?style=for-the-badge&logo=google&link=https%3A%2F%2Faiogoogle.readthedocs.io%2Fen%2Flatest%2F)


### Запуск

- __Склонируйте репозиторий__

```python
git clone git@github.com:dmsnback/cat_charity_fund.git
```
- __Перейдите в директорию с проектом__ 
```python
cd cat_charity_fund
```

- __Установите и активируйте виртуальное окружение__
```python
python3 -m venv venv
```
Для ```Windows```
```python
source venv/Scripts/activate
```
Для ```Mac/Linux```
```python
source venv/bin/activate
```
- __Установите зависимости из файла__ ```requirements.txt```

```python
python3 -m pip install --upgrade pip
```
```python
pip install -r requirements.txt
```

- __В корневой директории создайте файл__ ```.env```
```python
APP_TITLE=Кошачий благотворительный фонд (0.1.0)
APP_DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=YOU_SHALL_NOT_PASS!
FIRST_SUPERUSER_EMAIL=superuser@mail.com
FIRST_SUPERUSER_PASSWORD=superpassword
```
- __Для реализации отчёта в Google-таблице о проектах по скорости закрытия__

    - Создать сервисный аккаунт на платформе 
    [Google Cloud Platform](https://console.cloud.google.com/projectselector2/home/dashboard),
    получить JSON-файл с информацией о своем сервисном аккаунте

    - Дополнить ```.env``` файл

```python
EMAIL=Почта основного аккаунта Google
TYPE=Тип аккаунта
PROJECT_ID=ID проекта
PRIVATE_KEY_ID=ID приватного ключа
PRIVATE_KEY=Приватный ключ
CLIENT_EMAIL=Почта клиентского аккаунта
CLIENT_ID=ID клиентского аккаунта
AUTH_URI=Эндпоинт аутентификации
TOKEN_URI=Эндпоинт токена
AUTH_PROVIDER_X509_CERT_URL=Эндпоинт аутентификации сертификата
CLIENT_X509_CERT_URL=Эндпоинт сертификата
```

- __Выполните миграции__
```python
alembic upgrade head
```
- __Запустите приложение__
```python
uvicorn app.main:app --reload
```
#
После запуска проект будет доступен по адресу: 

- [http://127.0.0.1:8000](http://127.0.0.1:8000)

Документация к API досупна по адресам:

- ___Swagger:___ [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ___Redoc:___ [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)



#


### Автор

- [Титенков Дмитрий](https://github.com/dmsnback)

[Вернуться в начало](#Начало)
