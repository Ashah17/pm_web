import googlemaps
import folium
import geopy
from .read_itinerary import *
# from ortools.constraint_solver import pywrapcp, routing_enums_pb2 #for tsp
import numpy as np

def map_return():

    #don't need this for actual map

    itinerary = read_itinerary() #read itinerary file

    itineraryList = [region for region in list(itinerary.keys()) if region] #remove the empty string

    map_lists = []
    coordinates = []
    locations = []

    for location in itineraryList:
        places, coords, map = plot_points(itinerary, location)
        map_lists.append(map) #create a plotted point map for each location, add to list

        locations.append(places) #add list of places
        coordinates.append(coords) #add list of coords


    return locations, coordinates

    #map_lists contains all of the maps

def plot_points(itinerary, location):
    API_KEY = "AIzaSyBoUdA3oXBeSscLVfJ5K0UYQyXSk_SIzRo"
    gmaps = googlemaps.Client(key=API_KEY)

    #add places from itinerary file

    places =  itinerary[location][0]

    coordinates = []

    for place in places:
        place += " " + location #to restrict searches to the larger location
        geocode = gmaps.geocode(place) #geocode api for coordinates
        if geocode:
            loc = geocode[0]['geometry']['location']
            coordinates.append((loc['lat'], loc['lng']))
        else:
            #print the place that cant be found
            print(place + " can't be found")

    latSum = 0
    longSum = 0

    for lat, long in coordinates:
        latSum += lat
        longSum += long
    
    latSum /= len(coordinates)
    longSum /= len(coordinates)

    centroid = (latSum, longSum) #center of places in list

    map = map_preview(places, coordinates, centroid, location)

    return places, coordinates, map


#folium set up below to set up map preview

def map_preview(places, coordinates, centroid, region):
    # map_center = [39.8283, -98.5795] #center of usa for now, CHANGE TO DYNAMICALLY GO CENTER OF COUNTRY 

    mymap = folium.Map(location=centroid, zoom_start=4)

    # Add markers for each place
    for place, coord in zip(places, coordinates):
        folium.Marker(
            location=coord,
            popup=place,
        ).add_to(mymap)

    # Save the map to an HTML file

    html_name = str(region) + "_map.html"

    mymap.save(html_name)

    return mymap

###ONLY NEED THE METHOD BELOW FOR THE APP

def places_to_coords(places):
    API_KEY = "AIzaSyBoUdA3oXBeSscLVfJ5K0UYQyXSk_SIzRo"
    gmaps = googlemaps.Client(key=API_KEY)

    # print("TEHSE R PLACES\n")
    # print(places)

    #places and restaurants (passed in)

    coordinates = []

    for place in places:
        #the place has the location appended too
        # place += " " + location #to restrict searches to the larger location

        response = gmaps.find_place(
            input = place,
            input_type='textquery',
            fields=['formatted_address']
        )

        address = ""

        if response['status'] == 'OK' and response['candidates']:
            #if found address
            top_res = response['candidates'][0] #top result
            address = top_res.get('formatted_address') #get address
        else:
            print('no address found for ' + place)
            continue #no address found


        geocode = gmaps.geocode(place) #geocode api for coordinates ADDRESSES
        if geocode:
            loc = geocode[0]['geometry']['location']
            coordinates.append((loc['lat'], loc['lng']))
        else:
            #print the place that cant be found
            print(place + " can't be found")

    latSum = 0
    longSum = 0

    for lat, long in coordinates:
        latSum += lat
        longSum += long
    
    latSum /= len(coordinates)
    longSum /= len(coordinates)

    centroid = (latSum, longSum) #center of places in list

    # map = map_preview(places, coordinates, centroid, location) #don't need this

    coordinates.insert(0, centroid) #insert at start

    # print("THESE R COORDS")
    # print(coordinates)

    return coordinates #just want coordinates with centroid appended


# map_return()