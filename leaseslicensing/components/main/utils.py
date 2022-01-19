import requests
import json
from datetime import timedelta, date, datetime
import pytz
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection#, Polygon, MultiPolygon, LinearRing


def to_local_tz(_date):
    local_tz = pytz.timezone(settings.TIME_ZONE)
    return _date.astimezone(local_tz)

def check_db_connection():
    """  check connection to DB exists, connect if no connection exists """
    try:
        if not connection.is_usable():
            connection.connect()
    except Exception as e:
        connection.connect()

def _get_params(layer_name):
    return {
        'SERVICE': 'WFS',
        'VERSION': '1.0.0',
        'REQUEST': 'GetFeature',
        'typeName': layer_name,
        'maxFeatures': 50000,
        'outputFormat': 'application/json',
    }

def get_dbca_lands_and_waters_geojson():
    data = cache.get('dbca_legislated_lands_and_waters')
    if not data:
        URL = 'https://kmi.dpaw.wa.gov.au/geoserver/public/ows'
        PARAMS = _get_params('public:dbca_legislated_lands_and_waters')
        res = requests.get(url=URL, params=PARAMS)
        #geo_json = res.json()
        cache.set('dbca_legislated_lands_and_waters',res.json(), settings.LOV_CACHE_TIMEOUT)
        data = cache.get('dbca_legislated_lands_and_waters')
    return data

def get_dbca_lands_and_waters_geos():
    geojson = get_dbca_lands_and_waters_geojson()
    geoms = []
    for feature in geojson.get('features'):
        feature_geom = feature.get('geometry')
        geoms.append(GEOSGeometry('{}'.format(feature_geom)))
    return GeometryCollection(tuple(geoms))
    #return GeometryCollection(geoms)

