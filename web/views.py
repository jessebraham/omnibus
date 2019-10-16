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
        request, "web/index.html", context={"series": sort_books_by_series()}
    )


def search(request):
    query = request.GET.get("query")
    if query is not None:
        page = request.GET.get("page", 1)
        context = {
            "results": GoodreadsClient.search(query, page),
            "read": {b.id for b in Book.objects.all()},
            "page": page,
        }
    else:
        context = {}

    return render(request, "web/search.html", context=context)


def stats(request):
    return render(
        request, "web/stats.html", context={"stats": collection_stats()}
    )


def series(request, series_id):
    # Retrieve a list of all Book objects with a Series matching the provided
    # series ID, ordered by their titles.
    books = Book.objects.filter(series__id__exact=series_id).order_by("title")

    # If any Books are returned, they all have the same Series; store the
    # Series of the first result. Otherwise, the specified Series does not
    # exist to simply redirect back to the Index.
    series = books[0].series if books else None
    if series is None:
        return redirect("index")

    return render(
        request, "web/series.html", context={"books": books, "series": series}
    )


def book(request, book_id):
    book = Book.objects.get(id=book_id)
    if not book:
        return redirect("index")

    return render(request, "web/book.html", context={"book": book})


def add(request):
    book_id = request.GET.get("book_id")
    if not book_id:
        return JsonResponse({"success": False, "error": "no book_id provided"})

    resp = GoodreadsClient.book(book_id)
    book = BookSchema().load(resp)

    book.series = try_get_series(resp["work"][0]["id"])
    if book.series is not None:
        book.series.save()

    book.author = AuthorSchema().load(resp["authors"]["author"][0])
    book.author.save()

    book.save()

    return JsonResponse({"success": True, "error": None})


def remove(request):
    book_id = request.GET.get("book_id")
    if not book_id:
        return JsonResponse({"success": False, "error": "no book_id provided"})

    book = Book.objects.get(id=book_id)
    if not book:
        return JsonResponse({"success": False, "error": "invalid book_id provided"})

    book.delete()

    return JsonResponse({"success": True, "error": None})


def sync(request):
    author_schema = AuthorSchema()
    book_schema = BookSchema()

    for result in books_read_by_user():
        book = book_schema.load(result["book"])
        book.author = author_schema.load(result["book"]["authors"]["author"])
        book.series = try_get_series(result["book"]["work"][0]["id"])

        if book.series is not None:
            book.series.save()

        book.author.save()
        book.save()

    return redirect("stats")
