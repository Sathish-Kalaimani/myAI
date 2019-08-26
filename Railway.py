import requests, json
import datetime, time
import re
import urllib
from bs4 import BeautifulSoup as soup
from PIL import Image
from pytesseract import image_to_string

trainList=[]
journeyDate=""
fromStation=""
toStation=""

def getLiveStatus(trainNo):
    try:
        # baseUrl = "https://api.railwayapi.com/v2/live/train/"
        baseUrl ="https://www.confirmtkt.com/train-running-status/"
        #date = datetime.date.today()
        #url = baseUrl+trainNo+"/date/"+date.strftime("%m-%d-%Y")+"/apikey/"+"v_j_t_0_1_f_f_u_n_o"
        url = baseUrl+trainNo

        response_obj = requests.get(url)
        #print(response_obj.content)
        #result = response_obj.json()

        if response_obj.status_code == 200:
            place = response_obj.text.split("circle blink")[1].split("</span")[0].split(">")[-1:][0]
            print(place)
            delayTime = response_obj.text.split("circle blink")[1].split("color:#d9534f;")[1].split("</span>")[0].split(">")[-1:][0]
            print(delayTime)
            try:
                nextStation = response_obj.text.split("circle blink")[1].split("aria-hidden")[1].split("left:8px;")[1].split("</span>")[0].split(">")[-1:][0]
                print(nextStation)
            except Exception:
                nextStation ="" 

            if nextStation:
                if "delay" in delayTime.lower():
                    return "The train is at "+place+" "+delayTime+" . Next Station is "+nextStation
                else:
                    return "The train is at "+place+" on time. Next Station is "+nextStation
            else:
                return "The train has reached it's destination"


            return place
        
        else : 
             return "None" 
    
    except Exception as e:

        return "Some Error Occurred while getting train status"


def getTrainName(trainName,source):
    try:
        cur_time =  int(round(time.time() * 1000))
        url = "https://search.railyatri.in/mobile/trainsearch?callback=jQuery112002057801848788252_1565858562042&q="+trainName+"&slip_type=1&_="+str(cur_time)

        response_obj = requests.get(url)

        trains = response_obj.text
        formatReponse = trains.split("(")[1].split(")")[0]
        trainDetails = json.loads(formatReponse)
        for trains in trainDetails:
            return trains[0]
        
    except Exception as e:
        print(e)
        return "Some Error Occurred while fetching train number"



def getStationCode(place):
    cur_time = int(round(time.time()*1000))
    url = "https://search.railyatri.in/station/search?callback=jQuery112403673674748442557_1566210374335&q="+place+"&_="+str(cur_time)
    response = requests.get(url)
    data = response.text
    formatReponse = response.text.split("(")[1].split(")")[0]
    stationDetails = json.loads(formatReponse)
    for station in stationDetails:
        if place.upper() in station["name"]:
            return station['code']


def getTrainList(source,dest,day):
    global trainList,fromStation,toStation,journeyDate
    cur_time = int(round(time.time()*1000))
    fromStation = getStationCode(source)
    toStation = getStationCode(dest)
    journeyDate = day

    url = "https://www.irctc.co.in/eticketing/protected/mapps1/tbstns/"+fromStation+"/"+toStation+"/"+day+"?dateSpecific=N&ftBooking=N&redemBooking=N&journeyType=GN&captcha="
    
    response = requests.get(url,headers={"greq":str(cur_time)})
    responseData = json.loads(response.text)
    trainsData = responseData["trainBtwnStnsList"]
    for trains in trainsData:

        if isinstance(trains["avlClasses"],str):
            train = trains["trainNumber"]+"-"+trains["trainName"]+"-"+trains["departureTime"]+"-"+str(trains["avlClasses"])
        else: 
            train = trains["trainNumber"]+"-"+trains["trainName"]+"-"+trains["departureTime"]+"-"+trains["avlClasses"][-1:][0]
        
        trainList.append(train)
    return trainList


def getSeatAvailability(trainName):
    seats =[]
    trainNo =0
    coach = ""
    for train in trainList:
        if train.split("-")[1].strip().lower() in trainName.lower():
            trainNo = train.split("-")[0].strip()
            coach = train.split("-")[-1:][0].strip()
    
    cur_time = int(round(time.time()*1000))
    baseUrl = "https://www.irctc.co.in/eticketing/protected/mapps1/avlFareenquiry/"
    body={"enquiryType":"3","clusterFlag":"N","onwardFlag":"N","cod":"false","reservationMode":"N_MOBILE_ANDROID","autoUpgradationSelected":"false","ticketChoiceSameCoach":"false","reservationChoice":"99","ignoreChoiceIfWl":"true","concessionBooking":"false","generalistChildConfirm":"false","ftBooking":"false","loyaltyRedemptionBooking":"false","nosbBooking":"false","returnJourney":"false","connectingJourney":"false","moreThanOneDay":"true","ticketType":"E"}
    completeUrl = baseUrl+trainNo+"/"+journeyDate+"/"+fromStation+"/"+toStation+"/"+coach+"/GN/N"
    #print(completeUrl)
    response = requests.post(completeUrl,data=json.dumps(body),headers={"greq":str(cur_time),"Content-Type": "application/json"})
    responseData = json.loads(response.text)
    availability = responseData["avlDayList"]

    for avail in availability:
        seats.append(avail["availablityDate"]+":"+avail["availablityStatus"])

    return seats


#if __name__ == "__main__":    
    #trainNo = getTrainName("Double Decker","Bangalore")
    #print(trainNo)
    #trainNo = "12640"
    #getLiveStatus(trainNo)

        # config = configparser.RawConfigParser()
        # config.read("app.cfg")
        # print(config.get("rssFeeds","toi"))
    #data = getTrainList("Bangalore City","Jolarpettai","20190830")
    #getSeatAvailability("SESHADRI EXPRESS")
      #getSeatAvailability()
      #dt = "20-09-2019"
      #date = datetime.datetime.strptime(dt,"%d-%m-%Y")

      #formated  = date.strftime("%Y%m%d")
      #print(formated)
    
    