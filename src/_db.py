from threading import Lock
import sqlite3


class Database:

    def __init__(self) -> None:
        self.connected: bool = False
        self.lock: Lock = Lock()
        self.__connect()
        self.__first_time()

    def query(self, statement: str):
        cur = self.__start()
        self.lock.acquire()
        cur.execute(statement)
        result = cur.fetchall()
        cur.close()
        self.lock.release()
        if not result:
            return False
        return result

    def execute(self, statement: str, values: tuple | None = None):
        cur = self.__start()
        self.lock.acquire()
        if values is not None:
            cur.execute(statement, values)
        else:
            cur.execute(statement)
        self.db.commit()
        cur.close()
        self.lock.release()
        return True

    def __connect(self):
        self.db = sqlite3.connect('db.sqlite3')
        self.connected = True

    def __close(self):
        self.db.close()
        self.connected = False

    def __cursor(self):
        if self.connected:
            return self.db.cursor()
        return False

    def __start(self):
        if not self.connected:
            return False
        cur = self.__cursor()
        if not cur:
            return False
        return cur

    def __first_time(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS translation
            (id integer primary key autoincrement,
            key varchar(255),
            value longtext)
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS unstranslated
            (id integer primary key autoincrement,
            key varchar(255),
            value longtext)
        """)

    def _drop_table(self):
        self.execute("""drop table translation""")
        # self.execute("""drop table unstranslated""")


db = Database()

# db._drop_table()
