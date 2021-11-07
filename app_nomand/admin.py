from django.contrib import admin

# Register your models here.
from app_nomand.models import *

# admin.site.register(ExperienceTags)
admin.site.register(Experience)
admin.site.register(HotelInfo)
admin.site.register(HotelReservationItem)
admin.site.register(HotelAmenities)
admin.site.register(HotelImages)
admin.site.register(LocationCountry)
admin.site.register(LocationCity)
admin.site.register(GuestInfo)
admin.site.register(BookingStatus)
admin.site.register(BookingInfo)
