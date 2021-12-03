from rest_framework import serializers

from app_nomand.models import Experience, HotelInfo, HotelReservationItem, BookingInfo, GuestInfo


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['expid','exptag']


class FeaturedHotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInfo
        fields = ['hotelid','name','description','location_street','location_city','location_country']


class SearchHotelsSerializer(serializers.ModelSerializer):
    experiances_tags = ExperienceTagSerializer(many=True,read_only=True)
    class Meta:
        model = HotelInfo
        fields = ['hotelid','name','description','location_street','location_city','location_country','experiances_tags']


class HotelReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReservationItem
        fields = ['reservationItemId','reservation_item','priceinfo_usd','priceinfo_lkr',]



class HotelInfoSerializer(serializers.ModelSerializer):
    experiances_tags = ExperienceTagSerializer(many=True,read_only=True)
    hotel_reservation = HotelReservationItemSerializer(many=True,read_only=True)
    class Meta:
        model = HotelInfo
        fields = ['hotelid','name','description','location_street','location_city','location_country','experiances_tags','hotel_reservation']


class BookingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingInfo
        fields = '__all__'


class GuestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestInfo
        fields = '__all__'



