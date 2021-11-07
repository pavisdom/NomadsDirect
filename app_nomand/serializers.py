from rest_framework import serializers

from app_nomand.models import Experience, HotelInfo


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

class FeaturedHotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInfo
        fields = ['hotelid','name','description','location_street','location_city','location_country']

