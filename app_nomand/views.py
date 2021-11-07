from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_nomand.models import Experience, HotelInfo
from app_nomand.serializers import ExperienceSerializer, FeaturedHotelsSerializer


class ExperienceAPIView(APIView):
    def get(self,request):
        qs = Experience.objects.all()
        serializer = ExperienceSerializer(qs,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)



class FeaturedHotelsAPIView(APIView):
    def get(self,request):
        qs = HotelInfo.objects.all()
        serializer = FeaturedHotelsSerializer(qs,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)



