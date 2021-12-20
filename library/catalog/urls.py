from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, AuthorViewSet, CategoryViewSet, SerieViewSet


router = DefaultRouter()
router.register('books', BookViewSet)
router.register('authors', AuthorViewSet)
router.register('categories', CategoryViewSet)
router.register('series', SerieViewSet)

urlpatterns = [
    path('/', include(router.urls)),
]
