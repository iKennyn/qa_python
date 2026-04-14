import pytest
import data


class TestBooksCollector:
    @pytest.mark.parametrize('book_names', [
        (data.BOOK_HORROR_1, data.BOOK_HORROR_2), # Добавление двух книг
        (data.BOOK_FANTASY, data.BOOK_FANTASY, data.BOOK_CARTOONS), # Добавление трех книг, где две одинаковые
        ('Хроники Нарнии: Лев, Колдунья и Платяной шкаф', '',
         data.BOOK_HORROR_1, data.BOOK_HORROR_2), # Добавление 4-х книг, где две не подходят по длине
    ])
    def test_add_new_book_add_two_books(self, books_collector, book_names):
        for book_name in book_names:
            books_collector.add_new_book(book_name)
        assert len(books_collector.get_books_genre()) == 2

    def test_books_genre_is_empty(self, books_collector):
        book_name = data.BOOK_FANTASY
        books_collector.add_new_book(book_name)
        assert books_collector.get_book_genre(book_name) == ''

    @pytest.mark.parametrize('book_name, genre, expected_result', [
        (data.BOOK_COMEDY_1, data.COMEDY, 1),
        ('', '', 0)
    ])
    def test_dictionary_books_genre_is_not_null(self, books_collector, book_name, genre,
                                                expected_result):
        books_collector.add_new_book(book_name)
        books_collector.set_book_genre(book_name, genre)
        assert len(books_collector.get_books_genre()) == expected_result

    def test_book_genre_is_correct(self, books_collector):
        books_collector.add_new_book(data.BOOK_HORROR_1)
        books_collector.set_book_genre(data.BOOK_HORROR_1, data.HORROR)
        assert books_collector.get_book_genre(data.BOOK_HORROR_1) == data.HORROR

    def test_book_with_specific_genre_not_exists(self, books_collector, create_books_and_genre):
        assert books_collector.get_books_with_specific_genre('Роман') == []

    def test_books_suitable_for_children(self, books_collector, create_books_and_genre):
        children_books = books_collector.get_books_for_children()
        for book in children_books:
            genre = books_collector.get_book_genre(book)
            assert genre not in books_collector.genre_age_rating

    def test_books_with_specific_genre_horror(self, books_collector, create_books_and_genre):
        assert books_collector.get_books_with_specific_genre(data.HORROR) == [data.BOOK_HORROR_1, data.BOOK_HORROR_2]

    def test_add_book_in_favorites(self, books_collector):
        book_name = data.BOOK_FANTASY
        books_collector.add_new_book(book_name)
        books_collector.add_book_in_favorites(book_name)
        assert (book_name in books_collector.get_list_of_favorites_books()) == True

    def test_add_book_in_favorites_that_does_not_exist(self, books_collector):
        book_name = data.BOOK_FANTASY
        books_collector.add_book_in_favorites(book_name)
        assert (book_name in books_collector.get_list_of_favorites_books()) == False

    def test_delete_book_from_favorites(self, books_collector):
        book_name = data.BOOK_FANTASY
        books_collector.add_new_book(book_name)
        books_collector.add_book_in_favorites(book_name)
        books_collector.delete_book_from_favorites(book_name)
        assert (book_name in books_collector.get_list_of_favorites_books()) == False

    def test_get_books_genre_success(self, books_collector, create_books_and_genre):
        expected_dict = {
            data.BOOK_HORROR_1: data.HORROR,
            data.BOOK_COMEDY_1: data.COMEDY,
            data.BOOK_FANTASY: data.FANTASY,
            data.BOOK_HORROR_2: data.HORROR,
            data.BOOK_COMEDY_2: data.COMEDY,
            data.BOOK_DETECTIVES: data.DETECTIVES,
            data.BOOK_CARTOONS: data.CARTOONS,
        }
        assert books_collector.get_books_genre() == expected_dict

    def test_get_list_of_favorites_books_success(self, books_collector, create_books_and_genre):
        book_name = data.BOOK_FANTASY
        books_collector.add_book_in_favorites(book_name)
        assert books_collector.get_list_of_favorites_books() == [book_name]