#This is a Python3 Script
#Note you will need to change the correct directory each time you run it.
#title required
#title, date, location, keywords recommended

import csv
import cgi
import time
import html.parser
import re
import shlex
import os
import unicodedata

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

#CHANGE THESE
#csv file will be created in the same folder as this .py file
#will overwrite whatever is in this file
csv_filename = "test.csv"
#to get the directory name, right-click on a file inside the folder
#->Get Info-> Copy paste the Where field
directory_name = #Insert Directory Here
#CHANGE END

dirList = os.listdir(directory_name)
fileList=[]

print("Getting list of files")
for item in dirList:
    if item.lower().endswith("txt"):
        fileList.append(item)

csvf = open(csv_filename, encoding='utf-8', mode='w+')
firstRowHeader = ["File name*","Photo title (max 50 characters)*","Keywords (max 500 characters)","Date (See instructions for format)","Interval (Years | 1, 2, 3, 5, 10, 15)","Latitude , Longitude","Story","Use Date (TRUE or FALSE)","Date Range? (Y or N)","Licence (See instructions for options)","Copyright holder","Author","Original Link","Repository or Archive","Notes"]

a = csv.writer(csvf)
a.writerows([firstRowHeader])

    
for i in range(0, len(fileList)):
    filename = fileList[i]
    print("Parsing " + filename)
 
    inputfile = open(directory_name + "/" + filename, encoding='utf-8',mode='r')
    text = inputfile.readlines()
    wantedText = []

    #parse any html tags out                                      
    h = html.parser.HTMLParser()

    #remove the endline character from the text
    for i in range(0, len(text)):
        text[i]= h.unescape(text[i]).replace("\n","")

    #initialize lineNum variables
    keywordLineNum = 1
    titleLineNum = 1
    notesLineNum = 1
    photographerLineNum = 1
    urlLineNum = 1
    dateLineNum = 1
    geotagLineNum = 1
    
    #find lineNums for fields
    for i in range(0, len(text)):
        if (text[i] == "|  TITLE  |"): titleLineNum = i+2
        if (text[i] == "|  DESCRIPTION  |"): notesLineNum = i+2
        if (text[i] == "|  TAGS  |"): keywordLineNum = i+2
        if ("Photographer" in text[i]): photographerLineNum = i
        if ("Photo URL" in text[i]): urlLineNum = i
        if ("License" in text[i]): licenseLineNum = i
        if ("Taken Date" in text[i]): dateLineNum = i
        if ("Geotag" in text[i]): geotagLineNum = i

    #error checking
    if (titleLineNum == 1): print("ERROR: No title - "+ filename)
    if (titleLineNum == 1): print("Warning: No description - "+ filename)
    if (titleLineNum == 1): print("Warning: No tags/keywords - "+ filename)
    if (photographerLineNum == 1): print("ERROR: No photographer with file - "+ filename)
    if (urlLineNum == 1): print("Warning: No URL with file - " + filename)
    if (licenseLineNum == 1): print("Warning: No License with file - " + filename)
    if (dateLineNum == 1): print("ERROR: No date with file - " + filename)
    if (geotagLineNum == 1): print("ERROR: No geotag with file - " + filename)

    #description/story
    description = ""
    for j in range(notesLineNum, keywordLineNum - 4):
        text[j] = striphtml(text[j])
        description = description + text[j] + "    "
        description = description.replace(",", "")
    if (description == "no description"): description = ""
    
    #keywords
    keywords  = shlex.split(text[keywordLineNum])
    keyword_string = ", ".join(list(keywords))
    if (keyword_string == "(no, tags)"): keyword_string = ""
    
    #date
    date_string = text[dateLineNum][15:]
    GMTindex = date_string.find("GMT")
    date_string = date_string[:GMTindex]+date_string[GMTindex+9:]

    intermediate_date = time.strptime(date_string, "%c")
    date_string = time.strftime("%Y-%m-%d",intermediate_date)

    #lat_long
    lat_index = text[geotagLineNum].find("Latitude:") + 9
    comma_index = text[geotagLineNum].find(",")
    long_index = text[geotagLineNum].find("Longitude:") + 10
    lat_long = text[geotagLineNum][lat_index:comma_index] + ", " + text[geotagLineNum][long_index:]

    #license
    license_str = text[licenseLineNum][15:]
    if (license_str.find("Creative Commons") != -1):
        license_str = "CC"
    elif (license_str.find("All Rights Reserved") != -1):
        license_str = "C"
    elif (license_str.find("No known copyright restrictions") != -1):
        license_str = "N"
    elif (license_str.find("Public Domain") != -1):
        license_str = "PB"
    elif (license_str.find("Open Government") != -1):
        license_str = "OG"
    else: print("Warning: Unknown license with file - " + filename)
                            
    #filename
    filename = filename.replace("txt", "jpg")

    #append all the desired outputs to wantedText
    wantedText.append(filename)                 #filename
    wantedText.append(text[titleLineNum])       #photo title max 50 char
    wantedText.append(keyword_string[:500])     #keywords max 500
    wantedText.append(date_string)              #YYYY-MM-DD, not YYYY-MM-? or YYYY so far
    wantedText.append("")                      #interval years, not sure
    wantedText.append(lat_long)                 #latitude, longitude
    wantedText.append(description)                      #caption/notes = bulkr description
    wantedText.append("")                        #exact full date is not known
    wantedText.append("")                       #date range
    wantedText.append(license_str)              #license code
    if (photographerLineNum == 0): wantedText.append("")
    else: wantedText.append(text[photographerLineNum][15:])             #copyright holder
    wantedText.append("")                       #original photographer
    if (urlLineNum == 0): wantedText.append("")
    else: wantedText.append(text[urlLineNum][15:])            #link
    wantedText.append("")                       #collection
    wantedText.append("")                        #notes

    #write a file's row of information to the csv file
    a = csv.writer(csvf)
    a.writerows([wantedText])

    inputfile.close()

csvf.close()
print("All done!")
