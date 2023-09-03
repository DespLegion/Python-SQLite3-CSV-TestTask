# Python + SQLite3 + CSV Test task

Есть два csv файла `client.csv` и `server.csv`

В `sqlite` есть таблица `cheaters`.

Поля `client.csv`:

    timestamp ,
    player_id ,
    error_id ,
    json

Поля `server.csv`:

    timestamp ,
    event_id ,
    error_id ,
    json

Поля таблицы `cheaters`:

    player_id integer,
    ban_time string



## Задача 1.

Создать в `sqlite` пустую таблицу с полями:

    timestamp,
    player_id,
    event_id,
    error_id,
    json_server,
    json_client



## Задача 2.

Написать класс или функцию, которая:

1) Выгрузит данные из `client.csv` и `server.csv` за определенную дату.
2) Объединит данные из этих таблиц по `error_id`.
3) Исключит из выборки записи с `player_id`, которые есть в таблице `cheaters`,
но только в том случае если:
у `player_id` `ban_time` - это предыдущие сутки или раньше относительно `timestamp` из `server.csv`
4) Выгрузит данные в таблицу, созданную в Задаче 1. В ней должны бать следующие данные:

   `timestamp` из `server.csv`,  
   `player_id` из `client.csv`,  
   `error_id`  из сджойненных `server.csv` и `client.csv`,  
   `json_server` поле `json` из `server.csv`,  
   `json_client` поле `json` из `client.csv`  


## Задача 3*.
Замерить потребление памяти во время выполнения задачи

----------------------------------------------------

## Использованные библиотеки
1) `memory_profiler` (Для замера потребления памяти программой)

## Доступные консольные команды к файлу `main.py`
1) `db_init` - Создает в базе данных таблицу `incidents` со всеми необходимыми полями:

`timestamp` тип данных: `INTEGER`  
`player_id` тип данных: `INTEGER`  
`event_id` тип данных: `INTEGER`  
`error_id` тип данных: `TEXT`  
`json_server` тип данных: `TEXT`  
`json_client` тип данных: `TEXT`

2) `start_update` - Выполняет Задачу №2

----------------------------------------------------
#### Дата обновления `sqlite` базы данных, приложенной к проекту - `2021 05 01`
#### Для нормального функционирования программы необходимо поместить в корневую директорию проекта файлы `client.csv` и `server.csv` из оригинального задания или указать к ним путь в `config.py`