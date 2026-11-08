from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .analysis import analyze


@require_http_methods(["GET", "POST"])
def home(request):
    context = {}
    if request.method == "POST":
        text = request.POST.get("content", "")
        try:
            context["result"] = analyze(text)
        except ValueError as exc:
            context["error"] = str(exc)
        # O conteúdo enviado não é devolvido à página, gravado ou enviado a terceiros.
    response = render(request, "checker/home.html", context)
    response["Cache-Control"] = "no-store"
    response["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
    return response
