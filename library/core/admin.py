from django.contrib import admin

from . import models

admin.site.register(models.Author)
admin.site.register(models.Category)
admin.site.register(models.Series)
admin.site.register(models.Book)
