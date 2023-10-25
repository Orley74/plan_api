# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from django.http import HttpResponse,JsonResponse

sem_zim = ["01","09","10","11","12"]
sem_let = ["02","03","04","05","06","07","08"]
def get_group_name(request):
    url = 'https://old.wcy.wat.edu.pl/pl/rozklad'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    options = soup.find('select', {"class": "ctools-jump-menu-select form-select"}).find_all('option')

    group_names = []

    for option in options:
        group_names.append(option.text.strip())
    return JsonResponse(group_names, safe=False)

def check_actuality_plan(request):
    user_group = request.GET.get('group', "")
    if user_group != "":
        url = f'https://old.wcy.wat.edu.pl/pl/rozklad?grupa_id={user_group}'
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        date = soup.find('span', class_="head_info").text

        return JsonResponse(date, safe=False)
    else:
        return HttpResponse("Wpisz nazwe grupy")

def get_days(request):
    user_group = request.GET.get('group', "")
    url = f'https://old.wcy.wat.edu.pl/pl/rozklad?grupa_id={user_group}'
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

def get_plan(request):

    user_group = request.GET.get('group', "")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options)
    driver.implicitly_wait(1)
    resoult = {}

    driver.get(f"https://old.wcy.wat.edu.pl/pl/rozklad?grupa_id={user_group}")
    lessons = driver.find_elements(By.CLASS_NAME, "lesson")
    current_date = driver.find_element(By.CLASS_NAME, "head_info").get_attribute("innerHTML").split("-")[1]
    driver.quit()
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


    
    return JsonResponse(resoult)