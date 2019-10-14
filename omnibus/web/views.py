from django.http import JsonResponse
from django.shortcuts import redirect, render

from goodreads.client import GoodreadsClient
from goodreads.models import Book
from goodreads.schemas import AuthorSchema, BookSchema

from .helpers import (
    books_read_by_user,
    collection_stats,
    sort_books_by_series,
    try_get_series,
)


def index(request):
    return render(
        request,
        "web/index.html",
        context={"series": sort_books_by_series(), "stats": collection_stats()},
    )


def search(request):
    query = request.POST.get("query")
    if query is not None:
        page = request.POST.get("page", 1)
        context = {
            "results": GoodreadsClient.search(query, page),
            "read": {b.id for b in Book.objects.all()},
        }
    else:
        context = {}

    return render(request, "web/search.html", context=context)


def series(request, series_id):
    books = Book.objects.filter(series__id__exact=series_id)
    series = books[0].series if books else None
    if series is None:
        return redirect("index")

    return render(
        request, "web/series.html", context={"books": books, "series": series}
    )


def book(request, book_id):
    return render(request, "web/book.html")


def add(request):
    book_id = request.GET.get("book_id")
    if not book_id:
        return JsonResponse({"success": False, "error": "no book_id provided"})

    book = GoodreadsClient.book(book_id)
    book = BookSchema().load(book)

    book.series = try_get_series(book["work"][0]["id"])
    if book.series is not None:
        book.series.save()

    book.author.save()
    book.save()

    return JsonResponse({"success": True, "error": None})


def sync(request, user_id):
    author_schema = AuthorSchema()
    book_schema = BookSchema()

    for result in books_read_by_user(user_id):
        book = book_schema.load(result["book"])
        book.author = author_schema.load(result["book"]["authors"]["author"])
        book.series = try_get_series(result["book"]["work"][0]["id"])

        if book.series is not None:
            book.series.save()

        book.author.save()
        book.save()

    return JsonResponse({"success": True, "error": None})
