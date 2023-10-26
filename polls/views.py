import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.http import HttpResponse,JsonResponse
from django.views import View
import pyodbc



def connect():

    connection_string = (
                    "Driver={ODBC Driver 18 for SQL Server};Server=tcp:planwatdb.database.windows.net,1433;Database=plan;Uid=dbadmin;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

    conn = pyodbc.connect(connection_string)

sem_zim = ["01","09","10","11","12"]
sem_let = ["02","03","04","05","06","07","08"]

class group_name(View):
    
    def get(self,request, **kwargs):

        try:
            key = kwargs.get('key')
        except KeyError:
            return JsonResponse({"Podaj klucz"})
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        url = 'https://old.wcy.wat.edu.pl/pl/rozklad'
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find('select', {"class": "ctools-jump-menu-select form-select"}).find_all('option')
        group_names = []
        for option in options:
            group_names.append(option.text.strip())
        return JsonResponse(group_names, safe=False)
    
class prowadzacy(View):
    
    def get(self,request, **kwargs):
        
        try:
            key = kwargs.get('key')
        except KeyError:
            return JsonResponse({"Podaj klucz"})
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options)
        resoult = {}

        driver.get(f"https://old.wcy.wat.edu.pl/pl/planzajec")
        options = driver.find_element(By.TAG_NAME, "select").find_elements(By.TAG_NAME, "option")
        prow = {}
        for option in options:
            name = option.get_property("label")
            try:
                id = option.get_property("value").split("id=")[1]
            except IndexError:
                id = 'brak'
            prow[id]=name
        driver.quit()
        return JsonResponse(prow, safe=False)


class actuality_stud(View):
    def get(self, request, **kwargs):
        
        try:
            key = kwargs.get('key')
        except KeyError:
            return JsonResponse({"Podaj klucz"})
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        try:
            user_group = kwargs.get('group')
        except KeyError:
            return JsonResponse({"Podaj grupe idioto, group = nazwa_grupy"})
        
        if user_group != "":
            url = f'https://old.wcy.wat.edu.pl/pl/rozklad?grupa_id={user_group}'
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')

            date = soup.find('span', class_="head_info").text

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
            key = kwargs.get('key')
        except KeyError:
            return JsonResponse({"Podaj klucz"})
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        try:
            user_group = kwargs.get('group')
        except KeyError:
            return JsonResponse({"Podaj grupe idioto, group = nazwa_grupy"})

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options)
        driver.implicitly_wait(1)
        resoult = {}

        driver.get(f"https://old.wcy.wat.edu.pl/pl/rozklad?grupa_id={user_group}")
        lessons = driver.find_elements(By.CLASS_NAME, "lesson")
        current_date = driver.find_element(By.CLASS_NAME, "head_info").get_attribute("innerHTML").split("-")[1]
        
        if current_date in sem_zim:
            sem = sem_zim
        else:
            sem = sem_let

        for index in lessons:
            date = index.find_element(By.CLASS_NAME, "date").get_attribute("innerHTML")
            month = date.split("_")[1]

            if month in sem:
                full_info = index.find_element(By.CLASS_NAME, "info").get_attribute("innerHTML")
                display = index.find_element(By.CLASS_NAME, "name").get_attribute("innerHTML").split("<br>")
                block = index.find_element(By.CLASS_NAME,"block_id").get_attribute("innerHTML")[-1:]
            else:
                continue

            if date not in resoult:
                resoult[date] = {}

            resoult[date][block] = [display, full_info]
        driver.quit()

        return JsonResponse(resoult)
    
class plan_prow(View):
    def get(self,request,**kwargs):
        
        try:
            key = kwargs.get('key')
        except KeyError:
            return JsonResponse({"Podaj klucz"})
        if key!="karzel":
            return HttpResponse("bledny klucz")
        
        try:
            prow = kwargs.get('prow')
        except KeyError:
            return JsonResponse({"Podaj prowadzacego cepie, prow = nazwa_grupy zazwyczaj 2 pierwsze litery PS BZYKU CHUJ"})

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options)
        driver.implicitly_wait(1)
        resoult = {}

        driver.get(f"https://old.wcy.wat.edu.pl/pl/rozklad?grupa_id={prow}")
        lessons = driver.find_elements(By.CLASS_NAME, "lesson")
        current_date = driver.find_element(By.CLASS_NAME, "head_info").get_attribute("innerHTML").split("-")[1]
        
        if current_date in sem_zim:
            sem = sem_zim
        else:
            sem = sem_let

        for index in lessons:
            date = index.find_element(By.CLASS_NAME, "date").get_attribute("innerHTML")
            month = date.split("_")[1]

            if month in sem:
                full_info = index.find_element(By.CLASS_NAME, "info").get_attribute("innerHTML")
                display = index.find_element(By.CLASS_NAME, "name").get_attribute("innerHTML").split("<br>")
                block = index.find_element(By.CLASS_NAME,"block_id").get_attribute("innerHTML")[-1:]
            else:
                continue

            if date not in resoult:
                resoult[date] = {}

            resoult[date][block] = [display, full_info]
        driver.quit()

        return JsonResponse(resoult)
    
