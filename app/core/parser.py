import csv
from datetime import datetime
import time
import sys


class CSVParser:
    def __init__(self, settings, date_inp=None):
        self.server_file = settings["server_csv"]
        self.client_file = settings["client_csv"]

        if not date_inp:
            self.need_date = datetime.today().replace(hour=0, minute=0, second=0)
            self.need_date_end = self.need_date.replace(hour=23, minute=59, second=59)
        else:
            date_dict = date_inp.split(' ')

            self.need_date = datetime(
                day=int(date_dict[2]),
                month=int(date_dict[1]),
                year=int(date_dict[0]),
                hour=0,
                minute=0,
                second=0
            )
            self.need_date_end = datetime(
                day=int(date_dict[2]),
                month=int(date_dict[1]),
                year=int(date_dict[0]),
                hour=23,
                minute=59,
                second=59
            )
        self.unix_date_start = time.mktime(self.need_date.timetuple())
        self.unix_date_end = time.mktime(self.need_date_end.timetuple())

    def start_parser(self):
        print("---------------------------")
        print(
            f"Start time - {datetime.fromtimestamp(int(self.unix_date_start)).strftime('%Y-%m-%d %H:%M:%S')} "
            f"({self.unix_date_start})"
        )
        print(
            f"End time - {datetime.fromtimestamp(int(self.unix_date_end)).strftime('%Y-%m-%d %H:%M:%S')} "
            f"({self.unix_date_end})"
        )
        print("---------------------------")
        server_data = self.server_parser()
        client_data = self.client_parser()
        return self.join_client_server_data(server_data, client_data)

    def server_parser(self):

        server_data = []
        try:
            with open(self.server_file, "r") as server_csv:
                csv_reader = csv.DictReader(server_csv)
                for row in csv_reader:
                    if int(self.unix_date_start) <= int(row["timestamp"]) <= int(self.unix_date_end):
                        server_data.append(
                            {
                                "timestamp": row["timestamp"],
                                "event_id": row["event_id"],
                                "error_id": row["error_id"],
                                "json": row["description"]
                            }
                        )
            print(f"Server total - {len(server_data)}")
            return server_data
        except Exception as err:
            print(f"Server csv parser error - {err}!")
            sys.exit()

    def client_parser(self):
        client_data = []
        try:
            with open(self.client_file, "r") as client_csv:
                csv_client_reader = csv.DictReader(client_csv)
                for client_row in csv_client_reader:
                    if int(self.unix_date_start) <= int(client_row["timestamp"]) <= int(self.unix_date_end):
                        client_data.append(
                            {
                                "timestamp": client_row["timestamp"],
                                "player_id": client_row["player_id"],
                                "error_id": client_row["error_id"],
                                "json": client_row["description"]
                            }
                        )
            print(f"Client total - {len(client_data)}")
            return client_data
        except Exception as err:
            print(f"Client csv parser error - {err}!")
            sys.exit()

    def join_client_server_data(self, server_data, client_data):
        comp_data = []
        if len(server_data) >= len(client_data):
            for server_row in server_data:
                for client_row in client_data:
                    if server_row["error_id"] == client_row["error_id"]:
                        comp_data.append(
                            {
                                "timestamp": server_row["timestamp"],
                                "player_id": client_row["player_id"],
                                "event_id": server_row["event_id"],
                                "error_id": server_row["error_id"],
                                "json_server": server_row["json"],
                                "json_client": client_row["json"]
                            }
                        )
        else:
            for client_row in client_data:
                for server_row in server_data:
                    if server_row["error_id"] == client_row["error_id"]:
                        comp_data.append(
                            {
                                "timestamp": server_row["timestamp"],
                                "player_id": client_row["player_id"],
                                "event_id": server_row["event_id"],
                                "error_id": server_row["error_id"],
                                "json_server": server_row["json"],
                                "json_client": client_row["json"]
                            }
                        )
        print("---------------------------")
        print(f"Total Client-Server data {len(comp_data)}")
        return comp_data
