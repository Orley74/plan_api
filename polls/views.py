from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.http import HttpResponse,JsonResponse
from django.views import View
import neo4j
from selenium import webdriver
from neo4j import GraphDatabase, RoutingControl, exceptions
from urllib.parse import unquote
 
uri = 'neo4j+s://b35e138c.databases.neo4j.io'
auth = ("neo4j", 'VGfvQTk0VCkEzne79CGPXTKA_Eykhx0OwudLZUKG7sQ')


sem_zim = ["01","09","10","11","12"]
sem_let = ["02","03","04","05","06","07","08"]



def add_group(driver, ID):
    try:
        driver.execute_query(
        "Create (g:Group {ID: $name}) ",
        name=ID,database_="neo4j",
    )
    except neo4j.exceptions.ConstraintError:
        print(f"grupa {ID} jest juz w bazie danych")


def print_group(driver):
    records, _, _= driver.execute_query(
        "MATCH (g:Group)"
        "RETURN g.ID",
         database_="neo4j", routing_=RoutingControl.READ,
    )
    resoult = []
    for record in records:
        resoult.append(record['g.ID'])
    
    print(f"Znaleziono {len(resoult)} grup")
    return resoult

def add_prac(driver, ID, name):
 
    try:
        driver.execute_query(
        "Create (p:Pracownik {ID: $ID, name: $name}) ",
        ID=ID,name=name,database_="neo4j",
    )
    except neo4j.exceptions.ConstraintError:
        print(f"Pracownik {name} jest juz w bazie danych")

def print_prac(driver):
    records, _, _ = driver.execute_query(
        "MATCH (p:Pracownik)"
        "RETURN p",
         database_="neo4j", routing_=RoutingControl.READ,
    )
    resoult = {}
    for record in records:
        data = record.data()
        resoult[data['p']['ID']] = data['p']['name']
    
    print(f"Znaleziono {len(resoult)} grup")

    return resoult

def add_date(driver,all,group):
    
    for date in all.keys():

        for blok in all[date].keys():
            display = all[date][blok][0]
            full = all[date][blok][1]
            id_prow = display[3].split("[")[0]
            place = display[2]
            form = display[1]
            short = display[0]
            # print(id_prow, place, form, short, full)
            
            try:
                driver.execute_query(
                """Merge (b:Blok {id_prow: $id_prow, place: $place, date: $date, nr: $blok}) 
            
                On Create
                    SET 
                    b.id_prow = $id_prow,
                    b.place = $place,
                    b.date = $date,
                    b.nr = $blok,
                    b.groups = [$group],
                    b.form = $form,
                    b.short = $short,
                    b.full = $full

                On match
                    SET b.grups = CASE 
                        WHEN NOT $group IN b.groups THEN b.groups + $group
                        ELSE b.groups
               END
                """,
                date=date,group=group,blok=blok,id_prow=id_prow,place=place,form=form,short=short,full=full,database_="neo4j",
                )    
        
            except neo4j.exceptions.ConstraintError:
                print(f"Zajecia dnia: {date} sa juz dodane do bloku {blok}")

            try:
                driver.execute_query(
                """match (b:Blok), (p:Pracownik)
                Where p.ID = b.id_prow
                and b.nr = $blok
                and b.date = $date
                MERGE (p)-[pz:prowadz_zajecia]->(b)
                """,
                date=date,group=group,blok=blok,database_="neo4j",
            )
                
                driver.execute_query(
                """match (g:Group), (b:Blok)
                Where  g.ID in b.groups
                and b.date = $date
                and b.nr = $blok
                MERGE (g)-[bz:blok_zajec]->(b)""",
                date=date,group=group,blok=blok,database_="neo4j",
            )
            except neo4j.exceptions.ConstraintError:
                print(f"Powiazania sa juz wykonane")
            except e as Exception:
                print(e)

            print(f"Zakonczono dodawanie dnia: {date} do bloku {blok}")



    return ("Zakonczono dodawanie")

def print_plan(driver,group):
    print(f"wyswietlam plan dla {group}")
    records, _, _ = driver.execute_query(
        f"""MATCH (b:Block) where "{group}" in b.groups 
        RETURN b""",
         database_="neo4j", routing_=RoutingControl.READ)
    resoult = []
    for record in records:
        data = record.data()
        resoult.append(data['b'])

    print(f"Znaleziono {len(resoult)} wynikow")

    return resoult

def print_plan_prac(driver,id_prow):
    id_prow = unquote(id_prow, encoding='utf-8')
    print(f"wyswietlam plan dla {id_prow}")
    records, _, _ = driver.execute_query(
        f"""MATCH (p:Pracownik)-[:prowadzi_zajecia]->(b:Block) where p.ID="{id_prow}" return b""",
         database_="neo4j", routing_=RoutingControl.READ,
    )
    resoult = []
    for record in records:
        data = record.data()
        resoult.append(data['b'])
    print(f"Znaleziono {len(resoult)} wynikow")
    return resoult

