# Описание проекта
Проект «Todolist» представляет собой RESTful API, позволяющий пользователям создавать, просматривать, редактировать и удалять задачи. API предоставляет базовый функционал для управления списком дел, что делает его подходящим для использования в различных приложениях, от личных заметок до совместных проектов.
# Инструкция по использованию API
1. Клонирование репозитория:

`git clone https://github.com/palmistry911/to_do_list_project.git`

`cd to_do_list_project`

2. Создание виртуального окружения: (Рекомендуется)

`python -m venv venv`

`source venv/bin/activate` # Linux/macOS

`# venv\Scripts\activate ` # Windows

3. Установка зависимостей:

`pip install -r requirements.txt`

4. Запуск API:

`python app.py`

После запуска API будет доступен по адресу http://127.0.0.1:8000


# Описание эндпоинтов
## 1. `GET /tasks` - Получение списка всех задач

### Метод: GET

### Путь: `http://127.0.0.1:8000/tasks/`

### Описание:
Возвращает список всех задач в формате JSON.

### Запрос:
Никакие параметры не требуются.

### Ответ:
- Код состояния:  `200 OK`

- Тело: Список задачей в формате JSON.

### Пример запроса:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/tasks/' \
  -H 'accept: application/json' \
  -H 'X-CSRFTOKEN: de3euyQbXKDHMnz0e22Km52ntZvwvsOQLSZHAzYakCH3tZquiuk4oQFjaQwRWlSf'
