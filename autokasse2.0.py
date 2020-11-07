# -*- coding: utf-8 -*-
"""
Created on Mon May  4 18:06:54 2020

@author: phili
"""


import csv
import pandas as pd


# Listen definieren

avk_konto = []
avk_name = []
avk_bestand = []

gbk_konto = []
gbk_name = []
gbk_bestand = []

hk_konto = []
hk_name = []
hk_bestand = []

all_konto = []
all_name = []

avk_bestand_fin = []
gbk_bestand_fin = []
hk_bestand_fin = []


# Funktion definieren, die die Daten aus der csv Datei einliest
def einlesen(kasse, filename, konto, name, bestand):
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if 300000 < int(row[20]) < 500000:
                konto.append(int(row[20]))
                name.append(row[21])
                bestand.append(row[25])
                line_count += 1
        print(f'Processed {line_count} lines in {kasse}.')

# Funktion definieren, die zu Kontonummer Name raussucht
def search_name(kasse, all_konto, kasse_konto, all_name):
    for i in range (0, len(all_konto)):
        if all_konto[i] in kasse_konto:
            for n in range (0, len(avk_konto)):
                if all_konto[i] == kasse_konto[n]:
                    all_name.append(avk_name[n])
        else: all_name.append(f'doesnt exist in {kasse}')

# Funktion definieren, die zu Kontonummer Bestand raussucht
def search_bestand(kasse, all_konto, kasse_konto, kasse_bestand, kasse_bestand_fin):
    for i in range (0, len(all_konto)):
        if all_konto[i] in kasse_konto:
            for n in range (0, len(kasse_konto)):
                if all_konto[i] == kasse_konto[n]:
                    kasse_bestand_fin.append(kasse_bestand[n])
        else: kasse_bestand_fin.append(f'doesnt exist in {kasse}')
        
        
        
        

###############################################################################
        
def main():
    # Dateipfad definieren
    path = 'C:\\Users\\phili\\OneDrive\\Desktop\\AutoKasse\\'
    
    # Daten einlesen
    einlesen('avk', path+'avk.csv', avk_konto, avk_name, avk_bestand)
    einlesen('gbk', path+'gbk.csv', gbk_konto, gbk_name, gbk_bestand)
    einlesen('hk', path+'hk.csv', hk_konto, hk_name, hk_bestand)
    
        
    # liste mit allen auftauchendne kontonummern erstellen
    all_konto = sorted(list(dict.fromkeys(avk_konto + gbk_konto + hk_konto)))
    
    
    # zu Kontonummer passenden Namen raussuchen (nur in avk, wenn Namen dort fehlen wird "doesnt exist in avk" eingefügt)
    search_name('avk', all_konto, avk_konto, all_name)
    
    
    # zu Kontonummer passenden Bestand raussuchen
    search_bestand('avk', all_konto, avk_konto, avk_bestand, avk_bestand_fin)
    search_bestand('gbk', all_konto, gbk_konto, gbk_bestand, gbk_bestand_fin)
    search_bestand('hk', all_konto, hk_konto, hk_bestand, hk_bestand_fin)
    
    
    # listen in Aktivitas und AHs trennen
    ah = 0
    for i in range (0, len(all_konto)):
        if all_konto[i] >= 400000:
            ah = i
            break
    
    
    # daten in pandas DataFrame schreiben
    df1 = pd.DataFrame({'Konto': all_konto[:ah], 'Name': all_name[:ah], 'GBK': gbk_bestand_fin[:ah], 'HK': hk_bestand_fin[:ah], 'AVK': avk_bestand_fin[:ah]})
    df2 = pd.DataFrame({'Konto': all_konto[ah:], 'Name': all_name[ah:], 'GBK': gbk_bestand_fin[ah:], 'HK': hk_bestand_fin[ah:], 'AVK': avk_bestand_fin[ah:]})
    
    
    # aus DataFrame excel tabelle machen
    with pd.ExcelWriter(path+'output.xlsx') as writer:  
        df1.to_excel(writer, sheet_name='Aktivitas')
        df2.to_excel(writer, sheet_name='AH')
    
    
    #df.to_excel('output.xlsx')
        
        
main()

#TODO

#summe vergleichen: alle Bestände drin?