import sqlite3
import os
from typing import List, Tuple

#запись в базу данных с проверкой на существование анекдота
async def write_grade(joke: str, grade: int) -> None:
    try:
        db_path = os.path.join("Telegram_bot", "data.db")
        open(db_path, 'w').close()  # Создание и закрытие файла
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS jokes (id INTEGER PRIMARY KEY AUTOINCREMENT, joke TEXT, grade1 INTEGER, grade2 INTEGER, difference INTEGER)")
            # Проверяем, существует ли анекдот в базе данных
            cur.execute("SELECT id, grade1 FROM jokes WHERE joke = ?", (joke,))
            result = cur.fetchone()
            
            if result:
                joke_id, grade1 = result
                if grade1 is not None:
                    # Вычисляем разность между оценками
                    difference = (grade1 + grade) / 2
                    cur.execute("UPDATE jokes SET grade2 = ?, difference = ? WHERE id = ?", (grade, difference, joke_id))
                else:
                    cur.execute("UPDATE jokes SET grade1 = ? WHERE id = ?", (grade, joke_id))
            else:
                cur.execute("INSERT INTO jokes (joke, grade1) VALUES (?, ?)", (joke, grade))
            con.commit()
    except sqlite3.Error as e:
        print(f"Error writing to SQLite: {e}")

#чтение из базы данных
async def read_jokes_from_sqlite() -> List[Tuple[str, int, int, int]]:
    try:
        db_path = os.path.join("Telegram_bot", "data.db")
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT joke, grade1, grade2, difference FROM jokes WHERE grade1 IS NOT NULL AND grade2 IS NOT NULL")
            data = cur.fetchmany(3)
            return data
    except sqlite3.Error as e:
        print(f"Error reading from SQLite: {e}")
        return []
