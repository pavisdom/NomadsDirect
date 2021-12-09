from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_nomand.models import Experience, HotelInfo, LocationCity, LocationCountry
from app_nomand.serializers import ExperienceSerializer, FeaturedHotelsSerializer, SearchHotelsSerializer, \
    HotelInfoSerializer, GuestInfoSerializer, BookingInfoSerializer, LocationCitySerializer, LocationCountrySerializer


class ExperienceAPIView(APIView):
    def get(self,request):
        qs = Experience.objects.all()
        serializer = ExperienceSerializer(qs,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class LocationCityAPIView(APIView):
    def get(self,request):
        qs = LocationCity.objects.all()
        serializer = LocationCitySerializer(qs,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class LocationCountryAPIView(APIView):
    def get(self,request):
        qs = LocationCountry.objects.all()
        serializer = LocationCountrySerializer(qs,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)



class FeaturedHotelsAPIView(APIView):
    def get(self,request):
        qs = HotelInfo.objects.all()
        serializer = FeaturedHotelsSerializer(qs,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

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
        serializer = SearchHotelsSerializer(qs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class HotelInfoAPIView(APIView):
    def get_object(self, id):
        try:
            return HotelInfo.objects.get(hotelid=id)
        except HotelInfo.DoesNotExist:
            raise Http404

    def get(self,request,id):
        obj = self.get_object(id)
        serializer = HotelInfoSerializer(obj,context={'request':request})
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


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
            return Response({"message": "guest info invalid","data":guest_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        booking_data = requestData['bookingInfo']
        booking_data['guest'] = guest_obj.guestid
        booking_serializer = BookingInfoSerializer(data=booking_data)

        if booking_serializer.is_valid():
            booking_obj = booking_serializer.save()
        else:
            return Response({"message": "booking info invalid","data":booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # todo: an email sends to hotel 

        return Response({"message": "success","data":booking_serializer.data}, status=status.HTTP_200_OK)


