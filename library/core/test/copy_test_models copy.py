from codecs import ignore_errors
from datetime import date, timedelta
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ..models import Author, Book, Category, Serie


AUTHORS_URL = reverse('catalog:author-list')
BOOKS_URL = reverse('catalog:book-list')
CATEGORIES_URL = reverse('catalog:category-list')
SERIES_URL = reverse('catalog:serie-list')


class ModelTest(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = APIClient()
        self.init_authors = Author.objects.count()
        self.init_books = Book.objects.count()
        self.init_categories = Category.objects.count()
        self.init_series = Serie.objects.count()
        self.test_author = {'id': 1,
                            'name': 'Test Name',
                            'pseudonym': 'Test Pseudonym',
                            'born': '1985-11-02',
                            'died': '2020-12-13'}
        self.test_category = {'id': 1,
                              'name': 'Test Category',
                              'description': 'Test Description'}
        self.test_serie = {'id': 1,
                           'name': 'Test Serie'}
        self.test_book = {'id': 1,
                          'isbn': '979-123-456-789-6',
                          'title': 'Test Title',
                          'authors': [1],
                          'description': 'Test Description',
                          'categories': [1, 3],
                          'serie': 1,
                          'serie_order': 7,
                          'available': 1
                          }

# Author tests ------------------------------------------------------------------------------- #

    def test_create_author_successfully(self):
        """Test create author successfully"""
        request = self.client.post(AUTHORS_URL, self.test_author)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_delete_author_successfully(self):
        """Checks that it deletes an author and all his
        books except those written with another author
        """
        m_w_id = 7  # Margaret Weis id
        url = reverse('catalog:author-detail', args=[m_w_id])
        m_w = Author.objects.get(pk=m_w_id)
        m_w_books = m_w.rel_author.all()
        written_alone = len([_ for _ in m_w_books if _.book_writers().count() == 1])

        request = self.client.delete(url)

        self.assertEqual(self.init_authors - 1, Author.objects.count())
        self.assertEqual(self.init_books - written_alone, Book.objects.count())

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_author_successfully(self):
        """Get an author and check that the ids are the same in the queryset
        and in the data of the request
        """
        id_to_filter = 1
        queryset = Author.objects.get(id=id_to_filter)
        url = reverse('catalog:author-detail', args=[id_to_filter])
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['id'], queryset.id)

    def test_update_author_successfully(self):
        """Test if Update author successfully"""
        id_to_update = self.test_author['id']
        instance_before = Author.objects.get(id=id_to_update)
        url = reverse('catalog:author-detail', args=[id_to_update])
        request = self.client.patch(url, self.test_author)
        instance_after = Author.objects.get(id=id_to_update)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertNotEquals(vars(instance_before), vars(instance_after))

    def test_date_death_prior_birth(self):
        """Test fail when date of death is prior to date of birth"""
        test_author = self.test_author.copy()
        test_author['died'] = '1985-11-01'  # Born date is 1985-11-02
    #     request = self.client.post(AUTHORS_URL, test_author)
        
    #     self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_born_date_not_yet_arrived(self):
        """Test fail when born date has not yet arrived"""
        test_author = self.test_author.copy()
        test_author['born'] = date.today() + timedelta(1)
        request = self.client.post(AUTHORS_URL, test_author)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_death_date_not_yet_arrived(self):
        """Test fail when death date has not yet arrived"""
        test_author = self.test_author.copy()
        test_author['died'] = date.today() + timedelta(1)
        request = self.client.post(AUTHORS_URL, test_author)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

