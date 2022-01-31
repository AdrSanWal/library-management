from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from . import serializers, pagination
from core.models import Book, Author, Category, Serie
from rest_framework.response import Response
from rest_framework import status


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    pagination_class = pagination.CustomPagePagination
    filter_backends = (OrderingFilter,)

    def get_queryset(self):
        """Return all Books except if there are query parameters"""
        request = self.request.GET
        if 'q' in request:
            return self.queryset.filter(title__icontains=request['q'])
        if 'series' in request:
            return self.queryset.filter(serie=request['series'])
        if 'authors' in request:
            return self.queryset.filter(authors=request['authors'])
        if 'categories' in request:
            return self.queryset.filter(categories=request['categories'])
        if 'available' in request:
            return self.queryset.filter(available=request['available'])
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
