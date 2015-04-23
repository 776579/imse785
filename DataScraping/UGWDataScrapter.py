# **** COPYRIGHT ****
# IMSE785 
# DR. SHINGI CHANG
# WENBO WANG
# INDUSTRIAL MANUFACTURING AND SYSTEMS ENGINEERING
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
# Progressbar documents:
# https://code.google.com/p/python-progressbar/
import progressbar


# ---- function to fetch page given a date, and an airport code ----
def fetchPage(a_date, airport_code):
	# form the url properly with given values
	# need to include protocol type, i.e. "http" to indicate url type
	# otherwise a value error message will be triggered
	url_string = 'http://www.wunderground.com/history/airport/K' + airport_code + a_date.strftime('/%Y/%m/%d/') + 'DailyHistory.html'
	page = urllib2.urlopen(url_string)
	return page

def collectValues(from_date, to_date, airport_code, op):
	# print temperature values from from_date to to_date
	delta_days = int((to_date - from_date).days)

	# use current UNIX timestamp as file name
	outputFileName = datetime.now().strftime("%s")
	
	if op == 's': 
		# progress indicator
		progress = progressbar.ProgressBar()
		customized_range = progress(range(delta_days + 1))
	else: 
		customized_range = range((delta_days) + 1)
	# iterate through range starting from from_date to to_date
	# and print the values
	for n in customized_range:
		a_date = from_date + timedelta(n)
		try: 
			a_page = fetchPage(a_date, airport_code)
		except ValueError:
			print "\n> Error: Cannot fetch page, please try again!\n"
		
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

			result = a_date.strftime('%Y/%m/%d') + '\t' + mean_actual

		else: 
			# temperature data not available
			result = "NA"

		
		if op in ['s', 'ps', 'sp']:
			# user requested to save file
			with open(outputFileName, 'a') as outputFile:
				# write output to file
				outputFile.write(result + '\n')

			if op in ['ps', 'sp']:
				# user requested to print result too
				print result

			outputFile.close()
		else:
			print result

	



# ---- Main function ----
def main():
	# ============ some welcome msg ==========
	# ask user to input an airport code
	airport_code_input = raw_input('\n> Aiport code (XXX): ')

	# evaluate if input is a valid airport code
	with open("iata-airport-codes.txt") as iataFile:
		airport_info = ''
		for line in iataFile:
			(iata_code, iata_info) = line.split('\t')
			if iata_code == airport_code_input:
				airport_code = iata_code
				airport_info = iata_info
				break
		# ==== if airport_code is invalid ====
		# ==== exit program here ===
	iataFile.close()

	# ask user to input date range for retrieving data accordingly 
	from_date_input = raw_input('> Date range from (YYYY/MM/DD): ') 
	to_date_input = raw_input('> Date range to (YYYY/MM/DD): ')

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
		print "\n> Error: Incorrect date format, please try again!\n"
		sys.exit(0)

	# ask user to select data handling method
	op_input = raw_input('> Select operation (p-print, s-save, ps-print&save):')

	# ==== evaluate op_input ====
	op = op_input

	# Start getting data from user-specified date range
	delta_days = (to_date - from_date).days
	print "> Collecting data from " + from_date.strftime('%Y/%m/%d') + " to " + to_date.strftime('%Y/%m/%d') + " (" + str(delta_days + 1) + " days) at " + airport_info + "...\n(Press Ctrl-C to force-stop)\n"  

	collectValues(from_date, to_date, airport_code, op)


# Program starts executing here
main()
