from functools import partial

import httplib2
import googleapiclient.http
import google_auth_httplib2


def _build_request_inner(http, *args,  credentials=None, **kwargs):
    new_http = httplib2.Http()
    if credentials is not None:
        new_http = google_auth_httplib2.AuthorizedHttp(credentials, http=new_http)

    return googleapiclient.http.HttpRequest(new_http, *args, **kwargs)


def build_request(credentials=None):
    return partial(_build_request_inner, credentials=credentials)


def is_inside_gce() -> bool:
    """
    Returns True is the client is running in the GCE environment,
    False otherwise.

    Doc: https://cloud.google.com/compute/docs/storing-retrieving-metadata
    """
    h = httplib2.Http()
    try:
        resp_headers, _ = h.request(
            "http://metadata.google.internal/computeMetadata/v1/",
            headers={"metadata-flavor": "Google"},
            method="GET",
        )
    except (httplib2.HttpLib2Error, OSError):
        return False
    return True
