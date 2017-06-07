# -*- encoding: utf-8 -*-

from __future__ import print_function
#from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import codecs
#import webbrowser # to open web pages
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

#############################################################################
# Functions
#############################################################################

### cleaning functions
## remove duplicates from list
def no_duplicates(input_list):
	output = []
	seen = set()
	for value in input_list:
		if value not in seen:
			output.append(value)
			seen.add(value)
	return(output)

#### date functions
## recognise date in sibling
def is_date(sibling):
	if re.search("[0-9][0-9].[0-9]{4}",sibling) or re.search("[0-9][0-9]?.*[0-9]{4}", sibling):
		return(True)
	else:
		return(False)

## get the dates from a sibling
def get_date(sibling):
	dates = ['start and end dates']
	daten = re.findall('[0-9]{2}.[0-9]{2}.[0-9]{4}',sibling)
	for datum in daten:
		datum = datetime.strptime(datum,'%d.%m.%Y')
		dates.append(datum)
	return(dates)

## remove all line breaks and tabs from string
def remove_breaks_and_tabs(sibling):
	text = str(sibling.get_text().strip())
	# removing tabs
	text = text.replace("\t","")
	# removing line break 1
	text = text.replace("\r","")
	# removing line break 2
	text = text.replace("\n","")
	return(text)

#### EPG functions
## extract epg
def get_epg(child, I_want):
	text = str(remove_breaks_and_tabs(child))
	if (re.search("-", text) and I_want == "European Political Groups"):
		# get everything between colon and hyphen
		epg = re.findall("(?<=:)(.*)(?=-)", text)
	else:
		# get everything following the colon
		epg = re.findall(":(.*)", text)
	return(epg)

### Info_tag walk
## to extract parties, group, chairs, vice-chairs, substitutes and members, committees only
def info_walk(tag, start_condition, stop_condition, I_want):
	#######################################
	# walk over info_tag children
	if ("what_to_extract" in locals()):
		pass
	start_once = 0 # to start only at the first start condition encountered
	for child in tag.children:
		# stop condition in child (the topic below the topic to extract - can be multiple things)
		if (child.name == "h4" and child.string in stop_condition):
			#print ("Break in top child of", I_want, "routine")
			break
		# pass over condition (go to the next iteration until you arrive at topic of interest)
		if not (child.name == "h4" and child.string in start_condition):
			continue
		# start condition (but start only once if multiple starting conditions)
		if (start_once == 0 and child.string in start_condition and child.name == "h4"):
			start_once == 1 # to not start again
		################################################
		# begining the walk over the child's siblings
		for sibling in child.next_siblings:
			# stop conditions
			if (sibling.name == "h4" and sibling.string in stop_condition):
				#print ("Break in 2nd Lvl (Sibling)", I_want, "routine")
				break
			# get the contents of the sibling as unicode
			sibling_text = unicode(sibling).strip()
			# chek for dates in sibling (they indicate )
			if is_date(sibling_text):
				#########################################
				# correct tag indentified - now walking over the siblings children
				lvl3_counter = 0
				for lvl3_tag in sibling.children:
					try:
						# get the date
						lvl3_text = unicode(lvl3_tag).strip()
						datum = get_date(lvl3_text)
						#print(lvl3_text)
						#print(datum)
						#print(len(datum))
						#print (datum[1])
						#print (end_time)
						#print( datum[1] < end_time)
						#if (len(datum)==2 and datum[1] < end_time):
						#	print("shalala")
						

						# is the date in the current EP term?
						if (len(datum)==2 and datum[1] < end_time) or (len(datum)==3 and datum[1] < end_time and datum[2] > start_time):
						#if (datum[1] < end_time and datum[2] > start_time) or (len(datum==1) and datum[1] < end_time):
							#print("atze peng")
							#print(I_want)
							# counting the level 3 tags with dates in them
							lvl3_counter += 1
							#print(lvl3_counter)
							# what to extract
							if lvl3_counter == 1:
								#print(lvl3_tag)
								what_to_extract = list(get_epg(lvl3_tag, I_want))
								start_date_to_extract = [datum[1].strftime('%d.%m.%Y')]
								if len(datum)==3:
									end_date_to_extract = [datum[2].strftime('%d.%m.%Y')]
								# stip whitespaces
								for val, element in enumerate(what_to_extract):
									what_to_extract[val] = element.strip()
							else:
								what_to_extract.append(get_epg(lvl3_tag, I_want)[0])
								start_date_to_extract.append(datum[1].strftime('%d.%m.%Y'))
								end_date_to_extract.append(datum[2].strftime('%d.%m.%Y'))
								# stip whitespaces
								for val, element in enumerate(what_to_extract):
									what_to_extract[val] = element.strip()
							#print(what_to_extract)
							#print(len(what_to_extract))
							
							
							continue
						else:
							continue
					except:
	
						continue
	if "what_to_extract" in locals():
		if not "end_date_to_extract" in locals():
			if I_want == "European Political Groups" or "National parties" or "Chairmanships" or "Vice-Chairmanships" or "Members" or "Substitutes":
				if len(start_date_to_extract) == 1:
					end_date_to_extract = datetime.strptime("30.06.2019",'%d.%m.%Y')
					end_date_to_extract = [end_date_to_extract.strftime('%d.%m.%Y')]
				if len(start_date_to_extract) > 1:
					tmp_date = datetime.strptime("30.06.2019",'%d.%m.%Y')				
					for date_idx in range(0,len(start_date_to_extract)):  
						#print(date_idx)
						if date_idx == 0:
							end_date_to_extract = [tmp_date.strftime('%d.%m.%Y')]
						if date_idx > 0:
							end_date_to_extract.append(tmp_date.strftime('%d.%m.%Y'))

			return(what_to_extract, start_date_to_extract, end_date_to_extract)		
		else:
			return(what_to_extract, start_date_to_extract, end_date_to_extract)		
	#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#")
	return([], [], [])
	
	

