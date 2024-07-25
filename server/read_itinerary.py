#temp file needed to read from the itinerary text file

# from initial_itinerary import *
# from detailed_options import *


def read_itinerary():

    file = open("./Itinerary.txt", 'r')

    itinerary = file.read()
    
    listedItinerary = extract_details(itinerary)

    return listedItinerary
    

def breakdown_section(section):
    places = []
    restaurants = []
    tips = []
    transportation = []

    lines = section.split("\n")
    current_list = None

    for line in lines:
        line = line.strip()
        if "Places" in line:
            current_list = places
        elif "Restaurant" in line:
            current_list = restaurants
        elif "Tips" in line:
            current_list = tips
        elif "Transporation" in line:
            current_list = transportation
        elif line.startswith("* ") or line.startswith("- "):
            if current_list is not None:
                current_list.append(line[2:])
        elif line and current_list is transportation:
            transportation.append(line)

    return places, restaurants, tips, transportation


def extract_details(info_text):
    sections = info_text.split("***************")[1:]

    itinerary = {}

    for section in sections:
        lines = section.strip().split("\n")
        if lines:
            # Extract the city name from the first line
            city_line = lines[0].strip()
            city_name = city_line.split(" in ")[-1]
            # Extract information for the current city
            section_info = breakdown_section(section)
            # Add to the itinerary dictionary
            itinerary[city_name] = section_info

    return itinerary