```
### Пример ответа:
```
 [
  {
    "id": 1,
    "comments_count": 1,
    "comments": [
      {
        "task": 1,
        "comment": "Помыть рыбок два раза в день, тряпочкой"
      }
    ],
    "tags_count": 2,
    "tags": [
      {
        "name": "срочно"
      },
      {
        "name": "дом"
      }
    ],
    "name": "pomoite ribok!!!!!",
    "description": "pls",
    "status": "DRAFT",
    "due_data": "2025-01-06T15:37:31Z"
]

```
## 2. `GET /tasks/<int:task_id>`- Получение задачи по ID

### Метод: GET

### Путь: `[/users/{user_id}](http://127.0.0.1:8000/tasks/1/)`

### Описание:

 Возвращает задачу с указанным `task_id` в формате JSON.
 
### Параметры запроса:

- task_id (целое число): идентификатор задачи, которую нужно получить.
### Ответ:
-Код состояния:  `200 OK` если задача найденааа.

-Код состояния:  `404 Not Found` если задачи не существует.

-Тело: пользовательский объект в формате JSON

### Пример запроса:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/tasks/1/' \
  -H 'accept: application/json' \
  -H 'X-CSRFTOKEN: de3euyQbXKDHMnz0e22Km52ntZvwvsOQLSZHAzYakCH3tZquiuk4oQFjaQwRWlSf'
```
### Пример ответа:
```
{
  "id": 1,
  "comments_count": 1,
  "comments": [
    {
      "task": 1,
      "comment": "Помыть рыбок два раза в день, тряпочкой"
    }
  ],
  "tags_count": 2,
  "tags": [
    {
      "name": "срочно"
    },
    {
      "name": "дом"
    }
  ],
  "name": "pomoite ribok!!!!!",
  "description": "pls",
  "status": "DRAFT",
  "due_data": "2025-01-06T15:37:31Z"
}

```
##  3. `POST /tasks` - Создание новой задачи

### Метод: POST

### Путь: ` [/users/ ](http://127.0.0.1:8000/tasks/) `

### Описание:
Создание новой задачи.

### Тело запроса
1.`title`: (обязательный, `string`) Заголовок задачи.
2.`description`: (необязательный, `string`) Описание задачи.
3.`completed`: (необязательный, `boolean`, по умолчанию `false`) Статус выполнения задачи.

### Ответ:
Код состояния: ` 201 Created`

### Пример запроса:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: sloqgqNnVKqyBMapIoOvxBSn7bUpIvab0ZkTmrVmiCuUio1TMQ6PzmvjO2VK9oeA' \
  -d '{
  "name": "string",
  "description": "string",
  "status": "DRAFT",
  "due_data": "2025-01-13T16:22:46.520Z"
}'

```
### Пример ответа:
```
{
  "id": 3,
  "comments_count": 0,
  "comments": [],
  "tags_count": 0,
  "tags": [],
  "name": "string",
  "description": "string",
  "status": "DRAFT",
  "due_data": "2025-01-13T16:22:46.520000Z"
}
```
Response headers
```
allow: GET,POST,HEAD,OPTIONS 
 content-length: 163 
 content-type: application/json 
 cross-origin-opener-policy: same-origin 
 date: Mon,13 Jan 2025 16:22:49 GMT 
 referrer-policy: same-origin 
 server: WSGIServer/0.2 CPython/3.12.8 
 vary: Accept 
 x-content-type-options: nosniff 
 x-frame-options: DENY 
```

##  4. `PUT /tasks/<int:task_id>` - Обновление существующей задачи

### Метод: PUT

### Путь: ` [/users/{user_id}](http://127.0.0.1:8000/tasks/1/)`

### Описание:
Обновляет задачу с указанным `task_id`.

### Параметры:
1.`task_id`: (обязательный, `integer`) ID задачи, которую необходимо обновить.
2.(в теле запроса, JSON): любые параметры `title`, `description`, `completed` для обновления.

### Ответ:
- Код состояния: ` 200 OK` в случае успешного обновления задачи.
- Код состояния:  `404 Not Found` если задача не существует
- Тело: обновленная задача в формате JSON.

### Пример запроса:
```
curl -X 'PUT' \
  'http://127.0.0.1:8000/tasks/1/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: sloqgqNnVKqyBMapIoOvxBSn7bUpIvab0ZkTmrVmiCuUio1TMQ6PzmvjO2VK9oeA' \
  -d '{
  "name": "string",
  "description": "string",
  "status": "DRAFT",
  "due_data": "2025-01-13T16:26:20.585Z"
}'

```
### Пример ответа:
```
{
  "id": 1,
  "comments_count": 1,
  "comments": [
    {
      "task": 1,
      "comment": "Помыть рыбок два раза в день, тряпочкой"
    }
  ],
  "tags_count": 2,
  "tags": [
    {
      "name": "срочно"
    },
    {
      "name": "дом"
    }
  ],
  "name": "string",
  "description": "string",
  "status": "DRAFT",
  "due_data": "2025-01-13T16:26:20.585000Z"
}
```
##  5. `DELETE /tasks/<int:task_id>` - Удаление задачи

### Метод: DELETE

### Путь: ` [/users/{user_id}](http://127.0.0.1:8000/tasks/1/) `

### Описание:
Удаляет задачу с указанным `task_id`.

### Ответ:
-Код состояния:  `200 OK` в случае успешного удаления задачи.
-Код состояния:  `404 Not Found` если задачи не существует.
-Тело: Удаленная задача в формате JSON.

### Параметры запроса
`task_id`: (обязательный, `integer`) ID задачи, которую необходимо удалить.

### Пример запроса:
```
curl -X 'DELETE' \
  'http://127.0.0.1:8000/tasks/1/' \
  -H 'accept: application/json' \
  -H 'X-CSRFTOKEN: sloqgqNnVKqyBMapIoOvxBSn7bUpIvab0ZkTmrVmiCuUio1TMQ6PzmvjO2VK9oeA'

```
### Пример ответа:
```
 allow: GET,PUT,PATCH,DELETE,HEAD,OPTIONS 
 content-length: 0 
 cross-origin-opener-policy: same-origin 
 date: Mon,13 Jan 2025 16:30:06 GMT 
 referrer-policy: same-origin 
 server: WSGIServer/0.2 CPython/3.12.8 
 vary: Accept 
 x-content-type-options: nosniff 
 x-frame-options: DENY 

```

### Дополнительная информация
- Обработка ошибок: API возвращает соответствующие HTTP-коды ошибок, а также JSON-объект с описанием ошибки в случае некорректных данных или других проблем.
- База данных: по умолчанию используется база данных SQLite, файл tasks.db будет создан в корневой папке проекта.
- Тестирование: в проекте есть тесты, которые можно запустить с помощью команды pytest. Это поможет убедиться, что API работает корректно.
- Расширение API: API легко расширить, добавив новые конечные точки или функции.