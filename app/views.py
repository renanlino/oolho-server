from django.shortcuts import render, redirect
from app.models import Movement, Sensor, Space
from app.serializers import MovementSerializer, SensorSerializer, SpaceSerializer, SpaceChartSerializer
from rest_framework import permissions
from app.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError, NotAuthenticated
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import Http404
import app.utils as utils


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'app/dashboard.html'

    def get(self, request):
        ## Leitura parâmetros do GET:
        startDate, endDate = utils.extractDates(request)
        spaceToRender = request.GET.get('space', None)
        groupMode = request.GET.get('groupMode', "H")
        user = self.request.user

        ## Workaround de datas
        startDate, endDate = utils.normalizeDates(startDate, endDate)
        startDate_view = startDate.strftime("%d/%m/%Y")
        endDate_view = endDate.strftime("%d/%m/%Y")

        ## Lista de spaces e sensors para menu e tabela:
        spaces = Space.objects.filter(owner=user)
        sensors = Sensor.objects.filter(owner=user).order_by("id")

        ## Construção dinâmica das URLs
        baseAccumulativeEndpointURL = "/api/spaces/##SID##/chart?groupMode=##GMODE##&startDate=##SDATE##&endDate=##EDATE##&chartType=accumulative&format=json"
        baseMovementsEndpointURL = "/api/spaces/##SID##/chart?groupMode=##GMODE##&startDate=##SDATE##&endDate=##EDATE##&chartType=movements&format=json"

        accumulativeEndpointURL = baseAccumulativeEndpointURL.replace("##GMODE##", groupMode)
        accumulativeEndpointURL = accumulativeEndpointURL.replace("##SDATE##", startDate_view)
        accumulativeEndpointURL = accumulativeEndpointURL.replace("##EDATE##", endDate_view)

        movementsEndpointURL = baseMovementsEndpointURL.replace("##GMODE##", groupMode)
        movementsEndpointURL = movementsEndpointURL.replace("##SDATE##", startDate_view)
        movementsEndpointURL = movementsEndpointURL.replace("##EDATE##", endDate_view)

        ## Renderiza visão do espaço específico
        if spaceToRender is not None:
            try:
                currentSpaceName = Space.objects.get(pk=spaceToRender, owner=user).display_name
            except Space.DoesNotExist:
                currentSpaceName = "Erro"
                return render(request, "app/not_found.html", locals())
            spaceToRenderAsInt = int(spaceToRender)
            sensors = sensors.filter(space=spaceToRender)
            accumulativeEndpointURL = accumulativeEndpointURL.replace("##SID##", spaceToRender)
            movementsEndpointURL = movementsEndpointURL.replace("##SID##", spaceToRender)
            return render(request, self.template_name, locals())
        ## Renderiza visão geral
        else:
            spaceToRenderAsInt = -1
            currentSpaceName = "Visão Geral"
            accumulativeEndpointURL = accumulativeEndpointURL.replace("##SID##", "")
            movementsEndpointURL = movementsEndpointURL.replace("##SID##", "")
            return render(request, self.template_name, locals())


class SpaceChartView(APIView):
    serializer_class = SpaceChartSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly,)

    def get(self, request, pk):
        user = request.user
        startDate, endDate = utils.extractDates(request)
        startDate, endDate = utils.normalizeDates(startDate, endDate)
        if startDate is None or endDate is None:
            raise ValidationError("Parâmetro de data ausente")
        groupMode = request.GET.get('groupMode', "H")

        # TODO: não autenticado, pk nulo
        query = Movement.objects.filter(owner=user,
            sensor__space=pk).filter(
            occurrence_date__gte=startDate).filter(
            occurrence_date__lte=endDate).order_by("occurrence_date")

        chartType = request.GET.get('chartType', None )
        if chartType == "accumulative":
            return self.buildAccumulative(query, groupMode)
        elif chartType == "movements":
            return self.buildMovements(query, groupMode)
        elif chartType == "inside":
            return self.calculateInside()
        else:
            raise ValidationError("Tipo de gráfico ausente")

    def buildMovements(self, query, groupMode):
        queryData = utils.queryReader(query)

        entrances = []
        exits = []
        for entry in queryData:
            if entry[1] > 0:
                entrances.append(entry)
            else:
                exits.append(entry)

        entrancePandaData = utils.pandify(entrances, groupMode)
        exitPandaData = utils.pandify(exits, groupMode)

        movementsSeries = [
         {"name":"Entradas", "data":entrancePandaData},
         {"name":"Saídas", "data":exitPandaData}
        ]

        return Response(movementsSeries)

    def buildAccumulative(self, query, groupMode):
        queryData = utils.queryReader(query)

        accumulativePandaData = utils.pandify(queryData, groupMode)
        utils.generateAccumulative(accumulativePandaData)
        utils.applyOffset(accumulativePandaData)

        return Response(accumulativePandaData)

    def calculateInside(self):
        query = Movement.objects.filter(owner=user,
            sensor__space=pk).filter(
            occurrence_date__gte=startDate).filter(
            occurrence_date__lte=endDate).order_by("occurrence_date")

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
