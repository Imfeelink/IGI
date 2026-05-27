import logging

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger('apps.api')

MINSK_LAT = 53.9
MINSK_LON = 27.5667


@login_required
def external_data_view(request):
    weather = fetch_weather()
    exchange = fetch_exchange_rates()
    return render(
        request,
        'api/external_data.html',
        {'weather': weather, 'exchange': exchange},
    )


def fetch_weather():
    try:
        if settings.OPENWEATHER_API_KEY:
            url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {
                'lat': MINSK_LAT,
                'lon': MINSK_LON,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric',
                'lang': 'ru',
            }
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return {
                'source': 'OpenWeatherMap',
                'city': data.get('name', settings.DEFAULT_CITY),
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
            }
        url = 'https://api.open-meteo.com/v1/forecast'
        params = {
            'latitude': MINSK_LAT,
            'longitude': MINSK_LON,
            'current_weather': True,
            'timezone': 'Europe/Minsk',
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()['current_weather']
        return {
            'source': 'Open-Meteo',
            'city': settings.DEFAULT_CITY,
            'temp': data['temperature'],
            'description': f"Ветер {data['windspeed']} км/ч",
            'humidity': '—',
        }
    except requests.RequestException as exc:
        logger.error('Weather API error: %s', exc)
        return {'error': str(exc)}


def fetch_exchange_rates():
    try:
        url = 'https://api.frankfurter.app/latest'
        params = {'from': 'USD', 'to': 'BYN,EUR,RUB'}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            'source': 'Frankfurter API',
            'date': data.get('date'),
            'base': data.get('base'),
            'rates': data.get('rates', {}),
        }
    except requests.RequestException as exc:
        logger.error('Exchange API error: %s', exc)
        return {'error': str(exc)}
