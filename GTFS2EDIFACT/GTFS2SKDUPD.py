# -*- coding: utf-8 -*-
import datetime
from loader import load_files
from writer import create_PRD,create_POP,create_POR,create_PDT_ASD_SER


def convert_GTFS_to_SKDUPD():
    feed=load_files()
    config=feed['config']
    f=open("./SKDUPD/skdupd_without_header.r",'w')
    number=0
    for ID in feed['trips']:
        number+=1
        f.write(create_train(ID,number,feed))
    f.close()
    header_footer(config['ORG'],"./SKDUPD/skdupd_without_header.r", "./SKDUPD/SKDUPD_"+config['ORG']+".r", config['BEGIN'], config['END'])
    
def create_train(ID,number,feed):
    route_id,service_id=feed['trips'][ID]
    txt=create_PRD(ID,number,feed)
    txt+=create_POP(service_id,feed)
    txt+=create_POR(ID,feed)
    txt+=create_PDT_ASD_SER(ID,feed)
    return txt
    
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
    convert_GTFS_to_SKDUPD()
    print("Finished")
    
    