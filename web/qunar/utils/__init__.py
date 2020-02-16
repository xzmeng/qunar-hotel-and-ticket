import os
import json
from django.conf import settings

with open(os.path.join(settings.STATIC_ROOT, 'province_cities.json')) as f:
    province_cities = json.load(f)
