from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from city.lib import search_cities, refresh_cities


@login_required
def refresh(request):
    refresh_cities()
    return HttpResponse('Cities were successfully refreshed')


def autocomplete(request):

    query = request.GET.get('query')

    suggestions = [c.full_name for c in search_cities(query, limit=10)]

    return JsonResponse({
        'query': query,
        'suggestions': suggestions
    })
