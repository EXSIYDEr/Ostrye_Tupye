import sqlite3
from models import Item, User

DB_NAME = "warehouse.db"


def init_db():
    """Создание таблиц и заполнение начальными данными"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица товаров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            min_limit INTEGER NOT NULL,
            storage_place TEXT NOT NULL
        )
    ''')

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Заполнение стартовыми данными (если база пустая)
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        sample_items = [
            ("Бумага А4", "Бумага", "пачка", 450, 100, "А-1-3"),
            ("Ручки синие", "Письменное", "кор.", 500, 50, "Б-1-3"),
            ("Карандаши пр.", "Письменное", "кор.", 400, 50, "Б-1-3"),
            ("Тетради 38л.", "Тетради", "кор.", 300, 40, "В-1-3"),
            ("Бумага А5", "Бумага", "пачка", 450, 100, "А-1-3")
        ]
        cursor.executemany('''
            INSERT INTO items (name, category, unit, quantity, min_limit, storage_place)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_items)

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("admin", "admin123", "Администратор"))

    conn.commit()
    conn.close()


def get_all_items(search_query=None):
    """Получение всех товаров из БД и преобразование их в объекты класса Item"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if search_query:
        cursor.execute('''
            SELECT id, name, category, unit, quantity, min_limit, storage_place 
            FROM items 
            WHERE name LIKE ? OR category LIKE ?
        ''', (f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute('SELECT id, name, category, unit, quantity, min_limit, storage_place FROM items')

    rows = cursor.fetchall()
    conn.close()

    items = []
    for r in rows:
        item_obj = Item(id=r[0], name=r[1], category=r[2], unit=r[3],
                        quantity=r[4], min_limit=r[5], storage_place=r[6])
        items.append(item_obj.to_dict())
    return items


def get_stats():
    """Статистика для карточек верхнего бара"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), SUM(quantity) FROM items")
    total_types, total_quantity = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM items WHERE quantity < min_limit")
    critical_count = cursor.fetchone()[0]

    conn.close()
    return {
        "types_count": total_types or 0,
        "total_quantity": total_quantity or 0,
        "critical_count": critical_count or 0
    }
