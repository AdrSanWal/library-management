from django.contrib import admin

from . import models


class BookAdmin(admin.ModelAdmin):
    list_fields = ('title', 'authors')
    search_fields = ('authors',)
    list_filter = ('authors', 'categories')
    readonly_fields = ('created', 'updated')


class SerieAdmin(admin.ModelAdmin):
    list_fields = ('name',)
    search_fields = ('name',)
    readonly_fields = ('created', 'updated')


class AuthorAdmin(admin.ModelAdmin):
    list_fields = ('name', 'pseudonym')
    readonly_fields = ('created', 'updated')


class CategoryAdmin(admin.ModelAdmin):
    list_fields = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    readonly_fields = ('created', 'updated')


admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Serie, SerieAdmin)
admin.site.register(models.Book, BookAdmin)
