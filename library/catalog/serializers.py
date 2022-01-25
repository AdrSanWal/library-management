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
        read_only_fields = ('id',)

    def delete(self, pk):
        """Delete a Author instance"""
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, validated_data):
        """Create and return a new Author instance,
        given the validated data. Gets the error of validate the model
        """
        return Author.objects.create(**validated_data)

    def validate(self, attrs):
        instance = Author(**dict(attrs))
        try:
            instance.clean()
            return attrs
        except ValidationError as error:
            raise serializers.ValidationError(serializers.as_serializer_error(error))


class CategorySerializer(serializers.ModelSerializer):
    """Serializer of category model"""
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)

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
        read_only_fields = ('id',)

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

    # to show text in api, not ids
    authors = serializers.StringRelatedField(many=True)
    serie = serializers.StringRelatedField(many=False)
    categories = serializers.StringRelatedField(many=True)

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
            'loan_date',
            'expected_return_date',
        ]
        read_only_fields = ('id',)

    def validate(self, attrs):
        # Pops authors and categories because they are many to many field
        # and store them in self.authors and self.categories
        if 'authors' in attrs:
            self.authors = attrs.pop('authors')
        if 'categories' in attrs:
            self.categories = attrs.pop('categories')
        instance = Book(**dict(attrs))
        # self.context['request'].method # method
        try:
            instance.clean()
            return attrs
        except ValidationError as error:
            raise serializers.ValidationError(serializers.as_serializer_error(error))

    def create(self, validated_data):
        """Create and return a new Book instance,
        given the validated data.
        """
        instance = Book.objects.create(**validated_data)

        for author in self.authors:
            instance.authors.add(author)
        for category in self.categories:
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
