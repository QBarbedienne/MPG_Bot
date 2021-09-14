import pandas as pd 
import numpy as np
import scipy
import requests
from requests.auth import HTTPBasicAuth
import time
import json
import os

script_path = os.path.dirname(os.path.realpath(__file__))

with open(script_path + '\datas.txt') as f:
    lines = f.read().splitlines() 
print(lines)

if len(lines) == 4:
    ligue_data = lines[1].split('ligue_name : ')[1]
    player_token = lines[2].split('token : ')[1]

print(ligue_data)
print(player_token)

league='1'
# String_url = "https://api.monpetitgazon.com/championship/" + league + "/calendar/16"
String_url="https://api.monpetitgazon.com/league/"+ ligue_data +"/mercato"
# # print(String_url)
i=0

token = player_token
# # mpg_user='mpg_user_261105'
# while i<500:

# r = requests.get(String_url, auth=(mpg_user,token))
# print(r.status_code)
nbritter=0
# start=time.time()
MPG_CLIENT_VERSION="5.2.0"
response = requests.get(String_url, headers={'Authorization': token,"client-version": MPG_CLIENT_VERSION})
print(response.url)
print(response.json())
# payload = {'Delort'}
# response = requests.get(String_url, headers={'Authorization': token,"client-version": MPG_CLIENT_VERSION}, params=payload)
# r = requests.get('https://httpbin.org/get')
dfprev = pd.read_excel(script_path + '\players.xlsx')
print(dfprev)
try:
    budget = int(response.json()['budget'])
except:
    budget = 500
# elevations = response.read()

try:
    data = response.json()
    df3 = pd.json_normalize(data['availablePlayers'])
    print(df3.head())
    print(len(df3))
    Name = df3['lastname'].tolist()
    ide =  df3['id'].tolist()
    Price = df3['quotation'].tolist()
    # print(Name)
except:
    Name = dfprev['Nom'].tolist()
    Name  = [str(x).split('\xa0')[0] for x in Name]
    print('Nothing Online')


df = pd.read_excel(r'C:\Users\quent\Desktop\MPG\players.xlsx')
df = df.dropna()
Attaquant = 5
Mil = 7
Def = 7
Gardien = 2
# budget=500

Gardien2 = 1
Mil2 = 2
Def2 = 2
Attaquant2 = 2

SelectAtt = []
SelectMil = []
SelectDef = []
SelectGard = []
NoteMeanATT = 0
NoteMeanDef = 0
NoteMeanMil = 0
NoteMeanGard = 0

PresMeanATT = 0
PresMeanDef = 0
PresMeanMil = 0
PresMeanGard = 0

SelectAtt2=[]
SelectMil2=[]
SelectDef2=[]
SelectGard2=[]
# print(df)
print(df['Pres'])
df2=df[(df['Pres'] >= 0.3) & (df['Pres'] <= 0.5) ]
df=df[(df['Pres'] > 0.5)]
# print(df)
df=df.sort_values(by=['Note', 'Montant'], ascending=False)
df2=df2.sort_values(by=['Note', 'Montant'], ascending=False)
# with pd.option_context('display.max_rows', len(df[0]), 'display.max_columns', len(df)):  # more options can be specified also

# pd.set_option('display.max_rows', df.shape[0]+1)
# pd.set_option('display.max_columns', df.shape[1]+1)
# print(df)
EnPlus=[40,20,3,3]
listdf=df.values.tolist()
listdf2=df2.values.tolist()
JoueurPris=[]
for i in range(len(listdf)):
    joueur,poste,ville,note,but,montant,pres=listdf[i]
    # print(joueur)
    # print(str(joueur).split('\xa0')[0])
    try:
        try:
            Index=Name.index(str(joueur).split('\xa0')[0])
            montant=Price[Index]
        except:
            Index=0
            pass
        # print(Name)
        # print(str(joueur).split('\xa0')[0])
        # print()
        if str(joueur).split('\xa0')[0] in Name:
            if 'Attaquant' in poste and budget-montant>0 and Attaquant!=0:
                if len(SelectAtt)<2:
                    try:
                        SelectAtt.append([ide[Index],joueur,montant+EnPlus[0]])
                    except:
                        SelectAtt.append([0,joueur,montant+EnPlus[0]])
                    JoueurPris.append(joueur)
                else:
                    try:
                        SelectAtt.append([ide[Index],joueur,montant])
                    except:
                        SelectAtt.append([0,joueur,montant])
                    JoueurPris.append(joueur)
                NoteMeanATT+=note
                PresMeanATT+=pres
                Attaquant-=1
                if len(SelectAtt)<3:
                    budget-=montant+EnPlus[0]
                    del EnPlus[0]
                else:
                    budget-=montant+1
            elif 'Mil. ' in poste and budget-montant>0 and Mil!=0:
                try:
                    SelectMil.append([ide[Index],joueur,montant])
                except:
                    SelectMil.append([0,joueur,montant])
                JoueurPris.append(joueur)
                Mil-=1
                NoteMeanMil+=note
                PresMeanMil+=pres
                budget-=montant+1
            elif 'Def. ' in poste and budget-montant>0 and Def!=0:
                try:
                    SelectDef.append([ide[Index],joueur,montant])
                except:
                    SelectDef.append([0,joueur,montant])
                JoueurPris.append(joueur)
                NoteMeanDef+=note
                PresMeanDef+=pres
                Def-=1
                budget-=montant+1
            elif 'Gardien' in poste and budget-montant>0 and Gardien!=0:
                try:
                    SelectGard.append([ide[Index],joueur,montant])
                except:
                    SelectGard.append([0,joueur,montant])
                JoueurPris.append(joueur)
                Gardien-=1
                budget-=montant+1
                NoteMeanGard+=note
                PresMeanGard+=pres
        else:
            pass
    except:
        print('ouche')
        pass
