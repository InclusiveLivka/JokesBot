import unittest
import sqlite3
import os
import asyncio
from unittest.mock import patch
from app.database.engine import (
    initialize_database, write_grade, read_jokes_from_sqlite
)


class TestDatabaseFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_db_path = "test_data.db"
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def setUp(self) -> None:
        with patch('app.database.engine.DB_PATH', self.test_db_path):
            initialize_database()

    def test_initialize_database(self) -> None:
        with patch('app.database.engine.DB_PATH', self.test_db_path):
            initialize_database()
            with sqlite3.connect(self.test_db_path) as con:
                cur = con.cursor()
                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='jokes'")
                self.assertIsNotNone(cur.fetchone())

    def test_write_grade_new_joke(self) -> None:
        with patch('app.database.engine.DB_PATH', self.test_db_path):
            asyncio.run(write_grade("Test joke", 5))
            with sqlite3.connect(self.test_db_path) as con:
                cur = con.cursor()
                cur.execute(
                    "SELECT joke, grade1, grade2, difference FROM jokes WHERE joke='Test joke'")
                result = cur.fetchone()
                self.assertEqual(result, ("Test joke", 5, None, None))

    def test_write_grade_existing_joke_update(self) -> None:
        with patch('app.database.engine.DB_PATH', self.test_db_path):
            asyncio.run(write_grade("Test joke 2", 5))
            asyncio.run(write_grade("Test joke 2", 7))
            with sqlite3.connect(self.test_db_path) as con:
                cur = con.cursor()
                cur.execute(
                    "SELECT joke, grade1, grade2, difference FROM jokes WHERE joke='Test joke 2'")
                result = cur.fetchone()
                self.assertEqual(result, ("Test joke 2", 5, 7, 6))

    def test_read_jokes_from_sqlite(self) -> None:
        with patch('app.database.engine.DB_PATH', self.test_db_path):

            asyncio.run(write_grade("Joke 1", 4))
            asyncio.run(write_grade("Joke 1", 6))
            asyncio.run(write_grade("Joke 2", 5))
            asyncio.run(write_grade("Joke 2", 7))
            asyncio.run(write_grade("Joke 3", 3))
            asyncio.run(write_grade("Joke 3", 9))

            jokes = asyncio.run(read_jokes_from_sqlite())
            self.assertEqual(len(jokes), 3)
            self.assertIn(("Joke 1", 4, 6, 5), jokes)
            self.assertIn(("Joke 2", 5, 7, 6), jokes)
            self.assertIn(("Joke 3", 3, 9, 6), jokes)


if __name__ == "__main__":
    unittest.main()
