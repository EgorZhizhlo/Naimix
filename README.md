# Для запуска проекта необходимо создать .env файл в корне проекта вида:
    DB_HOST=хост(т.к мы используем базу данных внутри контейнера, то хост должен соответствовать контейнеру базы данных)
    DB_PORT=порт
    DB_USER=имя пользователя
    DB_PASSWORD=пароль пользователя
    DB_NAME=название базы данных
    SECRET_KEY=JWT ключ
    ALGORITHM=Алгоритм кодирования HS256
## Пример .env файла:
    DB_HOST=postgres
    DB_PORT=5432
    DB_USER=admin
    DB_PASSWORD=adminadmin
    DB_NAME=dbadmin
    SECRET_KEY=eyJhbQgKGlCI6IkpXVCJ9
    ALGORITHM=HS256

### Развертка:
    git clone https://github.com/EgorZhizhlo/Naimix.git
    cd Naimix
    docker-compose up --build
    docker-compose exec web alembic upgrade head
    docker-compose exec web alembic revision --autogenerate -m "Create migrations"
    docker-compose exec web alembic upgrade head
