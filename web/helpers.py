from collections import defaultdict

from django.conf import settings

from goodreads.client import GoodreadsClient
from goodreads.models import Author, Book, Publisher, Series
from goodreads.schemas import AuthorSchema, BookSchema, SeriesSchema


def categorize_by_series(book_list):
    books = defaultdict(list)

    for book in book_list:
        if book.series is not None:
            # Use a Tuple consisting of the series title and id as the key,
            # as both are required in the view.
            books[(book.series.title, book.series.id)].append(book)
        else:
            # The Uncategorized series is created automatically during database
            # migration.
            books[("Uncategorized", 0)].append(book)

    return books


def collection_stats():
    return {
        "totals": _totals_stats(),
        "authors": _author_stats(),
        "series": _longest_series_stats(),
        "publishers": _publisher_stats(),
    }


def _totals_stats():
    total_pages = sum(
        b.num_pages if b.num_pages else 0 for b in Book.objects.all()
    )

    return {
        "authors": Author.objects.count(),
        "series": Series.objects.count(),
        "books": Book.objects.count(),
        "pages": f"{total_pages:,}",
    }


def _author_stats():
    books = defaultdict(list)

    # Query all Books and sort them by Author name.
    for book in Book.objects.all():
        for author in book.authors.all():
            books[author.name].append(book)

    # Attempt to determine the top Author, as well as how many Books they have
    # in the collection.
    try:
        top_author = max(books, key=lambda k: len(books[k]))
        top_author_count = len(books[top_author])
        top_author_pages = sum(
            b.num_pages if b.num_pages else 0 for b in books[top_author]
        )
    except:
        top_author = None
        top_author_count = top_author_pages = 0

    return {
        "top": top_author,
        "count": top_author_count,
        "pages": f"{top_author_pages:,}",
    }


def _longest_series_stats():
    books = defaultdict(list)

    # Query all Books and sort them by Series title.
    for book in Book.objects.all():
        books[book.series.title].append(book)

    longest = None
    num_pages = 0

    for (series_title, series) in books.items():
        series_pages = sum(b.num_pages if b.num_pages else 0 for b in series)
        if series_pages > num_pages:
            longest = series_title
            num_pages = series_pages

    return {"longest": longest, "pages": f"{num_pages:,}"}


def _publisher_stats():
    books = defaultdict(list)

    for book in Book.objects.all().order_by("publisher"):
        books[book.publisher].append(book)

    return {key: len(value) for (key, value) in books.items()}


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
        uncategorized = Series.objects.get(id=0)
        return uncategorized


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


def create_book(book_id, rating=None):
    resp = GoodreadsClient.book(book_id)

    book = BookSchema().load(resp)
    book.save()

    resp_author = resp["authors"]["author"]
    if type(resp_author) != list:
        resp_author = [resp_author]

    for author in resp_author:
        a = AuthorSchema().load(author)
        a.save()
        book.authors.add(a)

    book.series = try_get_series(resp["work"][0]["id"])
    book.series.save()

    resp_publisher = resp["publisher"]
    if resp_publisher:
        (pub, created) = Publisher.objects.get_or_create(name=resp_publisher)
        book.publisher = pub

    if rating is not None and rating != 0:
        book.rating = rating

    book.save()
