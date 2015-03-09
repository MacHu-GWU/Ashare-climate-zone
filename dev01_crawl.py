##encoding=UTF-8

"""
a script to download county - climate zone information from:
    http://en.openei.org/wiki/ASHRAE_Climate_Zones
"""

from angora.LINEARSPIDER import *
from bs4 import BeautifulSoup as BS4
import pandas as pd

data = list()

climate_zone_url_dict = dict()
for i in range(1, 8+1):
    climate_zone_url_dict[i] = "http://en.openei.org/wiki/Climate_Zone_Number_{0}".format(i)
    
spider = Crawler()
for i, url in climate_zone_url_dict.items():
    print("crawling %s ..." % url)
    html = spider.html(url)
    soup = BS4(html)
    div = soup.find("div", id="mw-content-text")
    for a in div.find_all("a"): # after this, you have to manually clean up the error county data
        data.append( (i, a.text) )

df = pd.DataFrame(data, columns=["climate_zone", "county"])
df.to_csv("climate_zone_of_county.txt", sep="\t", index=False)
