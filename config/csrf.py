from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware


class LocalBrowserCsrfViewMiddleware(CsrfViewMiddleware):
    """Allow the in-app browser's opaque origin only for local opt-in runs."""

    def _origin_verified(self, request):
        if (
            settings.LOCAL_BROWSER_ORIGIN_COMPAT
            and request.META.get("HTTP_ORIGIN") == "null"
            and request.scheme == "http"
            and request.get_host().partition(":")[0] in {"127.0.0.1", "localhost"}
            and request.META.get("REMOTE_ADDR") in {"127.0.0.1", "::1"}
        ):
            return True
        return super()._origin_verified(request)

