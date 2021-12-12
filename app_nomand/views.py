from django.conf import settings
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_admin.models import Admin
from app_nomand.models import Experience, HotelInfo, LocationCity, LocationCountry
from app_nomand.serializers import ExperienceSerializer, FeaturedHotelsSerializer, SearchHotelsSerializer, \
    HotelInfoSerializer, GuestInfoSerializer, BookingInfoSerializer, LocationCitySerializer, LocationCountrySerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from src.utils import NDResponse


class ExperienceAPIView(APIView):
    def get(self,request):
        qs = Experience.objects.all()
        serializer = ExperienceSerializer(qs,many=True,context={"request":request})
        # return Response({"data":serializer.data},status=status.HTTP_200_OK)
        return NDResponse(status.HTTP_200_OK,data=serializer.data)


class LocationCityAPIView(APIView):
    def get(self,request):
        country = request.GET.get("country")
        qs = LocationCity.objects.all()
        if country:
            qs = qs.filter(country_id=country)
        serializer = LocationCitySerializer(qs,many=True)
        # return Response({"data":serializer.data},status=status.HTTP_200_OK)
        return NDResponse(status.HTTP_200_OK,data=serializer.data)


class LocationCountryAPIView(APIView):
    def get(self,request):
        qs = LocationCountry.objects.all()
        serializer = LocationCountrySerializer(qs,many=True)
        # return Response({"data":serializer.data},status=status.HTTP_200_OK)
        return NDResponse(status.HTTP_200_OK,data=serializer.data)


class FeaturedHotelsAPIView(APIView):
    def get(self,request):
        qs = HotelInfo.objects.all()
        serializer = FeaturedHotelsSerializer(qs,many=True)
        # return Response({"data":serializer.data},status=status.HTTP_200_OK)
        return NDResponse(status.HTTP_200_OK,data=serializer.data)


class HotelSearchView(APIView):
    def put(self,request):
        """
        :param request: {
                            "country" : "Sri Lanka",
                            'city": 2,
                            # "checkin" : "ISO FORMAT DATE",
                            # "checkout" : "ISO FORMAT DATE",
                            # "pax" : 2,
                            "ExperianceTags" : [12,34,1]
                        }
        TODO: filtration should have implemented
        :return:
        """
        requestData = request.data
        ex_tag = requestData.get("ExperianceTags",[])
        city = requestData.get("city")
        qs = HotelInfo.objects.all()
        if city:
            qs = qs.filter(location_city__cityid=city)
        if len(ex_tag):
            qs = qs.filter(experiances_tags__expid__in=ex_tag)

        ex_qs = Experience.objects.filter(expid__in=ex_tag)
        ex_serializer = ExperienceSerializer(ex_qs,many=True,context={"request":request})
        serializer = SearchHotelsSerializer(qs, many=True)
        # return Response({"data": serializer.data, "experiences": ex_serializer.data}, status=status.HTTP_200_OK)
        return NDResponse(status.HTTP_200_OK,data=serializer.data,experiences=ex_serializer.data)


class HotelInfoAPIView(APIView):
    def get_object(self, id):
        try:
            return HotelInfo.objects.get(hotelid=id)
        except HotelInfo.DoesNotExist:
            raise Http404

    def get(self,request,id):
        obj = self.get_object(id)
        serializer = HotelInfoSerializer(obj,context={'request':request})
        # return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return NDResponse(status.HTTP_200_OK,data=serializer.data)


class BookingAPIView(APIView):
    def post(self,request):
        """
        :param request: {
                    "guestInfo": {
                        "name": ...
                        "contactNumber": ...
                        "email": ...
                        "country": ...
                    }
                    "bookingInfo":{
                        "reservationItem": ...
                        "checkIn": ...
                        "checkOut": ...
                        //"booking_type": ...

                    }
        }
        :return:
        """

        requestData = request.data
        guest_serializer = GuestInfoSerializer(data=requestData['guestInfo'])
        if guest_serializer.is_valid():
            guest_obj = guest_serializer.save()
        else:
            # return Response({"message": "guest info invalid","data":guest_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return NDResponse(status.HTTP_400_BAD_REQUEST,message="guest info invalid", data=guest_serializer.errors)

        booking_data = requestData['bookingInfo']
        booking_data['guest'] = guest_obj.guestid
        booking_serializer = BookingInfoSerializer(data=booking_data)

        if booking_serializer.is_valid():
            booking_obj = booking_serializer.save()
        else:
            # return Response({"message": "booking info invalid","data":booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return NDResponse(status.HTTP_400_BAD_REQUEST,message="booking info invalid", data=booking_serializer.errors)

        ### send an email to ND admin
        # this segment should move to post signal
        is_email_send = True
        try:
            email_html = get_template('email.html')
            email_context = {
                "guest_name" : guest_obj.name,
                "guest_contact" : guest_obj.contactNumber,
                "guest_email" : guest_obj.email,
                "reservation_item": booking_obj.reservationItem.reservation_item,
                "hotel_name": booking_obj.reservationItem.hotel.name,
                "location": booking_obj.reservationItem.hotel.location,
                "experiences": booking_obj.reservationItem.hotel.experiences_list,
                "checkIn": booking_obj.checkIn,
                "checkOut": booking_obj.checkOut,
            }

            email_content = email_html.render(email_context)
            to_mail = Admin.objects.filter(is_active=True).values_list('email',flat=True)
            _email = EmailMultiAlternatives(subject="New Booking Request",from_email="nomandsdirect.lk <"+settings.EMAIL_HOST_USER+">", to=list(to_mail))
            _email.attach_alternative(email_content,'text/html')
            _email.send()
        except:
            is_email_send = False

        # return Response({"message": "success","data":booking_serializer.data}, status=status.HTTP_200_OK)
        return NDResponse(status.HTTP_201_CREATED,data=booking_serializer.data,is_email_send=is_email_send)


def test(request):
    return render(request,'email.html')