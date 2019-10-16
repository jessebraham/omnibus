from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("book/<int:book_id>/", views.book, name="book"),
    path("remove/", views.remove, name="remove"),
    path("search/", views.search, name="search"),
    path("series/<int:series_id>/", views.series, name="series"),
    path("stats/", views.stats, name="stats"),
    path("sync/", views.sync, name="sync"),
]
