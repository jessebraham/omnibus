import os

from django.apps import AppConfig


class WebConfig(AppConfig):
    name = "web"

    def ready(self):
        # When using the development server, `ready` is invoked twice; this
        # prevents the scheduler from being started twice, since the call to
        # `start` is not idempotent.
        if os.environ.get("RUN_MAIN") == "true":
            from .jobs import scheduler

            scheduler.start()
