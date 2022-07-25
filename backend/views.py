from django.views import render


def vue(request):
    return render(request, "index.html")
