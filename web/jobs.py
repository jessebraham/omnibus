from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import (
    DjangoJobStore,
    register_events,
    register_job,
)

from goodreads.models import Book
from goodreads.schemas import BookSchema
from .helpers import books_read_by_user, create_book


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), alias="default")


@register_job(scheduler, "interval", id="sync", seconds=settings.SYNC_INTERVAL)
def sync_job():
    # Create a set of all read Book IDs, so that we can quickly determine
    # whether or not the Book in question needs to be synced.
    read_book_ids = {b.id for b in Book.objects.all()}

    for result in books_read_by_user():
        book = BookSchema().load(result["book"])
        if book.id not in read_book_ids:
            create_book(book.id, result.get("rating"))


register_events(scheduler)
