from django.contrib import admin
from django.db import models
from .models import Province, City, \
    Hotel, HotelRatingStat, HotelComment, Sight


class CityInline(admin.TabularInline):
    model = City


class ProvinceAdmin(admin.ModelAdmin):
    inlines = [
        CityInline,
    ]


class HotelInline(admin.TabularInline):
    model = Hotel

class SightInline(admin.TabularInline):
    model = Sight


class CityAdmin(admin.ModelAdmin):
    inlines = [
        HotelInline,
        SightInline,
    ]


class HotelRatingStatInline(admin.StackedInline):
    model = HotelRatingStat


class HotelCommentInline(admin.TabularInline):
    model = HotelComment


class HotelAdmin(admin.ModelAdmin):
    inlines = [
        HotelRatingStatInline,
        HotelCommentInline
    ]


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelRatingStat)
admin.site.register(HotelComment)
admin.site.register(Sight)
