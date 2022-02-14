# 📁 Django Graduate Work

## 📖 Кратко о проекте

Проект представляет собой ВКР по направлению "Математическое обеспечение и администрирование
информационных систем" (МОАИС) 02.03.03 ЮРГПУ (НПИ) по теме "Информационная система учета
библиофонда". Библиофонд - ресурс, хранящий в открытом доступе литературу различного толка:
от художественной до технической и научной литературы, такие же ВКРы, курсовые и так далее.

Ссылка на загруженный на Heroku проект: [\*тык\*](https://graduateworkheroku.herokuapp.com).

---

## 🧾 TODO список (основные положения)

- [x] Инициировать проект (окружение, настройки, тестовый вывод домашней стр. и др.).
- [x] CRUD для библиофонда.
- [x] Выгрузка проекта на реальный хостинг для дополнительного плюсика при оценивании ВКР комиссией.

Более подробный TODO [тут](./graduateWork.todo).

---

## 💻 Запуск проекта

В проекте используется [poetry](https://github.com/python-poetry/poetry) -
менеджер зависимостей. Для его установки на OSX / Linuxosx / linux /
bashonwindows используейте команду:

```bash
curl -sSL https://install.python-poetry.org | python3 -

```

Для Windows:

```PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

```

Для успешной установки всех зависимостей и запуска виртуального окружения
необходимо запустить последовательно следующие команды в консоли:

```bash
git clone git@github.com:ALittleMoron/django-graduate-work.git
cd django-graduate-work
poetry install
poetry shell
```

Непосредственный запуск проекта:

```bash
cd путь-до-корневой-папки-репозитория/graduateWork

# замена настроек БД и ключа django под себя.

python3 manage.py collectstatic    # \
python3 manage.py makemigrations   #  Или все одной командой через &&
python3 manage.py migrate          # /

python3 manage.py runserver 8000   # либо полноценно через gunicorn, nginx и т.д.
```
