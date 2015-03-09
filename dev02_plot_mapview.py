##encoding=UTF-8

"""
a script to plot the climate zone map view
"""

from constant import state_abbr # {"state_2letter_shortname": "state_full_name"}
from fuzzywuzzy import process
from matplotlib import pyplot as plt
from angora.DATA import *
import numpy as np, pandas as pd

def prepare_data():
    ################################################
    # Process county's latitude and longitude data #
    ################################################
    zipcode_data = pd.read_csv("zip_code_database.csv", sep=",") # read county, state, la, lg source data
    coordinate = dict() # the mapping from county to couple of available state, la, lg combinations
    for county, state, la, lg in zip(zipcode_data["county"], # !!! The state here is abbreviation 
                                     zipcode_data["state"], 
                                     zipcode_data["latitude"],
                                     zipcode_data["longitude"],):
        try:
            if len(county) >= 1:
                county = county.lower().replace("county", "").strip()
                state = state.strip()
        
                if county in coordinate:
                    coordinate[county].append(state_abbr[state], la, lg)
                else:
                    coordinate[county] = [(state_abbr[state], la, lg)]
        except:
            pass
    choice_of_county = list(coordinate.keys())
    
    ###################################################
    # Process climate zone la, lg datapoint by county #
    ###################################################
    data = pd.read_csv("climate_zone_of_county.txt", sep="\t")
    climate_zone_view = {str(i): {"la": list(), "lg": list()} for i in range(1, 8+1)}
     
    for climate_zone, county_name in zip(data["climate_zone"], data["county"]):
        print("finding la, lg for %s ..." % county_name)
        county, state = county_name.split(",")
        county = county.lower().replace("county", "").strip()
        state = state.strip()
        
        choice, score = process.extractOne(county, choice_of_county) # find the right county name
    
        for candidate_state, la, lg in coordinate[choice]: # find the right state name
            if state == candidate_state: # if got it, save the la and lg
                climate_zone_view[climate_zone]["la"].append(la)
                climate_zone_view[climate_zone]["lg"].append(lg)
                print("\tsuccess!")
                
    safe_dump_js(climate_zone_view, "climate_zone_view.json")

prepare_data()

#################
# Plot Map View #
#################

def plot_climatezone_mapview():
    climate_zone_view = load_js("climate_zone_view.json")
    la1, lg1 = climate_zone_view["1"]["la"], climate_zone_view["1"]["lg"]
    la2, lg2 = climate_zone_view["2"]["la"], climate_zone_view["2"]["lg"]
    la3, lg3 = climate_zone_view["3"]["la"], climate_zone_view["3"]["lg"]
    la4, lg4 = climate_zone_view["4"]["la"], climate_zone_view["4"]["lg"]
    la5, lg5 = climate_zone_view["5"]["la"], climate_zone_view["5"]["lg"]
    la6, lg6 = climate_zone_view["6"]["la"], climate_zone_view["6"]["lg"]
    la7, lg7 = climate_zone_view["7"]["la"], climate_zone_view["7"]["lg"]
    la8, lg8 = climate_zone_view["7"]["la"], climate_zone_view["7"]["lg"]
    
    line1, = plt.plot(lg1, la1, ".")
    line2, = plt.plot(lg2, la2, ".")
    line3, = plt.plot(lg3, la3, ".")
    line4, = plt.plot(lg4, la4, ".")
    line5, = plt.plot(lg5, la5, ".")
    line6, = plt.plot(lg6, la6, ".")
    line7, = plt.plot(lg7, la7, ".")
    line8, = plt.plot(lg8, la8, ".", color = "#05FF1A")
    plt.legend([line1, line2, line3, line4, line5, line6, line7, line8],
               ["1", "2", "3", "4", "5", "6", "7", "8"])
    plt.show()

plot_climatezone_mapview()
    