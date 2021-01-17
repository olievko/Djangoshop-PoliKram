import requests

from django.apps import apps
from django.conf import settings

from model_search import model_search
from city.models import City


def search_cities(query, limit=None):

    if not query:
        return []

    queryset = model_search(
        query, City.objects.all(), ['city_title', 'area'])

    if limit is not None:
        return queryset[:limit]

    return queryset


def refresh_cities():

    api_domain = 'https://api.novaposhta.ua'

    api_path = '/v2.0/json/Address/getCities'

    api_data = {
        'apiKey': "008535bbb462fbb96fca95ba070a55bf",
        'modelName': 'Address',
        'calledMethod': 'getCities',
    }

    response = requests.post(api_domain + api_path, json=api_data)
    data = response.json()

    if not response.json().get('success'):
        raise Exception(','.join(response.get('errors')))

    City.objects.all().delete()

    cities = []

    for item in data.get('data'):

        params = {
            'city_title': item.get('Description'),
            'region': item.get('SettlementTypeDescription'),
            'area': item.get('AreaDescription'),
        }

        if apps.is_installed('modeltranslation'):

            langs = dict(settings.LANGUAGES)

            if 'uk' in langs:
                params.update({
                    'city_title': item.get('Description'),
                    'region': item.get('SettlementTypeDescription'),
                    'area': item.get('AreaDescription'),
                })

            if 'ru' in langs:
                params.update({
                    'city_title': item.get('DescriptionRu'),
                    'region': item.get('SettlementTypeDescriptionRu'),
                    'area': item.get('AreaDescriptionRu'),
                })

        cities.append(City(**params))

    City.objects.bulk_create(cities)

