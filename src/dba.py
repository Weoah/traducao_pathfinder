from src._db import db


class DatabaseAcess:

    def insert_translated_data(self, translated_data: dict) -> None:
        for key, value in translated_data.items():
            db.execute("""
                INSERT INTO translation
                (key, value)
                VALUES
                (?, ?)
            """, (key, value))

    def insert_untranslated_data(self, data_dict: dict) -> None:
        for key, value in data_dict.items():
            db.execute("""
                INSERT INTO unstranslated
                (key, value)
                VALUES
                (?, ?)
            """, (key, value))

    def get_untranslated_keys(self) -> tuple:
        result = db.query("""
            SELECT key, value
            FROM unstranslated
            WHERE key = 'Key'
        """)
        return result

    def get_untranslated_values(self) -> tuple:
        result = db.query("""
            SELECT key, value
            FROM unstranslated
            WHERE key = 'Value'
        """)
        return result

    def check_if_translated(self, key: str) -> tuple:
        result = db.query(f"""
            SELECT key
            FROM translation
            WHERE value = "{key}"
        """)
        return result


dba = DatabaseAcess()
