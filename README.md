# Python Server
## _Mathematical Server_

## Задача
Данный сервер создан с целью принимать задачи от клиента и запускать процесс анализа. Контролировать его и возвращать результаты обратны клиенту.
В будущем функционал будет расширен

## API
Документация по API расположена в файле openAPI.json, файл расположен внутри директории.

## Системные требования
 - Windows 10/11 или Ubuntu 20.04
 - Python 3.10 и новее

## Установка
1. Установить Python последней версии
2. Установить pip3 (Шаг только для пользователей Linux)
3. Установить все зависимости в проекте командой _pip install -r requirements.txt_ (В случаии Linux заменить _pip_ на _pip3_)
4. В файле setting.txt в строке _PYTHON_PATH=_ указать путь до Python

## Запуск проекта
Для запуска проекта необходимо выполнить несколько пунктов:
1. Запустить PostgreSql. Для этого можно воспользоваться docker compose, что лежит внутри репозитоия, либо запустить PostgreSql локально на компьютере на localhost и порт 5432
2. Перейти в дерикторию проекта и выполнить в консоли команду _python -m uvicorn cm.main:app --reload_

