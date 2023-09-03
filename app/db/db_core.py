import sqlite3


class DBCore:
    def __init__(self, db_conf):
        self.db_name = db_conf["db_name"]

    def db_init(self):
        try:
            conn = sqlite3.connect(f"file:{self.db_name}?mode=rw", uri=True)
            cursor = conn.cursor()

            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS incidents (
                timestamp INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                event_id INTEGER NOT NULL,
                error_id TEXT PRIMARY KEY,
                json_server TEXT NOT NULL,
                json_client TEXT NOT NULL
                )
                '''
            )

            conn.commit()
            print("Table successfully created")
        except sqlite3.Error as err:
            print(f"Table creation error- {err}!")
        finally:
            if 'conn' in locals():
                if conn:
                    conn.close()

    def get_cheaters(self):
        try:
            conn = sqlite3.connect(f"file:{self.db_name}?mode=ro", uri=True)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM cheaters')
            cheaters = cursor.fetchall()
            print(f"Total cheaters - {len(cheaters)}")
            print("---------------------------")
            return cheaters
        except sqlite3.Error as err:
            print(f"Get cheaters table error - {err}!")
        finally:
            if 'conn' in locals():
                if conn:
                    conn.close()

    def get_incidents(self):
        try:
            conn = sqlite3.connect(f"file:{self.db_name}?mode=ro", uri=True)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM incidents')
            incidents_base = cursor.fetchall()
            print(f"Total incidents - {len(incidents_base)}")
            print("---------------------------")
            return incidents_base
        except sqlite3.Error as err:
            print(f"Get incidents table error - {err}!")
        finally:
            if 'conn' in locals():
                if conn:
                    conn.close()

    def update_incident_table(self, data):
        inc_base = self.get_incidents()
        inc_counter = 0
        for inc in inc_base:
            for data_d in data:
                if inc[3] == data_d["error_id"]:
                    data.remove(data_d)
                    inc_counter += 1
        print(f"Incident already exists - {inc_counter}")
        formed_data = []
        for data_list in data:
            formed_data.append(
                (
                    int(data_list["timestamp"]),
                    int(data_list["player_id"]),
                    int(data_list["event_id"]),
                    data_list["error_id"],
                    data_list["json_server"],
                    data_list["json_client"],
                )
            )
        try:
            conn = sqlite3.connect(f"file:{self.db_name}?mode=rw", uri=True)
            cursor = conn.cursor()

            cursor.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?)", formed_data)

            conn.commit()
            print(f"Incident table successfully updated ({cursor.rowcount} rows)")
        except sqlite3.Error as err:
            print(f"Incident table update error - {err}!")
        finally:
            if 'conn' in locals():
                if conn:
                    conn.close()
