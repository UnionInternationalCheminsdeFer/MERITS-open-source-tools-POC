# -*- coding: utf-8 -*-
import csv

class xlsx_to_TSDUPD:
    def __init__(self,path):
        self.path=path
        self.f_stop=open(path['stops'],'r')
        self.f_prd =  open(path['prd'],'r')
        self.f_other_names = open(path['other_names'],'r',)
        self.f_other_informations = open(path['other_informations'],'r')
        self.edifact=open(self.path['edifact'],'w')
        self.ws_stops = csv.reader(self.f_stop, delimiter=';')
        self.ws_prd =  csv.reader(self.f_prd, delimiter=';')
        self.ws_other_names = csv.reader(self.f_other_names, delimiter=';')
        self.ws_other_informations = csv.reader(self.f_other_informations, delimiter=';')
        

        
    def create_TSDUPD(self):
        dic_relation={}
        for line in self.ws_other_informations:
            UIC1,UIC2,time,unit,rl1,rl2,ser,brand1,brand2,provider1,provider2=line
            if UIC1 not in dic_relation:
                dic_relation[UIC1]=[]
            dic_relation[UIC1]=dic_relation[UIC1]+[(UIC2,time,unit,rl1,rl2,ser,brand1,brand2,provider1,provider2)]
        
        dic_prd={}
        for line in self.ws_prd:
            UIC,service_brand1,service_brand2,connection_time,service_provider1,service_provider2=line
            if UIC not in dic_prd:
                dic_prd[UIC]=[]
            dic_prd[UIC]=dic_prd[UIC]+[(service_brand1,service_brand2,connection_time,service_provider1,service_provider2)]
        
        dic_other_names={}
        for line in self.ws_other_names:
            UIC,country,name=line
            if UIC not in dic_other_names:
                dic_other_names[UIC]=[]
            dic_other_names[UIC]=dic_other_names[UIC]+[(country,name)]
        
        #We pass the header
        next(self.ws_stops) 
        for line in self.ws_stops:
            typo,UIC,name,short_name,lat,lon,begin,end,delay,country,timezone,timezone2,resa=line
            
            txt='ALS+'+typo+'+'+UIC+':'+name
            if lat not in [None,'','None'] and lon not in [None,'','None']:
                txt+='+'+lat+'+'+lon
            txt+="'\n"
            txt+='POP+273'+':'+begin+'/'+end+"'\n"
            if delay not in [None,'','None']:
                txt+='POP+87:'+delay+"'\n"
            txt+="CNY+"+country+"'\n"
            txt+="TIZ+"+timezone+':'+timezone2+"'\n"
            if short_name not in [None,'','None']:
                txt+='IFT+X02+'+short_name+"'\n"
            
            if UIC in dic_other_names:
                for country,name in dic_other_names[UIC]:
                    txt+="IFT+AGW"
                    if country not in  [None,'','None']:
                        txt+="::::"+country
                    txt+='+'+name+"'\n"
                    
            if UIC in dic_prd:
                for service_brand1,service_brand2,connection_time,service_provider1,service_provider2 in dic_prd[UIC]:
                    txt+="PRD+:::"
                    if service_brand1 not in [None,'','None']:
                        txt+=service_brand1
                    txt+=':'
                    if service_brand2 not in [None,'','None']:
                        txt+=service_brand2
                    if connection_time in [None,'','None']:
                        connection_time=''
                        print('Warning : no connection time for ',UIC)
                    else:
                        txt+='::'+connection_time
                    if service_provider1 not in [None,'','None'] :
                         txt+='+'+service_provider1
                    elif service_provider2 not in [None,'','None']:
                        txt+='+'
                    if service_provider2 not in [None,'','None']:
                        txt+='*'+service_provider2
                    txt+="'\n"          
            
            if resa not in [None,'','None']:
                txt+='RFR+X01:'+resa+"'\n"
            PRD=False
            if UIC in dic_relation:
                for UIC2,time,unit,rl1,rl2,ser,brand1,brand2,provider1,provider2 in dic_relation[UIC]:
                    if UIC2 not in [None,'','None']:
                     txt+='RFR+AWN:'+UIC2+"'\n"
                    if time not in [None,'','None']:
                        txt+='MES+'+time+':'+unit+"'\n"
                    if rl1  not in [None,'','None']:
                        txt+='RLS+'+rl1+'+'+rl2+"'\n"
                    if brand1 or brand2 or provider1 or provider2 not in [None,'','None']:
                        txt+="PRD+:::"
                        PRD=True
                        if brand1 not in [None,'','None']:
                            txt+=brand1
                        txt+=':'
                        if brand2 not in [None,'','None']:
                            txt+=brand2
                        if provider1 not in [None,'','None'] :
                             txt+='+'+provider1
                        elif provider2 not in [None,'','None']:
                            txt+='+'
                        if provider2 not in [None,'','None']:
                            txt+='*'+provider2
                        txt+="'\n"
                        
                    if ser not in [None,'','None']:
                        if not PRD:
                            txt+="PRD'\n"
                        for SER in ser.split(';')[:-1]:
                            txt+="SER+"+SER+"'\n"
      
            self.edifact.write(txt)
        self.edifact.close()
              
if __name__ == "__main__":   
    path={}
    path['stops']='./CSV/TSDUPD_STOPS.csv'
    path['prd']='./CSV/TSDUPD_MCT.csv'
    path['other_names']='./CSV/TSDUPD_SYNONYMS.csv'
    path['other_informations']='./CSV/TSDUPD_FOOTPATH.csv'
    path['edifact']='./NEW_TSDUPD/new_tsdupd.r'
    tr=xlsx_to_TSDUPD(path)
    tr.create_TSDUPD()
    print("Finished")
