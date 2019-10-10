from collections import OrderedDict

import httpx
import xmltodict

from django.conf import settings


class GoodreadsClient:
    API_URL = "https://www.goodreads.com"

    @classmethod
    def search(cls, query, page=1):
        r = httpx.get(
            f"{cls.API_URL}/search/index.xml",
            params={
                "key": settings.GOODREADS_API_KEY,
                "q": query,
                "page": page,
            },
        )
        r.raise_for_status()

        resp = xmltodict.parse(r.content)
        resp = resp["GoodreadsResponse"]["search"]

        return cls.process_response(resp)

    @classmethod
    def series(cls, work_id):
        r = httpx.get(
            f"{cls.API_URL}/work/{work_id}/series",
            params={"key": settings.GOODREADS_API_KEY},
        )
        r.raise_for_status()

        resp = xmltodict.parse(r.content)
        resp = resp["GoodreadsResponse"]["series_works"]

        return cls.process_response(resp)

    @classmethod
    def process_response(cls, data):
        resp = {}

        if data is None:
            return resp

        for (key, value) in data.items():
            # Satisfy the OCD and make sure all keys are in snake case.
            key = key.lower().replace("-", "_")

            if type(value) == OrderedDict:
                # If the '@nil' key is present and it is set to 'true' (which
                # it always seems to be), there is no data.
                if "@nil" in value:
                    resp[key] = None
                # If the '@type' key is present and its value is 'integer',
                # convert the value associated with the '#text' key to an
                # integer.
                elif "@type" in value and value["@type"] == "integer":
                    resp[key] = int(value["#text"])
                # Otherwise, the value is another nested OrderedDict, so we'll
                # recurse.
                else:
                    resp[key] = cls.process_response(value)
            elif type(value) == list:
                # Process each child and associate the resulting values with
                # `key`.
                resp[key] = [cls.process_response(v) for v in value]
            else:
                # If the value is not an OrderedDict, simply carry its
                # key/value forward.
                resp[key] = value

            # Edge case! If there is only one 'work', convert it to a list.
            if key == "work" and type(resp[key]) != list:
                resp[key] = [resp[key]]

        return resp
