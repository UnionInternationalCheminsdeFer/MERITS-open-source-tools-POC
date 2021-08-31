# -*- coding: utf-8 -*-
import datetime


def str_to_date(txt):
    return datetime.date(int(txt[:4]),int(txt[4:6]),int(txt[6:]))

def del_last_zero(txt):
    if txt[-1]=='0':
        return del_last_zero(txt[:-1])
    return txt

def create_POP(service_id,feed):
    calendar_dates=feed['calendar_dates']
    calendar=feed['calendar']
    dic_special_days={}
    if service_id in calendar_dates:
        special_days=calendar_dates[service_id]
        for day,kind in special_days:
            dic_special_days[str_to_date(day)]=kind
        
    calend=calendar[service_id]
    current_day=str_to_date(calend[7])
    last_day=str_to_date(calend[8])
    begin=""
    end=""
    txt=""
    while current_day <= last_day:
        txt+=str(calend[current_day.weekday()])
        if current_day in dic_special_days:
            if dic_special_days[current_day]=='2':
                txt=txt[:-1]+'0'
            elif dic_special_days[current_day]=='1':
                if begin=="":
                    begin=current_day
                end=current_day
                txt=txt[:-1]+'1'

        if  txt[-1]=="1" and begin =="":
            begin=current_day
        if  txt[-1]=='0' and begin =="":
            txt=txt[:-1]
        if len(txt)>0 and txt[-1]=='1':
            end=current_day
        current_day+=datetime.timedelta(days=1)
    
    txt=del_last_zero(txt)
    txt="POP+273:"+begin.strftime('%Y-%m-%d')+'/'+end.strftime('%Y-%m-%d')+'::'+txt+"'\n"
    return txt

def create_PRD(ID,fake_number,feed):
    route_id,service_id=feed['trips'][ID]
    reservation=tariff=''
    agency_id,number,route_type=feed['routes'][route_id]
    if number=='':
        number=str(fake_number)
    
    #FOR SNCF
    #number=ID.split('F')[0][5:].split('R')[0]
    
    txt='PRD+'+number+':'+reservation+':'+tariff+':'+feed['dic_route_type'][route_type][0]+':::+'+feed['dic_org'][agency_id][0]+"'\n"
    return txt

def create_PDT_ASD_SER(ID,feed):
    """ May be used to had attributes
        This version of the program don't use it
    """ 
    txt=""
    equipement=services=facility=''
    stop_times=feed['stop_times']
    stops2UIC=feed['stops2UIC']
    stop_id1=stop_times[ID][0][2]
    stop_id2=stop_times[ID][-1][2]
    if equipement not in ['',None]:  
        txt+='ODI+'+stops2UIC[stop_id1][0]+'*'+stops2UIC[stop_id2][0]+'+1*'+str(len(stop_times[ID]))+"'\n"
        txt+='PDT++:::'+equipement+":::'\n"
        
    if services not in ['',None]:
        for asd in services.split(' '):
            if asd!='':
                txt+='ODI+'+stops2UIC[stop_id1][0]+'*'+stops2UIC[stop_id2][0]+'+1*'+str(len(stop_times[ID]))+"'\n"
                txt+='ASD+'+asd+"'\n"
             
    if facility not in ['',None]:
        for ser in facility.split(' '):
            if ser!='':
                txt+='ODI+'+stops2UIC[stop_id1][0]+'*'+stops2UIC[stop_id2][0]+'+1*'+str(len(stop_times[ID]))+"'\n"
                txt+='SER+'+ser+"'\n"       
    return txt
    
def check_time(time):
    global limit
    time=int(time.split(':')[0]+time.split(':')[1])
    if time>limit:
        time=str(time%2400).zfill(4)+':::1'
        limit+=2400
    else:
        time=str(time%2400).zfill(4)
    return time
    
    
def create_POR(ID,feed):
    global limit
    stop_times=feed['stop_times']
    stops2UIC=feed['stops2UIC']
    txt=''
    limit=2400
    arrival,departure,stop_id,pickup,drop_off=stop_times[ID][0]
    departure=check_time(departure)
    txt+='POR+'+stops2UIC[stop_id][0]+"+*"+departure+"'\n"
    
    for arrival,departure,stop_id,pickup,drop_off in stop_times[ID][1:-1]:
        arrival=check_time(arrival)
        departure=check_time(departure)
        try:
            txt+='POR+'+stops2UIC[stop_id][0]+'+'+arrival+"*"+departure+"+'\n"
        except Exception as e:
            print(e,stop_id)
    arrival,departure,stop_id,pickup,drop_off=stop_times[ID][-1]
    arrival=check_time(arrival)
    txt+='POR+'+stops2UIC[stop_id][0]+"+"+arrival+"'\n"

    return(txt)
    
    
    