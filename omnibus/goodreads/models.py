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
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)
    image_url = models.CharField(max_length=255)
    published = models.DateField(null=True)

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title})>"

    def __str__(self):
        return f"{self.title} ({self.id})"
