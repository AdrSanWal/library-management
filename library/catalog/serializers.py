from datetime import date
from django.core.exceptions import ValidationError

from rest_framework import serializers, status
from rest_framework.response import Response

from core.models import Author, Book, Category, Serie


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer of author model"""
    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        """Create and return a new Author instance,
        given the validated data. Gets the error of validate the model
        """
        instance = Author(**validated_data)
        try:
            instance.clean()
            instance.save()
        except ValidationError as error:
            raise serializers.ValidationError(serializers.as_serializer_error(error))
        return instance

    def delete(self, pk):
        """Delete a Author instance"""
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer of category model"""
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        """Create and return a new Category instance,
        given the validated data.
        """
        return Category.objects.create(**validated_data)

    def delete(self, pk):
        """Delete a Serie instance"""
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SerieSerializer(serializers.ModelSerializer):
    """Serializer of category model"""
    class Meta:
        model = Serie
        fields = '__all__'

    def create(self, validated_data):
        """Create and return a new Serie instance,
        given the validated data.
        """
        return Serie.objects.create(**validated_data)

    def delete(self, pk):
        """Delete a Serie instance"""
        serie = self.get_object(pk)
        serie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookSerializer(serializers.ModelSerializer):
    """Serializer of book model"""
    available = serializers.BooleanField(initial=True)

    class Meta:

        model = Book
        fields = [
            'id',
            'isbn',
            'title',
            'authors',
            'cover',
            'description',
            'categories',
            'serie',
            'serie_order',
            'available',
        ]

    def create(self, validated_data):
        """Create and return a new Book instance,
        given the validated data.
        """
        # Pops authors and categories because they are many to many field
        authors = validated_data.pop('authors')
        categories = validated_data.pop('categories')

        instance = Book(**validated_data)

        try:
            instance.clean()
            instance.save()
        except ValidationError as error:
            raise serializers.ValidationError(serializers.as_serializer_error(error))

        for author in authors:
            instance.authors.add(author)
        for category in categories:
            instance.categories.add(category)
        return instance

    def delete(self, pk):
        """Delete a Book instance"""
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, instance, validated_data):
        """Update a book instance"""
        return super().update(instance, validated_data)
