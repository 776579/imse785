# **** COPYRIGHT ****
# IMSE785 
# DR. SHINGI CHANG
# WENBO WANG
# INDUSTRIAL MANUFACTURING AND SYSTEMS ENGINEERING
# KANSAS STATE UNIVERSITY
# ALL RIGHTS RESERVED


import sys
import urllib2
# BeautifulSoup documents:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup as BS


# fetch webpage on Jan 1, 2015 at Manhattan airport
page = urllib2.urlopen('http://www.wunderground.com/history/airport/KMHK/2015/1/1/DailyHistory.html')

# properly structure the page
soup = BS(page)

# get elements with class names as "wx-value"
temp_values = soup.findAll(attrs={'class':'wx-value'})

# output the first element of this list
print temp_values[0].string