class help(View):
    def get(self,request):
        conn = connect()
        
        try:
            with conn.cursor as cursor:
                
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('john@example.com', 'mypassword'))
                conn.commit()
                print("Record inserted successfully")
        finally:
            conn.close
        help = """zawsze i wszedzie bzyku jebany bedzie
        <p> DO KAZDEGO ZAPYTANIA GET, POST ITP POTRZEBNY JEST KLUCZ DOSTEPU
        <br> taki klucz to bedzie karzel
        <br> przyklad: response = request.get(url, key="karzel")
        </p>
                <p>
                
                </p>
                    <div><b> spis wszystkich URL i szybkie objasnienie:</b></p>
                       <dfn>https://planwat.azurewebsites.net/polls/ </dfn> <p> -- to jest strona domyslna dalej bede pisal tylko rozszerzenia</p>  
                        <p><br><dfn>/prowadzacy </dfn>                              -- spis wszystkich prowadzacych w formacie: 
                            <p> {"Ad.P.": "Adamczyk Piotr"}, gdzie kluczem jest id prowadzacego a wartoscia imie i nazwisko </p><br>

                            Zeby byly polskie znaki musicie przy kazdym odbiorze JSON dopisac:
                            <p> with open(wasz_request, encoding="UTF-8):
                            </p> Nie, nie moglem tego zrobic tutaj </p><br>

                        <p><dfn>/actuality/stud                          </dfn> -- wypluwa ostatnia aktualizacje planu danej grupy 
                            <p> "Data aktualizacji:2023-10-25 00:25:35" </p </p><br>

                        <p><dfn>/days                                    </dfn> -- zwraca dni kalendarzowe jakby sie wam nie chcialo kalendarza wrzucac
                            <p> {"1": [["25", "IX"], ["02", "X"],...], "2": [...]} zwraca slownik gdzie id to 1,2,3... dni tygodnia od poniedzialku a wartosci to [dzien,miesiac]
                            </p></p><br>

                        <p><dfn>/plan/stud                              </dfn>  -- zwraca plan grupy zajec, przy GET wymaga podania grupy w formie group=nazwa_grupy i KLUCZA key=karzel
                            <p> zwraca slownik gdzie kluczem jest data, ktory zawiera slownik gdzie kluczem jest blok, ktory zawiera przedmiot. Dane o przedmiocie to lista gdzie 0 index to display a 1 to pelne info </p>
                            <p> {"dd-mm-rrrr": {"1": [display,full_info ], "2":...}, ...} max jest do 7 bloku </p/ </p><br>
                        
                        <p><dfn>/grp                                     </dfn> -- zwraca wszystkie grupy szkoleniowe, prosta lista 
                            <p> ["CHUJ", "chuj", "ChUj", "Bzyku", "To", "Kurwa"] </p> </p><br>
                        
                        <p><dfn>/plan/prow                               </dfn> -- dziala i zwraca to samo co plan dla studentow </p>
                        <p>tyle ze trzeba dac id prowadzacego przy GET, prow=id_prow
                        </div>
                        <br>jeszcze nie ma zapisywania do BD wiec wszystko robcie na requestach
                        <br>zrobie tak zeby zawsze JSON byly takie same to bez pierdolenia ze sie zmieni
                        <br>jak skonczycie front to podeslijcie i wstawie gotutaj
                        <br>formas czytaj juz o testach jednostkowych, dam ci dostep do serwera jak nauczysz sie cos robic
                        <br>zebys przypadkiem czegos nie rozjebala                        
                
                """
        return HttpResponse(help)