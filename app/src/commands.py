from app.db.db_core import DBCore
from app.core.parser import CSVParser
from app.core.core import Core
from config import db_conf, settings
from datetime import datetime


db = DBCore(db_conf)


def execute_from_command_line(argv=None):
    if len(argv) < 2:
        print("Вы не ввели команду! \nДоступные команды: start_update, db_init")
    elif argv[1] == "start_update":
        date_inp = input(
            f'Введите дату в формате Год Месяц День (Пример: 2021 05 01).'
            f'\nОставьте пустым для сегодняшней даты ({datetime.today().strftime("%Y %m %d")}) \n'
        )
        parser = CSVParser(settings, date_inp)
        parser_data = parser.start_parser()
        cheaters = db.get_cheaters()
        ban_checker = Core(parser_data, cheaters)
        data_for_upload = ban_checker.ban_checker()
        db.update_incident_table(data_for_upload)

    elif argv[1] == "db_init":
        db.db_init()
    elif argv[1] == "get_cheaters":
        db.get_cheaters()
    else:
        print("Неизвестная команда! \nДоступные команды: start_update, db_init")
