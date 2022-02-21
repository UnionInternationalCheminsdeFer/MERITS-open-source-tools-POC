# -*- coding: utf-8 -*-
import datetime

class HAFAS2EDIFACT:
    def __init__(self):
        self.load_mapping_stops("mapping_stops.txt")
        self.load_mapping_equipment("mapping_equipments.txt")
        self.load_mapping_attribute("mapping_attributes.txt")
        self.ID=0
        self.dic_calendar={}
        self.PRD=open('./csv/SKDUPD_TRAIN.csv','w')
        self.POR=open('./csv/SKDUPD_POR.csv','w')
        self.ODI=open('./csv/SKDUPD_ODI.csv','w')
        self.RELATION=open('./csv/SKDUPD_RELATION.csv','w')
        self.unmapped_stop={}
             
    def new_service(self):
        self.ID+=1
        self.dic_train={"ID":self.ID,
                        "service_number":'',
                        "service_characteristic":'',
                        "pricing_category":'',
                        "service_mode":'',
                        "service_name":'',
                        "service_provider":'',
                        "information_provider":'',
                        "reservation_company":'',
                        "begin":'',
                        "end":'',
                        "circulation_days":'',
                        "RFR_number":''}
        self.liste_por=[]
        self.dic_por={}
        self.por_pos=0
        self.liste_odi=[]
        self.dic_odi={}
        self.todo=[]
        self.off_diff=0

    def new_dic_odi(self):
        self.dic_odi={"ID":self.ID,
                      "FromStopNumber":'1',
                      "ToStopNumber":str(self.por_pos),
                      "ASD_or_SER_code":'',
                      "Reservation":'',
                      "Equipment":'',
                      "Tariff":''}
        
    def finish_service(self):
        if self.first:
            self.first=False
            return
        for line in self.todo:
            self.new_dic_odi()
            if line[:2]=='*G':
                self.dic_odi["Equipment"]=self.mapping_equipment[line.split()[1]]
                self.liste_odi.append(self.dic_odi)
            elif line[:2]=='*A':    
                attribute=self.mapping_attribute[line.split()[1]]    
                if '*' in attribute:
                    attribute=attribute.split('*')
                    for att in attribute[1:]:
                        self.todo.append('*A '+att)            
                    attribute=attribute[0]
                if attribute!='None':        
                    if attribute[0] in ['F','S','T']:            
                        self.dic_odi['ASD_or_SER_code']=attribute
                    elif attribute[0] == 'R':
                        self.dic_train['service_characteristic']=attribute[1:]
                    self.liste_odi.append(self.dic_odi)
        #Add weelchair for every service
        self.new_dic_odi()
        self.dic_odi['ASD_or_SER_code']='F28'
        self.liste_odi.append(self.dic_odi)
        self.write_train()
   
    def por(self,line):
        information_arrival=line[29]
        information_departure=line[36]
        if information_arrival=='-' and information_departure=='-':
            if self.ID == 5526:
                    print(line,self.ID,self.por_pos)
            return
        
        self.por_pos+=1
        self.dic_por={'ID':self.ID,
                      'pos':self.por_pos,
                      'UIC':'',
                      'arrival':'',
                      'offsetA':'',
                      'departure':'',
                      'offsetD':'',
                      'quay1':'',
                      'quay2':'',
                      'detail':'',
                      'boarding':'',
                      'message':'',
                      'load':'',
                      'unload':''}
        
        stop_code=line[:7]
        if stop_code not in self.mapping_uic:
            self.unmapped_stop[stop_code]=1
            self.dic_por['UIC']='UIC_code_not_mapped'
        else:
            self.dic_por['UIC']=self.mapping_uic[stop_code]
        
        arrival_time=line[30:35]      
        if arrival_time not in ['     ','']:
            arrival_time=int(arrival_time)-self.off_diff
            if arrival_time>=2400:
                self.dic_por['offsetA']='1'
                self.off_diff+=2400
                arrival_time=str(arrival_time-2400)#).zfill(2)+arrival_time[-2:]
            arrival_time=str(arrival_time).zfill(4)
            self.dic_por['arrival']=arrival_time
            
        departure_time=line[37:42]
        if departure_time not in ['     ','']:
            departure_time=int(departure_time)-self.off_diff
            if departure_time>=2400:
                self.dic_por['offsetD']=1
                self.off_diff+=2400
                departure_time=str(departure_time-2400)#.zfill(2)+departure_time[-2:]
            departure_time=str(departure_time).zfill(4)
            self.dic_por['departure']=departure_time
            
       
        information_arrival=line[29]
        information_departure=line[36]
        if information_arrival=='-' and information_departure=='-':
            self.dic_por['boarding']='4'
        elif information_arrival=='-':
            self.dic_por['boarding']='2'
        elif information_departure=='-':
            self.dic_por['boarding']='1'
        self.liste_por.append(self.dic_por)
        
    def clean_days(self,begin,days):
        current_day=self.str_to_date(begin)
        begin=None
        end=begin
        txt=''
        for day in days:
            if day=='1' and begin==None:
                begin=current_day
            if begin!=None:
                txt+=day
            if day=='1':
                end=current_day
            current_day+=datetime.timedelta(days=1)
        end=end-datetime.timedelta(days=1)-datetime.timedelta(days=1)
        delta=end-begin
        return (begin.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'),txt[:delta.days+1])
          
    def load_hafas(self,path='./Hafas/'):
        self.first=True
        with open(path+'fplan') as file:
            for line in file:
                if line[0]=='%':
                    continue
                if line[:2] =='*T' :
                    self.finish_service()
                    return
                if line[:2]=='*Z':
                    self.finish_service()
                    self.new_service()
                    self.dic_train['service_number']=line.split()[1].lstrip('0')
                    self.dic_train['service_provider']='0060'
                    
                elif line[:5] =='*A VE':
                    self.calendar(line.split()[4])
                elif line[:2] in ['*G','*A']:
                    self.todo.append(line)
                elif line[:2] =='*I':
                    pass
                else:
                    self.por(line)
                    
    def write_train(self):
        txt=''
        for value in self.dic_train.values():
            txt+=str(value)+';'
        txt=txt[:-1]+'\n'
        self.PRD.write(txt)
        
        txt=''
        for dic in self.liste_por:
            for key in ['ID', 'pos', 'UIC', 'arrival', 'offsetA', 'departure', 'offsetD', 'quay1', 'quay2', 'detail', 'boarding', 'message', 'load', 'unload']:
                txt+=str(dic[key])+';'
            txt=txt[:-1]+'\n'
        self.POR.write(txt)
        
        txt=''  
        for dic in self.liste_odi:
            for key in ['ID', 'FromStopNumber', 'ToStopNumber', 'ASD_or_SER_code', 'Reservation', 'Equipment', 'Tariff']:          
                txt+=str(dic[key])+';'
            txt=txt[:-1]+'\n'
        self.ODI.write(txt)
                    
    def str_to_date(self,txt):
        return datetime.date(int(txt[:4]),int(txt[5:7]),int(txt[-2:]))                
                    
    def calendar(self,reference):
        cal=self.dic_calendar[reference]
        days=bin(int(cal,16))[4:]
        begin,end,days=self.clean_days(self.dic_calendar['begin'], str(days))
        
        self.dic_train['begin']=begin
        self.dic_train['end']=end
        self.dic_train["circulation_days"]  =days
    
        
    def load_calendar(self,path='./Hafas/'):
        f= open(path+'eckdaten') 
        txt=f.read().split('\n')
        f.close()
        begin=txt[0][6:]+'-'+txt[0][3:5]+'-'+txt[0][:2]
        end=txt[1][6:]+'-'+txt[1][3:5]+'-'+txt[1][:2]
        self.dic_calendar['begin']=begin
        self.dic_calendar['end']=end
        
        with open(path+'bitfield') as file:
            for line in file:
                line=line.split()
                self.dic_calendar[line[0]]=line[1]
                
        
    def load_mapping_stops(self,fichier):
        self.mapping_uic={}
        with open(fichier) as file:
            for line in file:
                code,UIC=line[:-1].split(';')
                self.mapping_uic[code]=UIC    
    def load_mapping_equipment(self,fichier):
        self.mapping_equipment={}
        with open(fichier) as file:
            for line in file:
                code,equipment=line[:-1].split(';')
                self.mapping_equipment[code]=equipment
    
    def load_mapping_attribute(self,fichier):
        self.mapping_attribute={}
        with open(fichier) as file:
            for line in file:
                code,attribute=line[:-1].split(';')
                self.mapping_attribute[code]=attribute
                
    def close_file(self):
        self.PRD.close()
        self.POR.close()
        self.ODI.close()
        self.RELATION.close()
                
if __name__ == "__main__":
    a=HAFAS2EDIFACT()
    a.load_calendar()
    a.load_hafas()
    liste_stop_unmapped = list(a.unmapped_stop.keys())
    print("Please add this stops in the mapping file :")
    print(liste_stop_unmapped)
    
    