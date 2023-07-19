## Проект Foodgram:
![Foodgram workflow](https://github.com/nvkey/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Cайт Foodgram - «Продуктовый помощник». Позволяет делиться своими рецептами с другиии пользователями и автоматически составлять список покупок для вашего банкета.

#### Основной функционал:

* Рецепты
  * Просмотр
  * Добавление/удаление/редактирвоание
* Теги
  * Фильтрация рецептов по тэгам
* Ингредиенты
  * Добавление ингредиентов в рецепты
* Список избранного
  * Спиcок избранных рецептов
* Список покупок
  * Список рецертов для покупки ингредиентов
  * Загрузка списка рецептов и всех ингредиентов для покупки в формате .pdf
* Подписки
  * Подписки на других пользователей и просмотр их рецептов
#### Техническое описание проекта
Для работы приложения используется docker compose с разделением на четыре контейнера:
1. db - с базой данных PostgreSQL;
2. backend - с внутренними процессами сайта, Django;
3. frontend - с внещшшними процессами сайта; React;
4. nginx - c Nginx.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
``` bash
git clone git@github.com:nvkey/foodgram-project-react.git
cd foodgram-project-react
```
## Запуск проекта(используется Docker):

Для запуска проекта требуется создать файл .env в папке /infra/ со следующими ключами:
```bash
SECRET_KEY=<ваш_django_секретный_ключ>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Вы можете сгенерировать `DJANGO_SECRET_KEY` следующим образом. Из директории проекта /backend/ выполнить:

```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```
Полученный ключ скопировать в .env


Запуск docker-compose:
``` bash
cd infra
docker compose up -d --build 
```

Выполнить миграции, дата-миграции и сформировать статику:
``` bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --no-input 
```
Проект доступен по адресу:
http://localhost/


Тестовые пользователи:
``` bash
Тестовый гость сайта
email: test@test.ru
pwd: asdasd123!
log: test

Суперпользователь
log: admin
pwd: admin
email: admin@admin.ru

```

При необходимости создайте свою учетную запись администратора:
``` bash
docker compose exec web python manage.py createsuperuser
```

Спецификация взаимодействия frontend и backend контейнеров в формате Redoc, доступна по адресу:
http://localhost/api/docs/

Панель администратора доступна по адресу
http://localhost/admin


Рабочая версия проекта в ближайшее время будет доступна по адресу:
http://nvkey.ddns.net/
http://nvkey.ddns.net/admin/

Остановка docker-compose:
``` bash
docker-compose down -v 
```

### Автор
- [nvkey](https://github.com/nvkey) рад знакомству
