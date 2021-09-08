# -*- coding: utf-8 -*-
import glob


class SKDUPD_to_csv:
    def __init__(self,path):
        self.path=path
        self.fichier_odi=open(path['odi'],'w')
        self.fichier_por=open(path['por'],'w')
        self.fichier_train=open(path['train'],'w')
        self.fichier_relation=open(path['relation'],'w')
        self.fichier_train.write('ID;Service_number;Reservation;Tariff;Service_Mode;Service_Name;Service_Provider;not_used;Reservation_system;First_day;Last_day;Operation_days;Second_service_number\n')
        self.fichier_por.write('ID;Stop_number;UIC;Arrival_time;Arrival_offset;Departure_time;Departure_offset;Platform_arrival;Platform_departure;Stop_property;Traffic_restriction;Distance;Loading_vehicles;Unloading_vehicles;check_out;check_in\n')
        self.fichier_relation.write('ID;Stop_number;Service;Relation;Transfer_time;Certainty\n')
        self.fichier_odi.write('ID;FromStopNumber;ToStopNumber;ASD_or_SER;Reservation_in_equipment;Equipment;Tariff_in_equipment\n')
        self.inserer=False
        self.cpt_id=0
        
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
        
        self.liste_odi=[]
        self.new_odi_en_cours()
        self.liste_por=[]
        self.new_por_en_cours()
        self.relationship=[]
        
        self.cpt_por=0
        
    def process_message(self):            
        self.cpt_id+=1
        self.sql_train += '"'+str(self.cpt_id)+'";"'
        for X in ['PRD+','PRD+:','PRD+::','PRD+:::','PRD+::::::','PRD++','PRD++*','PRD++**','POP+:','POP+:/','POP+:::','RFR+:']:
            data=self.info_train[X]
            if X=='PRD+::::::' and data!='':
                data=data.replace('"','²"')
            self.sql_train+=data+'";"'
        self.sql_train=self.sql_train[:-2]+'\n'
       
        
        if self.liste_por!=[]:
            cpt=0
            
            for dico in self.liste_por:
                cpt+=1
                
                self.sql_por+='"'+str(self.cpt_id)+'";"'+str(cpt)+'";"'
                for X in ['POR+','POR++','POR++:::','POR++*','POR++*:::','POR+++','POR+++*','POR++++','TRF+','MES+','ASD+7','ASD+9','ASD+44','ASD+45']:
                    self.sql_por+=dico[X]+'";"'
                self.sql_por=self.sql_por[:-2]+'\n'
                
        if self.liste_odi!=[]:
            
            for dico in self.liste_odi:
                self.sql_odi+='"'+str(self.cpt_id)+'";"'
                for X in ['ODI++','ODI++*','value','PDT++','PDT++:::','PDT++::::::']:
                    self.sql_odi+=dico[X]+'";"'
                self.sql_odi=self.sql_odi[:-2]+'\n'
            
        
        if self.relationship!=[]:
            
            for liste in self.relationship:
                self.sql_relation+='"'+str(self.cpt_id)+'";"'
                for X in liste:
                    self.sql_relation+=X+'";"'
                
                txt=self.sql_relation[:-2]
                self.sql_relation=txt+'\n'
            
       
         
        
        
    def process_SKDUPD(self,fichier):
        self.sql_train= ''
        self.sql_odi = ''
        self.sql_por = ''
        self.sql_relation = ''
        data=open(fichier).read().split("'\n")
        for line in data:
            TAG=line[:3]
            """
            TODO
            """
            if TAG in ['UIB','UIH','MSD','ORG','HDR','UIT','UIZ']:
                continue
            elif TAG=='PRD':
                self.PRD(line)
            elif TAG=='POP':
                self.POP(line)
            elif TAG=='POR':
                self.POR(line)
            elif TAG=='ODI':
                self.ODI(line)
            elif TAG=='PDT':
                self.PDT(line)
            elif TAG=='SER':
                self.SER(line)
            elif TAG=='ASD':
                self.ASD(line)
            elif TAG=='TFF':
                self.TFF(line)
            elif TAG=='RFR':
                self.RFR(line)
            elif TAG=='RLS':
                self.RLS(line)
            elif TAG=='TRF':
                self.TRF(line)
            elif TAG=='TCE':
                self.TCE(line)
            elif TAG=='MES':
                self.MES(line)
            elif line!='':
                print("Cas non traité:",line)
        self.process_message()
        
        
        self.sql_train=self.sql_train[:-1]+'\n'
        self.fichier_train.write(self.sql_train)
    
        self.sql_por=self.sql_por[:-1]+'\n'
        self.fichier_por.write(self.sql_por)
    
    
        self.sql_odi=self.sql_odi[:-1]+'\n'
        self.fichier_odi.write(self.sql_odi)
    
        self.sql_relation=self.sql_relation[:-1]+'\n'
        self.fichier_relation.write(self.sql_relation) 
       
        
  
    
    def POR(self,data):
      
        self.cpt_por+=1
        self.dernier_arret=data[4:13]
        champs=self.process_line(data)
        for tag,valeur in champs:
            tag=tag.replace('POR++:::**:::','POR++*:::')                                            
            tag=tag.replace('POR++**:::','POR++*:::')
            tag=tag.replace('POR++:::*',('POR++*'))
            tag=tag.replace('POR++*++',('POR++++'))
            
            self.por_en_cours[tag]=valeur
        self.liste_por.append(self.por_en_cours)
        self.new_por_en_cours()
            
    def ODI(self,data):
        champs=self.process_line(data)
        for tag,valeur in champs:
            if tag in ['ODI++','ODI++*']:
                self.odi_en_cours[tag]=valeur
       
                
                 
     
    def PDT(self,data):
        champs=self.process_line(data)
        for tag,valeur in champs:
            self.odi_en_cours[tag]=valeur
        self.liste_odi.append(self.odi_en_cours)
        self.new_odi_en_cours()

        
        
    
    def POP(self,data):
        champs=self.process_line(data)
        for tag,valeur in champs:
            if tag=='POP+:':
                begin,end=valeur.split('/')
                self.info_train[tag]=begin
                self.info_train[tag+'/']=end
            else:
                self.info_train[tag]=valeur
            
    def RLS(self,data):
        liste=self.relationship[-1]
        liste[2]=data.split('+')[-1]
        self.relationship[-1]=liste
       
    
    def TRF(self,data):
        dico=self.liste_por[-1]
        dico['TRF+']=data.split('+')[-1]
        self.liste_por[-1]=dico
        
    def TCE(self,data):
        liste=self.relationship[-1]
        liste[3:5]=data.split('+')[1:]
        self.relationship[-1]=liste
      
    def MES(self,data):
        value=data[4:]
        dico=self.liste_por[-1]
        dico['MES+']=value
        self.liste_por[-1]=dico
        
            
        
       
        
            
    def RFR(self,data):
        if 'RFR+AVI' in data:
            self.info_train['RFR+:']=data.split(':')[-1]
        elif 'RFR+AUE' in data:
            relationship=['','','','','','']
            relationship[0:1]=[str(self.cpt_por),data.split(':')[-1]]
            self.relationship.append(relationship)
           
        else:
            raise Exception(data,"case not resolved")
                
    def SER(self,data):
        valeur=data[4:]
        self.odi_en_cours['value']='F'+valeur
        self.liste_odi.append(self.odi_en_cours)
        self.new_odi_en_cours()
        
    def TFF(self,data):
        valeur=data[4:]
       
        self.odi_en_cours['value']='T'+valeur
        self.liste_odi.append(self.odi_en_cours)
        self.new_odi_en_cours()
        
    def ASD(self,data):
        if data in ['ASD+7','ASD+9']:
            dic=self.liste_por[-1]
            dic[data]=data
            self.liste_por[-1]=dic
            return
        if data[:6] in ['ASD+44','ASD+45']:
            dic=self.liste_por[-1]
            dic[data[:6]]=data.split(':')[-1]
            self.liste_por[-1]=dic
            return
        valeur=data[4:]
        self.odi_en_cours['value']='S'+valeur
        self.liste_odi.append(self.odi_en_cours)
        self.new_odi_en_cours()
            
        
    def PRD(self,data):
        
        if self.inserer:
            self.process_message()
            
            self.sql_train=self.sql_train[:-1]+'\n'
            self.fichier_train.write(self.sql_train)
        
            self.sql_por=self.sql_por[:-1]+'\n'
            if self.sql_por!='\n':
                self.fichier_por.write(self.sql_por)
        
            self.sql_odi=self.sql_odi[:-1]+'\n'
            if self.sql_odi!='\n':
                self.fichier_odi.write(self.sql_odi)
        
            self.sql_relation=self.sql_relation[:-1]+'\n'
            if self.sql_relation!='\n':
                self.fichier_relation.write(self.sql_relation) 
            self.sql_train=''
            self.sql_odi = ''
            self.sql_por = ''
            self.sql_relation = ''
        else:
            self.inserer=True
        
        self.new_train()
        champs=self.process_line(data)
        for tag,valeur in champs:
            self.info_train[tag]=valeur
       
        
    def process_line(self,data):
        tag=data[:4]
        data=data[4:]
        liste_finale=[]
        data=[i.split(':') for i in data.split('+')]   
        for Xcpt,X in enumerate(data):
            cle=tag+'+'*Xcpt
            for Y in X:
                if '*' in Y:
                    dat=Y.split('*')
                    for Z in dat:
                        if Z!='':
                            liste_finale.append((cle,Z))
                        cle=cle+'*'
                elif Y!='':
                    liste_finale.append((cle,Y))
                cle=cle+':'
        return liste_finale
    
            
           
    def create_csv_file(self):
        for file in glob.glob(self.path['edifact']+'*.r'):
            if '\\' in file:
                file_name=file.split('\\')[-1]
            if "SKDUPD" in file_name.upper():
                print("Reading file : ",file)
                self.process_SKDUPD(file)
                self.fichier_odi.flush()
                self.fichier_por.flush()
                self.fichier_relation.flush()
                self.fichier_train.flush()
            
        self.fichier_odi.close()
        self.fichier_por.close()
        self.fichier_train.close()
        self.fichier_relation.close()
        return True

    
    
    
if __name__ == "__main__":   
    path={}
    path['odi']='./CSV/SKDUPD_ODI.csv'
    path['por']='./CSV/SKDUPD_POR.csv'
    path['train']='./CSV/SKDUPD_TRAIN.csv'
    path['relation']='./CSV/SKDUPD_RELATION.csv'
    path['edifact']='./SKDUPD/'
      
    tr=SKDUPD_to_csv(path)
    tr.create_csv_file() 
    print("Finished")
