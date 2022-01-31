from datetime import date, timedelta
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


AUTHORS_URL = reverse('catalog:author-list')
BOOKS_URL = reverse('catalog:book-list')
CATEGORIES_URL = reverse('catalog:category-list')
SERIES_URL = reverse('catalog:serie-list')


class SerializerTest(TestCase):

    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = APIClient()
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
        authors_before = len((self.client.get(AUTHORS_URL)).data['results'])
        request = self.client.post(AUTHORS_URL, self.test_author)
        authors_after = len((self.client.get(AUTHORS_URL)).data['results'])

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(authors_before + 1, authors_after)

    def test_update_author_successfully(self):
        """Test if Update author successfully"""
        id_to_update = self.test_author['id']
        url = reverse('catalog:author-detail', args=[id_to_update])
        request = self.client.put(url, self.test_author)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_partial_update_author_successfully(self):
        """Test if Update author successfully with patch"""
        id_to_update = self.test_author['id']
        url = reverse('catalog:author-detail', args=[id_to_update])
        update_field = {'pseudonym': 'Another Test Pseudonym'}
        request = self.client.patch(url, update_field)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_author_successfully(self):
        """Checks that it deletes an author and all his
        books except those written with another author
        """
        m_w_id = 7  # Margaret Weis id
        t_h_id = 8  # Tracy Raye Hickman id
        url = reverse('catalog:author-detail', args=[m_w_id])
        request = self.client.delete(url)

        url_books_m_w = f'{reverse("catalog:book-list")}?authors={m_w_id}'
        request_books_m_w = self.client.get(url_books_m_w)

        url_books_t_h = f'{reverse("catalog:book-list")}?authors={t_h_id}'
        request_books_t_h = self.client.get(url_books_t_h)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(request_books_m_w.data)  # There are no books of Margaret Weis
        self.assertEqual(len(request_books_t_h.data['results']), 7)

    def test_get_author_successfully(self):
        """Get an author and check that the status code is 200"""
        id_to_filter = 1
        url = reverse('catalog:author-detail', args=[id_to_filter])
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_post_date_death_prior_birth(self):
        """Test fail when post a date of death prior to date of birth"""
        test_author = self.test_author.copy()
        test_author['died'] = '1985-11-01'  # Born date is 1985-11-02
        post_request = self.client.post(AUTHORS_URL, test_author)
        error_message = post_request.data['died'][0].title()

        self.assertEqual(error_message, 'Death Date Cannot Be Earlier Than Birth Date')
        self.assertEqual(post_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_date_death_prior_birth(self):
        """Test fail when put a date of death prior to date of birth"""
        test_author = self.test_author.copy()
        test_author['died'] = '1985-11-01'  # Born date is 1985-11-02
        url = reverse('catalog:author-detail', args=[1])
        put_request = self.client.put(url, test_author)
        error_message = put_request.data['died'][0].title()

        self.assertEqual(error_message, 'Death Date Cannot Be Earlier Than Birth Date')
        self.assertEqual(put_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_date_death_prior_birth(self):
        """Test fail when patch a date of death prior to date of birth.
        With patch the date of birth must also be included
        """
        wrong_date = {'born': '1985-11-02', "died": "1985-11-01"}  # Born date is 1985-11-02
        url = reverse('catalog:author-detail', args=[1])
        patch_request = self.client.patch(url, wrong_date)
        error_message = patch_request.data['died'][0].title()

        self.assertEqual(error_message, 'Death Date Cannot Be Earlier Than Birth Date')
        self.assertEqual(patch_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_born_date_not_yet_arrived(self):
        """Test fail when post a born date that has not yet arrived"""
        test_author = self.test_author.copy()
        test_author['born'] = date.today() + timedelta(1)
        post_request = self.client.post(AUTHORS_URL, test_author)
        error_message = post_request.data['born'][0].title()

        self.assertEqual(error_message, 'The Date Has Not Yet Arrived')
        self.assertEqual(post_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_born_date_not_yet_arrived(self):
        """Test fail when put a born date that has not yet arrived"""
        test_author = self.test_author.copy()
        test_author['born'] = date.today() + timedelta(1)
        url = reverse('catalog:author-detail', args=[1])
        put_request = self.client.put(url, test_author)
        error_message = put_request.data['born'][0].title()

        self.assertEqual(error_message, 'The Date Has Not Yet Arrived')
        self.assertEqual(put_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_born_date_not_yet_arrived(self):
        """Test fail when put a born date that has not yet arrived"""
        wrong_date = {'born': date.today() + timedelta(1)}
        url = reverse('catalog:author-detail', args=[1])
        patch_request = self.client.patch(url, wrong_date)
        error_message = patch_request.data['born'][0].title()

        self.assertEqual(error_message, 'The Date Has Not Yet Arrived')
        self.assertEqual(patch_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_death_date_not_yet_arrived(self):
        """Test fail when post death date that has not yet arrived"""
        test_author = self.test_author.copy()
        test_author['died'] = date.today() + timedelta(1)
        post_request = self.client.post(AUTHORS_URL, test_author)
        error_message = post_request.data['died'][0].title()

        self.assertEqual(error_message, 'The Date Has Not Yet Arrived')
        self.assertEqual(post_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_death_date_not_yet_arrived(self):
        """Test fail when put a death date that has not yet arrived"""
        test_author = self.test_author.copy()
        test_author['died'] = date.today() + timedelta(1)
        url = reverse('catalog:author-detail', args=[1])
        put_request = self.client.put(url, test_author)
        error_message = put_request.data['died'][0].title()

        self.assertEqual(error_message, 'The Date Has Not Yet Arrived')
        self.assertEqual(put_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_death_date_not_yet_arrived(self):
        """Test fail when put a death date that has not yet arrived"""
        wrong_date = {'died': date.today() + timedelta(1)}
        url = reverse('catalog:author-detail', args=[1])
        patch_request = self.client.patch(url, wrong_date)
        error_message = patch_request.data['died'][0].title()

        self.assertEqual(error_message, 'The Date Has Not Yet Arrived')
        self.assertEqual(patch_request.status_code, status.HTTP_400_BAD_REQUEST)

# Category tests ----------------------------------------------------------------------------- #

    def test_create_category_successfully(self):
        """Test create category successfully"""
        categories_before = len((self.client.get(CATEGORIES_URL)).data['results'])
        request = self.client.post(CATEGORIES_URL, self.test_category)
        categories_after = len((self.client.get(CATEGORIES_URL)).data['results'])

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(categories_before + 1, categories_after)

    def test_delete_category_successfully(self):
        """Checks that it deletes a category correctly"""
        url = reverse('catalog:category-detail', args=[1])
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_category_successfully(self):
        """Get a category and check that the status code is 200"""
        id_to_filter = 1
        url = reverse('catalog:category-detail', args=[id_to_filter])
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_update_category_successfully(self):
        """Test if Update category successfully"""
        id_to_update = self.test_category['id']
        url = reverse('catalog:category-detail', args=[id_to_update])
        request = self.client.put(url, self.test_category)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_partial_update_category_successfully(self):
        """Test if Update category successfully with patch"""
        id_to_update = self.test_category['id']
        url = reverse('catalog:category-detail', args=[id_to_update])
        update_field = {'description': 'Another Test Description'}
        request = self.client.patch(url, update_field)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

# Serie tests -------------------------------------------------------------------------------- #

    def test_create_serie_successfully(self):
        """Test create serie successfully"""
        series_before = len((self.client.get(SERIES_URL)).data['results'])
        request = self.client.post(SERIES_URL, self.test_serie)
        series_after = len((self.client.get(SERIES_URL)).data['results'])

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(series_before + 1, series_after)

    def test_delete_serie_successfully(self):
        """Checks that it deletes a serie correctly"""
        url = reverse('catalog:serie-detail', args=[1])
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_serie_successfully(self):
        """Get a serie and check that the status response is 200"""
        id_to_filter = 1
        url = reverse('catalog:serie-detail', args=[id_to_filter])
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_update_serie_successfully(self):
        """Test if Update serie successfully"""
        id_to_update = self.test_serie['id']
        url = reverse('catalog:serie-detail', args=[id_to_update])
        request = self.client.put(url, self.test_serie)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_partial_update_serie_successfully(self):
        """Test if Update serie successfully with patch"""
        id_to_update = self.test_serie['id']
        url = reverse('catalog:serie-detail', args=[id_to_update])
        update_field = {'name': 'Another Test Name'}
        request = self.client.patch(url, update_field)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

# Book tests --------------------------------------------------------------------------------- #

    def test_create_book_successfully(self):
        """Test create book successfully"""
        books_before = len((self.client.get(BOOKS_URL)).data['results'])
        request = self.client.post(BOOKS_URL, self.test_book)
        books_after = len((self.client.get(BOOKS_URL)).data['results'])

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(books_before + 1, books_after)

    def test_delete_book_successfully(self):
        """Checks that it deletes a book correctly"""
        url = reverse('catalog:book-detail', args=[1])
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_book_successfully(self):
        """Get a book and check that the status response in 200"""
        id_to_filter = 1
        url = reverse('catalog:book-detail', args=[id_to_filter])
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_update_book_successfully(self):
        """Test if Update book successfully"""
        id_to_update = self.test_book['id']
        url = reverse('catalog:book-detail', args=[id_to_update])
        request = self.client.patch(url, self.test_book)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_book_wrong_control_digit(self):
        """Test if fails creating book with wrong control digit"""
        test_book = self.test_book.copy()
        test_book['isbn'] = '979-123-456-789-0'  # Correct digit is 6
        request = self.client.post(BOOKS_URL, test_book)
        error_message = request.data['isbn'][0].title()

        self.assertEqual(error_message, 'Format Correct But Control Digit Should Be 6')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_wrong_isbn(self):
        """Test if fails creating book with wrong isbn format"""
        test_book = self.test_book.copy()
        test_book['isbn'] = '976-123-456-789-6'  # 976 initial numbers are incorrect
        request = self.client.post(BOOKS_URL, test_book)
        error_message = request.data['isbn'][0].title()

        self.assertEqual(error_message, 'Your String Should Match The Conditions')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_serie_but_not_serie_order(self):
        """Test if fails creating book with serie field but serie_order empty"""
        test_book = self.test_book.copy()
        test_book.pop('serie_order')
        request = self.client.post(BOOKS_URL, test_book)
        error_message = request.data['serie_order'][0].title()

        self.assertEqual(error_message, 'If The Book Is From A Serie, It Must Have Serie_Order')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_serie_order_already_exist(self):
        """Test if fails creating book with an existing serie_order"""
        test_book = self.test_book.copy()
        test_book['serie_order'] = 1  # For the serie 1 serie_order = 1 already exists
        request = self.client.post(BOOKS_URL, test_book)
        error_message = request.data['serie_order'][0].title()

        self.assertEqual(error_message, 'This Order In The Serie Is Already Taken.\nUsed Orders: [1, 2, 3, 4, 5, 6]')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
