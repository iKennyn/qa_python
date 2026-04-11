import pytest
import data

from main import BooksCollector


@pytest.fixture
def books_collector():
    collector = BooksCollector()
    return collector

@pytest.fixture()
def create_books_and_genre(books_collector):
    for book_name, genre in zip(data.BOOKS_COLLECTOR, data.GENRES_COLLECTOR):
        books_collector.add_new_book(book_name)
        books_collector.set_book_genre(book_name, genre)