#############################################################################
# folders input output
#############################################################################
output_dir = "C:\\Users\\phili\\Dropbox\\Dokumente\\London\\UCL\\Dis\\EP data\\output"

# change directory
os.chdir(output_dir)

# reading csv file
with open ('mep_names.csv', 'rb') as csvfile:
	names_sheet = csv.reader(csvfile, delimiter=str(u","))
	terms, names, links = zip(*names_sheet)
terms = list(terms)
names = list(names)
links = list(links)

##############################################################################
# start of parliamentary terms
# constitutive session are in the beginning of July usually
# 8th EP: 1 July
# 7th EP: 14 July
# 6th EP: 20 July (end 30 July)
# 5th EP: ?
# 4th EP: ?
# 3rd EP: ?
# 2nd EP: ?
# 1st EP: ?
term_start = {1: "01.07.1979", 2: "01.07.1984", 3: "01.07.1989", 4: "01.07.1994",
5: "01.07.1999", 6: "20.07.2004", 7: "14.07.2009", 8: "01.07.2014"}
# end of parliamentary terms
term_end = {1: "30.06.1984", 2: "30.06.1989", 3: "30.06.1994", 4: "30.06.1999",
5: "30.06.2004", 6: "30.06.2009", 7: "30.06.2014", 8: "30.06.2019"}
# variable names
nationality = ["Nationality"]
birthdate = ["Date_Born"]
epg = ["EPG"] # european party group
party  = ["Party"] # national party
chair = ["Chairmanships"] # activities chaired by MEP
vice = ["Vice_Chairmanships"] # activities where MEP is vice-chair
member = ["Member"] # activities where MEP is a member
sub = ["Substitute"] # activities where MEP is a substiture
chair_debut = ["Chair_Start"]
chair_fin = ["Chair_End"]
vice_debut = ["Vice_Start"]
vice_fin = ["Vice_End"]
member_debut = ["Member_Start"]
member_fin = ["Member_End"]
sub_debut = ["Sub_Debut"]
sub_fin = ["Sub_Fin"]

