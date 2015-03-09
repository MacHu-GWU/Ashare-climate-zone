##encoding=UTF-8

from __future__ import print_function
from fuzzywuzzy import process
import pandas as pd

class Search_Box():
    def __init__(self):
        data = pd.read_csv("climate_zone_of_county.txt", sep="\t")
        self.choice_of_county = data["county"].tolist()
        self.climate_zone_dict = dict()
        
        for climate_zone, county_name in zip(data["climate_zone"], data["county"]):
            self.climate_zone_dict[county_name] = climate_zone

    def query(self, county_name):
        """get an exact result
        """
        choice, score = process.extractOne(county_name, self.choice_of_county)
        print("%s is in climate zone %s, your query string is '%s'." % (choice, 
                                                                        self.climate_zone_dict[choice],
                                                                        county_name))

    def search(self, county_name):
        """fuzzy search
        """
        for choice, score in process.extract(county_name, self.choice_of_county, limit=10):
            if score >= 50:
                print("%s is in climate zone %s" % (choice, self.climate_zone_dict[choice]))
    
if __name__ == "__main__":
    search_box = Search_Box()
    search_box.search("orang, califor")
