from django.core.validators import RegexValidator
from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=50)
    pseudonym = models.CharField(blank=True, max_length=100, null=True)
    born = models.DateField()
    died = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "author"
        verbose_name_plural = "authors"

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(blank=True, max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    isbn_error_message = "Your string should match the conditions"

    pattern = r'^(?=.{17}$)(^97(9|8)-\d{1,5}-\d{1,7}-\d{1,6}-\d$)'
    validator = RegexValidator(pattern, isbn_error_message)

    isbn = models.CharField(max_length=17, unique=True, validators=[validator])
    title = models.CharField(max_length=255)
    cover = models.URLField(default='https://islandpress.org/sites/default/files/default_book_cover_2015.jpg')
    author = models.ManyToManyField(Author, related_name='rel_author')
    description = models.CharField(max_length=1000, blank=True)
    categories = models.ManyToManyField(Category, related_name='rel_category')
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    series_order = models.IntegerField(blank=True, null=True)
    available = models.BooleanField(default=True)
    loan_date = models.DateField(blank=True, null=True)
    expected_return_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "book"
        verbose_name_plural = "books"

    def list_authors(self):
        queryset = self.author.values('full_name')
        list_qs = [_['full_name'] for _ in queryset]
        return list_qs

    def __str__(self):
        return f'{self.isbn}, {self.title}, {self.list_authors()}'
