from marshmallow import EXCLUDE, fields, post_load, Schema

from .models import Author, Book, Series


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class AuthorSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    role = fields.String(allow_none=True)
    average_rating = fields.Float(allow_none=True)
    ratings_count = fields.Integer(allow_none=True)

    @post_load
    def make_author(self, data, **kwargs):
        return Author(**data)


class SeriesSchema(BaseSchema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    primary_work_count = fields.Integer(allow_none=True)

    @post_load
    def make_series(self, data, **kwargs):
        return Series(**data)


class BookSchema(BaseSchema):
    id = fields.Integer()
    isbn = fields.String(allow_none=True)
    author = fields.Nested(AuthorSchema)
    series = fields.Nested(SeriesSchema)
    title = fields.String()
    description = fields.String(allow_none=True)
    image_url = fields.Url()
    small_image_url = fields.Url(allow_none=True)
    num_pages = fields.Integer(allow_none=True)
    publisher = fields.String(allow_none=True)
    publication_year = fields.Integer(allow_none=True)
    publication_month = fields.Integer(allow_none=True)
    publication_day = fields.Integer(allow_none=True)
    average_rating = fields.Float()
    ratings_count = fields.Integer()
    sequence_number = fields.Integer(allow_none=True)

    @post_load
    def make_book(self, data, **kwargs):
        return Book.create(data)
