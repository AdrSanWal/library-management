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
        # print('ha entrado en create--------------------------------')
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
        read_only_fields = ('id',)


class SerieSerializer(serializers.ModelSerializer):
    """Serializer of category model"""
    class Meta:
        model = Serie
        fields = '__all__'
        read_only_fields = ('id',)


# class CustomFields(serializers.RelatedField):
#     def to_representation(self, instance):
#         return instance.name

#     def to_internal_value(self, data):
#         print('data', data.id)
#         return data


class BookSerializer(serializers.ModelSerializer):
    """Serializer of book model"""
    available = serializers.BooleanField(initial=True)

    # authors = CustomFields(many=True, queryset=Author.objects.all())
    # serie = CustomFields(many=False, queryset=Serie.objects.all(), required=False)
    # categories = CustomFields(many=True, queryset=Category.objects.all())

    # def to_representation(self, instance):
    #     return instance.name

    # to show text in api, not ids
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        authors = AuthorSerializer(instance.authors.all(), many=True).data
        representation["authors"] = [author['name'] for author in authors]
        categories = CategorySerializer(instance.categories.all(), many=True).data
        representation["categories"] = [category['name'] for category in categories]
        serie = SerieSerializer(instance.serie, many=False).data
        representation["serie"] = serie['name']
        return representation

    def to_internal_value(self, data):
        print(self)
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
        read_only_fields = ('id',)

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
            return attrs
        except ValidationError as error:
            raise serializers.ValidationError(serializers.as_serializer_error(error))

    def delete(self, pk):
        """Delete a Book instance"""
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

    def update(self, instance, validated_data):
        """Update a Book instance"""
        return super().update(instance, validated_data)
