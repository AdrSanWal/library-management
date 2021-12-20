from django.contrib import admin

from . import models


class BookAdmin(admin.ModelAdmin):
    list_fields = ('title', 'author')
    search_fields = ('author',)
    list_filter = ('author', 'categories')
    readonly_fields = ('created', 'updated')


class SeriesAdmin(admin.ModelAdmin):
    list_fields = ('name',)
    search_fields = ('name',)
    readonly_fields = ('created', 'updated')


class AuthorAdmin(admin.ModelAdmin):
    list_fields = ('full_name', 'pseudonym')
    readonly_fields = ('created', 'updated')


class CategoryAdmin(admin.ModelAdmin):
    list_fields = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    readonly_fields = ('created', 'updated')


admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Series, SeriesAdmin)
admin.site.register(models.Book, BookAdmin)
