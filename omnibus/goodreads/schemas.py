from marshmallow import EXCLUDE, fields, post_load, Schema

from .models import Author, Book, Series


class AuthorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer()
    name = fields.String()

    @post_load
    def make_author(self, data, **kwargs):
        return Author(**data)


class SeriesSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer()
    title = fields.String()
    description = fields.String()

    @post_load
    def make_series(self, data, **kwargs):
        return Series(**data)


class BookSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer()
    title = fields.String()
    author = fields.Nested(AuthorSchema)
    series = fields.Nested(SeriesSchema)
    image_url = fields.Url()
    published = fields.Date()
    average_rating = fields.Float()
    ratings_count = fields.Integer()

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)
