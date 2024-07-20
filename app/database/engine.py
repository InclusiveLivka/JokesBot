import sqlite3
import os
import logging
from typing import List, Tuple


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

create_table_query = """
CREATE TABLE IF NOT EXISTS jokes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    joke        TEXT,
    grade1      INTEGER,
    grade2      INTEGER,
    difference  INTEGER
)
"""


def initialize_database() -> None:
    """Initialize the database by creating the necessary table if it doesn't
    exist."""
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_query)

            connection.commit()
            logger.info("Database initialized successfully.")

    except sqlite3.Error as error:
        logger.error(f"Error initializing database: {error}")

    except Exception as error:
        logger.error(f"Unexpected error initializing database: {error}")


async def write_grade(joke: str, grade: int) -> None:
    """
    Write a joke and its grade to the database. If the joke already exists,
    update its grades and calculate the average.

    Args:
        joke (str): The joke to write to the database.
        grade (int): The grade of the joke.
    """
    try:
        initialize_database()
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, grade1 FROM jokes WHERE joke = ?", (joke,))
            result = cursor.fetchone()

            if result:
                joke_id, existing_grade = result
                if existing_grade is not None:
                    average_grade = (existing_grade + grade) / 2
                    cursor.execute(
                        "UPDATE jokes SET grade2 = ?, difference = ? WHERE id = ?",
                        (grade, average_grade, joke_id)
                    )

                else:
                    cursor.execute(
                        "UPDATE jokes SET grade1 = ? WHERE id = ?",
                        (grade, joke_id)
                    )

            else:
                cursor.execute(
                    "INSERT INTO jokes (joke, grade1) VALUES (?, ?)",
                    (joke, grade)
                )
            connection.commit()
    except sqlite3.Error as error:
        logger.error(f"Error writing to SQLite: {error}")
        raise


async def read_jokes_from_sqlite() -> List[Tuple[str, int, int, int]]:
    """
    Retrieve jokes from the database that have both grades.

    Returns:
        List[Tuple[str, int, int, int]]: A list of jokes with their grades and
        differences.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            query = """
                SELECT joke, grade1, grade2, difference
                FROM jokes
                WHERE grade1 IS NOT NULL AND grade2 IS NOT NULL
            """
            cursor.execute(query)
            jokes_data = cursor.fetchmany(3)
        return jokes_data
    except sqlite3.Error as error:
        logger.error(f"Error retrieving graded jokes from SQLite: {error}")
        return []
    finally:
        if cursor:
            cursor.close()
