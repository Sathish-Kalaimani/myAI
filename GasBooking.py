import requests, json
import PIL 
from PIL import Image
from pytesseract import image_to_string
import datetime
import re

def bookGas():
    url = "https://my.ebharatgas.com/bharatgas/User/GetCaptcha"

    response = requests.get(url)
    with open("test.jpeg","wb") as f:
        f.write(response.content)
    
    img = Image.open("test.jpeg")

    print(image_to_string(img))


def getMonthName(name):
    if "jan" in name    : return 1
    elif "feb" in   name: return 2
    elif "mar" in   name: return 3
    elif "apr" in   name: return 4
    elif "may" in   name: return 5
    elif "jun" in   name: return 6
    elif "jul" in   name: return 7
    elif "aug" in   name: return 8
    elif "sep" in   name: return 9
    elif "oct" in   name: return 10
    elif "nov" in   name: return 11
    elif "dec" in   name: return 12
    else: raise ValueError


def getDateFromString(stringDate):
    #dt = datetime.datetime.strptime("%d%m%Y",date)
    try:
        tempDate = stringDate.split()
        day=0
        month=0
        year=0
        for temp in tempDate:

            if temp.isdigit() and len(temp)>=4:
                year = int(temp.strip())
            elif re.match("[\d+]",temp):
                day = int(re.sub("[^0-9]","",temp))
            elif len(temp) > 4:
                month = int(getMonthName(temp))

        if year==0:
            year = datetime.date.today().year
            date = datetime.datetime(int(year),month,day)
            return date.strftime("%Y%m%d")
        else:
            date = datetime.datetime(year,month,day)
            return date.strftime("%Y%m%d")
    except Exception as e:
        print(e)

    # day = int(stringDate.split()[0].strip())
    # month = getMonthName(stringDate.split()[1].strip())
    # year = int(stringDate.split()[2].strip())
    # date = datetime.datetime(year,int(month),day)
   

if __name__ == "__main__":
   
    dt = "trains from bangalore city to jolarpettai on 13 september"
    source = getDateFromString(dt.split("on")[1].strip())
    