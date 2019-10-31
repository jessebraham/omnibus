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
    print(book)
