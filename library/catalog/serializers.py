from django.core.exceptions import ValidationError

from rest_framework import serializers, status
from rest_framework.response import Response

from core.models import Author, Book, Category, Serie


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer of author model"""
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ('id', 'created')

    def validate(self, attrs):
        instance = Author(**dict(attrs))
        try:
            instance.clean()
            return attrs
        except ValidationError as error:
            raise serializers.ValidationError(serializers.as_serializer_error(error))

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

    def update(self, instance, validated_data):
        """Update and return an Author instance,
        given the validated data. Gets the error of validate the model
        """
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer of category model"""
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id', 'created')


class SerieSerializer(serializers.ModelSerializer):
    """Serializer of category model"""
    class Meta:
        model = Serie
        fields = '__all__'
        read_only_fields = ('id', 'created')


class BookSerializer(serializers.ModelSerializer):
    """Serializer of book model"""
    available = serializers.BooleanField(initial=True)

    # to show text in api, not ids
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["authors"] = AuthorSerializer(instance.authors, many=True).data
        representation["categories"] = CategorySerializer(instance.categories, many=True).data
        if representation["serie"]:
            representation["serie"] = SerieSerializer(instance.serie, many=False).data
        return representation

    def to_internal_value(self, data):
        if not self.partial:  # for post and put

            data['available'] = True if data['available']=='' else data['available']
            print(data)
            data['authors'] = [int(author['id']) for author in data['authors']]
            data['categories'] = [int(category['id']) for category in data['categories']]
            if data['serie'] == '':
                data = {**data, **{'serie': None, 'serie_order': None}}  # serie is not required
            else:
                data['serie'] = data['serie']['id']
        return super().to_internal_value(data)

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
        read_only_fields = ('id', 'created')

    def validate(self, attrs):
        # Pops authors and categories because they are many to many field
        # and store them in self.authors and self.categories
        if 'authors' in attrs:
            self.authors = attrs.pop('authors')
        if 'categories' in attrs:
            self.categories = attrs.pop('categories')
        instance = Book(**dict(attrs))
        try:
            instance.clean()
            if not self.partial:
                attrs.update({'authors': self.authors})
                attrs.update({'categories': self.categories})
            return attrs
        except ValidationError as error:
            raise serializers.ValidationError(serializers.as_serializer_error(error))

    def delete(self, pk):
        """Delete a Book instance"""
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