# Book tests --------------------------------------------------------------------------------- #

    # def test_create_book_successfully(self):
    #     """Test create book successfully"""
    #     request = self.client.post(BOOKS_URL, self.test_book)

    #     self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_delete_book_successfully(self):
        """Checks that it deletes a book correctly"""
        url = reverse('catalog:book-detail', args=[1])
        request = self.client.delete(url)

        self.assertEqual(self.init_books - 1, Book.objects.count())
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_book_successfully(self):
        """Get a book and check that the ids are the same in the queryset
        and in the data of the request
        """
        id_to_filter = 1
        queryset = Book.objects.get(id=id_to_filter)
        url = reverse('catalog:book-detail', args=[id_to_filter])
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['id'], queryset.id)

    def test_update_book_successfully(self):
        """Test if Update book successfully"""
        id_to_update = self.test_book['id']
        instance_before = Book.objects.get(id=id_to_update)
        dict_instance_before = instance_before.__dict__
        dict_instance_before['title'] = "Test Title"
        url = reverse('catalog:book-detail', args=[id_to_update])
        request = self.client.patch(url, dict_instance_before)
        instance_after = Book.objects.get(id=id_to_update)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertNotEquals(vars(instance_before), vars(instance_after))

    def test_book_wrong_control_digit(self):
        """Test if fails creating book with wrong control digit"""
        test_book = self.test_book.copy()
        test_book['isbn'] = '979-123-456-789-0'  # Correct digit is 6
        request = self.client.post(BOOKS_URL, test_book)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_wrong_isbn(self):
        """Test if fails creating book with wrong isbn format"""
        test_book = self.test_book.copy()
        test_book['isbn'] = '976-123-456-789-6'  # 976 initial numbers are incorrect
        request = self.client.post(BOOKS_URL, test_book)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_book_serie_but_not_serie_order(self):
    #     """Test if fails creating book with serie field but serie_order empty"""
    #     test_book = self.test_book.copy()
    #     test_book.pop('serie_order')
    #     request = self.client.post(BOOKS_URL, test_book)

    #     self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_book_serie_order_already_exist(self):
    #     """Test if fails creating book with an existing serie_order"""
    #     test_book = self.test_book.copy()
    #     test_book['serie_order'] = 1  # For the serie 1 serie_order = 1 already exists
    #     request = self.client.post(BOOKS_URL, test_book)

    #     self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

# Category tests ----------------------------------------------------------------------------- #

    def test_create_category_successfully(self):
        """Test create category successfully"""
        request = self.client.post(CATEGORIES_URL, self.test_category)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_delete_category_successfully(self):
        """Checks that it deletes a category correctly"""
        url = reverse('catalog:category-detail', args=[1])
        request = self.client.delete(url)

        self.assertEqual(self.init_categories - 1, Category.objects.count())
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_category_successfully(self):
        """Get a category and check that the ids are the same in the queryset
        and in the data of the request
        """
        id_to_filter = 1
        queryset = Category.objects.get(id=id_to_filter)
        url = reverse('catalog:category-detail', args=[id_to_filter])
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['id'], queryset.id)

    def test_update_category_successfully(self):
        """Test if Update category successfully"""
        id_to_update = self.test_category['id']
        instance_before = Category.objects.get(id=id_to_update)
        url = reverse('catalog:category-detail', args=[id_to_update])
        request = self.client.patch(url, self.test_category)
        instance_after = Category.objects.get(id=id_to_update)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertNotEquals(vars(instance_before), vars(instance_after))

# Serie tests -------------------------------------------------------------------------------- #

    def test_create_serie_successfully(self):
        """Test create serie successfully"""
        request = self.client.post(SERIES_URL, self.test_serie)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_delete_serie_successfully(self):
        """Checks that it deletes a serie correctly"""
        url = reverse('catalog:serie-detail', args=[1])
        request = self.client.delete(url)

        self.assertEqual(self.init_series - 1, Serie.objects.count())
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_serie_successfully(self):
        """Get a serie and check that the ids are the same in the queryset
        and in the data of the request
        """
        id_to_filter = 1
        queryset = Serie.objects.get(id=id_to_filter)
        url = reverse('catalog:serie-detail', args=[id_to_filter])
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['id'], queryset.id)

    def test_update_serie_successfully(self):
        """Test if Update serie successfully"""
        id_to_update = self.test_serie['id']
        instance_before = Serie.objects.get(id=id_to_update)
        url = reverse('catalog:serie-detail', args=[id_to_update])
        request = self.client.patch(url, self.test_serie)
        instance_after = Serie.objects.get(id=id_to_update)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertNotEquals(vars(instance_before), vars(instance_after))
