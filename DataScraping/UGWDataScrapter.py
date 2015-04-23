# **** COPYRIGHT ****
# IMSE785 DR. SHINGI CHANG
# KANSAS STATE UNIVERSITY
# ALL RIGHTS RESERVED


import sys
import urllib2
# Datetime documents: 
# https://docs.python.org/2/library/time.html
from datetime import datetime
from datetime import timedelta
# BeautifulSoup documents:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup as BS


# ---- function to fetch page given a date, and an airport code ----
def fetchPage(a_date, airport_code):
	# form the url properly with given values
	# need to include protocol type, i.e. "http" to indicate url type
	# otherwise a value error message will be triggered
	url_string = 'http://www.wunderground.com/history/airport/K' + airport_code + a_date.strftime('/%Y/%m/%d/') + 'DailyHistory.html'
	page = urllib2.urlopen(url_string)
	return page

def collectValues(from_date, to_date, airport_code):
	# print temperature values from from_date to to_date
	delta_days = int((to_date - from_date).days)

	# iterate through range starting from from_date to to_date
	# and print the values
	for n in range(delta_days + 1):
		a_date = from_date + timedelta(n)
		try: 
			a_page = fetchPage(a_date, airport_code)
		except ValueError:
			print "\n>Error: Cannot fetch page, please try again!\n"
		
		# load the page into a beautiful soup data structure
		soup = BS(a_page)

		wx_spans = soup.findAll(attrs={'class':'wx-value'})

		if len(wx_spans) > 6: 
			# parse temperature values
			mean_actual = wx_spans[0].string
			mean_avg = wx_spans[1].string
			max_actual = wx_spans[2].string
			max_avg = wx_spans[3].string
			max_record = wx_spans[4].string
			min_actual = wx_spans[5].string
			min_avg = wx_spans[6].string
			min_record = wx_spans[7].string

			print a_date.strftime('%Y/%m/%d'), ":", mean_actual	

		else: 
			# temperature data not available
			print "NA"


# ---- Main function ----
def main():
	# ============ some welcome msg ==========
	# ask user to input an airport code
	airport_code_input = raw_input('>Enter an aiport code with format XXX: ')

	# evaluate if input is a valid airport code
	with open("iata-airport-codes.txt") as f:
		airport_info = ''
		for line in f:
			(iata_code, iata_info) = line.split('\t')
			if iata_code == airport_code_input:
				airport_code = iata_code
				airport_info = iata_info
				break
		# ==== if airport_code is invalid ====

	# ask user to input date range for retrieving data accordingly 
	from_date_input = raw_input('>Date range starts from (YYYY/MM/DD): ') 
	to_date_input = raw_input('>Date range ends at (YYYY/MM/DD): ')

	# convert user input into a datetime object
	# if unsuccessful, through a value error exception
	try:
		from_date = datetime.strptime(from_date_input, '%Y/%m/%d')
		to_date = datetime.strptime(to_date_input, '%Y/%m/%d')

		# just in case some user input the start/end dates in wrong order
		if from_date > to_date :
			date_switch = from_date
			from_date = to_date
			to_date = date_switch
			# print "\n>Calmly switched from_date and to_date\n"
	except ValueError:
		print "\n>Error: Incorrect date format, please try again!\n"
		sys.exit(0)



	# Start getting data from user-specified date range
	delta_days = (to_date - from_date).days
	print ">Collecting data from " + from_date.strftime('%Y/%m/%d') + " to " + to_date.strftime('%Y/%m/%d') + " (" + str(delta_days + 1) + " days) at " + airport_info + "...\n"  

	collectValues(from_date, to_date, airport_code)


# Program starts executing here
main()