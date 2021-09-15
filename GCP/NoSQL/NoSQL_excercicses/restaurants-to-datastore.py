import sys
import json
import csv
import os
from google.cloud import datastore

def to_unicode(string):
    return unicode(string, "utf-8")

def convert():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #dirppal = BASE_DIR[:-4]
    readFile = os.path.join(BASE_DIR, "restaurants.json")

    # Instantiates a client
    datastore_client = datastore.Client()

    # The kind for the new entity
    kind = 'restaurants'

    print ('\n' + 'Convert to Datastore - Please Wait' + '\n')

    lines = []

    with open(readFile, "r") as f:
        lines = f.readlines()

    for line in lines:
        jsondata = json.loads(line)

        # The Cloud Datastore key for the new entity
        rest_key = datastore_client.key(kind)

        # Prepares the new entity
        restaurants = datastore.Entity(key=rest_key)

        restaurant_id = jsondata.get("restaurant_id")
        name = jsondata.get("name")
        cuisine = jsondata.get("cuisine")
        borough = jsondata.get("borough")

        #address
        address = jsondata.get("address", {})

        zipcode = address.get("zipcode", '')
        street = address.get("street", '')
        building = address.get("building", '')

        coord = address.get("coord", [0, 0] )
        longitude = coord[0]
        latitude = coord[1]

        restaurants['id'] = to_unicode(restaurant_id)
        restaurants['name'] = to_unicode(name)
        restaurants['cuisine'] = to_unicode(cuisine)
        restaurants['borough'] = to_unicode(borough)

        restaurants['zipcode'] = to_unicode(zipcode)
        restaurants['street'] = to_unicode(street)
        restaurants['building'] = to_unicode(street)

        restaurants['longitude'] = longitude
        restaurants['latitude'] = latitude

        # Saves the entity
        datastore_client.put(restaurants)


    print ('\n' + 'Saved Rows to csv' + '\n')

if __name__ == '__main__':
    convert()