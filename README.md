
# HeadHunter Vacancy Project
## Description
Проект создан для получения актуальных вакансий  избранных компаний, полученных через API HeadHunter.

## Structure
Проект состоит из пакета src 
-basic_class содержит базовыйй класс "APIBasic" взаимодействие с API
и базовый класс "BasicManager"  взаимодействия с БД
-api_connect содержит класс HHAPIClient клиент для взаимодействия с API hh.ru,
проверяет доступность компаний по ID, собирает вакансии
-DBManager содержит класс DBManager реализующий методы предоставления, необходимой информации из БД
-рализованы функции по созданию БД сохранению данных в БД

В main.py реализована функция взаимодействия с пользователем.

## Stack

- [Python 3.12]
- [ООП]
- [Poetry]
- [Pytest]
- [JSON]
- [SQL]
- [Postgres]
- [Flake8]
- [Isort]
- [Black]

## install 

1. Клонируйте репозиторий:
```
git clone https://github.com/aleksospishev/sky_sql_course.git
```

2. Установите зависимости:
```
poetry install
```
3. Запуск:
```
python main.py
```