#!/usr/bin/python
import csv
import json
import urllib2
import time
from nvd3 import pieChart

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

path = "/Volumes/Raid/NetUser/tlarmst3/Sites/"

#pulling CSVs into lists
males = list(csv.reader(open("/Volumes/Raid/NetUser/tlarmst3/Sites/male.csv", "rb")))
males.sort()
flat_males = [ ]
flat_males = [val for sublist in males for val in sublist]

females = list(csv.reader(open("/Volumes/Raid/NetUser/tlarmst3/Sites/female.csv", "rb")))
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
date = (time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S"))

#display results

statement = "Of %s current pledgers, %s percent are male, %s percent are female, and %s percent are unclear." %(total, male_pct, female_pct, tie_pct)

site_path = "/Volumes/Raid/NetUser/tlarmst3/Sites/"

#write latest values to running CSV
with open(site_path + "results.csv", "a") as csvfile:
	resultswriter = csv.writer(csvfile, delimiter=',')
	resultswriter.writerow([date, male_pct, female_pct, tie_pct, total])

#grabbing values to write to web page

with open(site_path + "results.csv", "rb") as csvread:
	reader= csv.reader(csvread, skipinitialspace=True, quoteing=csv.QUOTE_NONNUMERIC)
	dates, males, females, ties, totals = zip(*reader)

#converting to strings to feed into JavaScript"

date_string = str(dates)
male_string = str(males)
female_string = str(females)
tie_string = str(ties)
total_string = str(totals)

#Writing the web page

with open(site_path + "index.html", "wb" ) as out:
	out.write("<!DOCTYPE html>\n")
	out.write("<html lang=\"en\">\n")
	out.write("\t<head>\n")
	out.write("<meta charset=\"utf-8\">\n")
	out.write("\t \t<title>Pledge History</title>\n")
	#out.write(statement)
	#out.write("\n")
	out.write("\t \t<script type=\"text/javascript\" src=\"../Sites/d3/d3.js\"></script>\n")
	#CSS Style
	out.write("\t \t<style type=\"text/css\">\n")
	out.write("\t \t \t div.bar { \n")
	out.write("\t \t \t \t display: inline-block;\n")
	out.write("\t \t \t \t width: 20px;\n")
	out.write("\t \t \t \t height: 75px; \n")
	out.write("\t \t \t \t margin-right: 2px;\n")
	out.write("\t \t \t \t background-color: teal; \n")
	out.write("\t \t \t } \n")
	out.write("\t \t </style> \n")
	out.write("\t </head>\n")
	#trying a bar graph of male percentage
	out.write("\t <body>\n")
	out.write("\t \t<script type=\"text/javascript\">\n")
	out.write("\t \t \t var dataset =")
	out.write(male_string)
	out.write(";\n")
	out.write("\t \t \t d3.select(\"body\").selectAll(\"div\")\n")
	out.write("\t \t \t \t .data(dataset)\n")
	out.write("\t \t \t \t .enter()\n")
	out.write("\t \t \t \t .append(\"div\")\n")
	out.write("\t \t \t \t .attr(\"class\", \"bar\")\n")
	out.write("\t \t \t \t .style(\"height\", function(d) { \n")
	out.write("\t \t \t \t \t var barHeight = d; \n")
	out.write("\t \t \t \t \t return barHeight + \"px\"; \n")
	out.write("\t \t \t \t });\n")
	out.write("\t \t </script>\n")
	out.write("\t </body>\n")
	out.write("\t </html>\n")
