import pandas as pd
import json
import random
import csv

with open('./public/toulouse.json', 'r') as file:
    data = json.load(file)
    long = []
    lat = []
    nb = []

    for i in range(len(data)):
        long.append(data[i]['longitude'])
        lat.append(data[i]['latitude'])
        nb.append(random.randint(0, 6))
        print(long)

    with open('./public/toulouse_cleaned.csv', 'w', ) as file:
        writer = csv.writer(file)
        fields = ['lat', 'lng', 'nb']

        writer.writerow(fields)
        for i in range(len(data)):
            writer.writerow([lat[i], long[i], nb[i]])
