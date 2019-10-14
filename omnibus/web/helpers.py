from collections import defaultdict

from goodreads.client import GoodreadsClient
from goodreads.models import Author, Book, Series
from goodreads.schemas import SeriesSchema


def sort_books_by_series():
    books = defaultdict(list)

    for book in Book.objects.all():
        if book.series is not None:
            # Use a Tuple consisting of the series title and id as the key,
            # as both are required in the view.
            books[(book.series.title, book.series.id)].append(book)
        else:
            books[("Uncategorized", 0)].append(book)

    return books


def collection_stats():
    books = defaultdict(list)
    for book in Book.objects.all():
        books[book.author.name].append(book)

    try:
        top_author = max(books, key=lambda k: len(books[k]))
        top_author_count = len(
            Book.objects.filter(author__name__exact=top_author)
        )
    except:
        top_author = top_author_count = None

    return {
        "total_authors": Author.objects.count(),
        "total_books": Book.objects.count(),
        "total_series": Series.objects.count(),
        "top_author": top_author,
        "top_author_count": top_author_count,
    }


def books_read_by_user(user_id):
    results = []
    page = 1

    while True:
        resp = GoodreadsClient.shelf(user_id, "read", page)
        results += resp["review"]

        if int(resp["@end"]) >= int(resp["@total"]):
            break

        page += 1

    return results


def try_get_series(work_id):
    try:
        series = GoodreadsClient.series(work_id)
        series = series["series_work"]

        if type(series) == list:
            series = series[0]

        return SeriesSchema().load(series["series"])
    except:
        return None
