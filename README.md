# Mad project

## Technical requirements
1) Необходим api endpoint с jwt авторизацией (с проверкой поля isDoctor == true) в теле самого jwt-токена
JWT-токены необходимо подписывать с помощью секретного ключа (алгоритм HS256)
2) Данный API Endpoint должен вернуть список пациентов (3 штуки)
3) Данные пациента должны содержать 4 поля 
{
    id,
    date_of_birth (Дата рождения пациента),
    diagnoses (массив строк с названиями диагнозов),
    created_at (дата создания записи)
}
4) Код должен быть снабжён комментариями и README с инструкц
иями по поднятию сервера и отправке запросов
5) Код должен быть запушен в git-репозиторий (github, gitlab, bitbucket - любой на выбор). Желательно с коммитами по ходу написания кода

### Pre requirements
* python^3.9
* poetry
* postgresql

### Install requirements
* `poetry install`


### Run migrations
* `python manage.py migrate`

### Runserver
* `python manage.py runserver`

### Run tests
* `pytest`

## Environment variables
| Name | Default | Description |
|------|---------|-------------|
| DJANGO_DEBUG | 1 | 1 - debug <br>0 - for production |
| DJANGO_SECRET_KEY | debug-secret-key | Project secret key, that will be used for generating user passwords, authentication tokens and etc.|
| DJANGO_ALLOWED_HOSTS | * | Hosts allowed to access the server. Many hosts should be separated by comma. `*` - allow from all hosts. |
| DJANGO_DATABASE_URL | | Required. Postgres database url. Example: `DJANGO_DATABASE_URL=postgres://db_user:db_password@localhost:5432/db_name`.|
