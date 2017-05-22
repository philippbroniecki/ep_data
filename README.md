# ep_data
Scrape information on MEPs from the EP's Legislative Observatory

Python 2.6 scripts:
1) "01_get_names_and_links.py" scrapes a list of names of MEPs  from a particular term and saves that into the output folder as mep_names.csv
2) "02_get_mep_specific_info3.py" scrapes party, party group affiliations, and committee memberships and saves them in the output folder as mep_info.csv (does not work for EP8)
3) "03_get_mep_specific_info3_ep8_only" does the same as the previous script for the 8th EP.

In all 3 files one must set the working directory. Additionally, in "get_names_and_links.py" one must also set the term to scrape (line 25). You need to have BeautifulSoup installed.
