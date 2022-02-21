# -*- coding: utf-8 -*-
import csv2SKDUPD
import Hafas2csv
import datetime

def header(first_date,last_date,today,org):
    reference=today.strftime("%Y-%m-%dT%H%M%S")
    txt="UIB+UNOB:4+"+reference+"'\n"
    txt+="UIH+SKDUPD:D:04A+1+"+reference+"'\n"
    txt+="MSD+AAR:61'\n"
    txt+="ORG+"+org+"+++"+org+"'\n"
    txt+="HDR+81+273:"+first_date+"/"+last_date+"*45:"+reference[:-2]+"+"+reference+"'\n"
    return txt

def footer(nbr,today):
    reference=reference=today.strftime("%Y-%m-%dT%H%M%S")
    txt="UIT+1+"+str(nbr)+"'\n"
    txt+="UIZ+"+reference+"+1'"
    return txt

def header_footer(org,before,after,first_date,last_date):
    nbr=0
    writer=open(after,'w')
    today=datetime.datetime.now()
    writer.write(header(first_date, last_date, today,org))
    with open(before) as reader:
            for nbr,line in enumerate(reader):
                writer.write(line)
    writer.write(footer(nbr+6   , today))
    
if __name__ == "__main__":   
    H2E=Hafas2csv.HAFAS2EDIFACT()
    H2E.load_calendar()
    H2E.load_hafas()
    liste_stop_unmapped = list(H2E.unmapped_stop.keys())
    print("Please add this stops in the mapping file :")
    print(liste_stop_unmapped)
    H2E=None
    C2S=csv2SKDUPD.csv_to_SKDUPD()
    C2S.create_all_services()
    org='0060'
    name=org+'_'+datetime.date.today().strftime("%Y-%m-%d")
    header_footer(org,"./edifact/skdupd_no_header.r", "./edifact/SKDUPD_"+name+".r", "2022-01-01", "2022-12-11")
    
    print("The End")