from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

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


@login_required
def collections(request):
    user = request.user
    hotels = user.hotels.all()
    sights = user.sights.all()
    return render(request, 'collections.html',
                  {'hotels': hotels,
                   'sights': sights})

@login_required
def like_hotel(request, seq_no):
    user = request.user
    hotel = get_object_or_404(Hotel, seq_no=seq_no)
    user.hotels.add(hotel)
    messages.info(request, '收藏成功~')
    return redirect('qunar:hotels')

@login_required
def dislike_hotel(request, seq_no):
    user = request.user
    hotel = get_object_or_404(Hotel, seq_no=seq_no)
    user.hotels.remove(hotel)
    messages.info(request, '取消成功')
    return redirect('qunar:collections')

@login_required
def like_sight(request, sight_id):
    user = request.user
    sight = get_object_or_404(Sight, sight_id=sight_id)
    user.sights.add(sight)
    messages.info(request, '收藏成功~')
    return redirect('qunar:sights')

@login_required
def dislike_sight(request, sight_id):
    user = request.user
    sight = get_object_or_404(Sight, sight_id=sight_id)
    user.sights.remove(sight)
    messages.info(request, '取消成功')
    return redirect('qunar:collections')
