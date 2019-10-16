from collections import defaultdict

from django.conf import settings

from goodreads.client import GoodreadsClient
from goodreads.models import Author, Book, Series
from goodreads.schemas import SeriesSchema


def sort_books_by_series():
    books = defaultdict(list)

    # FIXME: ordering by title doesn't always work due to inconsistent
    # formatting of titles.
    for book in Book.objects.order_by("title"):
        if book.series is not None:
            # Use a Tuple consisting of the series title and id as the key,
            # as both are required in the view.
            books[(book.series.title, book.series.id)].append(book)
        else:
            books[("Uncategorized", 0)].append(book)

    return books


def collection_stats():
    (top_author, top_author_count) = _top_author_stats()
    (longest_series, num_pages) = _longest_series_stats()

    return {
        "total_authors": Author.objects.count(),
        "total_books": Book.objects.count(),
        "total_series": Series.objects.count(),
        "top_author": top_author,
        "top_author_count": top_author_count,
        "longest_series": longest_series,
        "longest_series_num_pages": num_pages,
    }


def _top_author_stats():
    books = defaultdict(list)

    # Query all Books and sort them by Author.
    for book in Book.objects.all():
        books[book.author.name].append(book)

    # Attempt to determine the top Author, as well as how many Books they have
    # in the collection.
    try:
        top_author = max(books, key=lambda k: len(books[k]))
        top_author_count = len(books[top_author])
    except:
        top_author = top_author_count = None

    return (top_author, top_author_count)


def _longest_series_stats():
    books = defaultdict(list)

    # Query all Books and sort them by Series.
    for book in Book.objects.all():
        if book.series:
            books[book.series.title].append(book)

    longest = None
    num_pages = 0

    for (series_title, series) in books.items():
        series_pages = sum(b.num_pages if b.num_pages else 0 for b in series)
        if series_pages > num_pages:
            longest = series_title
            num_pages = series_pages

    return (longest, num_pages)


def try_get_series(work_id):
    try:
        series = GoodreadsClient.series(work_id)
        series = series["series_work"]

        # FIXME: probably shouldn't just select the first option automatically
        # if there are multiple choices...
        if type(series) == list:
            series = series[0]

        return SeriesSchema().load(series["series"])
    except:
        return None


def books_read_by_user():
    results = []
    page = 1

    while True:
        resp = GoodreadsClient.shelf(settings.GOODREADS_USER_ID, "read", page)
        results += resp["review"]

        if int(resp["@end"]) >= int(resp["@total"]):
            break

        page += 1

    return results
