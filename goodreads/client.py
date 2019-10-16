from collections import OrderedDict

import httpx
import xmltodict

from django.conf import settings


class GoodreadsClient:
    API_URL = "https://www.goodreads.com"

    @classmethod
    def book(cls, book_id):
        return cls._api_request(
            f"{cls.API_URL}/book/show/{book_id}.xml", "book"
        )

    @classmethod
    def search(cls, query, page=1):
        return cls._api_request(
            f"{cls.API_URL}/search/index.xml",
            "search",
            {"q": query, "page": page},
        )

    @classmethod
    def series(cls, work_id):
        return cls._api_request(
            f"{cls.API_URL}/work/{work_id}/series", "series_works"
        )

    @classmethod
    def shelf(cls, user_id, shelf, page=1):
        return cls._api_request(
            f"{cls.API_URL}/review/list/{user_id}.xml",
            "reviews",
            {"shelf": shelf, "page": page, "per_page": 200, "v": 2},
        )

    @classmethod
    def _api_request(cls, url, resp_key, params={}):
        # Ensure the `params` dict always has "key" set to the configured
        # Goodreads API key.
        params.update({"key": settings.GOODREADS_API_KEY})

        # Make the GET request using the provided URL and parameters, raising
        # an exception if an error occurs.
        r = httpx.get(url, params=params, timeout=30)
        r.raise_for_status()

        # Parse the response to a dict, and extract the data under the provided
        # `resp_key`.
        resp = xmltodict.parse(r.content)
        resp = resp["GoodreadsResponse"][resp_key]

        return cls._process_response(resp)

    @classmethod
    def _process_response(cls, data):
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
                # If the '@type' key is present and its value is 'float',
                # convert the value associated with the '#text' key to a
                # float.
                elif "@type" in value and value["@type"] == "float":
                    resp[key] = float(value["#text"])
                # Otherwise, the value is another nested OrderedDict, so we'll
                # recurse.
                else:
                    resp[key] = cls._process_response(value)
            elif type(value) == list:
                # Process each child and associate the resulting values with
                # `key`.
                resp[key] = [cls._process_response(v) for v in value]
            else:
                # If the value is not an OrderedDict, simply carry its
                # key/value forward.
                resp[key] = value

            # Edge case! If there is only one 'work', convert it to a list.
            if key == "work" and type(resp[key]) != list:
                resp[key] = [resp[key]]

        return resp
