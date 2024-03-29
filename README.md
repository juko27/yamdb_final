![Did it :boom:](https://github.com/VivSRD/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект **YaMDb** собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

# Алгоритм регистрации пользователей

1. Пользователь отправляет запрос с параметром `email` на `/auth/email/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email` .
3. Пользователь отправляет запрос с параметрами `email` и `confirmation_code` на `/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на `/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

# Пользовательские роли

- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

- **Аутентифицированный пользователь** — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять **свои** отзывы и комментарии.

- **Модератор** — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.

- **Администратор** — полные права на управление проектом и всем его содержимым. Может создавать и удалять категории и произведения. Может назначать роли пользователям.

- **Администратор Django** — те же права, что и у роли **Администратор**.

## Техническое описание проекта YaMDb

К проекту по адресу http://127.0.0.1:8000/redoc/ подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.  

## Переменные окружения

Для подключения к базе данных необходимо заполнить файл .ENV значениями для:
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
