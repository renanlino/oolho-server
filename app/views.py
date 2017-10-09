from django.shortcuts import render
from app.models import Movement, Sensor
from app.serializers import MovementSerializer, SensorSerializer
from rest_framework import permissions
from app.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from django.views.generic import TemplateView



# Create your views here.

class DashboardView(TemplateView):
    template_name = 'app/dashboard.html'
    model = Movement

    def get(self, request):
        query = self.get_queryset().order_by("occurrence_date")
        data = []
        numRevert = {"IN":1, "OUT":-1}
        cumulative = 0
        for entry in query:
            xAxis = entry.occurrence_date.strftime("%d/%m %H:%M:%S")
            cumulative += numRevert[entry.direction]
            data.append([xAxis, cumulative])
        yMin = min([entry[1] for entry in data])
        yMax = max([entry[1] for entry in data])
        return render(request, self.template_name, locals())

    def get_queryset(self):
        user = self.request.user
        return Movement.objects.filter(owner=user)

class SensorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Sensor.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MovementViewSet(viewsets.ModelViewSet):
    serializer_class = MovementSerializer
    permission_classes = (permissions.IsAuthenticated,
                            IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Movement.objects.filter(owner=user)

    def perform_create(self, serializer):
        selectedSensor = Sensor.objects.get(pk=serializer.validated_data.get("sensor").id)
        if selectedSensor.owner == self.request.user:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied
