# API для работы с товарами

## Запуск 
1. Добавить в .env следующе переменные окружения для работы с базой данных:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=admin # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

2. Убедитесь, что у вас
   установлен [Docker](https://www.docker.com/products/docker-desktop)
   и запустите проект командой:

```bash
docker-compose up 
```
## Доступные методы

| endpoint | Тип запроса | Описание |
| :--- | :--- | :--- | 
| api/v1/products/ | GET | Получение всех неудаленных товаров |
| api/v1/products/? | GET | Фильтрация товаров(доступные GET параметры: name, category_id, category, price_min, price_max, published)|
| api/v1/products/ | POST | Создание товара |
| api/v1/products/<product_id>/ | PUT/PATCH | Редактирование товара |
| api/v1/products/<product_id>/ | DELETE | Удаление товара |
| api/v1/categories/ | GET | Получение всех категорий |
| api/v1/categories/ | POST | Создание категории |
| api/v1/categories/<сategory_id>/ | PUT/PATCH | Редактирование категории |
| api/v1/categories/<сategory_id>/ | DELETE | Удаление категории |