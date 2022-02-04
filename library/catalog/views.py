from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from . import serializers, pagination
from core.models import Book, Author, Category, Serie


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    pagination_class = pagination.CustomPagePagination
    filter_backends = (OrderingFilter,)

    def get_queryset(self):
        """Return all Books except if there are query parameters, in this ViewSet
        you can combine queries in the same order that they have been declared here
        """
        request = self.request.GET
        if 'q' in request:
            self.queryset = self.queryset.filter(title__icontains=request['q'])
        if 'categories' in request:
            self.queryset = self.queryset.filter(categories=request['categories'])
        if 'authors' in request:
            self.queryset = self.queryset.filter(authors=request['authors'])
        if 'own' in request:
            from django.db.models import Q
            # self.queryset = self.queryset.filter(~Q(authors=8), authors=request['own'])
            self.queryset = self.queryset.filter(authors=request['own'])
            own_books = [_.id for _ in self.queryset if _.authors.count() == 1]
            self.queryset = self.queryset.filter(id__in=own_books)
        if 'series' in request:
            self.queryset = self.queryset.filter(serie=request['series'])
        if 'available' in request:
            self.queryset = self.queryset.filter(available=request['available'])
        return self.queryset


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    pagination_class = pagination.CustomPagePagination
    filter_backends = (OrderingFilter,)

    def get_queryset(self):
        """Return all Authors except if there is q in the parameters"""
        request = self.request.GET
        if 'q' in request:
            return self.queryset.filter(name__icontains=request['q'])
        return self.queryset



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = pagination.CustomPagePagination
    filter_backends = (OrderingFilter,)

    def get_queryset(self):
        """Return all Categories except if there is q in the parameters"""
        request = self.request.GET
        if 'q' in request:
            return self.queryset.filter(name__icontains=request['q'])
        return self.queryset


class SerieViewSet(ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = serializers.SerieSerializer
    pagination_class = pagination.CustomPagePagination
    filter_backends = (OrderingFilter,)

    def get_queryset(self):
        """Return all Series except if there is q in the parameters"""
        request = self.request.GET
        if 'q' in request:
            return self.queryset.filter(name__icontains=request['q'])
        return self.queryset
