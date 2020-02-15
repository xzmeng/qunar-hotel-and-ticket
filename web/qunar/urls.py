from django.urls import path

from . import views

app_name = 'qunar'

urlpatterns = [
    path('', views.index),
    path('hotels/all', views.hotels_all, name='hotels'),
    path('hotel/<str:seq_no>', views.hotel_detail, name='hotel_detail'),
    path('hotel/<str:seq_no>/like', views.like_hotel, name='like_hotel'),
    path('hotel/<str:seq_no>/dislike', views.dislike_hotel, name='dislike_hotel'),
    path('sights/all', views.sights_all, name='sights'),
    path('sight/<int:sight_id>', views.sight_detail, name='sight_detail'),
    path('sight/<int:sight_id>/like', views.like_sight, name='like_sight'),
    path('sight/<int:sight_id>/dislike', views.dislike_sight, name='dislike_sight'),
    path('collections', views.collections, name='collections')
]

