from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("book/<int:book_id>/", views.book, name="book"),
    path("search/", views.search, name="search"),
    path("series/<int:series_id>/", views.series, name="series"),
    path("sync/<int:user_id>/", views.sync, name="sync"),
]
