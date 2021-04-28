# YaMDB
### Описание
Учебный проект Яндекс.Практикум. В проекте разализовано API для отзывов о
различных произведениях с их каталогизацией. Проект разворачивается в трех
Docker-контейнерах.

[![Actions Status](https://github.com/kuzminArtur/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/kuzminArtur/yamdb_final/actions)

## Запуск проекта
- Установить Docker согласно инструкции https://docs.docker.com/engine/install/
- Установить Docker-compose согласно инструкции https://docs.docker.com/compose/install/
- Клонировать репозиторий командой 
```bash
git clone https://github.com/kuzminArtur/infra_sp2.git
```
- В корне проекта выполнить
```bash
docker-compose up
```
- При первом запуске так же следует выполнить
```bash
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```
- Для наполнения базы данных начальными данными:
```bash
docker-compose exec web python manage.py loaddata fixtures.json
```
### Внимание! При загрузке тестовых данных суперпользователь будет изменен!
**Логин**: root@root.com\
**Пароль**: root

## Альтернативный вариант с использованием make
- Запуск проекта:
```bash
make up
```
- Выполнение миграций
```bash
make migrate
```
- Создание суперпользователя
```bash
make createsu
```
- Сбор статики
```bash
make collectstatic
```
- Загрузка тестовых данных
```bash
make fixture
```
- Остановка проекта
```bash
make down
```
- Пересборка образа
```bash
make build
```

Проект доступен по адресу http://daytedomen.tk/

### Автор
Студент Яндекс.Практикума Кузьмин Артур
