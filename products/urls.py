from django.urls import path
from .views import (
    BookListCreateView, BookDetailView,
    PhoneListCreateView, PhoneDetailView,
    ClothesListCreateView, ClothesDetailView,
)

urlpatterns = [
    # Books
    path("books/", BookListCreateView.as_view(), name="book-list"),
    path("books/<uuid:id>/", BookDetailView.as_view(), name="book-detail"),  # UUID Support

    path("phones/", PhoneListCreateView.as_view(), name="phone-list"),
    path("phones/<uuid:id>/", PhoneDetailView.as_view(), name="phone-detail"),  # UUID Support

    path("clothes/", ClothesListCreateView.as_view(), name="clothes-list"),
    path("clothes/<uuid:id>/", ClothesDetailView.as_view(), name="clothes-detail"),

]
