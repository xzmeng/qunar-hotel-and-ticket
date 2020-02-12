from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('hotels/all', views.hotels_all),
    path('hotel/<str:seq_no>', views.hotel_detail),
    path('sights/all', views.sights_all),
    path('sight/<int:sight_id>', views.sight_detail),
]
