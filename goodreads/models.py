import re

from django.db import models


class Publisher(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)

    def __repr__(self):
        return f"<Publisher(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"{self.name} (#{self.id})"


class Author(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    role = models.CharField(max_length=64, null=True)
    average_rating = models.FloatField(null=True)
    ratings_count = models.IntegerField(null=True)

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"{self.name} (#{self.id})"


class Series(models.Model):
    class Meta:
        verbose_name_plural = "Series"

    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    primary_work_count = models.IntegerField(null=True)

    def __repr__(self):
        return f"<Series(id={self.id}, title={self.title})>"

    def __str__(self):
        return f"{self.title} (#{self.id})"


class Book(models.Model):
    class Meta:
        ordering = ("sequence_number", "title")

    id = models.BigIntegerField(primary_key=True)
    isbn = models.CharField(max_length=64, null=True)
    authors = models.ManyToManyField(Author)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image_url = models.URLField()
    num_pages = models.IntegerField(null=True)
    publication_year = models.IntegerField(null=True)
    publication_month = models.IntegerField(null=True)
    publication_day = models.IntegerField(null=True)
    average_rating = models.FloatField(null=True)
    ratings_count = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    sequence_number = models.IntegerField(null=True)

    @classmethod
    def create(cls, data):
        book = cls(**data)
        book._set_sequence_number()
        return book

    def _set_sequence_number(self):
        re_seq_number = r"(vol|book|#)[^\d]*(\d+).*"
        m = re.search(re_seq_number, self.title, re.IGNORECASE)

        # Hacky use of exceptions. If the `match` object doesn't have a value
        # at the specified index, or we cannot convert the value to an integer,
        # just give up.
        try:
            self.sequence_number = int(m[2])
        except (KeyError, TypeError):
            pass

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title})>"

    def __str__(self):
        return f"{self.title} (#{self.id})"
