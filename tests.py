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

    @pytest.mark.parametrize('book_name, genre', [
        (data.BOOK_COMEDY_1, data.COMEDY),
        (data.BOOK_FANTASY, ''),  # пустая строка = нет жанра
    ])
    def test_books_genre_is_empty(self, books_collector, book_name, genre):
        books_collector.add_new_book(book_name)

        if genre: # проверяем, если genre вернул False, не добавляем жанр
            books_collector.set_book_genre(book_name, genre)
        assert books_collector.get_book_genre(book_name) == genre

    @pytest.mark.parametrize('book_name, genre, add_book, expected_result', [
        (data.BOOK_COMEDY_1, data.COMEDY, True, 1),
        ('', '', False, 0)
    ])
    def test_dictionary_books_genre_is_not_null(self, books_collector, book_name, genre, add_book,
                                                expected_result):
        if add_book:
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

    @pytest.mark.parametrize('book_name, book_exists, expected_result', [
        (data.BOOK_HORROR_1, True, True),  # книга существует
        ('Bий', False, False),  # книга не существует
    ])
    def test_add_book_in_favorites(self, books_collector, book_name, book_exists, expected_result):
        if book_exists:
            books_collector.add_new_book(book_name)

        books_collector.add_book_in_favorites(book_name)
        assert (book_name in books_collector.get_list_of_favorites_books()) == expected_result

    @pytest.mark.parametrize('book_name, book_exists, expected_result', [
        (data.BOOK_HORROR_1, True, False),  # книга существует и ее удалили
        ('Bий', False, False),  # книга не существует
    ])
    def test_delete_book_from_favorites(self, books_collector, book_name, book_exists, expected_result):
        if book_exists:
            books_collector.add_new_book(book_name)

        books_collector.add_book_in_favorites(book_name)
        books_collector.delete_book_from_favorites(book_name)
        assert (book_name in books_collector.get_list_of_favorites_books()) == expected_result
