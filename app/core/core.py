from datetime import datetime, timedelta


class Core:
    def __init__(self, c_s_parsed_data, cheaters):
        self.c_s_parsed_data = c_s_parsed_data
        self.cheaters = cheaters

    def ban_checker(self):
        for cheater in self.cheaters:
            for incident in self.c_s_parsed_data:
                if int(incident["player_id"]) == int(cheater[0]):
                    inc_date = datetime.strptime(
                        datetime.fromtimestamp(
                            int(incident["timestamp"])
                        ).strftime('%Y-%m-%d %H:%M:%S'),
                        '%Y-%m-%d %H:%M:%S'
                    )
                    ch_date = datetime.strptime(cheater[1], '%Y-%m-%d %H:%M:%S')
                    if ch_date < inc_date - timedelta(days=1):
                        self.c_s_parsed_data.remove(incident)
        print(f"Updated Client-Server data - {len(self.c_s_parsed_data)}")
        print("---------------------------")
        return self.c_s_parsed_data
