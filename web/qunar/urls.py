from django.urls import path

from . import views

app_name = 'qunar'

urlpatterns = [
    path('', views.index),
    path('hotels/all', views.hotels_all, name='hotels'),
    path('hotel/<str:seq_no>', views.hotel_detail),
    path('sights/all', views.sights_all, name='sights'),
    path('sight/<int:sight_id>', views.sight_detail),
]