class group_name(View):
    
    def get(self,request, **kwargs):
        
        # try:
        #     key = request.META['HTTP_KEY']
        # except KeyError:
        #     return JsonResponse({"Podaj klucz"}, safe=False)
        # if key!="karzel":
        #     return JsonResponse({"Zly klucz"}, safe=False)
        
        with GraphDatabase.driver(uri,auth=auth) as driver:
            records = print_group(driver)

        return JsonResponse(records, safe=False)
    
    def options(self,request, **kwargs):
        
        
        with GraphDatabase.driver(uri,auth=auth) as driver:
            records = print_group(driver)

        return JsonResponse(records, safe=False)
    
    def post(self,request,**kwargs):
        
        try:
            key = request.META['HTTP_KEY']
        except KeyError:
            return JsonResponse({"Podaj klucz"}, safe=False)
        if key!="karzel":
            return JsonResponse({"Zly klucz"}, safe=False)
    
        url = 'https://old.wcy.wat.edu.pl/pl/rozklad'
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find('select', {"class": "ctools-jump-menu-select form-select"}).find_all('option')
        with GraphDatabase.driver(uri, auth=auth) as driver:
            for option in options:
                try:
                    add_group(driver, option.text.strip())
                except Exception as e:
                    print(e)
                finally:
                    driver.close()
        print("pomyslnie zaaktualizowano nazwy grup")
        return HttpResponse(["pomyslnie zaaktualizowano nazwy grup"])
    
class prowadzacy(View):
    
    def get(self,request, **kwargs):
        
    #     try:
    #         key = request.META['HTTP_KEY']
    #     except KeyError:
    #         return JsonResponse({"Podaj klucz"})
    #     if key!="karzel":
    #         return HttpResponse("bledny klucz")
        
        
        with GraphDatabase.driver(uri,auth=auth) as driver:
            records = print_prac(driver)
        
        return JsonResponse(records, safe=False)

    def options(self,request, **kwargs):
        
        
        with GraphDatabase.driver(uri,auth=auth) as driver:
            records = print_prac(driver)
            
        return JsonResponse(records, safe=False)
    def post(self,request,**kwargs):

        try:
            key = request.META['HTTP_KEY']
        except KeyError:
            return JsonResponse({"Podaj klucz"})
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options)

        driver.get(f"https://old.wcy.wat.edu.pl/pl/planzajec")
        options = driver.find_element(By.TAG_NAME, "select").find_elements(By.TAG_NAME, "option")

        with GraphDatabase.driver(uri, auth=auth) as driver:
            for option in options:
                try:
                    name = option.get_property("label")
                    try:
                        id = option.get_property("value").split("id=")[1]
                    except IndexError:
                        id = 'brak'
                    add_prac(driver,id,name)
                
                except Exception as e:
                    print(e)
                finally:
                    driver.close()

        print("pomyslnie zaaktualizowano prowadzacych")
        return HttpResponse(["pomyslnie zaaktualizowano prowadzacych"])

class actuality_stud(View):
    def get(self, request, **kwargs):
        
        try:
            key = request.META['HTTP_KEY']
        except KeyError:
            return JsonResponse({"Podaj klucz"})
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        try:
            user_group = request.META['HTTP_GRP']
        except KeyError:
            return JsonResponse({"Podaj grupe, group = nazwa_grupy"})
        
        if user_group != "":
            url = f'http://old.wcy.wat.edu.pl/pl/rozklad?grupa_id={user_group}'
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')

            date = soup.find('span', class_="head_info")

            

            return JsonResponse(date, safe=False)
        else:
            return HttpResponse("Wpisz nazwe grupy")

class days(View):
    def get(self, request, **kwargs):
        
        try:
            key = kwargs.get('key')
        except KeyError:
            return JsonResponse({"Podaj klucz"})
        if key!="karzel":
            return HttpResponse("bledny klucz")
        url = f'https://old.wcy.wat.edu.pl/pl/rozklad?grupa_id=WCY20IK1S0'
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        plan = soup.find('div', class_="rozklad_container")
        week = {}
        day_name = 1
        for days in plan.find_all('div', class_="day_v1"):
            dates = []
            for day in days.find_all('div', class_="date"):
                dates.append([day.find('span', class_="date1").text, day.find('span', class_="date2").text])
            week[day_name] = dates
            day_name += 1
        return JsonResponse(week)

