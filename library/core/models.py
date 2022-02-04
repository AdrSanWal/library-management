from datetime import date, timedelta

from django.core.validators import URLValidator
from django.db import models

from .validators import DatesValidator, IsbnValidator, clean_author_dates, clean_series_order


class Author(models.Model):
    name = models.CharField(max_length=50)
    pseudonym = models.CharField(blank=True, max_length=100, null=True)
    born = models.DateField(validators=[DatesValidator()])
    died = models.DateField(blank=True, null=True, validators=[DatesValidator(born)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    indexes = [
        models.Index(fields=['name']),
    ]

    class Meta:
        ordering = ["name"]
        verbose_name = "author"
        verbose_name_plural = "authors"

    def get_books(self, authorship):
        """Return a list with the id of books from the author.
        If authorship == 'many' return the books written by the author
        and those written with another author. If authorship != 'many'
        returns the books written only by the author.
        """
        books = self.rel_author.all()  # All books from author (self)
        if authorship == 'many':
            return [_.id for _ in books]
        return [_.id for _ in books if _.book_writers().count() == 1]

    def delete(self, *args, **kwargs):
        """Delete author, and all his related books that
        have not been written by someone else
        """
        authors_books = self.get_books('one')
        Book.objects.filter(id__in=authors_books).delete()
        super(Author, self).delete(*args, **kwargs)

    def clean(self):
        clean_author_dates(self)
        return super().clean()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(blank=True, max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Serie(models.Model):
    name = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "serie"
        verbose_name_plural = "series"

    def list_order_books(self):
        """Returns a list with the order of books sorted"""
        books = self.rel_serie.all()
        return sorted([book.serie_order for book in books])

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=17,
                            unique=True,
                            validators=[IsbnValidator()])
    title = models.CharField(max_length=255)
    cover = models.URLField(blank=True, validators=[URLValidator])
    authors = models.ManyToManyField(Author, related_name='rel_author')
    description = models.CharField(max_length=1000, blank=True)
    categories = models.ManyToManyField(Category, related_name='rel_category')
    serie = models.ForeignKey(Serie,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name='rel_serie')
    serie_order = models.IntegerField(blank=True, null=True)
    available = models.BooleanField(default=True)
    loan_date = models.DateField(blank=True, null=True)
    expected_return_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = "book"
        verbose_name_plural = "books"
        indexes = [
            models.Index(fields=['title']),
        ]

    def clean(self):
        clean_series_order(self)
        return super().clean()

    def save(self, *args, **kwargs):
        """If there is no cover, a cover image not available is linked to it.
        If available is set to False, the loan date is set as current, and
        the return date as current plus loan_days
        """
        if self.serie_order and not self.serie:
            self.serie_order = None

        if not self.cover:
            self.cover = 'https://islandpress.org/sites/default/files/default_book_cover_2015.jpg'

        loan_days = 7
        if not self.available:
            self.loan_date = date.today()
            self.expected_return_date = self.loan_date + timedelta(loan_days)
        else:
            self.loan_date = None
            self.expected_return_date = None
        return super().save(*args, **kwargs)

    def book_writers(self):
        """Return authors ids"""
        queryset = self.authors.values('id')
        return queryset

    def list_authors(self):
        queryset = self.authors.values('name')
        list_qs = [_['name'] for _ in queryset]
        return list_qs

    def __str__(self):
        return f'{self.isbn}, {self.title}, {self.list_authors()}'
