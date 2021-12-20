from rest_framework import serializers

from core import models


class BookSerializer(serializers.ModelSerializer):
    """Serializer of book model"""
    class Meta:
        model = models.Book
        fields = ['id', 'isbn', 'title']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer of author model"""
    class Meta:
        model = models.Author
        fields = ['id', 'full_name']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer of category model"""
    class Meta:
        model = models.Category
        fields = ['id', 'name']


class SerieSerializer(serializers.ModelSerializer):
    """Serializer of category model"""
    class Meta:
        model = models.Serie
        fields = ['id', 'name']