# print(SelectAtt)
# print(SelectMil)
# print(SelectDef)
# print(SelectGard)
for i in range(len(listdf2)):
    joueur,poste,ville,note,but,montant,pres=listdf2[i]
    # print(joueur)
    # print(str(joueur).split('\xa0')[0])
    try:
        Index=Name.index(str(joueur).split('\xa0')[0])
        montant=Price[Index]
        if joueur in JoueurPris:
            pass
        else:
            if str(joueur).split('\xa0')[0] in Name:
                if 'Gardien' in poste and budget-montant>0 and Gardien2!=0:
                    SelectGard.append([ide[Index],joueur,montant])
                    Gardien2-=1
                    budget-=montant
                    NoteMeanGard+=note
                    PresMeanGard+=pres
                elif 'Attaquant' in poste and budget-montant>0 and Attaquant2!=0:
                    SelectAtt.append([ide[Index],joueur,montant])
                    Attaquant2-=1
                    NoteMeanATT+=note
                    PresMeanATT+=pres
                    # if len(SelectAtt)<3:
                    #     budget-=montant+EnPlus[0]
                    #     del EnPlus[0]
                    # else:
                    budget-=montant
                elif 'Mil. ' in poste and budget-montant>0 and Mil2!=0:
                    SelectMil.append([ide[Index],joueur,montant])
                    Mil2-=1
                    NoteMeanMil+=note
                    PresMeanMil+=pres
                    budget-=montant
                elif 'Def. ' in poste and budget-montant>0 and Def2!=0:
                    SelectDef.append([ide[Index],joueur,montant])
                    Def2-=1
                    NoteMeanDef+=note
                    PresMeanDef+=pres
                    budget-=montant
            else:
                pass
    except:
        # print('nooo')
        pass
print(SelectAtt)
print(SelectMil)
print(SelectDef)
print(SelectGard)
try:
    print('Notes Moy (Att/Mil/Def/Gard):')
    print(NoteMeanATT/len(SelectAtt))
    print(NoteMeanDef/len(SelectDef))
    print(NoteMeanMil/len(SelectMil))
    print(NoteMeanGard/len(SelectGard))
    print('présence Moy (Att/Mil/Def/Gard):')
    print(PresMeanATT/len(SelectAtt))
    print(PresMeanDef/len(SelectDef))
    print(PresMeanMil/len(SelectMil))
    print(PresMeanGard/len(SelectGard))
except:
    pass
SelectTeam=SelectAtt+SelectMil+SelectDef+SelectGard
print('Budget Mercato Restant : %i'%budget)
print(SelectTeam)
print(len(SelectTeam))
jsonString = json.dumps(SelectTeam)
data={}
toast=[]*len(SelectTeam)
for i in range(len(SelectTeam)):
    doto={}
    ider,osef,price=SelectTeam[i]
    print(ider)
    doto["id"]=str(ider)
    doto["price"]=int(price)
    toast.append(doto)
    # print(toast[i])
# print(toast)
data['players']=toast
json_data = json.dumps(data)
print(json_data)
# payload = {'key1': 'value1', 'key2': 'value2'}

response = requests.post(String_url, headers={'Authorization': token,"client-version": MPG_CLIENT_VERSION}, json=json_data)
print(response)
print(response.url)
print(response.json())