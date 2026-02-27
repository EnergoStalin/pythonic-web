# Дефолтная конфигурация

### Важное для запуска

| Переменная окружения | Дефолтное значение       | Описание                                                                                                         |
| -------------------- | ------------------------ | -------------------------------------------------------------------------                                        |
| ENVIRONMENT          | development              | Включает/выключает плюшки для дебаггинга                                                                         |
| PORT                 | 8080                     | Порт ingress                                                                                                     |
| DOMAIN               | 127.0.0.1                | Домен ingress                                                                                                    |
| BASE_URL             | http://${DOMAIN}:${PORT} | URL на котором работает бэкэнд (может быть полезно для запуска вне докера)                                       |
| WWW_URL              | http://${DOMAIN}:${PORT} | URL на котором работает фронтенд (для CORS)                                                                      |
| UID                  | 1000                     | Хотелось бы конечно что бы и для api сработало но не в текущем дистрибьюшене поэтому только User id для postgres |
| GID                  | 1000                     | Аналогично только Group id                                                                                       |

Остальную конфигурацию можно найти в `config.py` файлах раскиданных по `src`.

# Запуск

```sh
docker compose up -d
```

<details>
<summary>С `pgadmin` (без предефайненного соединения)</summary>

```sh
COMPOSE_PROFILES=debug docker compose up -d
```

| Переменная окружения | Дефолтное значение       |
| -------------------- | ------------------------ |
| PGADMIN_PORT         | 8081                     |

</details>

<details>
<summary>Полный debug пакет c OpenAPI эндпоинтом. (без remote debugging конечно же)</summary>

```sh
ENVIRONMENT=development COMPOSE_PROFILES=debug docker compose up -d
```

</details>

## Ссылки

> С учётом дефолтного `$PORT`

[WWW](http://127.0.0.1:8080)

<details>
<summary><a href="http://127.0.0.1:8080/docs">OpenAPI</a></summary>

Включено только при `ENVIRONMENT == development`

```sh
ENVIRONMENT=development docker compose up -d
```

</details>

<details>
<summary><a href="http://127.0.0.1:8081">PGAdmin</a></summary>

Включено только при `debug in COMPOSE_PROFILES`

```sh
COMPOSE_PROFILES=debug docker compose up -d
```

</details>

# Пару слов про фреймворки

## FastAPI

Много чего хорошего про него слышал + видел пару проектиков на нём. По опыту использования архитектура мне понравилась очень удобный Dependency Injection да и OpenAPI эндпонт из коробки. Посталю минус только за отсутвие интеграции с базами данных.

## ORM

### Tortoise

Не заработал в lifecycle FastAPI но по доке самый удобный. Потратил ощутимое количество времени перед тем как забить и перейти на следующую пару.

### SQLAlchemy & SQLModel

Говорить что FastAPI не имеет интеграций с БД было очень неосторожно. Собственно финальный вариант сошёлся на его SQLModel который чуть чуть поприятнее голой SQLAlchemy хоть и не выглядит как совсем высокооуровневая абстракция из за чего пришлось самому реализовывать необходимые операции([db/operations](https://github.com/EnergoStalin/pythonic-web/tree/master/services/api/src/api/db/operations)). Дефайнить поля голым SQLAlchemy невыносимо.

# Пару слов про архитектуру

Каждый роутер в приложении так и напрашивается на вынесение в микросервис на что я изначально и ориентировался. Но как оказалось без инфраструктуры поддержки и настроенного релизного цикла вспомогательных библиотек пытаться в адекватную DRY сборку только докером не целесообразно из за чего я в последствии отказался от этого решения. Наследием данного решения является теперь уже излишний [jwks](http://127.0.0.1:8080/.well-known/jwks.json) эндпоинт.

## Авторизация

Поскольку я не успел описать всё в OpenAPI схеме придётся выписать старым добрым текстом. Описывает только идею стоящую за эндпоинтом.

- POST /auth login&password - получаешь `access_token` в `Set-Cookie` вместе с `refresh_token` + `expire_at` + `access_token` в теле запроса.
- POST /auth/refresh - кормишь валидный(присутсвует в базе + не истёк) `refresh_token` получаешь новый `access_token`
- POST /auth/validate - валидирует сигнатуру токенов публичным ключом
- GET /auth/config - возвращает конфиг для валидации полей ввода

## Storage

На данный момен самый стабильный можно даже на [фронте](http://127.0.0.1:8080/media.html) потыкать.

Я бы может и сам реализовал обработку `multipart/form-data` но время... время...

- POST /storage/files - загрузка одного/нескольких файлов через `multipart/form-data`
- GET /storage/files/{name} - возвращает файл с именем `name`
- GET /storage/files - возвращает список файлов `name, mime, url`
- GET /storage/config - возвращает конфиг принимаемых разрешений файлов

Для простоты авторизация в storage не используется хотя добавить её при надобности не должно составить проблем.

## User

- GET /user/me - получаешь свой [UserInfo](https://github.com/EnergoStalin/pythonic-web/blob/master/services/api/src/api/models/UserInfo.py)

Остальное WIP

Время потраченное на возвращение в общество [![wakatime](https://wakatime.com/badge/user/e95ece5f-54ed-4ef2-9ff3-b88a5a8bfc5c/project/4b474662-419f-43a5-bf21-d7191fda0e9f.svg)](https://wakatime.com/badge/user/e95ece5f-54ed-4ef2-9ff3-b88a5a8bfc5c/project/4b474662-419f-43a5-bf21-d7191fda0e9f)