##############################################################################
## looping over links list
main_counter = 0
for index, link in enumerate(links[1:]): # loop over all links
#for index, link in enumerate(links[1:2]): # for testing
	print ("#############################################################################")

	# to navigate to MEP history
	history_link = re.sub('\_home.html$', '', link)
	history_link = link + "_history.html"

	# loop index
	main_counter += 1

	# which term
	term = terms[main_counter]
	#print( term_end[int(term)])
	start_time = datetime.strptime(term_start[int(term)],'%d.%m.%Y')
	end_time = datetime.strptime(term_end[int(term)], '%d.%m.%Y')

	# download page and check if download okay
	content = requests.get(link)
	hist_content = requests.get(history_link)
	content.raise_for_status()
	hist_content.raise_for_status()

	soup = BeautifulSoup(content.text.decode('utf-8', 'ignore'), "html.parser")
	hist_soup = BeautifulSoup(hist_content.text.decode('utf-8', 'ignore'), "html.parser")

	##############################
	# this tag contains main info
	info_tag = soup.find("div", {"class": "boxcontent nobackground"})
	history_tag = hist_soup.find("div", {"class": "boxcontent nobackground"})
	## nationality
	# get the nationality tag
	nat_tag = soup.find("li", {"class": "nationality noflag"})
	nat_tag = (nat_tag.get_text()).strip()
	# taking only the first line (sometimes the country is followed by the party)
	try:
		test = nat_tag
		nat_tag = re.findall("(.*)(?=\n)", nat_tag)[0]
	except:
		pass

	############################
	## european party group
	epg_tag, epg_start, epg_end = info_walk(tag = history_tag, 
		start_condition = ["Political groups"], 
		stop_condition = ["National parties"], 
		I_want = "European Political Groups")
	if len(epg_tag) == 1 :
		epg_tag = ''.join(epg_tag)
	else:
		epg_tag = '; '.join(map(str, epg_tag))

	##########################
	# national party
	party_tag, party_start, party_end = info_walk(tag = history_tag,
		start_condition = ["National parties"],
		stop_condition = ["Chair", "Vice-Chair","Member","Substitute"],
		I_want = "National parties")
	if len(party_tag) == 1 :
		party_tag = ''.join(party_tag)
	else:
		party_tag = '; '.join(map(str, party_tag))

	##########################
	hist_soup.find("div", {"class": "boxcontent nobackground"})
	# date of birth
	try:
		birth_tag = soup.find(string=re.compile("birth")).strip()
		#birth_tag = soup.find("span", {"class": "more_info"})
		print (birth_tag)
		if is_date(birth_tag):
			birth_tag = re.findall("[0-9][0-9]?\s+\w+\s+[0-9]{4}", birth_tag)[0].strip()
			m_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
			8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
			for month in m_names:
				if m_names[month] in birth_tag:
					birth_tag = birth_tag.replace(m_names[month], str(month))
					birth_tag = datetime.strptime(birth_tag,'%d %m %Y')
					birth_tag = birth_tag.strftime('%d.%m.%Y')
		else:
			birth_tag = []
	except:
		pass

	#########################
	# Chair
	# info-tag-walk routine works in all EPs
	chair_tag, chair_start, chair_end = info_walk(tag = history_tag,
		start_condition = ["Chair"],
		stop_condition = ["Vice-Chair","Member","Substitute"],
		I_want = "Chairmanships")
	chair_tag = '; '.join(map(str, chair_tag))
	chair_start = '; '.join(map(str, chair_start))
	chair_end = '; '.join(map(str, chair_end))

	#########################
	# Vice-chairs
	vice_tag, vice_start, vice_end = info_walk(tag = history_tag,
		start_condition = ["Vice-Chair"],
		stop_condition = ["Member", "Substitute"],
		I_want = "Vice-Chairmanships")
	vice_tag = '; '.join(map(str, vice_tag))
	vice_start = '; '.join(map(str, vice_start))
	vice_end = '; '.join(map(str, vice_end))

	#########################
	# Members
	member_tag, member_start, member_end = info_walk(tag = history_tag,
		start_condition = ["Member"],
		stop_condition = ["Substitute"],
		I_want = "Members")
	member_tag = '; '.join(map(str, member_tag))
	member_start = '; '.join(map(str, member_start))
	member_end = '; '.join(map(str, member_end))

	#########################
	# Substitue
	sub_tag, sub_start, sub_end = info_walk(tag = history_tag,
		start_condition = ["Substitute"],
		stop_condition = [""],
		I_want = "Substitutes")
	sub_tag = '; '.join(map(str, sub_tag))
	sub_start = '; '.join(map(str, sub_start))
	sub_end = '; '.join(map(str, sub_end))

	#########################################################
	# appending lists
	#########################################################
	# append the committee activities list
	#webbrowser.open(link)
	print (names[index+1])
	print (link)
	## nationality
	nationality.append(nat_tag)
	print (nationality[index+1].decode('utf-8', 'ignore'))
	## date of birth
	birthdate.append(birth_tag)
	## epgs
	#epg_tag = no_duplicates(epg_tag)
	epg.append(epg_tag)
	print ("EPG:", epg_tag)
	## national parties
	party.append(party_tag)
	print ("Nat. party:", party_tag)
	## chairmanships
	#chair_tag = no_duplicates(chair_tag)
	chair.append(chair_tag)
	chair_debut.append(chair_start)
	chair_fin.append(chair_end)
	## vice-chairmanships
	#vice_tag = no_duplicates(vice_tag)
	vice.append(vice_tag)
	vice_debut.append(vice_start)
	vice_fin.append(vice_end)
	## members
	#member_tag = no_duplicates(member_tag)
	member.append(member_tag)
	member_debut.append(member_start)
	member_fin.append(member_end)
	## substitutes
	#sub_tag = no_duplicates(sub_tag)
	sub.append(sub_tag)
	sub_debut.append(sub_start)
	sub_fin.append(sub_end)
		# chair count
	if chair[index+1].count(";") == 0:
		if len(chair[index+1]) > 0:
			chaircount = 1
		else:
			chaircount = 0
	else:
		chaircount = chair[index+1].count(";") + 1
	# vice chair count
	if vice[index+1].count(";") == 0:
		if len(vice[index+1]) > 0:
			vicecount = 1
		else:
			vicecount = 0
	else:
		vicecount = vice[index+1].count(";") + 1
	# member count
	if member[index+1].count(";") == 0:
		if len(member[index+1]) > 0:
			membercount = 1
		else:
			membercount = 0
	else:
		membercount = member[index+1].count(";") + 1
	# substitute count
	if sub[index+1].count(";") == 0:
		if len(sub[index+1]) > 0:
			subcount = 1
		else:
			subcount = 0
	else:
		subcount = sub[index+1].count(";") + 1
	print ("Chairs:", chaircount, "Vice-Chairs:", vicecount, "Members:", membercount, "Substitutes:", subcount)
	print ("Percent done:", format((index / float(len(links)))*100, '.2f') )

#######################################################################################
# putting together the output sheet
mep_info_sheet = zip(names, links, nationality, birthdate, epg, party, chair, chair_debut,
	chair_fin, vice, vice_debut, vice_fin, member, member_debut, member_fin, sub,
	sub_debut, sub_fin)

# change directory
os.chdir(output_dir)

# writing to csv
sheet_name = 'mep_info.csv'
f = open(sheet_name,"wb")
fw = csv.writer(f)
fw.writerows(mep_info_sheet)
f.close()
