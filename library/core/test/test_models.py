from codecs import ignore_errors
from datetime import date, timedelta
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ..models import Author, Book, Category, Serie


class ModelTest(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = APIClient()
        self.init_authors = Author.objects.count()
        self.init_books = Book.objects.count()
        self.init_categories = Category.objects.count()
        self.init_series = Serie.objects.count()
        self.test_author = {'id': 100,
                            'name': 'Test Name',
                            'pseudonym': 'Test Pseudonym',
                            'born': '1985-11-02',
                            'died': '2020-12-13'}
        self.test_category = {'id': 100,
                              'name': 'Test Category',
                              'description': 'Test Description'}
        self.test_serie = {'id': 100,
                           'name': 'Test Serie'}
        self.test_book = {'id': 100,
                          'isbn': '979-123-456-789-6',
                          'title': 'Test Title',
                          'description': 'Test Description',
                          'serie_order': 7,
                          'available': 1
                          }

# Author tests ------------------------------------------------------------------------------- #

    def test_date_death_prior_birth_model(self):
        """Test fail when date of death is prior to date of birth"""
        test_author = self.test_author.copy()
        test_author['died'] = '1985-11-01'  # Born date is 1985-11-02
        author = Author(**test_author)
        with self.assertRaises(ValidationError):
            author.full_clean()

    def test_born_date_not_yet_arrived(self):
        """Test fail when born date has not yet arrived"""
        test_author = self.test_author.copy()
        test_author['born'] = date.today() + timedelta(1)
        author = Author(**test_author)
        with self.assertRaises(ValidationError):
            author.full_clean()

    def test_death_date_not_yet_arrived(self):
        """Test fail when death date has not yet arrived"""
        test_author = self.test_author.copy()
        test_author['died'] = date.today() + timedelta(1)
        author = Author(**test_author)
        with self.assertRaises(ValidationError):
            author.full_clean()

    def test_delete_books_deleting_author(self):
        """Test that deleting an author deletes all his books"""
        # Author Brandon Sanderson has 6 books written by him
        author = Author.objects.get(id=1)
        author.delete()

        self.assertEqual(self.init_authors - 1, Author.objects.all().count())
        self.assertEqual(self.init_books - 6, Book.objects.all().count())

    def test_delete_own_books_deleting_author(self):
        """Test that deleting an author deletes all his books except
        those he has written with another writer
        """
        # Author Margaret Weiss has 11 books written by her. 4 written by her own
        # and 7 written with Tracy Raye Hickman
        author = Author.objects.get(id=7)
        author.delete()

        self.assertEqual(self.init_authors - 1, Author.objects.all().count())
        self.assertEqual(self.init_books - 4, Book.objects.all().count())

# Book tests --------------------------------------------------------------------------------- #

    # def test_book_wrong_control_digit(self):
    #     """Test if fails creating book with wrong control digit"""
    #     cre_upd = {'created': '2013-10-29T09:14:03.895210Z',
    #                'updated': '2013-10-29T09:14:03.895210Z'}
    #     author = Author(**self.test_author, **cre_upd)
    #     author.save()
        # category = Category(**self.test_category, **cre_upd)
        # category.save()
        # serie = Serie(**self.test_serie, **cre_upd)
        # serie.save()
        # test_book = self.test_book
        # book = Book(**test_book)
        # book.authors.add(author)
        # book.categories.add(category)
        # book.serie = serie

        # book.isbn = '979-123-456-789-0'  # Correct digit is 6
        # book.isbn = '978-84-473-5602-7'  # Correct isbn for test

        # with self.assertRaises(ValidationError):
        #     book.full_clean()

    # def test_book_wrong_isbn(self):
    #     """Test if fails creating book with wrong isbn format"""
    #     instance = Book.objects.get(id=1).__dict__
    #     instance.pop('_state')
    #     instance['isbn'] = '979-123-456-789-6'  # Can't start with 976
    #     alter_book = Book(**instance)
    #     with self.assertRaises(ValidationError):
    #         alter_book.full_clean()

    # def test_book_serie_but_not_serie_order(self):
    #     """Test if fails creating book with serie field but serie_order empty"""
    #     instance = Book.objects.get(id=1).__dict__
    #     instance.pop('_state')
    #     instance.pop('serie_order')
    #     alter_book = Book(**instance)
    #     with self.assertRaises(ValidationError):
    #         alter_book.full_clean()





#     # def test_book_serie_order_already_exist(self):
#     #     """Test if fails creating book with an existing serie_order"""
#     #     test_book = self.test_book.copy()
#     #     test_book['serie_order'] = 1  # For the serie 1 serie_order = 1 already exists
#     #     request = self.client.post(BOOKS_URL, test_book)

#     #     self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

# # Category tests ----------------------------------------------------------------------------- #

#     def test_create_category_successfully(self):
#         """Test create category successfully"""
#         request = self.client.post(CATEGORIES_URL, self.test_category)

#         self.assertEqual(request.status_code, status.HTTP_201_CREATED)

#     def test_delete_category_successfully(self):
#         """Checks that it deletes a category correctly"""
#         url = reverse('catalog:category-detail', args=[1])
#         request = self.client.delete(url)

#         self.assertEqual(self.init_categories - 1, Category.objects.count())
#         self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

#     def test_get_category_successfully(self):
#         """Get a category and check that the ids are the same in the queryset
#         and in the data of the request
#         """
#         id_to_filter = 1
#         queryset = Category.objects.get(id=id_to_filter)
#         url = reverse('catalog:category-detail', args=[id_to_filter])
#         request = self.client.get(url)

#         self.assertEqual(request.status_code, status.HTTP_200_OK)
#         self.assertEqual(request.data['id'], queryset.id)

#     def test_update_category_successfully(self):
#         """Test if Update category successfully"""
#         id_to_update = self.test_category['id']
#         instance_before = Category.objects.get(id=id_to_update)
#         url = reverse('catalog:category-detail', args=[id_to_update])
#         request = self.client.patch(url, self.test_category)
#         instance_after = Category.objects.get(id=id_to_update)

#         self.assertEqual(request.status_code, status.HTTP_200_OK)
#         self.assertNotEquals(vars(instance_before), vars(instance_after))

# # Serie tests -------------------------------------------------------------------------------- #

#     def test_create_serie_successfully(self):
#         """Test create serie successfully"""
#         request = self.client.post(SERIES_URL, self.test_serie)

#         self.assertEqual(request.status_code, status.HTTP_201_CREATED)

#     def test_delete_serie_successfully(self):
#         """Checks that it deletes a serie correctly"""
#         url = reverse('catalog:serie-detail', args=[1])
#         request = self.client.delete(url)

#         self.assertEqual(self.init_series - 1, Serie.objects.count())
#         self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

#     def test_get_serie_successfully(self):
#         """Get a serie and check that the ids are the same in the queryset
#         and in the data of the request
#         """
#         id_to_filter = 1
#         queryset = Serie.objects.get(id=id_to_filter)
#         url = reverse('catalog:serie-detail', args=[id_to_filter])
#         request = self.client.get(url)

#         self.assertEqual(request.status_code, status.HTTP_200_OK)
#         self.assertEqual(request.data['id'], queryset.id)

#     def test_update_serie_successfully(self):
#         """Test if Update serie successfully"""
#         id_to_update = self.test_serie['id']
#         instance_before = Serie.objects.get(id=id_to_update)
#         url = reverse('catalog:serie-detail', args=[id_to_update])
#         request = self.client.patch(url, self.test_serie)
#         instance_after = Serie.objects.get(id=id_to_update)

#         self.assertEqual(request.status_code, status.HTTP_200_OK)
#         self.assertNotEquals(vars(instance_before), vars(instance_after))
