from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("books/<int:book_id>/", views.book, name="book"),
    path("books/<int:book_id>/edit/", views.edit_book, name="edit_book"),
    path("remove/", views.remove, name="remove"),
    path("search/", views.search, name="search"),
    path("series/<int:series_id>/", views.series, name="series"),
    path("series/<int:series_id>/edit/", views.edit_series, name="edit_series"),
    path("stats/", views.stats, name="stats"),
    path("sync/", views.sync, name="sync"),
]
