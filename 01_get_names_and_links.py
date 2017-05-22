# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup # process web page
import urllib2 # get web page
import csv # writing csv files
import os # ordnerstruktur

import sys
reload(sys)
#sys.setdefaultencoding('utf8')
sys.setdefaultencoding('utf8')

# folders input output
output_dir = "C:\\Users\\phili\\Documents\\GitHub\\ep_data\\output"

# root stem of source page
root_page = "http://www.europarl.europa.eu"

# variables
mep_names = ['MEP_Name']
mep_links = ['MEP_Links']
ep_term = ['EP_Term']

# which EPs to scrape (ie, 1st, 2nd ...)
terms = range(4, 5) # e.g. (4,5) will take the 4th EP
#terms = 6

# looping over parliamentary terms
for term in terms:

    # screen output
    print "#######################################################"
    print "Parliamentary Term:", term
    # fetch page
    url = root_page + "/meps/en/directory.html?filter=all&leg=" + str(term)
    print "Fetching from:", url
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    # the tag that identifies MEPs
    meps_tag = soup.find_all("div", {"class": "mep_details"})
    # the names of the MEP
    for index in range(0, len(meps_tag)):
        # encoding strings properly to utf-8
        meps = meps_tag[index].a.string.encode('utf-8').strip()
        mep_names.append(meps)
        link = root_page+str(meps_tag[index].a.attrs.get('href'))
        mep_links.append(link)
        ep_term.append(term)
    # screen output number of MEPs this legislative term
    print "Number of MEPs:", len(meps_tag)

#######################################################################################
# putting together the output sheet
names_sheet = zip(ep_term,mep_names,mep_links)

# change directory
os.chdir(output_dir)

# writing to csv
sheet_name = 'mep_names.csv'
f = open(sheet_name,"wb")
fw = csv.writer(f)
fw.writerows(names_sheet)
f.close()
