import random
import requests
from requests.auth import HTTPBasicAuth
import sys
from datetime import datetime, timedelta

def main():
    usersInside = 0
    baseTime = datetime.now()
    idSensor = int(input("Digite a ID do sensor: "))
    user = input("Digite o usuário: ")
    password = input("Digite a senha: ")
    duration = int(input("Digite a duração máxima da simulação em minutos: "))
    movement = {
        "sensor": idSensor,
        "direction": None,
        "received_date": None,
        "occurrence_date": None
    }
    maxTime = timedelta(minutes=duration)
    end = baseTime + maxTime
    while baseTime < end:
        timelapse = timedelta( seconds = random.randint(10, 120) )
        baseTime += timelapse
        occurrence_date = baseTime.strftime("%Y-%m-%dT%H:%M:%S-03:00")
        movement["occurrence_date"] = occurrence_date
        direction = random.choice([1, -1])
        if direction == -1 and usersInside > 0:
            movement["direction"] = "OUT"
        elif direction == -1 and usersInside == 0:
            movement["direction"] = "IN"
            direction = 1
        else:
            movement["direction"] = "IN"
        usersInside += direction
        print("%s\t %s \t(%d users inside)" %(movement["occurrence_date"],
                movement["direction"], usersInside))
        response = requests.post("https://gentle-lake-67733.herokuapp.com/movements/",
                        auth=HTTPBasicAuth(user, password), data=movement)
        if response.status_code > 300:
            print("\t> Status Code: %d (%s)" %(response.status_code, response.text))
        else:
            print("\t> Status Code: %d" %(response.status_code))

main()
