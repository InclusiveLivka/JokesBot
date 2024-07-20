import sqlite3
import os
import logging
from typing import List, Tuple


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")


def initialize_database() -> None:
    """Initialize the database by creating the necessary table if it doesn't
    exist."""
    try:
        with sqlite3.connect(DB_PATH) as con:

            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jokes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    joke TEXT,
                    grade1 INTEGER,
                    grade2 INTEGER,
                    difference INTEGER
                )
            """)

            con.commit()
            logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")


async def write_grade(joke: str, grade: int) -> None:
    """
    Write a joke and its grade to the database. If the joke already exists,
    update its grades and calculate the difference.

    Args:
        joke (str): The joke to write to the database.
        grade (int): The grade of the joke.
    """
    try:
        initialize_database()
        with sqlite3.connect(DB_PATH) as con:

            cur = con.cursor()
            cur.execute("SELECT id, grade1 FROM jokes WHERE joke = ?", (joke,))
            result = cur.fetchone()

            if result:
                joke_id, grade1 = result
                if grade1 is not None:
                    difference = (grade1 + grade) / 2
                    cur.execute(
                        "UPDATE jokes SET grade2 = ?, difference = ? WHERE id = ?", (
                            grade, difference, joke_id
                        )
                    )
                    logger.info(
                        f"Joke ID {joke_id} updated with grade2: {grade} and difference: {difference}.")
                else:
                    cur.execute(
                        "UPDATE jokes SET grade1 = ? WHERE id = ?", (
                            grade, joke_id
                        )
                    )
                    logger.info(
                        f"Joke ID {joke_id} updated with grade1: {grade}.")
            else:
                cur.execute(
                    "INSERT INTO jokes (joke, grade1) VALUES (?, ?)", (
                        joke, grade
                    )
                )
                logger.info("New joke inserted into the database.")
            con.commit()
    except sqlite3.Error as e:
        logger.error(f"Error writing to SQLite: {e}")


async def read_jokes_from_sqlite() -> List[Tuple[str, int, int, int]]:
    """
    Read jokes from the database that have both grades.

    Returns:
        List[Tuple[str, int, int, int]]: A list of jokes with their grades and
        differences.
    """
    try:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("""
                SELECT joke, grade1, grade2, difference 
                FROM jokes 
                WHERE grade1 IS NOT NULL AND grade2 IS NOT NULL
            """)
            data = cur.fetchmany(3)
            logger.info("Jokes retrieved successfully from the database.")
            return data
    except sqlite3.Error as e:
        logger.error(f"Error reading from SQLite: {e}")
        return []
