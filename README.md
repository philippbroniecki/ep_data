# ep_data
Scrape information on MEPs from the EP's Legislative Observatory

Python 2.6 scripts:
1) "01_get_names_and_links.py" scrapes a list of names of MEPs  from a particular term and saves that into the output folder as mep_names.csv
2) "02_get_mep_specific_info3.py" scrapes MEP info and saves to the output folder as mep_info.csv (does not work for EP8)
    - variables are MEP_Name; MEP_Links; Nationality; Date_Born; EPG; Party; Chairmans; Chair_Start; Chair_End; Vice_Chair; Vice_Start; Vice_End; Member; Meber_Start; Member_End; Substitute; Sub_Debut; Sub_Fin
3) "03_get_mep_specific_info3_ep8_only" does the same as the previous script for the 8th EP.

In all 3 files one must set the working directory. Additionally, in "get_names_and_links.py" one must also set the term to scrape (line 25). You need to have BeautifulSoup installed.

The variables: EPG; Party; Chairmans; Chair_Start; Chair_End; Vice_Chair; Vice_Start; Vice_End; Member; Meber_Start; Member_End; Substitute; Sub_Debut; Sub_Fin can all have more than 1 entry per cell. An MEP who was a member in three committees, e.g. will have 3 entries in the Member variable, the Member_Start variable, and the Member_End variable seperated by a semicolon.
