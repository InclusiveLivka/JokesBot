import unittest
from unittest.mock import patch, MagicMock

import requests
from bs4 import BeautifulSoup

from app.utils.jokes import fetch_jokes_page, extract_jokes, get_random_joke


class TestJokeFetching(unittest.TestCase):

    @patch('app.utils.jokes.requests.get')
    def test_fetch_jokes_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><div class="anekdot">Joke 1</div><div class="anekdot">Joke 2</div></body></html>'
        mock_get.return_value = mock_response

        soup = fetch_jokes_page(1)
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(len(soup.find_all("div", class_="anekdot")), 2)

    def test_extract_jokes(self):
        html_content = '<html><body><div class="anekdot">Joke 1</div><div class="anekdot">Joke 2</div></body></html>'
        soup = BeautifulSoup(html_content, "html.parser")

        jokes = extract_jokes(soup)
        self.assertEqual(len(jokes), 2)
        self.assertEqual(jokes[0].text, "Joke 1")
        self.assertEqual(jokes[1].text, "Joke 2")

    @patch('app.utils.jokes.fetch_jokes_page')
    @patch('app.utils.jokes.extract_jokes')
    @patch('random.randint')
    @patch('random.choice')
    def test_get_random_joke(
        self,
        mock_choice,
        mock_randint,
        mock_extract_jokes,
        mock_fetch_jokes_page
    ) -> None:

        mock_soup = MagicMock()
        mock_fetch_jokes_page.return_value = mock_soup

        mock_jokes = [MagicMock(text="Joke 1"), MagicMock(text="Joke 2")]
        mock_extract_jokes.return_value = mock_jokes

        mock_randint.return_value = 1
        mock_choice.return_value = mock_jokes[0]

        joke = get_random_joke()
        self.assertEqual(joke, "Joke 1")

    @patch('app.utils.jokes.fetch_jokes_page')
    @patch('app.utils.jokes.extract_jokes')
    def test_get_random_joke_no_jokes(
        self,
        mock_extract_jokes,
        mock_fetch_jokes_page
    ) -> None:

        mock_soup = MagicMock()
        mock_fetch_jokes_page.return_value = mock_soup

        mock_extract_jokes.return_value = []

        joke = get_random_joke()
        self.assertIsNone(joke)

    @patch(
        'app.utils.jokes.requests.get', side_effect=requests.RequestException
    )
    def test_get_random_joke_request_exception(self, mock_get):
        joke = get_random_joke()
        self.assertIsNone(joke,)


if __name__ == "__main__":
    unittest.main()
