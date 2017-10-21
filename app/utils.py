import pandas as pd
import numpy as np
from django.utils import timezone
from datetime import datetime
import math

def extractDates(request):
    startDate = request.GET.get('startDate', None )
    endDate = request.GET.get('endDate', None)
    return startDate, endDate

def normalizeDates(startDate, endDate):
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

def queryReader(query):
    data = []
    numRevert = {"IN":1, "OUT":-1}
    for entry in query:
        xAxis = str(entry.occurrence_date)
        value = numRevert[entry.direction] * entry.value
        data.append([xAxis, value])
    return data

def pandify(data, gmode):
    dataf = pd.DataFrame(data)
    if len(dataf) > 0:
        dataf[0] = pd.to_datetime(dataf[0])
        regroup = dataf.set_index(0).groupby(pd.Grouper(freq=gmode)).sum()
        regroup[1].fillna(0, inplace=True)
        regroup = regroup.to_records()
        regroup.sort(axis=0)
        regroup = regroup.tolist()
        convRegroup = []
        for entry in regroup:
            if math.isnan(entry[1]):
                print(entry)
            convRegroup.append( [ str(entry[0]), entry[1] ] )
    else:
        return []
    return convRegroup

def generateAccumulative(data):
    accSum = 0
    for i in range(len(data)):
        accSum += data[i][1]
        data[i][1] = accSum

def applyOffset(data):
    values = [i[1] for i in data]
    if len(values) > 0 and min(values) < 0:
        for i in range(len(data)):
            data[i][1] += abs(min(values))
