from collections import defaultdict

from django.http import JsonResponse
from django.shortcuts import redirect, render

from goodreads.client import GoodreadsClient
from goodreads.models import Author, Book, Series
from goodreads.schemas import BookSchema, SeriesSchema


def index(request):
    series = defaultdict(list)
    for book in Book.objects.all():
        if book.series is not None:
            series[book.series.title].append(book)
        else:
            series["Uncategorized"].append(book)

    return render(
        request,
        "web/index.html",
        context={
            "series": series,
            "num_authors": Author.objects.count(),
            "num_books": Book.objects.count(),
            "num_series": Series.objects.count(),
        },
    )


def search(request):
    query = request.POST.get("query")
    if query is not None:
        results = GoodreadsClient.search(query)
        request.session["search_results"] = results
        context = {
            "results": results,
            "read": [b.id for b in Book.objects.all()],
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

    works = request.session["search_results"]["results"]["work"]
    work = next(w for w in works if w["best_book"]["id"] == int(book_id))

    try:
        series = GoodreadsClient.series(work["id"])
        series = series["series_work"]
        if type(series) == list:
            series = series[0]
        series = series["series"]
        series = SeriesSchema().load(series)
    except:
        series = None

    book = BookSchema().load(work["best_book"])
    book.series = series

    book.author.save()
    if book.series is not None:
        book.series.save()
    book.save()

    return JsonResponse({"success": True, "errors": []})
