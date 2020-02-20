from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from charts import HotelRatingPie, Top10SaleSightsBar, Top10ScoreSightsBar, \
    Top10ExpensiveHotelsBar, HotelPriceHistogram
from .models import Hotel, Sight, City
from .utils import province_cities


def index(request):
    return render(request, 'index.html')


class HotelList(ListView):
    paginate_by = 20

    def get_queryset(self):
        city_name = self.kwargs['city_name']
        if city_name == 'all':
            return Hotel.objects.order_by('seq_no')
        else:
            city = get_object_or_404(City, name=city_name)
            hotels = city.hotels.order_by('seq_no')
            return hotels

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_name = self.kwargs['city_name']
        context['top_10_expensive_hotels_bar_url'] = \
            Top10ExpensiveHotelsBar(city_name).url
        context['hotels_price_histogram_url'] = \
            HotelPriceHistogram(city_name).url
        if city_name != 'all':
            context['city_name'] = self.kwargs['city_name']
        return context


class SightList(ListView):
    paginate_by = 20

    def get_queryset(self):
        city_name = self.kwargs['city_name']
        if city_name == 'all':
            return Sight.objects.order_by('sight_id')
        else:
            city = get_object_or_404(City, name=city_name)
            sights = city.sights.order_by('sight_id')
            return sights

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_name = self.kwargs['city_name']
        context['top_10_sale_sights_bar_url'] = Top10SaleSightsBar(city_name).url
        context['top_10_score_sights_bar_url'] = Top10ScoreSightsBar(city_name).url
        if city_name != 'all':
            context['city_name'] = self.kwargs['city_name']
        return context


def hotel_detail(request, seq_no):
    hotel = Hotel.objects.get(seq_no=seq_no)
    rating_pie_url = HotelRatingPie(hotel.seq_no).url
    return render(request, 'hotel_detail.html',
                  {'hotel': hotel,
                   'rating_pie_url': rating_pie_url})


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
    return redirect(request.META.get('HTTP_REFERER'))


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
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike_sight(request, sight_id):
    user = request.user
    sight = get_object_or_404(Sight, sight_id=sight_id)
    user.sights.remove(sight)
    messages.info(request, '取消成功')
    return redirect('qunar:collections')

def hot_map(request):
    return render(request, 'qunar/hot_map.html')
