from django.urls import path

from . import views

app_name = 'qunar'

urlpatterns = [
    path('', views.index),

    path('hotels/<str:city_name>', views.HotelList.as_view(), name='hotels'),
    path('sights/<str:city_name>', views.SightList.as_view(), name='sights'),

    path('hotel/<str:seq_no>', views.hotel_detail, name='hotel_detail'),
    path('hotel/<str:seq_no>/like', views.like_hotel, name='like_hotel'),
    path('hotel/<str:seq_no>/dislike', views.dislike_hotel, name='dislike_hotel'),

    path('sight/<int:sight_id>', views.sight_detail, name='sight_detail'),
    path('sight/<int:sight_id>/like', views.like_sight, name='like_sight'),
    path('sight/<int:sight_id>/dislike', views.dislike_sight, name='dislike_sight'),
    path('collections', views.collections, name='collections')
]

