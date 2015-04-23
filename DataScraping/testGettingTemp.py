import sys
import urllib2
from datetime import datetime
# Datetime documents: 
# https://docs.python.org/2/library/time.html
from bs4 import BeautifulSoup as BS
# BeautifulSoup documents:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/

# ---- function to fetch page given a date, and an airport code ----
def fetchPage(a_date, airport_code):

	# form the url properly with given values
	# need to include protocol type, i.e. "http" to indicate url type
	# otherwise a value error message will be triggered
	url_string = 'http://www.wunderground.com/history/airport/K' + airport_code + a_date.strftime('/%Y/%m/%d/') + 'DailyHistory.html'
	page = urllib2.urlopen(url_string)
	return page

# ---- function to check if a start_date, end_date combination is valid
def checkDates(start_date, end_date) : 
	return True

# ---- Main function ----
# Program starts executing here
def main():
	# ============ some welcome msg ==========
	# ask user to input an airport code
	airport_code_input = raw_input('Please enter an aiport code with format XXX: ')

	# ask user to input date range for retrieving data accordingly 
	start_date_input = raw_input('Please enter start date with format YYYY/MM/DD: ') 
	end_date_input = raw_input('Please enter end date with format YYYY/MM/DD: ') 


	# ============ evaluate if input is a valid airport code
	airport_code = airport_code_input

	# convert user input into a datetime object
	# if unsuccessful, through a value error exception
	try:
		start_date = datetime.strptime(start_date_input, '%Y/%m/%d')
		end_date = datetime.strptime(end_date_input, '%Y/%m/%d') 
	except ValueError:
		print "\n>Error:\n>Incorrect date format, please try again!\n"
		sys.exit(0)

	# just in case some user input the start/end dates in wrong order
	if start_date > end_date :
		date_switch = start_date
		start_date = end_date
		end_date = date_switch
		print "\n>Calmly switched start date and end date\n"

	# Start getting data from user-specified date range
	delta_days = (end_date - start_date).days
	print ">Collecting data from " + start_date.strftime('%Y/%m/%d') + " to " + end_date.strftime('%Y/%m/%d') + " (" + str(delta_days) + " days) at " + airport_code + "..."  


	page = fetchPage(start_date, airport_code)
	# load the page into a beautiful soup data structure
	soup = BS(page)

	wx_spans = soup.findAll(attrs={'class':'wx-value'})

	# parse temperature values
	mean_actual = wx_spans[0].string
	mean_avg = wx_spans[1].string
	max_actual = wx_spans[2].string
	max_avg = wx_spans[3].string
	max_record = wx_spans[4].string
	min_actual = wx_spans[5].string
	min_avg = wx_spans[6].string
	min_record = wx_spans[7].string

	print mean_actual

main()