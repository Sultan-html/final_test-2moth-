import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def find_user_by_name(self, name):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return self.cursor.fetchone()

    def execute_transaction(self, operations):
        for operation in operations:
            self.cursor.execute(*operation)
        self.connection.commit()

class User:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db_manager.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER
            )
        ''')
        self.db_manager.connection.commit()

    def add_user(self, name, age):
        self.db_manager.cursor.execute(
            "INSERT INTO users (name, age) VALUES (?, ?)", (name, age)
        )
        self.db_manager.connection.commit()

    def get_user(self, user_id):
        self.db_manager.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return self.db_manager.cursor.fetchone()

    def delete_user(self, user_id):
        self.db_manager.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.db_manager.connection.commit()

class Admin(User):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.db_manager.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                level INTEGER
            )
        ''')
        self.db_manager.connection.commit()

    def add_admin(self, name, level):
        self.db_manager.cursor.execute(
            "INSERT INTO admins (name, level) VALUES (?, ?)", (name, level)
        )
        self.db_manager.connection.commit()

class Customer(User):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.db_manager.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                purchase_count INTEGER
            )
        ''')
        self.db_manager.connection.commit()

    def add_customer(self, name, purchase_count):
        self.db_manager.cursor.execute(
            "INSERT INTO customers (name, purchase_count) VALUES (?, ?)", (name, purchase_count)
        )
        self.db_manager.connection.commit()

# Пример использования
db_manager = DatabaseManager("my_database.db")
user_manager = User(db_manager)
admin_manager = Admin(db_manager)
customer_manager = Customer(db_manager)

user_manager.add_user("Нуразиз", 16)
admin_manager.add_admin("Ислам", 20)
customer_manager.add_customer("Анамир", 5)

print(user_manager.get_user(1))
print(db_manager.find_user_by_name("Нуразиз"))

db_manager.execute_transaction([
    ("INSERT INTO users (name, age) VALUES (?, ?)", ("Eve", 30)),
    ("INSERT INTO users (name, age) VALUES (?, ?)", ("Frank", 35))
])

db_manager.close_connection()
