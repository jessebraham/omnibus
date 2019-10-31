from collections import defaultdict

from django.db.models.functions import Lower

from goodreads.models import Author, Book, Publisher, Series


class Stats:
    @classmethod
    def collection_stats(cls):
        return {
            "totals": cls.totals(),
            "authors": cls.authors(),
            "series": cls.series(),
            "publishers": cls.publishers(),
        }

    @classmethod
    def totals(cls):
        total_authors = len(
            {a for b in Book.objects.all() for a in b.authors.all()}
        )
        total_series = len({b.series for b in Book.objects.all() if b.series})
        total_publishers = len(
            {b.publisher for b in Book.objects.all() if b.publisher}
        )
        total_pages = sum(cls.count_pages({None: Book.objects.all()}).keys())

        # Since we create the Uncategorized Series automatically, and it's not
        # technically a Series, don't count it in the stats.
        return {
            "authors": Author.objects.count(),
            "series": total_series - 1,
            "books": Book.objects.count(),
            "publishers": total_publishers,
            "pages": f"{total_pages:,}",
        }

    @classmethod
    def authors(cls):
        books = defaultdict(list)

        # Query all Books and sort them by their Authors' names.
        for book in Book.objects.all():
            for author in book.authors.all():
                books[author.name].append(book)

        # Sum the number of pages of each book read.
        author_totals = cls.count_pages(books)

        # Extract the top 3 highest-valued keys from the Author page totals, and
        # return the stats for each.
        return [
            {
                "name": author_totals[key],
                "books": len(books[author_totals[key]]),
                "pages": f"{key:,}",
            }
            for key in cls.top_n(author_totals.keys(), 3)
        ]

    @classmethod
    def series(cls):
        books = defaultdict(list)

        # Query all Books and sort them by their Series' title. Ignore the
        # Uncategorized series (ie series.id == 0).
        for book in Book.objects.all():
            if book.series is not None and book.series.id != 0:
                books[book.series.title].append(book)

        # Sum the number of pages of each book read.
        series_totals = cls.count_pages(books)

        # Extract the top 3 highest-valued keys from the Series page totals, and
        # return the stats for each.
        series_stats = []
        for key in cls.top_n(series_totals.keys(), 3):
            title = series_totals[key]
            series = books[title][0].series
            series_stats.append(
                {
                    "id": series.id,
                    "title": title,
                    "books": len(books[title]),
                    "pages": f"{key:,}",
                }
            )

        return series_stats

    @staticmethod
    def publishers():
        books = defaultdict(list)

        for book in Book.objects.order_by(Lower("publisher__name")):
            books[book.publisher].append(book)

        return {key: len(value) for (key, value) in books.items()}

    @staticmethod
    def count_pages(books):
        totals = {}
        for (name, series) in books.items():
            pages = sum(b.num_pages if b.num_pages else 0 for b in series)
            totals[pages] = name
        return totals

    @staticmethod
    def top_n(keys, count):
        return list(sorted(keys, reverse=True))[:count]
