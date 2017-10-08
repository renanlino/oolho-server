from django.shortcuts import render
from app.models import Movement, Sensor
from app.serializers import MovementSerializer, SensorSerializer
from rest_framework import generics
from rest_framework import permissions
from app.permissions import IsOwnerOrReadOnly


# Create your views here.
class SensorList(generics.ListCreateAPIView):
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Sensor.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Sensor.objects.filter(owner=user)


class MovementList(generics.ListCreateAPIView):
    serializer_class = MovementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Movement.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MovementDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Movement.objects.filter(owner=user)
