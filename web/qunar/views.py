from django.shortcuts import render

from .models import Hotel, Sight


def index(request):
    return render(request, 'index.html')


def hotels_all(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels_all.html',
                  {'hotels': hotels})


def hotel_detail(request, seq_no):
    hotel = Hotel.objects.get(seq_no=seq_no)
    return render(request, 'hotel_detail.html',
                  {'hotel': hotel})


def sights_all(request):
    sights = Sight.objects.all()
    return render(request, 'sights_all.html',
                  {'sights': sights})


def sight_detail(request, sight_id):
    sight = Sight.objects.get(sight_id=sight_id)
    return render(request, 'sight_detail.html',
                  {'sight': sight})
