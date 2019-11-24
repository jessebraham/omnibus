import os

from django.apps import AppConfig
from django.conf import settings


class WebConfig(AppConfig):
    name = "web"

    def ready(self):
        debug = settings.DEBUG
        run_main = os.environ.get("RUN_MAIN") != "true"

        # When using the development server, `ready` is invoked twice; since
        # the call to `start` is not idempotent, we need to prevent it from
        # being called a second time.
        # HOWEVER, the value of `RUN_MAIN` we're looking for depends on whether
        # we're in development or production mode. This is a major pain in the
        # ass.
        if (debug and not run_main) or (not debug and run_main):
            from .jobs import scheduler

            scheduler.start()
