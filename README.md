# Python Server
## _Mathematical Server_

## Задача
Данный сервер создан с целью принимать задачи от клиента и запускать процесс анализа. Контролировать его и возвращать результаты обратны клиенту.
В будущем функционал будет расширен

## API
Чтобы ознакомиться с текущей версией API на основе которой разрабатывается проект, необходимо перейти по [Формализация API](https://docs.google.com/document/d/16H4hBA4kUtjGOg0otnWg5-KFDb8lJPlFyrPuu39Wrk4/edit?usp=sharing).

## Системные требования
 - Windows 10/11
 - Python 3.10 и новее
 - Любой текстовый редактор (Мы рекомендуем Visual Studio Code)

## Установка
Первично необходимо установить последнюю версию Python.
В нашем случае это версия _3.10_
Для установки всех необходимых зависимомтей, необходимо воспользоваться командой:
_pip install -r requirements.txt_

## Запуск проекта
Для запуска проекта необходимо перейти в консоли в репозиторий проекта и выполнить команду:
_python -m uvicorn cmd.main:app --reload_

## Возможные ошибки
Так же возможна ошибка при запуске проекта, тогда необходимо выполнить устанвоку библиотек напряму с помщью команд:
_pip install fastapi_
_pip install "uvicorn[standard]"_
При устанвоке на _Linux_ или _MacOs_ необходимо добавить _3_ к команде _pip_ и писать _pip3..._