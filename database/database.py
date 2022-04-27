import sqlite3

event_table = """
CREATE TABLE IF NOT EXISTS events ( 
    id PRIMARY KEY NOT NULL, 
    name TEXT,
    type TEXT,
    url TEXT, 
    localDate TEXT,
    classificationsSegmentID  TEXT,
    price_range TEXT,
    latitude TEXT,
    longitude TEXT,
    images VARCHAR
);

"""


class Database:
    def __init__(self, db_name='events') -> None:
        print('*******************************')
        print('starting the database...')
        print('populating the database.')
        self.init_tables()
        print('Database ready to use')
        # Keep tract to prevent another request to the api
        self.is_loaded = False

    def init_tables(self):
        # Create a connection
        try:
            self.con = sqlite3.connect('events.db',check_same_thread=False)
            self.cursor = self.con.cursor()
            self.cursor.execute(event_table)
            self.con.commit()

        except sqlite3.Error as e:
            print(e)
            print("Error Creating the database connection")

    def is_loaded(self):
        return self.is_loaded

    def event_rows(self):
        no_rows = self.cursor.execute("SELECT COUNT(*) FROM events")
        rows = no_rows.fetchone()
        return rows[0]

    def get_connection(self):
        return self.con

    def insert_event(self, data_tuple):
        print('\n-----------------------------------------------')

        print(f'Inserting a row. {data_tuple}')
        print(f'len of data tuples is {data_tuple}')
        query = f'INSERT INTO events (id,name,type,url,localDate,classificationsSegmentID,price_range,latitude,longitude,images TEXT) value(?,?,?,?,?,?,?,?,?,?)'
        self.cursor.execute(query, data_tuple),
        print(f'Finished  inserting the row')
        self.is_loaded = True

    def insert_events(self, data_tuples):
        print('\n-----------------------------------------------')

        print('Inserting multiple rows')
        query = f'INSERT INTO events (id,name,type,url,localDate,classificationsSegmentID,price_range,latitude,longitude,images) values(?,?,?,?,?,?,?,?,?,?)'
        try:
            self.cursor.executemany(query, data_tuples)
        except sqlite3.IntegrityError:
            pass 
        print(f'Finished inserting {self.cursor.rowcount} rows')
        print('\n-----------------------------------------------')
        self.con.commit()

    def get_events(self):
        print('Retrieving the database records: ')

        data = self.cursor.execute('SELECT * FROM events;').fetchall()
        return data
