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
    author = fields.Nested(AuthorSchema)
    series = fields.Nested(SeriesSchema)
    title = fields.String()
    title_without_series = fields.String()
    description = fields.String(allow_none=True)
    image_url = fields.Url()
    small_image_url = fields.Url(allow_none=True)
    large_image_url = fields.Url(allow_none=True)
    num_pages = fields.Integer(allow_none=True)
    publisher = fields.String(allow_none=True)
    published = fields.Integer(allow_none=True)
    average_rating = fields.Float()
    ratings_count = fields.Integer()

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)
