# Overview
MERITS (Multiple East-West Railways Integrated Timetable Storage) is a database, owned by UIC, containing the integrated timetable data of many European and some non-European countries (Russia, Turkey, Belarus), comprising a few hundred railway undertakings (RUs), which are published twice a week. https://uic.org/passenger/passenger-services-group/merits#Glossary

MERITS use the EDIFACT format and messages. SKDUPD for timetable, TSDUPD for locations. 
The MERITS open source tools below provide Python code to convert the EDIFACT format in another formats as GTFS or CSV or to transfer location data into Excel file

# Convert TSDUPD file <=> EXCEL file
Download TSDUPD2xlsx.py and xlsx2TSDUPD.py in a directory

install openpyxl with the command **pip install openpyxl** in the windows shell

Create 3 directories named : TSDUPD, XLSX, NEW_TSDUPD

Copy a TSDUPD file in the TSDUPD directory

TSDUPD2xlsx.py will read the TSDUDP directory and create the excel files in the XLSX directory
xlsx2TSDUPD.py will read the XLSX directory and create a TSDUPD file in the NEW_TSDUPD directory

**/!\ Warning : When editing the excel files, always force the format to text only !**

# Convert TSDUPD file <=> CSV file
Download TSDUPD2csv.py and csv2TSDUPD.py in a directory

Create 3 directories named : TSDUPD, CSV, NEW_TSDUPD

Copy a TSDUPD file in the TSDUPD directory

TSDUPD2csv.py will read the TSDUDP directory and create the csv files in the CSV directory

csv2TSDUPD.py will read the CSV directory and create a TSDUPD file in the NEW_TSDUPD directory

**/!\ Warning : Do not edit the csv files with excel, since it will change the format of the dates & numbers**

# Convert SKDUPD file <=> CSV file
Download SKDUPD2csv.py and csv2SKDUPD.py in a directory

Create 3 directories named : SKDUPD, CSV, NEW_SKDUPD

Copy the SKDUPD files in the SKDUPD directory

SKDUPD2csv.py will read the SKDUDP directory and create the csv files in the CSV directory

csv2SKDUPD.py will read the CSV directory and create a SKDUPD file in the NEW_SKDUPD directory

**/!\ Warning : Do not edit the csv files with excel, since it will change the format of the dates & numbers**

# Convert GTFS file => SKDUPD file
Download GTFS2edifact.py

Create 2 directories named : GTFS, NEW_SKDUPD

Copy the GTFS files in the GTFS directory

Create the mapping files for agency and stops

GTFS2edifact.py will read the GTFS directory and create a new SKDUPD file in the NEW_SKDUPD directory