class plan_stud(View):
    def get(self,request,**kwargs):  
        
        try:
            key = request.META['HTTP_KEY']
        except KeyError:
            return JsonResponse({"Podaj klucz"}, safe=False)
        if key!="karzel":
            return JsonResponse({"Zly klucz"}, safe=False)
        
        try:
            user_group = request.META['HTTP_GRP']
        except KeyError:
            return JsonResponse({"Podaj grupe, group = nazwa_grupy"})
        

        with GraphDatabase.driver(uri,auth=auth) as driver:
            records = print_plan(driver,user_group)
        return JsonResponse(records, safe=False)
    

    def post(self,request,**kwargs):  
        
        try:
            key = request.META['HTTP_KEY']
        except KeyError:
            return HttpResponse("Podaj klucz")
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        try:
            user_group = request.META['HTTP_GRP']
        except KeyError:
            return HttpResponse("Podaj grupe, group = nazwa_grupy")

        
        confirm = request.META['HTTP_CONFIRM']
        if confirm != "tak":
            return HttpResponse["uzyj get, post jest do zapisu do BD i wymaga confirm='tak'"]

        
        return JsonResponse({"x":"d"},safe = False)
    
class plan_prow(View):
    def get(self,request,**kwargs):
        
        try:
            key = request.META['HTTP_KEY']
        except KeyError:
            return HttpResponse("Podaj klucz")
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        try:
            prow = request.META['HTTP_PROW']
        except KeyError:
            return JsonResponse({"Podaj prowadzacego, prow = nazwa_grupy zazwyczaj 2 pierwsze litery"})

        with GraphDatabase.driver(uri,auth=auth) as driver:
            records = print_plan_prac(driver,prow)

        return JsonResponse(records, safe=False)
    
class help(View):
    def get(self,request):
       
        
        help = """
        <p> DO KAZDEGO ZAPYTANIA GET, POST ITP POTRZEBNY JEST KLUCZ DOSTEPU
        <br> taki klucz to bedzie karzel
        <br> przyklad: groups_key = {'key': 'karzel'}
        <br> groups = requests.get('https://planwat.azurewebsites.net/polls/grp', headers=groups_key)
        </p>
                <p>
                
                </p>
                    <div><b> spis wszystkich URL i szybkie objasnienie:</b></p>
                       <dfn>https://planwat.azurewebsites.net/polls/ </dfn> <p> -- to jest strona domyslna dalej bede pisal tylko rozszerzenia</p>  
                        <p><br><dfn>/prowadzacy </dfn>                              -- spis wszystkich prowadzacych w formacie: 
                            <p> {"Ad.P.": "Adamczyk Piotr"}, gdzie kluczem jest id prowadzacego a wartoscia imie i nazwisko </p><br>

                            Zeby byly polskie znaki musicie przy kazdym odbiorze JSON dopisac:
                            <p> with open(wasz_request, encoding="UTF-8):
                            </p> </p><br>

                        <p><dfn>/actuality/stud                          </dfn> -- wypluwa ostatnia aktualizacje planu danej grupy 
                            <p> "Data aktualizacji:2023-10-25 00:25:35" </p </p><br>

                        <p><dfn>/days                                    </dfn> -- zwraca dni kalendarzowe
                            <p> {"1": [["25", "IX"], ["02", "X"],...], "2": [...]} zwraca slownik gdzie id to 1,2,3... dni tygodnia od poniedzialku a wartosci to [dzien,miesiac]
                            </p></p><br>

                        <p><dfn>/plan/stud                              </dfn>  -- zwraca plan grupy zajec, przy GET wymaga podania grupy w formie group=nazwa_grupy i KLUCZA key=karzel
                            <p> zwraca slownik gdzie kluczem jest data, ktory zawiera slownik gdzie kluczem jest blok, ktory zawiera przedmiot. Dane o przedmiocie to lista gdzie 0 index to display a 1 to pelne info </p>
                            <p> {"dd-mm-rrrr": {"1": [display,full_info ], "2":...}, ...} max jest do 7 bloku </p/ </p><br>
                        
                        <p><dfn>/grp                                     </dfn> -- zwraca wszystkie grupy szkoleniowe, prosta lista 
                            <p> ["a","b","c"] </p> </p><br>
                        
                        <p><dfn>/plan/prow                               </dfn> -- dziala i zwraca to samo co plan dla studentow </p>
                        <p>tyle ze trzeba dac id prowadzacego przy GET, prow=id_prow
                        </div>
                        <br>jeszcze nie ma zapisywania do BD wiec wszystko robcie na requestach
                                   
                
                """
        return HttpResponse(help)
    
class plan_stud_karwo(View):
    def get(self,request,**kwargs):  
        
        user_group = request.GET.get('grupa')
        with GraphDatabase.driver(uri,auth=auth) as driver:
            records = print_plan(driver,user_group)
        return JsonResponse(records, safe=False)
    
class plan_prow_karwo(View):
    def get(self,request,**kwargs):  
        
        prow = request.GET.get('prow')
        with GraphDatabase.driver(uri,auth=auth) as driver:
            records = print_plan_prac(driver,prow)
        return JsonResponse(records, safe=False)
