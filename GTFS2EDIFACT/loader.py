# -*- coding: utf-8 -*-
import csv

def read_config_file():
    config={}
    f=open("./config/config.txt")
    txt=f.read().split('\n')
    for line in txt[:-1]:
        if txt!='':
            k,v=line.split(",")
            config[k]=v
    return config

def read_gtfs_file_with_list(file,head_liste):
    dic={}
    head={}
    
    with open(file,encoding="utf-8-sig", newline='') as f:
        reader = csv.reader(f)
        header=next(reader)
        for cpt,X in enumerate(header):
            for Y in head_liste:
                if X==Y:
                    head[Y]=cpt
            
        for row in reader:
            tab=[]
            for X in head_liste[1:]:
                tab.append(row[head[X]])
            if row[head[head_liste[0]]] not in dic:
                dic[row[head[head_liste[0]]]]=[]
            dic[row[head[head_liste[0]]]]=dic[row[head[head_liste[0]]]]+[tab]
    return dic
    

def read_gtfs_file(file,head_liste):
    dic={}
    head={}
    
    with open(file,encoding="utf-8-sig", newline='') as f:
        reader = csv.reader(f)
        header=next(reader)
        for cpt,X in enumerate(header):
            for Y in head_liste:
                if X==Y:
                    head[Y]=cpt
            
        for row in reader:
            tab=[]
            for X in head_liste[1:]:
                tab.append(row[head[X]])
            dic[row[head[head_liste[0]]]]=tab
    return dic

def load_files():
    head_liste=['trip_id','route_id','service_id']
    trips=read_gtfs_file('./GTFS/trips.txt',head_liste)
    
    head_liste=['agency_id','agency_name','agency_timezone']
    agency=read_gtfs_file('./GTFS/agency.txt',head_liste)
    
    head_liste=['route_id','agency_id','route_short_name','route_type']
    routes=read_gtfs_file('./GTFS/routes.txt',head_liste)
    
    head_liste=['service_id','monday','tuesday','wednesday','thursday','friday','saturday','sunday','start_date','end_date']
    calendar=read_gtfs_file('./GTFS/calendar.txt',head_liste)
    
    head_liste=['stop_id','stop_name','stop_lat','stop_lon']
    stops=read_gtfs_file('./GTFS/stops.txt',head_liste)
    
    head_liste=['stop_id','UIC']
    stops_mapping=read_gtfs_file('./config/stops_mapping.txt',head_liste)
   
    head_liste=['org','UIC_org']
    dic_org=read_gtfs_file('./config/organisation conversion.txt',head_liste)
    
    head_liste=['route_id','edifact_id']
    dic_route_type=read_gtfs_file('./config/route_type.txt',head_liste)

    head_liste=['service_id','date','exception_type']
    try:
        calendar_dates=read_gtfs_file_with_list('./GTFS/calendar_dates.txt',head_liste)
    except FileNotFoundError :
        calendar_dates={}
    
    head_liste=['trip_id','arrival_time','departure_time','stop_id','pickup_type','drop_off_type']
    stop_times=read_gtfs_file_with_list('./GTFS/stop_times.txt',head_liste)
    
    config=read_config_file()
    feed={"agency":agency,
          "routes":routes,
          "calendar":calendar,
          "calendar_dates":calendar_dates,
          "stops":stops,
          "trips":trips,
          "calendar_dates":calendar_dates,
          "stop_times":stop_times,
          "stops2UIC":stops_mapping,
          "dic_org":dic_org,
          "dic_route_type":dic_route_type,
          "config":config}
    return feed


    
    