from django.conf import settings
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import redirect, render

from goodreads.client import GoodreadsClient
from goodreads.models import Book, Publisher, Series
from goodreads.schemas import BookSchema

from .helpers import books_read_by_user, categorize_by_series, create_book
from .stats import Stats


# ----------------------------------------------------------------------------
# Template Views


def index(request):
    return render(
        request,
        "web/index.html",
        context={"books": categorize_by_series(Book.objects.all())},
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
        request, "web/stats.html", context={"stats": Stats.collection_stats()}
    )


def manage(request):
    if request.method == "POST":
        series_id = request.POST.get("series_id")
        title = request.POST.get("title")
        publisher_name = request.POST.get("name")

        if series_id is not None and title is not None:
            series = Series(id=series_id, title=title, description="")
            series.save()
        elif publisher_name is not None:
            publisher = Publisher(name=publisher_name)
            publisher.save()

    return render(
        request,
        "web/manage.html",
        context={"goodreads_user_id": settings.GOODREADS_USER_ID},
    )


def series(request, series_id):
    books = Book.objects.filter(series__id=series_id)
    series = books[0].series if books else None
    if series is None:
        return redirect("index")

    return render(
        request, "web/series.html", context={"books": books, "series": series}
    )


def edit_series(request, series_id):
    series = Series.objects.get(id=series_id)
    if not series:
        return redirect("index")

    if request.method == "POST":
        series.title = request.POST.get("title", series.title)
        series.save()
        return redirect("series", series_id=series.id)

    return render(request, "web/edit_series.html", context={"series": series})


def book(request, book_id):
    book = Book.objects.get(id=book_id)
    if not book:
        return redirect("index")

    return render(request, "web/book.html", context={"book": book})


def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if not book:
        return redirect("index")

    if request.method == "POST":
        book.title = request.POST.get("title", book.title)
        publisher = request.POST.get("publisher", book.publisher)
        book.publisher = Publisher.objects.get(id=publisher)
        book.series = Series.objects.get(
            id=request.POST.get("series", book.series.id)
        )
        book.save()
        return redirect("book", book_id=book.id)

    return render(
        request,
        "web/edit_book.html",
        context={
            "book": book,
            "publishers": Publisher.objects.order_by(Lower("name")),
            "series": Series.objects.order_by(Lower("title")),
        },
    )


def publisher(request, publisher_id):
    books = Book.objects.filter(publisher__id=publisher_id)
    if not books:
        return redirect("index")

    return render(
        request,
        "web/publisher.html",
        context={
            "books": categorize_by_series(books),
            "publisher": books[0].publisher,
        },
    )


# ----------------------------------------------------------------------------
# AJAX Views


def add(request):
    book_id = request.GET.get("book_id")
    if not book_id:
        return JsonResponse({"success": False, "error": "no book_id provided"})

    create_book(book_id)

    return JsonResponse({"success": True, "error": None})


def remove(request):
    book_id = request.GET.get("book_id")
    if not book_id:
        return JsonResponse({"success": False, "error": "no book_id provided"})

    book = Book.objects.get(id=book_id)
    if not book:
        return JsonResponse(
            {"success": False, "error": "invalid book_id provided"}
        )

    book.delete()

    return JsonResponse({"success": True, "error": None})


def sync(request):
    # Create a set of all read Book IDs, so that we can quickly determine
    # whether or not the Book in question needs to be synced.
    read_book_ids = {b.id for b in Book.objects.all()}

    for result in books_read_by_user():
        book = BookSchema().load(result["book"])
        if book.id not in read_book_ids:
            create_book(book.id, result.get("rating"))

    return redirect("index")
