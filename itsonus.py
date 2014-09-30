import csv
import json
import urllib2

def read_url_data( base ):

#  Read URL data from site page-by-page until done
#
#  base:  Base URL

	nm_list = [ ]						# List of pledgers' names

	i = 0								# Page to read
	while True:							# While not done reading

	# Grab the current page from the itsonus.org site

		site = base + '/' + str( i )
		url = urllib2.urlopen( site )
		doc = url.read()
		url.close()

	# Parse JSON and save names

		data = json.loads( doc )
		for p in data[ "pledgers" ]:
			nm = [ ]
			nm = p[ "first_name" ].lower().strip()
			#nm[ "last" ] = p[ "last_name" ].lower().strip()
			#nm[ "full" ] = nm[ "first" ] + ' ' + nm[ "last" ]

	# Convert from UTF-8 to ASCII (lazily, by ignoring things)

			nm = nm.encode( 'ascii', 'ignore' )
			#nm[ "last" ] = nm[ "last" ].encode( 'ascii', 'ignore' )
			#nm[ "full" ] = nm[ "full" ].encode( 'ascii', 'ignore' )

			nm_list.append( nm )

	# Check for end of data, otherwise move to next page of pledgers

		if data[ "nextPage" ] == False:
			break
		else:
			i = i + 1

	return nm_list						# Return list of names

#  End function read_url_data


#  Mainline

nm_list = read_url_data( 'http://itsonus.org/api/pledgers' )
#nm_list = sorted( nm_list, key=lambda nm: nm[ "first" ] )
nm_list.sort()

#translating tuple into list

path = 'C:/Users/Tammy/Documents/Grad School/Random practice/'

#pulling CSVs into lists
males = list(csv.reader(open(path + 'male.csv', 'rb')))
males.sort()
flat_males = [ ]
flat_males = [val for sublist in males for val in sublist]

females = list(csv.reader(open(path + 'female.csv', 'rb')))
females.sort()
flat_females = [ ]
flat_females = [val for sublist in females for val in sublist]

#checking pledgers list against male list, counting males
male_total = 0
for pledge in nm_list:
	for dude in flat_males:
		if pledge == dude:
			male_total= male_total+1

#checking pledgers list against female list, counting females
female_total = 0
for pledge in nm_list:
	for lady in flat_females:
		if pledge == lady:
			female_total=female_total+1

#calculating percentages
male_total=float(male_total)
female_total=float(female_total)
total = float(len(nm_list))
overlap = (male_total + female_total) - total
male_pct = round(100*((male_total-overlap)/total),2)
female_pct = round(100*((female_total-overlap)/total),2)
tie_pct = round(100*(overlap/total),2)
total=int(total)

#displaying results

print "Of %s current pledgers, %s percent are male, %s percent are female, and %s percent are unclear." %(total, male_pct, female_pct, tie_pct)
