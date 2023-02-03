import requests
from bs4 import BeautifulSoup
import csv
limite = 2
i = 0

def GET (Link):
    page = requests.get(f"http://www.annonce-algerie.com/{Link}")
    src = page.content 
    soup = BeautifulSoup(src, "lxml")
    trss = soup.find_all("tr",{'class':'da_entete'})
    trs = trss[0]    
    name1= trs.contents[0]

    Photos = {
        'photo01' : soup.find_all("img",{'id':'PhotoMax_0'}),
        'photo02' : soup.find_all("img",{'id':'PhotoMin_0'}),
        'photo03' : soup.find_all("img",{'id':'PhotoMin_1'}),
        'photo04' : soup.find_all("img",{'id':'PhotoMin_2'}),
        'photo05' : soup.find_all("img",{'id':'PhotoMin_3'})
    }
    try:
        Data = {
            'name': name1.text,
             trs.parent.contents[5].find('td').text : trs.parent.contents[5].find('td', {'class':'da_field_text'}).text, # categorie
             trs.parent.contents[9].find('td').text: trs.parent.contents[9].find('td', {'class':'da_field_text'}).text,  # localisation
             'Adresse' : soup.find("span",{'class':'da_contact_adr_soc'}).text,                                          # adresse
             trs.parent.contents[17].find('td').text: trs.parent.contents[17].find('td', {'class':'da_field_text'}).text,  # surface
             trs.parent.contents[21].find('td').text: trs.parent.contents[21].find('td', {'class':'da_field_text'}).text,  # prix
             trs.parent.contents[25].find('td').text: trs.parent.contents[25].find('td', {'class':'da_field_text'}).text,  # description                          
             'creature' : soup.find("span",{'class':'da_contact_rais_soc'}).text,
             'telephone' : soup.find("span",{'class':'da_contact_value'}).text,
             'date' : soup.find_all("td",{'class':'da_field_text'})[6].text,
             'photos': Photos }
       
    except: 
        try:
            Data = {
                'name': name1.text,
                 trs.parent.contents[5].find('td').text : trs.parent.contents[5].find('td', {'class':'da_field_text'}).text,
                 trs.parent.contents[9].find('td').text: trs.parent.contents[9].find('td', {'class':'da_field_text'}).text,
                 trs.parent.contents[13].find('td').text: trs.parent.contents[13].find('td', {'class':'da_field_text'}).text,
                 trs.parent.contents[17].find('td').text: trs.parent.contents[17].find('td', {'class':'da_field_text'}).text,
                 trs.parent.contents[21].find('td').text: trs.parent.contents[21].find('td', {'class':'da_field_text'}).text,
                 trs.parent.contents[25].find('td').text : trs.parent.contents[25].find('td', {'class':'da_field_text'}).text, # description 
                 'creature' : soup.find("span",{'class':'da_contact_rais_soc'}).text,
                 'telephone' : soup.find("span",{'class':'da_contact_value'}).text,
                 'date' : soup.find_all("td",{'class':'da_field_text'})[6].text,
                 'photos': Photos }

        except:
            try:
                Data = {
                       'name': name1.text,
                       trs.parent.contents[5].find('td').text : trs.parent.contents[5].find('td', {'class':'da_field_text'}).text,
                        trs.parent.contents[9].find('td').text: trs.parent.contents[9].find('td', {'class':'da_field_text'}).text,
                        'Adresse' : trs.parent.contents[9].find('td', {'class':'da_field_text'}).text, 
                        trs.parent.contents[13].find('td').text: trs.parent.contents[13].find('td', {'class':'da_field_text'}).text,
                        trs.parent.contents[17].find('td').text: trs.parent.contents[17].find('td', {'class':'da_field_text'}).text,
                        trs.parent.contents[21].find('td').text: trs.parent.contents[21].find('td', {'class':'da_field_text'}).text,
                        'creature' : soup.find("span",{'class':'da_contact_rais_soc'}).text,
                        'telephone' : soup.find("span",{'class':'da_contact_value'}).text,
                        'date' : soup.find_all("td",{'class':'da_field_text'})[6].text,
                        'photos': Photos
                        }
            except:
                    Data = {
                       'name': name1.text,
                       trs.parent.contents[5].find('td').text : trs.parent.contents[5].find('td', {'class':'da_field_text'}).text,
                        trs.parent.contents[9].find('td').text: trs.parent.contents[9].find('td', {'class':'da_field_text'}).text,
                        'Adresse' : trs.parent.contents[9].find('td', {'class':'da_field_text'}).text, 
                        trs.parent.contents[13].find('td').text: trs.parent.contents[13].find('td', {'class':'da_field_text'}).text,
                        trs.parent.contents[17].find('td').text: trs.parent.contents[17].find('td', {'class':'da_field_text'}).text,
                        trs.parent.contents[21].find('td').text: trs.parent.contents[21].find('td', {'class':'da_field_text'}).text,
                        'creature' : " ",
                        'telephone' : soup.find("span",{'class':'da_contact_value'}).text,
                        'date' : soup.find_all("td",{'class':'da_field_text'})[6].text,
                        'photos': Photos
                        }
    return Data

page = requests.get(f"http://www.annonce-algerie.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=DZ&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num=1")
src = page.content 
soup = BeautifulSoup(src, "lxml")
num = soup.find_all("table",{'class':'RecordsNumber'})
numAnnonce = num[0].find('b').text.strip()
numero = ''.join(filter(str.isdigit, numAnnonce))

def numPage(numero,limite):
    if ((int(numero) % limite) != 0):
      j = int(numero) / limite + 1
    else:
      j = int(numero) / limite
    a = int(numero)%limite 
    return int(j) , a 

j = 1
list = []

while j < numPage(numero,limite)[0]:
    k = 0
    index = 0
    while k < limite :
        try:
           page = requests.get(f"http://www.annonce-algerie.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=DZ&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num={1}")
           src = page.content 
           soup = BeautifulSoup(src, "lxml")
           nameTag = soup.find_all("tr",{'class':'Tableau1'})
           a = nameTag[index].contents[7].find('a').get("href")
           index = index + 1
           list.append(GET(a))
        #    print(GET(a))
           k = k + 1
        except:
           print(f'Erooor in scrapping annonce num {j}')
    j = j+1
    k = 0
    w = 0
    index = 0
    if j == numPage(numero,limite)[0]-1 :
        while k < numPage(numero,limite)[1]:
             try:
              page = requests.get(f"http://www.annonce-algerie.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=DZ&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num={1}")
              src = page.content 
              soup = BeautifulSoup(src, "lxml")
              nameTag = soup.find_all("tr",{'class':'Tableau1'})
              a = nameTag[index].contents[7].find('a').get("href")
              index = index + 1
              list.append(GET(a))
              k = k + 1
             except:
              print(f'Erooor in scrapping annonce num {j}')
Header=['Annonces']
with open ('Data.csv' ,'w') as csvfile:
     write= csv.writer(csvfile)
     write.writerow(Header)
     write.writerow(list)
     print('le fichier de scrapping est bien créé ')
