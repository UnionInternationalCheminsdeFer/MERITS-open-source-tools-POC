# -*- coding: utf-8 -*-
import csv
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
    
class csv_to_SKDUPD:
    def __init__(self,path):
        self.path=path
        
    def new_odi_en_cours(self):
        self.odi_en_cours={'ODI++':'',
                           'ODI++*':'',
                           'value':'',
                           'PDT++':'',
                           'PDT++:::':'',
                           'PDT++::::::':''}
        
    def new_por_en_cours(self):
        self.por_en_cours={'POR+':'',
                           'POR++':'',
                           'POR++:::':'',
                           'POR++*':'',
                           'POR++*:::':'',
                           'POR+++':'',
                           'POR+++*':'',                           
                           'POR++++':'',
                           'TRF+':'',
                           'MES+':'',
                           'ASD+7':'',
                           'ASD+9':'',
                           'ASD+44':'',
                           'ASD+45':''}                      
                           
    def new_train(self):
        self.info_train={'PRD+':'',
                         'PRD+:':'',
                         'PRD+::':'',
                         'PRD+:::':'',
                         'PRD+::::::':'',
                         'PRD++':'',
                         'PRD++*':'',
                         'PRD++**':'',
                         'POP+':'',
                         'POP+:':'',
                         'POP+:/':'',
                         'POP+:::':'',
                         'RFR+:':''}  
     
    def clean(self,txt):
        txt=txt.replace("::::::+",'+')
        txt=txt.replace("**'","'")
        txt=txt.replace('*+','+')
        txt=txt.replace('²','*')
        txt=txt.replace("+*'","+'")
        txt=txt.replace("+*+","++")
        return txt
        
    def PRD_POP(self,ID):
        service_number,service_characteristic,pricing_category,service_mode,service_name,service_provider,information_provider,reservation_company,beginning_date,end_date,circulation_days,RFR_number=self.dic_train[ID]
        txt_prd='PRD+'+service_number+':'+service_characteristic+':'+pricing_category+':'+service_mode+':::'+service_name+'+'+service_provider
        txt_prd+='*'+information_provider+'*'+reservation_company+"'\n"
        txt=self.clean(txt_prd)
        if RFR_number!='':
            txt_RFR='RFR+AVI:'+RFR_number+"'\n"
            txt+=self.clean(txt_RFR)
        txt_pop='POP+273:'+beginning_date+'/'+end_date+'::'+circulation_days+"'\n"
        txt+=self.clean(txt_pop)
        return txt
        
    def POR(self,ID):
        txt=''
        for cpt,row in enumerate(self.dic_por[ID]):
            pos,UIC,arrival,offsetA,departure,offsetD,quay1,quay2,detail,boarding,message,load,unload,check_out,check_in=row
            if offsetA=='1':
                offsetA=':::1'
            if offsetD=='1':
                offsetD=':::1'
            txt_por='POR+'+UIC+'+'+arrival+offsetA+'*'+departure+offsetD+'+'+quay1+'²'+quay2
            if detail!='':
                txt_por+='+'+detail
            txt_por+="'\n"
            txt_por=self.clean(txt_por)
   
           
            txt+=txt_por
            if message!='':
                txt+='MES+'+message+"'\n"
                               
            if load!='':
                txt+=load+"'\n"
            if unload!='':
                txt+=unload+"'\n"
                
            
            if check_out!='':
                txt+='ASD+44::'+check_out+"'\n"
            if check_in!='':
                txt+='ASD+45:'+check_in+"'\n"
                
            if boarding!='':
                txt+="TRF+"+boarding+"'\n"
                
          
                
           
            if ID in self.dic_relation:
                for row in self.dic_relation[ID]:
                    if str(cpt+1) ==row[0]:
                        stop_pos,service_number,relationship,transfer_time,typo,nop,nop2=row
                        txt+='RFR+AUE:'+service_number+"'\n"
                        txt+='RLS+13+'+relationship+"'\n"
                        if transfer_time!='' or typo!='':
                            txt+='TCE+'+transfer_time+'+'+typo+"'\n"""
        return txt
       
    def ODI(self,ID):
        txt=''
            
        if ID in self.dic_odi:
            for row in self.dic_odi[ID]:
                start,end,value,reservation,equipment,tariff=row
                if start!='':
                    uic1=self.dic_por[ID][int(start)-1][1]
                    uic2=self.dic_por[ID][int(end)-1][1]
                    txt+='ODI+'+uic1+'*'+uic2+'+'+start+'*'+end+"'\n"
                    
                if value!='':
                    if value[0]=='S':
                        txt+="SER+"+value[1:]+"'\n"
                    elif value[0]=='A':
                        txt+="ASD+"+value[1:]+"'\n"
                    elif value[0]=='T':
                        txt+="TFF+"+value[1:]+"'\n"
                if equipment !='' or reservation!='' or tariff!='':
                    txt+='PDT++'+reservation+':::'+equipment+':::'+tariff+"'\n"
                
        return txt
                
           
       
  
    
    def create_train(self,ID):
        txt=self.PRD_POP(ID)
        txt+=self.POR(ID)
        txt+=self.ODI(ID)
        return txt
        
        
        
    def load(self,path):
        self.dic_train={}
        with open(path+'SKDUPD_TRAIN.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"',doublequote=False, escapechar='²')
            #We ignore the first line
            next(reader) 
            for row in reader:
                self.dic_train[row[0]]=row[1:]
        self.dic_relation={}
        with open(path+'SKDUPD_RELATION.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            #We ignore the first line
            next(reader) 
            for row in reader:
                if row==[]:
                    continue
                if row[0] not in self.dic_relation:
                    self.dic_relation[row[0]]=[]
                self.dic_relation[row[0]]=self.dic_relation[row[0]]+[row[1:]]
        self.dic_por={}
        with open(path+'SKDUPD_POR.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            #We ignore the first line
            next(reader) 
            for row in reader:
                if row==[]:
                    continue
                if row[0] not in self.dic_por:
                    self.dic_por[row[0]]=[]
                self.dic_por[row[0]]=self.dic_por[row[0]]+[row[1:]]
        self.dic_odi={}
        with open(path+'SKDUPD_ODI.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            #We ignore the first line
            next(reader) 
            for row in reader:
                if row==[]:
                    continue
                if row[0] not in self.dic_odi:
                    self.dic_odi[row[0]]=[]
                self.dic_odi[row[0]]=self.dic_odi[row[0]]+[row[1:]]

    def create_all_services(self):
        self.load(self.path['csv'])
        f=open(self.path['edifact'],'w')
        for X in range(1,len(self.dic_train)+1):
            f.write(self.create_train(str(X)))
            
        f.close()
    
    
    
if __name__ == "__main__":   
    path={}
    path['csv']='./CSV/'
    path['edifact']='./NEW_SKDUPD/temp.r'
    tr=csv_to_SKDUPD(path)
    tr.create_all_services()
    org='0000'
    begin_date="2021-01-01"
    end_date="2021-12-12"
    header_footer(org,"./NEW_SKDUPD/temp.r", "./NEW_SKDUPD/new_SKDUPD.r",begin_date ,end_date )
    
    print("Finished")
