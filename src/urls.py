"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_nomand import views as nomand_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('services/experiencesList',nomand_view.ExperienceAPIView.as_view()),
    path('services/LocationCityList',nomand_view.LocationCityAPIView.as_view()),
    path('services/LocationCountryList',nomand_view.LocationCountryAPIView.as_view()),
    path('services/featuredHotels',nomand_view.FeaturedHotelsAPIView.as_view()),
    path('services/search',nomand_view.HotelSearchView.as_view()),
    path('services/reservation',nomand_view.BookingAPIView.as_view()),
    path('services/hotelinfo/<int:id>',nomand_view.HotelInfoAPIView.as_view()),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
