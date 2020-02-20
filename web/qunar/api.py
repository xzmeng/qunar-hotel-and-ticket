from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import City, Sight


def get_sight_points(request):
    city_name = request.GET.get('city_name')
    print(repr(city_name))
    if not city_name:
        sights = Sight.objects.all()
    else:
        city = get_object_or_404(City, name=city_name)
        sights = city.sights.all()
    result = []
    for sight in sights:
        lng, lat = sight.point.split(',')
        lng, lat = str(lng), str(lat)
        result.append({
            'lng': lng,
            'lat': lat,
            'count': sight.sale_count
        })
    return JsonResponse(result, safe=False)

