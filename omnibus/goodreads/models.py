from django.db import models


class Author(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"{self.name} ({self.id})"


class Series(models.Model):
    class Meta:
        verbose_name_plural = "Series"

    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __repr__(self):
        return f"<Series(id={self.id}, title={self.title})>"

    def __str__(self):
        return f"{self.title} ({self.id})"


class Book(models.Model):
    id = models.BigIntegerField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    title_without_series = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    image_url = models.CharField(max_length=255)
    small_image_url = models.CharField(max_length=255, null=True)
    large_image_url = models.CharField(max_length=255, null=True)
    num_pages = models.IntegerField(null=True)
    publisher = models.CharField(max_length=64, null=True)
    published = models.IntegerField(null=True)
    average_rating = models.FloatField(null=True)
    ratings_count = models.IntegerField(null=True)

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title})>"

    def __str__(self):
        return f"{self.title} ({self.id})"
