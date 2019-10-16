from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment
from webpack_loader.templatetags.webpack_loader import render_bundle


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {"render_bundle": render_bundle, "static": static, "url": reverse}
    )
    return env
