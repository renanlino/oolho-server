import random
import requests
from requests.auth import HTTPBasicAuth
import sys
from datetime import datetime, timedelta

PROD = "https://adeusdentinho.herokuapp.com/api/movements/?format=json"
LOCAL = "http://localhost:8000/api/movements/?format=json"

def main():
    usersInside = 0
    baseTime = datetime.now()
    idSensor = int(input("Digite a ID do sensor: "))
    duration = int(input("Digite a duração máxima da simulação em minutos: "))
    user = input("Digite o usuário (eletricademo): ")
    if user == '':
        user = "eletricademo"
    password = input("Digite a senha: ")
    if password == '':
        password = "140897hr"
    server = input("Local (l) ou Produção (P)?: ")
    offset = input("Digite o offset em horas (0): ")
    if offset != '':
        offset = timedelta(hours = int(offset))
        baseTime += offset

    if server.upper() == "L":
        URL = LOCAL
    else:
        URL = PROD
    movement = {
        "sensor": idSensor,
        "direction": None,
        "received_date": None,
        "occurrence_date": None
    }
    maxTime = timedelta(minutes=duration)
    end = baseTime + maxTime
    while baseTime < end:
        quantity = random.randint(-usersInside, usersInside + 1)
        for i in range(abs(quantity)):
            timelapse = timedelta( seconds = random.randint(60, 5*60) )
            baseTime += timelapse
            occurrence_date = baseTime.strftime("%Y-%m-%dT%H:%M:%SZ")
            movement["occurrence_date"] = occurrence_date
            direction = abs(quantity)/quantity
            if direction == -1:
                movement["direction"] = "OUT"
            else:
                movement["direction"] = "IN"

            usersInside += direction
            print("%s\t %s \t(%d users inside)" %(movement["occurrence_date"],
                    movement["direction"], usersInside))
            response = requests.post(URL,
                            auth=HTTPBasicAuth(user, password), data=movement)
            if response.status_code > 300:
                print("\t> Status Code: %d (%s)" %(response.status_code, response.text))
            else:
                print("\t> Status Code: %d" %(response.status_code))

main()
