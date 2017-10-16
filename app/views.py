from django.shortcuts import render, redirect
from app.models import Movement, Sensor, Space
from app.serializers import MovementSerializer, SensorSerializer, SpaceSerializer
from rest_framework import permissions
from app.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime
from django.http import Http404
import pandas as pd
import numpy as np


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'app/dashboard.html'
    model = Movement

    def get(self, request):
        startDate = request.GET.get('startDate', None )
        endDate = request.GET.get('endDate', None)
        groupMode = request.GET.get('groupMode', "H")
        startDate, endDate = self.normalizeDates(startDate, endDate)
        startDate_view = startDate.strftime("%d/%m/%Y")
        endDate_view = endDate.strftime("%d/%m/%Y")

        spaceToRender = request.GET.get('space', None)
        if spaceToRender == '':
            spaceToRender = None
        spaces = self.getSpaces()

        sensors = self.getSensors(spaceToRender)

        if spaceToRender is None:
            spaceToRenderAsInt = -1
            currentSpaceName = "Visão Geral"
            pandaData = []
            return render(request, self.template_name, locals())
        else:
            try:
                currentSpaceName = Space.objects.get(pk=spaceToRender).display_name
            except:
                raise Http404("O espaço solicitado não existe.")
            query = self.getMovements(spaceToRender).filter(
                occurrence_date__gte=startDate).filter(
                occurrence_date__lte=endDate).order_by("occurrence_date")
            queryData = self.queryReader(query)
            """print("Query:")
            print(queryData)
            print()"""
            pandaData = self.pandify(queryData, groupMode)
            """print("Pandify:")
            print(pandaData)
            print()"""
            self.generateAccumulative(pandaData)
            """print("Accumulative:")
            print(pandaData)
            print()"""
            self.applyOffset(pandaData)
            """print("Offset:")
            print(pandaData)
            print()"""
            spaceToRenderAsInt = int(spaceToRender)
            return render(request, self.template_name, locals())

    def normalizeDates(self, startDate, endDate):
        current_tz = timezone.get_current_timezone()
        if startDate is None:
            startDate = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            startDate = datetime.strptime(startDate, "%d/%m/%Y")
            startDate = current_tz.localize(startDate)
        if endDate is None:
            endDate = timezone.now().replace(hour=23, minute=59, second=59, microsecond=59)
        else:
            endDate = datetime.strptime(endDate, "%d/%m/%Y")
            endDate = endDate.replace(hour=23, minute=59, second=59, microsecond=59)
            endDate = current_tz.localize(endDate)
        return startDate, endDate

    def get_queryset(self):
        user = self.request.user
        return Movement.objects.filter(owner=user)

    def getSpaces(self):
        user = self.request.user
        return Space.objects.filter(owner=user)

    def getSensors(self, spaceToRender):
        user = self.request.user
        if spaceToRender is not None:
            return Sensor.objects.filter(owner=user, space=spaceToRender)
        else:
            return Sensor.objects.filter(owner=user)

    def getMovements(self, spaceToRender):
        user = self.request.user
        movements = Movement.objects.filter(owner = user,
                    sensor__space = spaceToRender)
        return movements

    def queryReader(self, query):
        data = []
        numRevert = {"IN":1, "OUT":-1}
        for entry in query:
            xAxis = str(entry.occurrence_date)
            value = numRevert[entry.direction] * entry.value
            data.append([xAxis, value])
        return data

    def pandify(self, data, gmode):
        dataf = pd.DataFrame(data)
        if len(dataf) > 0:
            dataf[0] = pd.to_datetime(dataf[0])
            regroup = dataf.set_index(0).groupby(pd.Grouper(freq=gmode)).sum().to_records()
            regroup.sort(axis=0)
            regroup = regroup.tolist()
            convRegroup = []
            for entry in regroup:
                convRegroup.append( [ str(entry[0]), entry[1] ] )
        else:
            return []
        return convRegroup

    def generateAccumulative(self, data):
        accSum = 0
        for i in range(len(data)):
            accSum += data[i][1]
            data[i][1] = accSum

    def applyOffset(self, data):
        values = [i[1] for i in data]
        if len(values) > 0 and min(values) < 0:
            for i in range(len(data)):
                data[i][1] += abs(min(values))

class SpaceViewSet(viewsets.ModelViewSet):

    serializer_class = SpaceSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Space.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SensorViewSet(viewsets.ModelViewSet):

    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Sensor.objects.filter(owner=user)

    def perform_create(self, serializer):
        selectedSpace = Space.objects.get(pk=serializer.validated_data.get("space").id)
        if selectedSpace.owner == self.request.user:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied


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
            selectedSensor.last_seen = timezone.now()
            selectedSensor.save()
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied

def HomeView(request):
    return redirect("/dashboard")
