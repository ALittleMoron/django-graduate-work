# 📁 Django Graduate Work

## 📖 Кратко о проекте

Проект представляет собой ВКР по направлению "Математическое обеспечение и администрирование
информационных систем" (МОАИС) 02.03.03 ЮРГПУ (НПИ) по теме "Информационная система учета
библиофонда". Библиофонд - ресурс, хранящий в открытом доступе литературу различного толка:
от художественной до технической и научной литературы, такие же ВКРы, курсовые и так далее.

---

## 🧾 TODO список (основные положения)

- [x] Инициировать проект (окружение, настройки, тестовый вывод домашней стр. и др.).
- [ ] CRUD для библиофонда.
- [ ] Выгрузка проекта на реальный хостинг для дополнительного плюсика при оценивании ВКР комиссией.

Более подробный TODO [тут](./graduateWork.todo).

---

## 💻 Запуск проекта

В проекте используется [poetry](https://github.com/python-poetry/poetry) -
менеджер зависимостей. Для его установки на OSX / Linuxosx / linux /
bashonwindows используейте команду:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

```

Для Windows:

```PowerShell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -

```

Для успешной установки всех зависимостей и запуска виртуального окружения
необходимо запустить последовательно следующие команды в консоли:

```bash
git clone git@github.com:ALittleMoron/django-graduate-work.git
cd django-graduate-work
poetry install
poetry shell
```
