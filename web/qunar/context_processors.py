from django.conf import settings
from .utils import province_cities


def cities(request):
    return {
        'province_cities': province_cities,
    }
