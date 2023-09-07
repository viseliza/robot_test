from bs4 import BeautifulSoup
from datetime import datetime
import requests
import os
import wget
import textract


months = [
 'январь',
 'февраль',
 'март',
 'апрель',
 'май',
 'июнь',
 'июль',
 'август',
 'сентябрь',
 'октябрь',
 'ноябрь',
 'декабрь']


def groupReplacement():
    url = "https://portal.novsu.ru/univer/timetable/spo/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find('table', {'class':'viewtablewhite'})
    
    for i in table.find_all('div'):
        if (i.text == "ПТК"):
            return i.find('a').get('href')

def monthReplacement():
    url = groupReplacement()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find('table', {'class':'viewtablewhite'})
    
    for i in table.find_all('div'):
        month = i.text.split()[0].lower()
        year = i.text.split()[1].lower()

        if (month == months[datetime.now().month - 1] \
            and year == str(datetime.now().year)):
            return i.find('a').get('href')
        
def dayReplacement():
    page = requests.get(monthReplacement())
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find('table', {'class':'viewtablewhite'})
    
    for i in table.find_all('div'):
        day = i.text.split(".")[0]
        if day[0] == "0":
            day = day[1]
        if (day == str(datetime.now().day)):
            return i.find('a').get('href')


def nowDate():
    date = datetime.now()
    day = str(date.day)
    month = str(date.month)
    if (len(day) == 1): day = f"0{day}"
    if (len(month) == 1): month = f"0{month}"

    return f"{day}.{month}.{date.year}.doc"

# Скачивание замен с сайта
def downloadFile():
    if nowDate() in os.listdir("src"):
        pass
    else:
        wget.download(dayReplacement(), out="src")
    

# Все содержимое файла в текстовом формате

def parseDocument(group):
    downloadFile()
    text = textract.process(f"src/{nowDate()}")
    text = text.decode("utf-8") 

    text_arr = text.split("\n")
    result = ""
    
    for i in range(len(text_arr)):
        if (text_arr[i] == group):
            if "будет" in text_arr[i+3]:
                result += f"Группа {text_arr[i]}, пара: {text_arr[i+1]}\nДисциплина по расписанию: {text_arr[i+2]}\n{text_arr[i+3]}\n\n"
            else:
                result += f"Группа {text_arr[i]}, пара: {text_arr[i+1]}\nДисциплина по расписанию: {text_arr[i+2]}\nИзменено на {text_arr[i+3]}, в ауд. {text_arr[i+4]}\n\n"
    
    if result == "": result = f"Замен для группы {group} на сегодня нет"
    return result
